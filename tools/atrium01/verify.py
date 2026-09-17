"""Check saved scene portability and measured brief; run after reopening the .blend."""
import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
from design import *
assert GROSS_AREA==2400
assert len([r for r in ROOMS if r[0] in ['bedroom-2','bedroom-3','primary']])==3
assert len([r for r in ROOMS if 'bath' in r[0]])==3
libraries=[]
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    path=Path(bpy.path.abspath(lib.filepath));assert path.is_file(),path
    libraries.append({'relative_path':lib.filepath,'resolved':True})
assert libraries,'Expected a linked shared tile library'
s=bpy.context.scene
report={'blender':bpy.app.version_string,'reopened_scene_objects':len(s.objects),'gross_enclosed_area_sqft':GROSS_AREA,'bedrooms':3,'bathrooms':3,'asset_links':libraries,'camera':s.camera.name,'roof_present':bool(bpy.data.collections.get('09 Roof | hide for cutaway')),'render_dimensions':[s.render.resolution_x,s.render.resolution_y]}
path=ROOT/'homes/atrium-01/model/model-validation.json';path.write_text(json.dumps(report,indent=2)+'\n');print('VERIFIED',report)
