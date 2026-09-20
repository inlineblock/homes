"""Fresh Bonsai import and source-hash checks for the current Atrium 01 IFC.

Run separately from native export; no native scene is saved:
  blender --background --factory-startup --python-exit-code 1
    --python tools/atrium01/verify_bonsai.py
Optionally append -- --runtime-path /path/to/compatible/extracted/site-packages.
The installed Bonsai extension is enabled only in this process if necessary.
"""
import argparse
import hashlib
import json
import runpy
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOME = ROOT/'homes'/'atrium-01'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-path', type=Path)
    parser.add_argument('--addon-module', default='bl_ext.user_default.bonsai')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    if args.runtime_path:
        runtime = args.runtime_path.expanduser().resolve()
        assert (runtime/'bonsai').is_dir() and (runtime/'ifcopenshell').is_dir()
        sys.path.insert(0, str(runtime))

    import bpy
    import addon_utils
    import ifcopenshell
    import ifcopenshell.geom
    import ifcopenshell.util.unit

    native = HOME/'model'/'atrium-01.blend'
    path = HOME/'model'/'atrium-01.ifc'
    source_hash, ifc_hash = sha256(native), sha256(path)
    exported = json.loads((path.parent/'ifc-validation.json').read_text())
    assert exported['schema_errors'] == 0
    assert exported['source_blend_sha256'] == source_hash, 'IFC source is stale'
    assert exported['ifc_sha256'] == ifc_hash, 'IFC differs from its schema receipt'
    preferences_file = Path(bpy.utils.user_resource('CONFIG'))/'userpref.blend'
    preferences_hash = sha256(preferences_file) if preferences_file.exists() else None
    try:
        bpy.ops.bim.load_project.get_rna_type()
    except (AttributeError, RuntimeError, KeyError):
        # default_set creates the required in-memory preferences entry. No
        # save_userpref call is made, and the saved-file hash is checked below.
        assert addon_utils.enable(args.addon_module, default_set=True, persistent=False) is not None
    preferences = bpy.context.preferences.addons[args.addon_module].preferences
    preferences.save_metadata_blend_file = False

    with tempfile.TemporaryDirectory(prefix='atrium01-bonsai-') as cache:
        preferences.cache_dir = cache
        original_argv = sys.argv
        try:
            sys.argv = ['verify_bonsai.py', '--', 'atrium-01']
            runpy.run_path(str(ROOT/'tools/common/verify_bonsai.py'), run_name='__main__')
        finally:
            sys.argv = original_argv

        import bonsai.tool as tool
        model = tool.Ifc.get()
        assert model is not None and model.schema == 'IFC4'
        assert abs(ifcopenshell.util.unit.calculate_unit_scale(model)-1.0) < 1e-9
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        checks = []
        # Cross-check real imported meshes against independent IFC tessellation
        # for core envelope classes. This catches unit/placement import errors.
        for kind in ('IfcSlab', 'IfcWall', 'IfcRoof'):
            products = [entity for entity in model.by_type(kind) if entity.Representation]
            assert products, 'Missing classified '+kind
            if kind == 'IfcWall':
                # Collection fallback can also classify small tracks as walls;
                # prefer a true enclosure segment for this dimensional check.
                products = [entity for entity in products if 'solid' in (entity.Name or '')] or products
            entity = sorted(products, key=lambda e: e.Name or '')[0]
            obj = tool.Ifc.get_object(entity)
            assert obj is not None and obj.type == 'MESH' and len(obj.data.vertices) >= 4
            points = [obj.matrix_world @ v.co for v in obj.data.vertices]
            actual = [min(p[i] for p in points) for i in range(3)] + [max(p[i] for p in points) for i in range(3)]
            shape = ifcopenshell.geom.create_shape(settings, entity)
            verts = shape.geometry.verts
            reference = [min(verts[i::3]) for i in range(3)] + [max(verts[i::3]) for i in range(3)]
            error = max(abs(a-b) for a, b in zip(actual, reference))
            assert error < .001, (entity.Name, error)
            checks.append({'class': kind, 'name': entity.Name, 'bounds_m': actual,
                           'maximum_import_bounds_error_m': error})

        assert sha256(native) == source_hash and sha256(path) == ifc_hash
        assert (sha256(preferences_file) if preferences_file.exists() else None) == preferences_hash
        receipt_path = path.parent/'bonsai-validation.json'
        receipt = json.loads(receipt_path.read_text())
        receipt.update({
            'source_blend_sha256': source_hash, 'ifc_sha256': ifc_hash,
            'blender_version': bpy.app.version_string,
            'ifcopenshell_version': ifcopenshell.version,
            'saved_preferences_unchanged': True,
            'geometry_units': 'meters', 'actual_import_geometry': checks,
            'runtime': 'Explicit process-local runtime' if args.runtime_path else 'Installed Blender Python environment',
            'limits': 'Fresh IFC import and selected actual mesh bounds checked; classified concept geometry is not complete semantic BIM or engineered construction documentation.',
        })
        receipt_path.write_text(json.dumps(receipt, indent=2)+'\n')
        print('ATRIUM_BONSAI_VERIFIED', json.dumps(receipt), flush=True)


if __name__ == '__main__':
    main()
