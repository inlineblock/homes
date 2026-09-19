"""Verify a reopened home's exact native library pins and actual direct adoption.

``audit_asset_adoption()`` is read-only. Running this script directly retains the
original behavior of writing the current home's successful adoption receipt.
"""
import json
from collections import defaultdict
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]


def resolve_library(library):
    """Resolve a Library datablock's path after native reopen.

    Blender normalizes indirect Library.filepath values relative to the open
    main file (verified with Blender 4.5.14). Passing library.parent here applies
    that relative path twice and creates false missing dependencies. The
    ``library=`` argument instead applies to paths *inside* linked datablocks,
    for example an image.filepath relative to image.library.
    """
    assert not library.is_missing, f'Blender reports a missing library: {library.filepath}'
    return Path(bpy.path.abspath(library.filepath)).resolve()


def audit_asset_adoption(home=None, *, write_receipt=False):
    home = Path(home) if home is not None else Path(bpy.data.filepath).resolve().parent.parent
    meta = json.loads((home / 'project.json').read_text())
    actual = {}
    manifests = {}
    uses = defaultdict(list)
    for library in bpy.data.libraries:
        assert library.filepath.startswith('//'), f'Non-relative library: {library.filepath}'
        path = resolve_library(library)
        assert path.is_relative_to(ROOT / 'library'), f'Library outside shared catalog: {path}'
        assert path.is_file(), f'Missing native library: {path}'
        manifest = path.parent / 'asset.json'
        assert manifest.is_file(), f'Missing asset manifest: {manifest}'
        asset = json.loads(manifest.read_text())
        actual[path] = (asset['id'], asset['version'])
        manifests[path] = asset

    for obj in bpy.context.scene.objects:
        collection = obj.instance_collection if obj.instance_type == 'COLLECTION' else None
        if collection and collection.library:
            path = resolve_library(collection.library)
            if path in actual:
                uses[actual[path]].append(obj.name)
        for slot in obj.material_slots:
            if slot.material and slot.material.library:
                path = resolve_library(slot.material.library)
                if path in actual:
                    uses[actual[path]].append(obj.name + ' (material)')

    pins = {(dep['id'], dep['version']) for dep in meta['asset_dependencies']}
    loaded = set(actual.values())
    assert pins == loaded, {
        'missing_pins': sorted(loaded - pins),
        'unused_manifest_pins': sorted(pins - loaded),
    }
    rows = []
    for asset_id, version in sorted(pins):
        names = uses[(asset_id, version)]
        # Linked materials can be declared dependencies of directly adopted collections.
        parents = []
        if not names:
            for path, (parent_id, parent_version) in actual.items():
                dependencies = manifests[path].get('dependencies', [])
                declared = any(
                    dep.get('id') == asset_id and dep.get('version') == version
                    for dep in dependencies if isinstance(dep, dict)
                )
                if declared and uses[(parent_id, parent_version)]:
                    parents.append(parent_id)
        assert names or parents, (asset_id, version, 'loaded but no direct use or declared adopted parent')
        rows.append({
            'id': asset_id,
            'version': version,
            'direct_placements_or_material_assignments': len(names),
            'examples': names[:8],
            'adopted_parent_dependencies': parents,
        })
    report = {
        'home': meta['id'],
        'native_library_pins_match_manifest': True,
        'asset_versions': len(rows),
        'assets': rows,
    }
    if write_receipt:
        (home / 'model/asset-adoption.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    result = audit_asset_adoption(write_receipt=True)
    print('ASSET_ADOPTION_VERIFIED', result['home'], result['asset_versions'], flush=True)
