"""Record an actual visual review after native verification; never infer a pass.

Call only after inspecting the current preview AND detail. Reviewer and notes
are required so a successful render alone cannot masquerade as visual review.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(slug, reviewer, notes):
    folder = ROOT / 'library/landscape' / slug / 'v001'
    manifest = json.loads((folder / 'asset.json').read_text())
    receipt = json.loads((folder / 'validation.json').read_text())
    native = folder / manifest['files']['blender']
    assert receipt['native_reopened'] and receipt['fresh_linked_host_instances'] == 3
    assert receipt['native_sha256'] == digest(native), 'Reverify changed native first'
    images = [folder / 'preview.png', folder / 'detail.png']
    assert all(p.exists() and p.stat().st_mtime >= native.stat().st_mtime for p in images), 'Rerender stale images first'
    receipt['visual_review'] = {
        'status': 'pass', 'scope': 'Architectural concept landscape use; not photographic macro vegetation',
        'reviewer': reviewer, 'notes': notes,
        'image_sha256': {p.name: digest(p) for p in images},
    }
    manifest['review'].update(native_reopen_checked=True, native_preview_checked=True)
    manifest['review']['host_placement_checked'] = False
    manifest['review']['scope'] = 'Isolated native and linked-host checks; nursery evidence is separate; no home adoption'
    manifest['files'].update(preview='preview.png', detail='detail.png', validation='validation.json')
    manifest['adoption_status'] = 'Reviewed shared concept asset; no existing home adoption claimed.'
    for name, value in [('asset.json', manifest), ('validation.json', receipt)]:
        (folder / name).write_text(json.dumps(value, indent=2) + '\n')
    path = folder / 'README.md'
    content = path.read_text().split('\n<!-- native-review -->')[0].rstrip()
    content += '\n\n<!-- native-review -->\n## Native visual review\n\n'
    content += '![Three editable plant variants](preview.png)\n\n![Actual modeled detail](detail.png)\n\n'
    content += notes + '\n\n'
    content += ('Reviewed for architectural concept landscape use. Close views retain simplified botanical geometry and procedural surfaces; '
                'these are not photographic macro plants. Native reopen, measured bounds and fresh linked instances are recorded in '
                '[validation.json](validation.json). The [comparative nursery](../../nursery/README.md) tests shared placement; '
                'no existing home adoption is claimed.\n')
    path.write_text(content)
    print('REVIEW_RECORDED', slug)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets', nargs='+', required=True)
    p.add_argument('--reviewer', required=True)
    p.add_argument('--notes', required=True)
    args = p.parse_args()
    for slug in args.assets:
        record(slug, args.reviewer, args.notes)
