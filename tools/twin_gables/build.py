"""Reproducible Twin Gables native build; no gallery or document promotion."""
import argparse,sys,json,os,math,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).resolve().parent)]
from common import geometry as g
from common.geometry import F,box,area,camera,material
from common.materials import noise_material
from assets import material as linked_material,PINS
from design import *
import architecture,interior
import importlib.util
spec=importlib.util.spec_from_file_location('twin_site',Path(__file__).with_name('site.py'));site=importlib.util.module_from_spec(spec);spec.loader.exec_module(site)
HOME=ROOT/'homes'/SLUG
if not (HOME/'design-intent.md').exists():raise RuntimeError('Record design intent before geometry')
bpy.ops.wm.read_factory_settings(use_empty=True)
M={
 'cedar':linked_material('warm-vertical-cedar','v003'),
 'roof':linked_material('charcoal-standing-seam','v002'),
 'plaster':linked_material('warm-limestone-plaster'),
 'stone':linked_material('coastal-honed-limestone'),
 'oak':linked_material('smoked-oak'),
 'dark':linked_material('charcoal-facade-panel'),
 'meadow':noise_material('Illustrative woodland meadow',(.08,.125,.046),(.19,.235,.09),85,.92,.012),
 'soil':noise_material('Illustrative garden loam',(.06,.055,.037),(.13,.11,.07),35,1,.015),
 'paving':noise_material('Site-specific subdued driveway',(.14,.15,.14),(.23,.23,.21),60,.85,.003),
 'glass':material('Twin Gables clear envelope glass',(.95,.98,.96),.045),
}
p=M['glass'].node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
architecture.build(M);print('ARCHITECTURE_READY',flush=True)
interior.build(M);print('INTERIOR_READY',flush=True)
site.build(M);print('SITE_READY',flush=True)
g.collection('10 Lighting and cameras')
world=bpy.data.worlds.new('Daylight woodland sky');world.use_nodes=True;bpy.context.scene.world=world
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(29);sky.sun_rotation=math.radians(225);sky.sun_intensity=.8
l.new(sky.outputs['Color'],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.28
area('Large cool front fill',(34,-30,30),(34,25,5),1200,40,(.84,.91,1))
area('Large garden fill',(34,95,30),(34,30,5),1500,50,(.87,.93,1))
for name,args in VIEWS.items():camera(name,*args)
s=bpy.context.scene;s.camera=bpy.data.objects['01-front'];s.unit_settings.system='IMPERIAL';s.unit_settings.length_unit='FEET';s.unit_settings.scale_length=1
s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=True;s.cycles.max_bounces=10;s.cycles.transparent_max_bounces=12
s.render.resolution_x=1800;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.0
s['home_id']=SLUG;s['gross_enclosed_area_sqft']=AREA;s['bedrooms']=2;s['bathrooms']=3;s['flex_guest_beds']=1;s['stage']='Architectural concept with generic equipment; engineering and site unverified'
s.render.filepath='//../outputs/work/01-front.png'
(HOME/'model').mkdir(parents=True,exist_ok=True)
path=HOME/'model'/f'{SLUG}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path))
# Actual native links include transitive materials and hardware.
for lib in bpy.data.libraries:
 folder=Path(bpy.path.abspath(lib.filepath)).resolve().parent;meta=json.loads((folder/'asset.json').read_text());PINS[meta['id']]=meta['version']
(HOME/'model/asset-pins.json').write_text(json.dumps([{'id':k,'version':v,'path':os.path.relpath(ROOT/'library'/k/v,HOME)+'/'} for k,v in sorted(PINS.items())],indent=2)+'\n')
# Portable plan records derive from actual furnished asset bounds and exact wall source.
items=[]
for o in s.objects:
 if o.instance_type!='COLLECTION' or not o.get('shared_asset_id'):continue
 aid=o['shared_asset_id'];ver=o['shared_asset_version']
 if aid.split('/')[0] not in ['furniture','cabinetry','appliances','fixtures']:continue
 if any(k in aid for k in ['lighting','pendant','hood']):continue
 meta=json.loads((ROOT/'library'/aid/ver/'asset.json').read_text());bounds=meta.get('bounds_m')
 if bounds:
  lo,hi=bounds['min'],bounds['max']
 else:
  dims=meta.get('dimensions_m',[1,1,1]);lo=[-dims[0]/2,-dims[1]/2,0];hi=[dims[0]/2,dims[1]/2,dims[2]]
 if 'vanity-basin' in aid:lo=[-.275,-.2286,0];hi=[.275,.2286,.2]
 pts=[o.matrix_world@Vector((x,y,0)) for x,y in [(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])]]
 items.append({'name':o.name,'kind':aid.split('/')[0],'asset':aid,'footprint':[[round(p.x/F,4),round(p.y/F,4)] for p in pts],'rotation':o.rotation_euler.z})
for o in s.objects:
 if o.type=='MESH' and ('stone' in o.name.lower() and ('Island' in o.name or 'vanity' in o.name or 'cooking' in o.name)):
  pts=[o.matrix_world@Vector(v) for v in o.bound_box];items.append({'name':o.name,'kind':'counter','rect':[min(p.x for p in pts)/F,min(p.y for p in pts)/F,max(p.x for p in pts)/F,max(p.y for p in pts)/F]})
records={'units':'feet','footprint':[0,0,WIDTH,DEPTH],'courtyard':COURT,'rooms':ROOMS,'walls':architecture.PLAN_WALLS,'furnishings':items,'site':[{'name':'Two parking spaces','kind':'parking','rect':[71,-30,95,28]},{'name':'Rear terrace','kind':'terrace','rect':[-1,60,69,72.4]},{'name':'Private entry path','kind':'path','rect':[29.95,-36,38.05,0]},{'name':'Parking pedestrian link','kind':'path','rect':[35,-22.5,79,-17.5]},{'name':'Road','kind':'road','rect':[-41,-50,109,-30]},{'name':'Parking bay 1','kind':'parking','rect':[73,-9,82,11]},{'name':'Parking bay 2','kind':'parking','rect':[84,-9,93,11]},{'name':'West court planting','kind':'planting','rect':[28.075,13.5,31.925,32.5]},{'name':'East court planting','kind':'planting','rect':[36.075,13.5,39.925,32.5]},{'name':'Central maple planting','kind':'planting','rect':[32.25,22.25,35.75,25.75]}],'plan_trees':[{'at':[34,24],'radius':7.1,'name':'Japanese maple'}],'roof':{'roof_eave_ft':EAVE,'roof_ridge_ft':RIDGE,'nominal_lining_eave_ft':CEILING_EAVE,'nominal_lining_ridge_ft':CEILING_RIDGE,'ridge_cover_underside_ft':16.45,'rafter_cover_lower_chord_at_wall_ft':10.73,'rafter_peak_lower_chord_ft':16.33,'flat_bed_support_ft':10,'connector_finished_ft':12},'limitations':['Site-specific concept only, not engineered or jurisdiction approved.','Dimensions are gross wall grid unless specifically called clear.']}
(HOME/'model/plan-data.json').write_text(json.dumps(records,indent=2)+'\n')
print('TWIN_NATIVE_READY',len(s.objects),'objects',len(PINS),'pins',AREA,'sqft',flush=True)
