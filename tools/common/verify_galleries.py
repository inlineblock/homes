#!/usr/bin/env python3
"""Check registered PNG gallery coverage and Markdown embeds; visual QA stays manual."""
import argparse
import json
from pathlib import Path
import re
import struct
from urllib.parse import unquote, urlsplit
import zlib

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
ROLES = {'arrival', 'outdoor', 'site'}
VIEWS = {'exterior', 'interior', 'cutaway'}


def local_path(base, value):
    """Resolve a local Markdown destination, ignoring presentation query/fragment."""
    url = urlsplit(value)
    if url.scheme or url.netloc:
        raise ValueError('must be a local relative path')
    path = Path(unquote(url.path))
    if not url.path or path.is_absolute():
        raise ValueError('must be a nonempty relative path')
    return (base / path).resolve()


def markdown_images(text):
    """Read inline and reference-style images, excluding fenced/inline code."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text,
                  flags=re.M | re.S)
    text = re.sub(r'(`+).*?\1', '', text, flags=re.S)
    references = {}
    # An optional Markdown title may follow the destination before the close.
    closing = re.compile(r'''^\s*(?:(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\([^)]*\))\s*)?\)''')
    for match in re.finditer(r'^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)', text, re.M):
        references[' '.join(match[1].lower().split())] = match[2].strip('<>')
    for match in re.finditer(r'!\[((?:\\.|[^\]\\])*)\]', text):
        alt = match[1]
        tail = text[match.end():]
        if tail.startswith('('):
            tail = tail[1:].lstrip()
            if tail.startswith('<'):
                end = tail.find('>')
                if end != -1 and closing.match(tail[end + 1:]):
                    yield alt, tail[1:end]
                continue
            # Unquoted destinations may contain balanced parentheses.
            depth = 0
            destination = []
            escaped = False
            end = 0
            for end, char in enumerate(tail):
                if escaped:
                    destination.append(char)
                    escaped = False
                    continue
                if char == '\\':
                    escaped = True
                    continue
                if char == ')' and depth == 0 or char.isspace():
                    break
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                destination.append(char)
            else:
                end = len(tail)
            if destination and closing.match(tail[end:]):
                yield alt, ''.join(destination)
        else:
            ref = re.match(r'\[([^\]]*)\]', tail)
            key = (ref[1] or alt) if ref else alt
            key = ' '.join(key.lower().split())
            if key in references:
                yield alt, references[key]


def png_dimensions(path):
    """Check PNG structure/CRCs and dimensions without decoding or judging pixels."""
    with path.open('rb') as stream:
        if stream.read(8) != PNG_SIGNATURE:
            raise ValueError('not PNG bytes (possibly a Git LFS pointer)')
        dimensions = None
        has_data = False
        first = True
        remaining = path.stat().st_size - 8
        while remaining:
            header = stream.read(8)
            if len(header) != 8:
                raise ValueError('truncated PNG chunk header')
            size, kind = struct.unpack('>I4s', header)
            if size > remaining - 12:
                raise ValueError('truncated PNG chunk')
            payload = stream.read(size)
            checksum = stream.read(4)
            remaining -= size + 12
            if zlib.crc32(kind + payload) & 0xffffffff != struct.unpack('>I', checksum)[0]:
                raise ValueError('PNG chunk checksum mismatch')
            if first:
                if kind != b'IHDR' or size != 13:
                    raise ValueError('missing PNG IHDR header')
                dimensions = struct.unpack('>II', payload[:8])
                if not all(dimensions):
                    raise ValueError('zero PNG width or height')
                first = False
            if kind == b'IDAT':
                has_data |= bool(size)
            if kind == b'IEND':
                if size or remaining or not has_data:
                    raise ValueError('invalid PNG end or missing image data')
                return dimensions
        raise ValueError('missing PNG end chunk')


class GalleryVerifier:
    def __init__(self, root):
        self.root = root.resolve()
        self.errors = []
        self.png_cache = {}
        self.readme_cache = {}

    def fail(self, scope, message):
        self.errors.append(f'{scope}: {message}')

    def embeds(self, readme):
        if readme in self.readme_cache:
            return self.readme_cache[readme]
        found = set()
        try:
            text = readme.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as error:
            self.fail(readme.relative_to(self.root), f'cannot read README: {error}')
            text = ''
        for alt, destination in markdown_images(text):
            try:
                path = local_path(readme.parent, destination)
            except ValueError:
                continue  # Remote images do not satisfy local gallery coverage.
            if not alt.strip():
                self.fail(readme.relative_to(self.root), f'empty image alt text for {destination}')
                continue
            found.add(path)
        self.readme_cache[readme] = found
        return found

    def image(self, home, value, prefix, scope):
        if not isinstance(value, str):
            self.fail(scope, 'image path must be a string')
            return None
        try:
            path = local_path(home, value)
            try:
                path.relative_to((home / prefix).resolve())
            except ValueError:
                raise ValueError(f'path must remain inside {prefix}/')
            if path.suffix.lower() != '.png':
                raise ValueError('gallery image must have a .png extension')
            if path not in self.png_cache:
                try:
                    self.png_cache[path] = png_dimensions(path)
                except (OSError, ValueError, struct.error) as error:
                    self.png_cache[path] = str(error)
            if isinstance(self.png_cache[path], str):
                raise ValueError(self.png_cache[path])
            return path
        except ValueError as error:
            self.fail(scope, f'{value}: {error}')
            return None

    def entries(self, manifest, key, scope):
        value = manifest.get(key)
        if not isinstance(value, list):
            self.fail(scope, f'{key} must be a list')
            return []
        return value

    def coverage(self, renders, scope):
        if len(renders) < 5:
            self.fail(scope, f'needs at least 5 unique actual renders; found {len(renders)}')
        interiors = sum(item['view'] == 'interior' for item in renders.values())
        if interiors < 2:
            self.fail(scope, f'needs at least 2 interior renders; found {interiors}')
        roles = {item.get('exterior_role') for item in renders.values() if item['view'] == 'exterior'}
        missing = ROLES - roles
        if missing:
            self.fail(scope, 'needs distinct exterior images for missing roles: ' + ', '.join(sorted(missing)))

    def home(self, home):
        scope = str(home.relative_to(self.root))
        count_before = len(self.errors)
        try:
            manifest = json.loads((home / 'gallery.json').read_text(encoding='utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            self.fail(scope, f'cannot read gallery.json: {error}')
            return
        if not isinstance(manifest, dict):
            self.fail(scope, 'gallery.json must contain an object')
            return
        if type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1:
            self.fail(scope, 'schema_version must be 1')
        renders = {}
        for index, item in enumerate(self.entries(manifest, 'renders', scope)):
            label = f'{scope} renders[{index}]'
            if not isinstance(item, dict):
                self.fail(label, 'must be an object')
                continue
            if not isinstance(item.get('caption'), str) or not item['caption'].strip():
                self.fail(label, 'caption must be nonempty')
            if not isinstance(item.get('view'), str) or item['view'] not in VIEWS:
                self.fail(label, 'view must be exterior, interior or cutaway')
                continue
            role = item.get('exterior_role')
            if role is not None and (item['view'] != 'exterior' or not isinstance(role, str) or role not in ROLES):
                self.fail(label, 'exterior_role must be arrival, outdoor or site on an exterior render')
                continue
            path = self.image(home, item.get('path'), 'outputs/images', label)
            if path is not None:
                if path in renders:
                    self.fail(label, f'duplicate render file: {item["path"]}')
                else:
                    renders[path] = item
        self.coverage(renders, scope)
        levels = self.entries(manifest, 'required_levels', scope)
        if not levels or any(not isinstance(level, str) or not level.strip() for level in levels):
            self.fail(scope, 'required_levels must contain nonempty level names')
        levels = [level for level in levels if isinstance(level, str) and level.strip()]
        if len(set(levels)) != len(levels):
            self.fail(scope, 'required_levels contains duplicate levels')
        plans = {}
        represented = set()
        for index, item in enumerate(self.entries(manifest, 'plans', scope)):
            label = f'{scope} plans[{index}]'
            if not isinstance(item, dict):
                self.fail(label, 'must be an object')
                continue
            if not isinstance(item.get('caption'), str) or not item['caption'].strip():
                self.fail(label, 'caption must be nonempty')
            level = item.get('level')
            if level not in levels:
                self.fail(label, 'level must match a required_levels entry')
            path = self.image(home, item.get('path'), 'outputs/plans', label)
            if path is not None:
                if path in plans:
                    self.fail(label, 'duplicate plan file; each level needs its own plan image')
                else:
                    plans[path] = item
                    if isinstance(level, str):
                        represented.add(level)
        for level in sorted(set(levels) - represented):
            self.fail(scope, f'missing actual floor-plan PNG for level {level}')
        feature_paths = set()
        feature_ids = set()
        for index, item in enumerate(self.entries(manifest, 'signature_features', scope)):
            label = f'{scope} signature_features[{index}]'
            if not isinstance(item, dict):
                self.fail(label, 'must be an object')
                continue
            for key in ('id', 'label'):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    self.fail(label, f'{key} must be nonempty')
            feature_id = item.get('id')
            if isinstance(feature_id, str):
                if feature_id in feature_ids:
                    self.fail(label, f'duplicate feature id: {feature_id}')
                feature_ids.add(feature_id)
            paths = self.entries(item, 'renders', label)
            if not paths:
                self.fail(label, 'needs at least one registered feature render')
            for value in paths:
                try:
                    if not isinstance(value, str):
                        raise ValueError('path must be a string')
                    path = local_path(home, value)
                    if path not in renders:
                        raise ValueError('not a registered actual render')
                    feature_paths.add(path)
                except ValueError as error:
                    self.fail(label, f'{value}: {error}')
        for readme in (home / 'README.md', home / 'outputs/README.md'):
            missing = (set(renders) | set(plans)) - self.embeds(readme)
            for path in sorted(missing):
                self.fail(readme.relative_to(self.root), f'missing image embed: {path.relative_to(home)}')
        root_embeds = self.embeds(self.root / 'README.md')
        root_renders = {path: item for path, item in renders.items() if path in root_embeds}
        self.coverage(root_renders, f'README.md [{home.name}]')
        for path in sorted((feature_paths | set(plans)) - root_embeds):
            self.fail(f'README.md [{home.name}]', f'missing feature/plan image embed: {path.relative_to(self.root)}')
        state = 'OK' if len(self.errors) == count_before else 'FAIL'
        print(f'{state} {home.name}: {len(renders)} renders, {len(plans)} level plans, {len(feature_ids)} features')

    def run(self):
        homes = sorted(path.parent for path in (self.root / 'homes').glob('*/project.json'))
        if not homes:
            self.fail('repository', 'no home projects found under homes/*/project.json')
        for home in homes:
            self.home(home)
        for error in self.errors:
            print(f'ERROR {error}')
        if self.errors:
            print(f'Gallery verification failed: {len(self.errors)} issue(s).')
            return 1
        print(f'Gallery files and README coverage verified for {len(homes)} homes. Visual classifications and quality require manual review.')
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2],
                        help='Repository root (defaults to this script\'s repository).')
    args = parser.parse_args()
    return GalleryVerifier(args.root).run()


if __name__ == '__main__':
    raise SystemExit(main())
