"""Export the saved metric Atrium 01 scene through the shared IFC4 exporter.

Run in a fresh Blender process with the current native file open:
  blender --background --factory-startup homes/atrium-01/model/atrium-01.blend
    --python-exit-code 1 --python tools/atrium01/export_ifc.py
If the installed environment is unavailable, append
  -- --runtime-path /path/to/compatible/extracted/site-packages
The optional runtime is process-local; this script does not install packages,
change saved preferences, or save the Blender scene.
"""
import argparse
import hashlib
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT/'homes'/'atrium-01'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-path', type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.runtime_path:
        runtime = args.runtime_path.expanduser().resolve()
        assert (runtime/'ifcopenshell').is_dir(), 'Runtime does not contain IfcOpenShell'
        sys.path.insert(0, str(runtime))

    import bpy
    import ifcopenshell
    import ifcopenshell.util.unit

    native = HOME/'model'/'atrium-01.blend'
    assert Path(bpy.data.filepath).resolve() == native.resolve(), 'Open the current Atrium 01 native model'
    manifest = json.loads((HOME/'project.json').read_text())
    assert manifest['id'] == 'atrium-01' and manifest['units'] == 'meters'
    assert bpy.context.scene.unit_settings.system == 'METRIC'
    assert abs(bpy.context.scene.unit_settings.scale_length-1.0) < 1e-9
    source_hash = sha256(native)
    exporter = ROOT/'tools'/'common'/'export_scene_ifc.py'
    exporter_hash = sha256(exporter)
    runpy.run_path(str(exporter), run_name='__main__')
    assert sha256(native) == source_hash, 'Native file changed during export'
    assert sha256(exporter) == exporter_hash, 'Shared exporter changed during export'

    path = HOME/'model'/'atrium-01.ifc'
    model = ifcopenshell.open(str(path))
    assert model.schema == 'IFC4'
    assert abs(ifcopenshell.util.unit.calculate_unit_scale(model)-1.0) < 1e-9
    receipt_path = path.parent/'ifc-validation.json'
    receipt = json.loads(receipt_path.read_text())
    assert receipt['schema_errors'] == 0 and not receipt['errors']
    receipt.update({
        'source_blend_sha256': source_hash,
        'ifc_sha256': sha256(path),
        'exporter': 'tools/common/export_scene_ifc.py',
        'exporter_sha256': exporter_hash,
        'blender_version': bpy.app.version_string,
        'ifcopenshell_version': ifcopenshell.version,
        'geometry_units': 'meters',
        'runtime': 'Explicit process-local runtime' if args.runtime_path else 'Installed Blender Python environment',
        'limits': 'Classified concept geometry and explicitly tagged linked products; no construction, engineering, installation or complete furnishing/BIM certification. Planning-zone labels are documented in the plans rather than exported as measured IFC spaces.',
    })
    receipt_path.write_text(json.dumps(receipt, indent=2)+'\n')
    print('ATRIUM_IFC_EXPORTED', json.dumps(receipt), flush=True)


if __name__ == '__main__':
    main()
