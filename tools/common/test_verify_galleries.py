"""Isolated gallery regressions: python3 -m unittest discover -s tools/common -p 'test_verify_galleries.py'."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

from verify_galleries import GalleryVerifier
from write_catalog import write_catalog


def png_bytes(red):
    def chunk(kind, payload):
        return (struct.pack('>I', len(payload)) + kind + payload +
                struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff))
    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(bytes((0, red, 0, 0)))) + chunk(b'IEND', b''))


class GalleryPhotographicTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / 'homes/example'
        (self.home / 'outputs/images').mkdir(parents=True)
        (self.home / 'outputs/plans').mkdir()
        (self.home / 'project.json').write_text('{}')
        self.manifest = {
            'schema_version': 1, 'renders': [], 'required_levels': ['main'],
            'plans': [{'path': 'outputs/plans/main.png', 'level': 'main', 'caption': 'Main plan'}],
            'signature_features': [],
        }
        for index, name in enumerate(('arrival', 'outdoor', 'site', 'kitchen', 'living')):
            value = f'outputs/images/{name}.png'
            (self.home / value).write_bytes(png_bytes(index))
            render = {'path': value, 'caption': name, 'view': 'exterior' if index < 3 else 'interior'}
            if index < 3:
                render['exterior_role'] = name
            self.manifest['renders'].append(render)
        (self.home / 'outputs/plans/main.png').write_bytes(png_bytes(10))
        (self.home / 'outputs/images/photo.png').write_bytes(png_bytes(11))
        (self.home / 'outputs/photo-study.md').write_text('Prompt: preserve the source. Tool: Imagegen.')
        self.manifest['photographic_hero'] = self.study('outputs/images/photo.png', 'arrival')
        self.order = ['outputs/images/photo.png'] + [r['path'] for r in self.manifest['renders']] + ['outputs/plans/main.png']
        self.write_readmes()

    def study(self, path, source):
        source = f'outputs/images/{source}.png'
        return {
            'path': path, 'source_render': source, 'kind': 'ai-photographic-study',
            'caption': 'AI photographic study', 'tool': 'Imagegen (built-in)',
            'source_sha256': hashlib.sha256((self.home / source).read_bytes()).hexdigest(),
            'image_sha256': hashlib.sha256((self.home / path).read_bytes()).hexdigest(),
            'provenance': 'outputs/photo-study.md',
        }

    def write_readmes(self, root_order=None):
        for destination, prefix, order in (
            (self.home / 'README.md', '', self.order),
            (self.home / 'outputs/README.md', '../', self.order),
        ):
            destination.write_text('\n'.join(f'![View]({prefix}{path})' for path in order))
        order = root_order if root_order is not None else ['outputs/images/photo.png', 'outputs/plans/main.png']
        row = '| ' + ' | '.join(f'![View](homes/example/{path})' for path in order) + ' |'
        (self.root / 'README.md').write_text('| Photo | Plan |\n| --- | --- |\n' + row +
                                           '\n\n[Full home](homes/example/README.md)\n')

    def verify(self):
        (self.home / 'gallery.json').write_text(json.dumps(self.manifest))
        verifier = GalleryVerifier(self.root)
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            result = verifier.run()
        return result, verifier.errors, capture.getvalue()

    def assert_failure(self, message):
        result, errors, _ = self.verify()
        self.assertEqual(result, 1)
        self.assertTrue(any(message in error for error in errors), errors)

    def test_legacy_one_study_passes_and_reports_honest_count(self):
        result, errors, output = self.verify()
        self.assertEqual((result, errors), (0, []))
        self.assertIn('photographic studies: 1', output)
        self.assertIn('counts do not establish full-tour completion', output)

    def test_interior_cannot_be_exterior_hero(self):
        self.manifest['photographic_hero'] = self.study('outputs/images/photo.png', 'kitchen')
        self.assert_failure('exterior photographic study needs an exterior native source')

    def test_path_alias_cannot_hide_interior_in_exterior_list(self):
        study = self.study('outputs/images/photo.png', 'kitchen')
        study['source_render'] = 'outputs/images/../images/kitchen.png'
        self.manifest['photographic_exteriors'] = [study]
        self.assert_failure('exterior photographic study needs an exterior native source')

    def test_valid_source_alias_is_resolved_consistently(self):
        self.manifest['photographic_hero']['source_render'] = 'outputs/images/../images/arrival.png'
        result, errors, _ = self.verify()
        self.assertEqual((result, errors), (0, []))

    def test_exterior_cannot_be_an_interior_study(self):
        self.manifest['photographic_interiors'] = [copy.deepcopy(self.manifest['photographic_hero'])]
        self.assert_failure('interior photographic study needs an interior native source')

    def test_selected_image_alias_cannot_duplicate_hero(self):
        study = copy.deepcopy(self.manifest['photographic_hero'])
        study['path'] = 'outputs/images/../images/photo.png'
        self.manifest['photographic_exteriors'] = [study]
        self.assert_failure('duplicate photographic study file')

    def test_same_source_can_have_distinct_selected_studies(self):
        photo = 'outputs/images/photo-dusk.png'
        (self.home / photo).write_bytes(png_bytes(12))
        self.manifest['photographic_exteriors'] = [self.study(photo, 'arrival')]
        self.order.append(photo)
        self.write_readmes()
        result, errors, output = self.verify()
        self.assertEqual((result, errors), (0, []))
        self.assertIn('photographic studies: 2', output)

    def test_root_native_before_hero_fails(self):
        order = self.order.copy()
        order[0], order[1] = order[1], order[0]
        self.write_readmes(root_order=order)
        self.assert_failure('root catalog must lead this home with its photographic study')

    def test_unrelated_images_before_root_hero_are_allowed(self):
        readme = self.root / 'README.md'
        readme.write_text('![Logo](logo.png)\n![Another home](homes/other/photo.png)\n' + readme.read_text())
        result, errors, _ = self.verify()
        self.assertEqual((result, errors), (0, []))

    def test_full_gallery_is_rejected_in_root(self):
        self.write_readmes(root_order=self.order)
        self.assert_failure('exactly one photographic hero and one registered floor plan')

    def test_catalog_writer_replaces_legacy_spread_and_keeps_full_home(self):
        self.write_readmes(root_order=self.order)
        (self.home / 'project.json').write_text('{"name": "Example"}')
        (self.home / 'gallery.json').write_text(json.dumps(self.manifest))
        home_page = (self.home / 'README.md').read_text()
        with contextlib.redirect_stdout(io.StringIO()):
            write_catalog(self.root)
            first = (self.root / 'README.md').read_text()
            write_catalog(self.root)
        self.assertEqual(first, (self.root / 'README.md').read_text())
        self.assertEqual(home_page, (self.home / 'README.md').read_text())
        result, errors, _ = self.verify()
        self.assertEqual((result, errors), (0, []))

    def test_plan_must_be_registered(self):
        self.write_readmes(root_order=['outputs/images/photo.png', 'outputs/images/site.png'])
        self.assert_failure('exactly one photographic hero and one registered floor plan')

    def test_root_preview_row_must_be_side_by_side(self):
        readme = self.root / 'README.md'
        readme.write_text(readme.read_text().replace(' | ![View]', '\n![View]'))
        self.assert_failure('side by side in one table row')

    def test_landing_page_link_required(self):
        readme = self.root / 'README.md'
        readme.write_text(readme.read_text().replace('[Full home](homes/example/README.md)', ''))
        self.assert_failure('must link to the full home landing page')

    def test_compact_root_does_not_relax_home_coverage(self):
        readme = self.home / 'README.md'
        readme.write_text(readme.read_text().replace('![View](outputs/images/kitchen.png)', ''))
        self.assert_failure('missing image embed: outputs/images/kitchen.png')

    def test_caption_and_tool_must_be_nonempty_strings(self):
        hero = self.manifest['photographic_hero']
        for key in ('caption', 'tool'):
            original = hero[key]
            for value in ('', '  ', None, 42):
                with self.subTest(key=key, value=value):
                    hero[key] = value
                    self.assert_failure(f'{key} must be nonempty')
            hero[key] = original

    def test_stale_source_is_rejected(self):
        (self.home / 'outputs/images/arrival.png').write_bytes(png_bytes(99))
        self.assert_failure('source_sha256 differs from the reviewed image')


if __name__ == '__main__':
    unittest.main()
