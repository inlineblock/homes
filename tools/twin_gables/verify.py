"""Fresh native reopening, actual asset/file/room/height checks; no resave."""
import sys,json,hashlib,os
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from design import SLUG,AREA,ROOMS,VIEWS
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes'/SLUG
errors=[];s=bpy.context.scene
if abs(s.get('gross_enclosed_area_sqft',0)-AREA)>.01:errors.append('area')
links=[]
for lib in bpy.data.libraries:
 p=Path(bpy.path.abspath(lib.filepath)).resolve()
 if not p.exists():errors.append('missing library:'+str(p))
 if not lib.filepath.startswith('//'):errors.append('absolute library:'+lib.filepath)
 if not p.is_relative_to(ROOT/'library'):errors.append('outside library:'+str(p))
 meta=json.loads((p.parent/'asset.json').read_text());links.append({'id':meta['id'],'version':meta['version'],'path':os.path.relpath(p,HOME),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for name in VIEWS:
 if name not in bpy.data.objects or bpy.data.objects[name].type!='CAMERA':errors.append('camera:'+name)
if len([o for o in s.objects if o.get('shared_asset_id','').startswith('cabinetry/')])<12:errors.append('storage absent')
for name,rect,height in ROOMS:
 if height==10:
  o=bpy.data.objects.get(name+' finished flat ceiling')
  if not o:errors.append('ceiling:'+name)
  elif abs((o.location.z-o.dimensions.z/2)/.3048-10)>.01:errors.append('ceiling datum:'+name)
report={'model_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'blender':bpy.app.version_string,'area_sqft':AREA,'room_program':ROOMS,'scene_objects':len(s.objects),'cameras':list(VIEWS),'asset_links':links,'errors':errors,'limitations':['Architectural concept, not structural or permit documentation.','Door/fixture clearances use generic library envelopes, not selected product approvals.','Site context and parking are illustrative; survey, climate and jurisdiction unassigned.']}
(HOME/'model/native-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('TWIN_REOPEN',json.dumps({'objects':len(s.objects),'links':len(links),'errors':errors}),flush=True)
if errors:raise RuntimeError(errors)
