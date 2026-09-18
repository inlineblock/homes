"""Rebuild the first Lindon brick remodel concept. Blender 4.5, all meters."""
import sys, math, json, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(Path(__file__).parent),str(ROOT/'tools')]
import bpy
from mathutils import Vector
from common import geometry as g
from common.finish_palette import palette, textured
from common.timber_materials import apply_grain
from utils import *
import design
from openings import proposed_openings
from envelope import aperture_wall,wall_piece,build_roof,build_decks,build_entry,guard,poly_area,OPENING_SCHEDULE

SLUG='lindon-brick-house'
HOME=ROOT/'homes'/SLUG
for p in ['model','outputs/work','outputs/images','outputs/plans','assets','references/local']:(HOME/p).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection':bpy.data.collections.remove(c)
M=palette(ROOT)
from library.build_lindon_assets import BRICK_NAME
with bpy.data.libraries.load(str(ROOT/'library/materials/warm-red-brick/v001/warm-red-brick.blend'),link=True) as (src,dst):dst.materials=[BRICK_NAME]
M['brick']=dst.materials[0]
M['cedar']=material(ROOT,'warm-vertical-cedar','v003')
M['deck']=material(ROOT,'mountain-thermo-ash','v002')
M['roof']=material(ROOT,'charcoal-standing-seam')
M['concrete']=textured('Fine charcoal mineral foundation',(.21,.20,.185),(.28,.27,.24),80,.86,.001)
levels=design.LEVELS
level_names={'main':'Ground floor','upper':'Upper floor','basement':'Walkout basement'}
floor_objects=[]

def cut_void(obj,polygon,z):
    cutter=prism('Temporary stair opening cutter',polygon,z-.8,z+.8,M['plaster'])
    mod=obj.modifiers.new('Real floor void','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)

g.collection('02 Architecture | reconstructed floor polygons and stair voids')
for key,data in levels.items():
    z=data['z'];poly=data['footprint']
    floor=tag(prism(f'{key} occupied floor',poly,z-.24,z,M['oak']),'IfcSlab',level_names[key])
    floor.data.materials.append(M['brick'])
    for face in floor.data.polygons:
        if abs(face.normal.z)<.5:face.material_index=1
    floor['floor_area_role']='occupied';floor['level_key']=key
    for hole in data.get('voids',[]):
        cut_void(floor,hole.get('polygon',hole) if isinstance(hole,dict) else hole,z)
    floor_objects.append(floor)
garage=getattr(design,'GARAGE_POLYGON',getattr(design,'GARAGE_FOOTPRINT',[(14.60,1.70),(20.21,7.33),(28.63,-.64),(23.27,-5.97),(19.87,-2.54),(19.32,-3.07)]))
garagefloor=tag(prism('Three-car angled garage floor',garage,-.29,-.05,M['concrete']),'IfcSlab')
garagefloor['floor_area_role']='garage';floor_objects.append(garagefloor)
# Close the narrow roof strips where the upstairs footprint steps back from
# the garage. The upstairs floor remains the ceiling over occupied rooms.
cap_outline=list(garage)
if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(cap_outline,cap_outline[1:]+cap_outline[:1]))<0:cap_outline.reverse()
garagecap=tag(prism('Garage setback roof and ceiling',cap_outline,3.005,3.275,M['roof']),'IfcSlab')
garagecap.data.materials.append(M['brick']);garagecap.data.materials.append(M['ceiling'])
for face in garagecap.data.polygons:
    if abs(face.normal.z)<.5:face.material_index=1
    elif face.normal.z<-.5:face.material_index=2
cut_void(garagecap,levels['upper']['footprint'],3.25)

g.collection('01 Architecture | red brick exterior and redesigned openings')
for key,data in levels.items():
    z=data['z'];poly=data['footprint'];height=2.98 if key!='basement' else 2.91
    for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
        L=math.dist(a,b)
        if L<.05:continue
        ops=proposed_openings(key,a,b)
        aperture_wall(ROOT,f'{key} facade {i+1}',a,b,z,height,ops,M,level_names[key])
    # Ceiling is a separate collection object. No render-only ceiling removal
    # is saved into the canonical furnished scene.
    g.collection('07 Finishes | '+key+' ceilings')
    ceil=prism(key+' ceiling',poly,z+height,z+height+.07,M['ceiling'])
    ceil.data.materials.append(M['brick']);ceil.data.materials.append(M['roof'])
    for face in ceil.data.polygons:
        if abs(face.normal.z)<.5:face.material_index=1
        elif face.normal.z>.5:face.material_index=2
    for hole in data.get('ceiling_voids',[]):cut_void(ceil,hole.get('polygon',hole) if isinstance(hole,dict) else hole,z+height)
    g.collection('01 Architecture | '+key+' envelope continues')

# The garage has actual large door openings and a clear interior access edge.
for i,(a,b) in enumerate(zip(garage,garage[1:]+garage[:1])):
    L=math.dist(a,b);mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    if L<.1:continue
    if my<1 and L>4 and (b[0]-a[0])*(b[1]-a[1])<0:
        u=(Vector(b)-Vector(a))/L
        w=L-.65;start=Vector(a)+u*.325;end=Vector(b)-u*.325
        wall_piece('Garage door jamb',a,tuple(start),-.05,3.25,M['brick'])
        wall_piece('Garage door jamb',tuple(end),b,-.05,3.25,M['brick'])
        wall_piece('Garage door head',tuple(start),tuple(end),2.55,3.25,M['brick'])
        for j in range(19):
            obj=wall_piece('Flush timber garage door board',tuple(start),tuple(end),.04+j*.131,.04+j*.131+.119,M['cedar'],.095)
            tag(obj,'IfcDoor')
    else:
        aperture_wall(ROOT,'Garage side brick wall',a,b,-.05,3.3,proposed_openings('main',a,b),M,'Ground floor')

