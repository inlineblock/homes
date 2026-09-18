"""Reopen every committed home from this checkout; validate actual portable assets."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];reports=[]
for manifest_path in sorted((ROOT/'homes').glob('*/project.json')):
    home=manifest_path.parent;meta=json.loads(manifest_path.read_text());path=home/meta['deliverables']['presentation_model']
    assert path.read_bytes()[:7]==b'BLENDER',f'{path}: not a materialized Blender file (check Git LFS)'
    bpy.ops.wm.open_mainfile(filepath=str(path))
    libraries=[]
    for lib in bpy.data.libraries:
        assert lib.filepath.startswith('//'),lib.filepath
        resolved=Path(bpy.path.abspath(lib.filepath)).resolve()
        assert resolved.is_relative_to(ROOT),f'External dependency: {resolved}'
        assert resolved.is_file(),resolved
        libraries.append(lib.filepath)
    floor=[o for o in bpy.context.scene.objects if o.type=='MESH' and any(c.name.startswith('02 Architecture') for c in o.users_collection)]
    # New source-traced homes have concave/angled slabs. Their XY bounding box
    # is not floor area. Measure horizontal top faces after actual void cuts.
    tagged=[o for o in bpy.context.scene.objects if o.get('floor_area_role')]
    sqft=(sum(sum(p.area for p in o.data.polygons if p.normal.z>.9) for o in tagged)/(.3048**2)
          if tagged else sum(o.dimensions.x*o.dimensions.y/(.3048**2) for o in floor))
    assert abs(sqft-meta['gross_enclosed_area_sqft'])<.02,(meta['id'],sqft)
    marked_beds=[o for o in bpy.context.scene.objects if o.get('bed_count')==1]
    beds=marked_beds or [o for o in bpy.context.scene.objects if ' bed frame' in o.name]
    assert len(beds)==meta['bedrooms']
    reports.append({'home':meta['id'],'native_model_reopened':True,'measured_enclosed_floor_sqft':round(sqft,2),'modeled_beds':len(beds),'relative_libraries':len(libraries)})
print('REPOSITORY_VERIFIED',json.dumps(reports),flush=True)
