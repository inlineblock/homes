"""Classify the current native scene through the shared IFC exporter; no native save."""
import sys,runpy,json,hashlib,argparse
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/eichler-twin-gables'
p=argparse.ArgumentParser();p.add_argument('--runtime-path',type=Path)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if a.runtime_path:sys.path.insert(0,str(a.runtime_path))
try:import ifcopenshell
except ImportError:
 candidates=list((Path(bpy.utils.user_resource('EXTENSIONS'))/'.local/lib').glob('*/site-packages'))
 for c in candidates:sys.path.insert(0,str(c))
 import ifcopenshell
native=Path(bpy.data.filepath);native_sha=hashlib.sha256(native.read_bytes()).hexdigest()
for o in bpy.context.scene.objects:
 if o.get('shared_asset_id','').startswith(('assemblies/','openings/')):o['ifc_class']='IfcCovering'
 aid=o.get('shared_asset_id','')
 if aid.startswith(('cabinetry/','appliances/','fixtures/')):
  o['ifc_class']='IfcFurnishingElement' if aid.startswith('cabinetry/') else 'IfcSanitaryTerminal' if any(k in aid for k in ['basin','sink','tub','toilet','shower']) else 'IfcLightFixture' if 'lighting-' in aid or 'pendant' in aid else 'IfcBuildingElementProxy'
  o['export_linked_geometry']=True
 if o.type=='MESH' and ('open door' in o.name or 'Opaque entry pivot' in o.name or 'recessed sliding leaf' in o.name):o['ifc_class']='IfcDoor'
exporter=ROOT/'tools/common/export_scene_ifc.py';exporter_sha=hashlib.sha256(exporter.read_bytes()).hexdigest()
runpy.run_path(str(exporter),run_name='__main__')
assert hashlib.sha256(native.read_bytes()).hexdigest()==native_sha
path=HOME/'model/eichler-twin-gables.ifc';report_path=HOME/'model/ifc-validation.json';r=json.loads(report_path.read_text())
r.update({'source_blend_sha256':native_sha,'ifc_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'exporter_sha256':exporter_sha,'blender':bpy.app.version_string,'ifcopenshell':ifcopenshell.version,'limits':'Classified concept mesh geometry; not complete parametric BIM, selected equipment, construction or engineering documentation.'})
report_path.write_text(json.dumps(r,indent=2)+'\n')