g.collection('06 Architecture | source-aligned interior partitions and open doors')
for key,data in levels.items():
    z=data['z'];h=2.91
    for index,w in enumerate(data.get('interior_wall_segments',[])):
        if (key=='basement' and w.get('name') in ['Stair storage north','Stair storage west','Stair storage east']) or (key=='main' and w.get('name','').startswith('Coat closet')):continue
        a,b=w['a'],w['b'];d=Vector(b)-Vector(a);L=d.length
        if L<.03:continue
        u=d/L;cur=0
        def part(t0,t1,bottom,top):
            if t1-t0<.02:return
            obj=wall_piece(w.get('name',key+' partition'),tuple(Vector(a)+u*t0),tuple(Vector(a)+u*t1),z+bottom,z+top,M['plaster'],.13)
            tag(obj,'IfcWall',level_names[key])
        for off,width in w.get('openings',[]):
            part(cur,off,0,h);part(off,off+width,2.35,h)
            # Open leaf at 80deg, leaving the source opening legible.
            if width<1.35:
                hinge=Vector(a)+u*(off+.02);d2=Vector((-u.y,u.x));center=hinge+d2*(width-.04)/2
                door=box('Open interior door',(center.x,center.y,z+1.16),(width-.04,.045,2.32),M['oak'],.004)
                door.rotation_euler.z=math.atan2(d2.y,d2.x);tag(door,'IfcDoor',level_names[key])
            cur=off+width
        part(cur,L,0,h)

build_decks(M);build_roof(M);build_entry(M)

# Use native shared furnishings and planting, rather than baked backdrop images.
if '--shell' not in sys.argv:
    from interiors import build_interiors
    interior_result=build_interiors(ROOT,M)
    from interiors import RECESSED_LIGHTS
    for x,y,z in RECESSED_LIGHTS:
        ceiling=min([o for o in bpy.context.scene.objects if o.name in ['main ceiling','upper ceiling','basement ceiling']], key=lambda o:abs(min(v.co.z for v in o.data.vertices)-z))
        cutter=cyl('Temporary recessed-light aperture',(x,y,z+.10),.044,.4,M['dark'])
        bpy.context.view_layer.objects.active=ceiling
        mod=ceiling.modifiers.new('Recessed light aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
        bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
import importlib.util
site_spec=importlib.util.spec_from_file_location('lindon_site',Path(__file__).parent/'site.py')
site_module=importlib.util.module_from_spec(site_spec);site_spec.loader.exec_module(site_module)
site_result=site_module.build_site(ROOT,M)

from stairs import build_stairs
stair_receipt=build_stairs(M)
(HOME/'model'/'stair-review.json').write_text(json.dumps(stair_receipt,indent=2)+'\n')

g.collection('20 Cameras and illumination')
CAMERAS={
 '01-front-arrival':((35,-39,12),(12,6,3.2),47),
 '02-rear-terraces':((30,41,9),(14,14,2.7),46),
 '03-roof-and-site':((65,-44,49),(15,14,1),45),
 '04-brick-and-windows':((-14,-19,8),(7,7,3),51),
 '07-pool-garden':((39,38,3.1),(18,19,2.0),33),
 '08-court-and-garage':((54,9,5),(22,6,2.5),43),
}
for name,(loc,target,lens) in CAMERAS.items():camera(name,loc,target,lens)

world=bpy.data.worlds.new('Soft late-afternoon sky');world.use_nodes=True;bpy.context.scene.world=world
n=world.node_tree.nodes;l=world.node_tree.links
sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(32);sky.sun_rotation=math.radians(215);sky.altitude=.8;sky.air_density=1.1;sky.dust_density=.8;sky.sun_disc=False
l.new(sky.outputs['Color'],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.42
sun=bpy.data.lights.new('Soft afternoon sun','SUN');sun.energy=2.2;sun.angle=.08;sun.color=(1,.91,.81)
o=bpy.data.objects.new(sun.name,sun);g.ACTIVE.objects.link(o);o.rotation_euler=(math.radians(35),math.radians(-25),math.radians(-35))
area('Broad photographic sky fill',(7,-11,19),(11,8,4),1900,14,(.82,.90,1))

scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=True;scene.cycles.max_bounces=8
scene.cycles.transparent_max_bounces=8;scene.cycles.transmission_bounces=6
scene.render.resolution_x=1800;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.5
scene.render.film_transparent=False;scene.camera=bpy.data.objects['01-front-arrival']
scene.render.filepath='//../outputs/work/01-front-arrival.png';scene['concept_stage']='Listing-based first remodel concept; site and dimensions approximate'
scene['source_listing_area_sqft']=6807;scene['bedrooms']=7

# Explicit physical-meter grain mapping for local timber members.
bpy.context.view_layer.update()
apply_grain([M['cedar'],M['deck']])
from library.build_lindon_assets import apply_brick_uv
for obj in bpy.context.scene.objects:
    if obj.type=='MESH' and obj.library is None and any(mat==M['brick'] for mat in obj.data.materials):apply_brick_uv(obj)

native=HOME/('outputs/work' if '--shell' in sys.argv else 'model')/f'{SLUG}.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(native))
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath))
bpy.ops.wm.save_as_mainfile(filepath=str(native))
(HOME/'model'/'opening-schedule.json').write_text(json.dumps(OPENING_SCHEDULE,indent=2)+'\n')
print('LINDON_NATIVE_SAVED',native,flush=True)
