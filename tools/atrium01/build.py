"""Build the coordinated courtyard concept; meter geometry and exact library pins."""
import bpy,sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from common import geometry as g
from common.materials import palette
from api import box,rod,cyl,area,camera,asset,linked_material,write_layout,dependencies
import design as d
import architecture,interiors,shading
HOME=ROOT/'homes/atrium-01'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):bpy.data.collections.remove(c)
M=palette()
for key,slug in [('walnut','warm-walnut'),('stone','coastal-honed-limestone'),('plaster','warm-limestone-plaster'),('dark','charcoal-facade-panel'),('fabric','woven-oatmeal')]:M[key]=linked_material(slug)
site=architecture.build(ROOT,M,asset,box,rod,cyl)
g.collection('03 Interiors | linked furnishings and equipment')
inside=interiors.build(ROOT,M,asset,box,rod,cyl,area)
# Actual downlight bores continue through the ceiling finish into the reserved
# assembly depth; fixture bodies must not be pasted over an uncut surface.
from mathutils import Vector
bpy.context.view_layer.update()
cut_receipts=[]
for item in inside.get('ceiling_cutouts',[]):
    x,y,z=item['center_m'];radius=item['radius_m']+.001;depth=item['housing_depth_m']+.004
    cutter=cyl('Temporary lighting housing aperture',(x,y,z+depth/2-.006),radius,depth+.024,M['dark'],32)
    bpy.context.view_layer.update();targets=[]
    for obj in list(bpy.context.scene.objects):
        if obj.type!='MESH' or obj==cutter or not any(c.name.startswith('09 Roof') for c in obj.users_collection):continue
        bounds=[obj.matrix_world@Vector(v) for v in obj.bound_box]
        low=[min(v[i] for v in bounds) for i in range(3)];high=[max(v[i] for v in bounds) for i in range(3)]
        if low[0]<x+radius and high[0]>x-radius and low[1]<y+radius and high[1]>y-radius and low[2]<z+depth and high[2]>z-.02:
            mod=obj.modifiers.new('Actual recessed housing aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
            bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=mod.name);targets.append(obj.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
    assert targets, ('No ceiling at fixture',item)
    cut_receipts.append({'name':item['name'],'center_m':item['center_m'],'cut_meshes':targets,'diameter_m':radius*2,'housing_depth_m':depth})
# The extraction duct has an actual opening through the roof and ceiling.
exhaust_xy=(50.25*.3048,8.78*.3048)
cutter=box('Temporary cooking exhaust aperture',(*exhaust_xy,(d.HEIGHT+3.72)/2),(.35,.31,3.72-d.HEIGHT+.04),M['dark'])
bpy.context.view_layer.update();exhaust_targets=[]
for obj in list(bpy.context.scene.objects):
    if obj.type!='MESH' or obj==cutter or not any(c.name.startswith('09 Roof') for c in obj.users_collection):continue
    bounds=[obj.matrix_world@Vector(v) for v in obj.bound_box]
    if min(v.x for v in bounds)<exhaust_xy[0]+.175 and max(v.x for v in bounds)>exhaust_xy[0]-.175 and min(v.y for v in bounds)<exhaust_xy[1]+.155 and max(v.y for v in bounds)>exhaust_xy[1]-.155 and max(v.z for v in bounds)>d.HEIGHT-.02:
        mod=obj.modifiers.new('Actual cooking exhaust roof aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
        bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=mod.name);exhaust_targets.append(obj.name)
bpy.data.objects.remove(cutter,do_unlink=True)
assert exhaust_targets
inside['exhaust_roof_aperture']={'center_xy_m':list(exhaust_xy),'size_xy_m':[.35,.31],'cut_meshes':exhaust_targets}
inside['modeled_ceiling_apertures']=cut_receipts
inside['bedroom_shades']=shading.build(ROOT,asset)
from common.timber_materials import grain_uv
for obj in bpy.context.scene.objects:
    if obj.type=='MESH' and obj.library is None and any(mat == M['walnut'] for mat in obj.data.materials):grain_uv(obj)
write_layout()
g.collection('10 Lighting and cameras')
world=bpy.data.worlds.new('Clear mild daylight');bpy.context.scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links
sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(35);sky.sun_rotation=math.radians(135);sky.sun_intensity=.35
l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.22
sun=bpy.data.lights.new('Warm daylight sun','SUN');sun.energy=2.0;sun.angle=.07
o=bpy.data.objects.new(sun.name,sun);g.ACTIVE.objects.link(o);o.rotation_euler=(math.radians(24),math.radians(-35),math.radians(-30))
F=.3048
from cameras import CAMERAS as views
for name,(loc,target,lens) in views.items():camera(name,tuple(v*F for v in loc),tuple(v*F for v in target),lens)
# Broad, physically placed daylight portals supplement the sky, outside glazing.
for name,loc,target,power,size in [
('East kitchen daylight',(61,21,7),(50,20,4),260,8),
('Court daylight',(32,20,12),(47,19,4),300,9),
('Rear living daylight',(51,46,7),(51,36,4),260,10),
('Primary north daylight',(7,46,7),(7,37,3),180,8),
('Primary soft bounce',(4,33,8.3),(11,38,3),120,5),
('Bath soft bounce',(19,36,8.4),(17,40,3),110,4)]:
    area(name,[v*F for v in loc],[v*F for v in target],power,size*F,(.91,.95,1))
s=bpy.context.scene;s.camera=bpy.data.objects['03-exterior'];s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=True;s.cycles.max_bounces=10;s.cycles.transparent_max_bounces=12
s.render.resolution_x=1600;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.45
s['design_stage']='Coordinated architectural concept; engineering and products unverified'
s['enclosed_gross_area_sqft']=2400;s['bedrooms']=3;s['bathrooms']=3
s['ceiling_plane_m']=10.5*F;s['beam_clear_m']=9.5*F;s['service_clear_m']=9*F
s['area_formula']='60 x 44 - 16 x 15 = 2400 sqft; gross including walls; excludes open atrium, carport, canopy and terraces'
s.render.filepath='//../outputs/images/03-exterior.png'
(HOME/'model').mkdir(parents=True,exist_ok=True)
# Prune unused palette datablocks; direct shared links are retained by scene use.
for mat in list(bpy.data.materials):
    if mat.users==0 and mat.library is None:bpy.data.materials.remove(mat)
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/atrium-01.blend'))
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/atrium-01.blend'))
meta={'schema_version':1,'id':'atrium-01','name':'Atrium 01','status':'concept','units':'meters','display_units':'feet-inches','target_area_sqft':2400,'gross_enclosed_area_sqft':2400,'area_basis':s['area_formula'],'bedrooms':3,'bathrooms':3,'storeys':[{'name':'Ground floor','elevation_m':0}], 'software':{'blender':bpy.app.version_string},'ceiling_heights_m':{'finished_ceiling_plane':10.5*F,'lowest_main_beam':9.5*F,'service_ceiling':9*F},'asset_dependencies':dependencies(),'deliverables':{'presentation_model':'model/atrium-01.blend','architectural_model':'model/atrium-01.ifc','floor_plan':'outputs/plans/floor-plan.svg','floor_plan_pdf':'outputs/plans/floor-plan.pdf','floor_plan_preview':'outputs/plans/floor-plan.png','primary_render':'outputs/images/03-exterior.png','render_gallery':'outputs/README.md','renders':[f'outputs/images/{name}.png' for name in views]}}
(HOME/'project.json').write_text(json.dumps(meta,indent=2)+'\n')
(HOME/'model/design-metadata.json').write_text(json.dumps({'site':site,'interiors':inside},indent=2,default=str)+'\n')
print('ATRIUM_MODEL_SAVED',len(s.objects),len(meta['asset_dependencies']),flush=True)
