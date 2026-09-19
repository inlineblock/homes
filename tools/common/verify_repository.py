"""Read-only native, portable-link and adoption checks for every repository home.

Run with Blender --factory-startup --background --python-exit-code 1 --python
this_file. A failure in one home does not hide results for the remaining homes.
"""
import argparse
import json
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_asset_adoption import audit_asset_adoption, resolve_library

ROOT = Path(__file__).resolve().parents[2]


def verify_home(manifest_path):
    home = manifest_path.parent
    meta = json.loads(manifest_path.read_text())
    report = {'home': meta['id'], 'failures': []}
    path = home / meta['deliverables']['presentation_model']
    with path.open('rb') as model:
        assert model.read(7) == b'BLENDER', f'{path}: not a materialized Blender file (check Git LFS)'
    bpy.ops.wm.open_mainfile(filepath=str(path), use_scripts=False)
    report['native_model_reopened'] = True

    def check(name, action):
        try:
            report[name] = action()
        except Exception as error:
            report['failures'].append({'check': name, 'error': str(error)})

    def portable_libraries():
        for library in bpy.data.libraries:
            assert library.filepath.startswith('//'), f'Non-relative library: {library.filepath}'
            resolved = resolve_library(library)
            assert resolved.is_relative_to(ROOT), f'External dependency: {resolved}'
            assert resolved.is_file(), f'Missing library: {resolved}'
        return len(bpy.data.libraries)

    def enclosed_floor_area():
        floor = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH'
                 and any(collection.name.startswith('02 Architecture') for collection in obj.users_collection)]
        # Source-traced concave/angled slabs require top-face areas after void cuts.
        tagged = [obj for obj in bpy.context.scene.objects if obj.get('floor_area_role')]
        sqft = (sum(sum(face.area for face in obj.data.polygons if face.normal.z > .9)
                    for obj in tagged) / (.3048 ** 2) if tagged else
                sum(obj.dimensions.x * obj.dimensions.y / (.3048 ** 2) for obj in floor))
        assert abs(sqft - meta['gross_enclosed_area_sqft']) < .02, {
            'measured_sqft': sqft, 'manifest_sqft': meta['gross_enclosed_area_sqft'],
        }
        return round(sqft, 2)

    def bedroom_count():
        marked = [obj for obj in bpy.context.scene.objects if obj.get('bed_count') == 1]
        beds = marked or [obj for obj in bpy.context.scene.objects if ' bed frame' in obj.name]
        assert len(beds) == meta['bedrooms'], {'modeled_beds': len(beds), 'manifest_bedrooms': meta['bedrooms']}
        return len(beds)

    def asset_schedule():
        schedule = home / 'assets/README.md'
        assert schedule.is_file() and schedule.read_text().strip(), f'Missing or empty asset-use schedule: {schedule}'
        return str(schedule.relative_to(ROOT))

    check('relative_libraries', portable_libraries)
    check('measured_enclosed_floor_sqft', enclosed_floor_area)
    check('modeled_beds', bedroom_count)
    check('asset_use_schedule', asset_schedule)
    check('asset_adoption', lambda: audit_asset_adoption(home, write_receipt=False))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--homes', nargs='+', help='Audit only these home folder names; omit to audit all.')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    manifests = sorted((ROOT / 'homes').glob('*/project.json'))
    if args.homes:
        known = {path.parent.name for path in manifests}
        unknown = set(args.homes) - known
        if unknown:
            parser.error(f'Unknown home folders: {sorted(unknown)}')
        manifests = [path for path in manifests if path.parent.name in args.homes]
    assert manifests, 'No home manifests found for verification'
    reports = []
    for manifest_path in manifests:
        try:
            report = verify_home(manifest_path)
        except Exception as error:
            report = {'home': manifest_path.parent.name,
                      'failures': [{'check': 'manifest_or_native_reopen', 'error': str(error)}]}
        reports.append(report)
        print('HOME_VERIFIED' if not report['failures'] else 'HOME_VERIFICATION_FAILED',
              json.dumps(report), flush=True)
    failed = [report for report in reports if report['failures']]
    print('REPOSITORY_VERIFICATION_FAILED' if failed else 'REPOSITORY_VERIFIED',
          json.dumps({'homes': len(reports), 'passed': len(reports) - len(failed),
                      'failed_homes': [report['home'] for report in failed]}), flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
