"""Generate Atrium 01. Run using Blender --background --python this-file."""
import bpy,sys,math,random,json
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(Path(__file__).parent))
from common import geometry as g
from common.geometry import box,cyl,sphere,rod,curve,area,collection,camera,F
from common.materials import palette
from design import *
import kitchen
random.seed(26)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name!='Collection':bpy.data.collections.remove(c)
M=palette();HOME=ROOT/'homes/atrium-01'

def segment(name,a,b,z,h,thick,mat):
    mid=((a[0]+b[0])/2,(a[1]+b[1])/2,z+h/2)
    return box(name,mid,(abs(b[0]-a[0]) if a[1]==b[1] else thick,abs(b[1]-a[1]) if a[0]==b[0] else thick,h),mat,.014)
def glazing(name,a,b,sill=.12,head=8.7,door=False):
    dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);n=max(1,round(length/4))
    for j in range(n+1):
        x=a[0]+dx*j/n;y=a[1]+dy*j/n
        box(name+' mullion',(x,y,(head+sill)/2),(.11,.11,head-sill),M['black'],.006)
    for z in [sill,head]:segment(name+' frame',a,b,z,.1,.11,M['black'])
    for j in range(n):
        p=(a[0]+dx*(j+.04)/n,a[1]+dy*(j+.04)/n);q=(a[0]+dx*(j+.96)/n,a[1]+dy*(j+.96)/n)
        segment(name+' pane',p,q,sill+.1,head-sill-.2,.025,M['glass'])
    if door:
        x=a[0]+dx*.58;y=a[1]+dy*.58
        rod(name+' sliding pull',(x+.09,y+.09,3),(x+.09,y+.09,4.2),.032,M['black'])

collection('01 Architecture | walls and glazing')
for name,a,b,t,opens in WALLS:
    length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
    point=lambda d:(a[0]+ux*d,a[1]+uy*d)
    cursor=0
    for offset,w,sill,head,kind in sorted(opens):
        if offset>cursor:segment(name+' solid',point(cursor),point(offset),0,HEIGHT,t,M['plaster'])
        if sill:segment(name+' sill',point(offset),point(offset+w),0,sill,t,M['plaster'])
        segment(name+' header',point(offset),point(offset+w),head,HEIGHT-head,t,M['plaster'])
        if kind in ['window','glass','entry']:glazing(name+' '+kind,point(offset),point(offset+w),sill,head,kind=='entry')
        if kind=='door':
            # Door leaf deliberately shown open, preserving clear passage.
            inward=-1 if name in ['bedroom-gallery','entry-bath-east','pantry-east'] else 1
            p=point(offset);leaf=box(name+' open walnut door',(p[0]+(inward*1.45 if uy else 0),p[1]+(1.45 if ux else 0),3.7),(2.9 if uy else .12,.12 if uy else 2.9,7.4),M['walnut'],.025)
        cursor=offset+w
    if cursor<length:segment(name+' solid',point(cursor),point(length),0,HEIGHT,t,M['plaster'])
for name,a,b in COURTYARD_GLAZING:glazing(name,a,b,door=True)
collection('02 Architecture | floors')
for x1,y1,x2,y2 in SLABS:box('Honed concrete floor',((x1+x2)/2,(y1+y2)/2,-.20),(x2-x1,y2-y1,.4),M['concrete'],.02)
roof=collection('09 Roof | hide for cutaway')
for x1,y1,x2,y2 in SLABS:
    box('Flat insulated roof',((x1+x2)/2,(y1+y2)/2,9.4),(x2-x1,y2-y1,.6),M['plaster'],.015)
    # Interior ceiling board rhythm, derived from the floor footprint to leave atrium open.
    for i in range(int((x2-x1)/.65)):
        x=x1+.325+i*.65
        box('Painted tongue-and-groove ceiling',(x,(y1+y2)/2,9.08),(.63,y2-y1,.075),M['plaster'],.006)
collection('08 Structure | exposed fir')
for y in [0,8,16,24,32,40,44]:
    spans=[(0,22),(38,60)] if 10<y<25 else [(0,60)]
    for x1,x2 in spans:box('Exposed fir beam',((x1+x2)/2,y,8.63),(x2-x1,.38,.65),M['fir'],.02)
for x in [22,38]:
    box('Atrium edge beam',(x,17.5,8.65),(.38,15,.6),M['fir'],.02)
    for y in [10,25]:box('Atrium timber post',(x,y,4.35),(.3,.3,8.7),M['fir'],.018)
kitchen.build(ROOT,M)

collection('04 Furnishings | living and dining')
# Dining table, six upholstered chairs.
box('Dining tabletop',(48.5,26.3,2.55),(8,3.6,.20),M['walnut'],.22)
for x in [45.4,51.6]:
    for y in [25.1,27.5]:rod('Dining table leg',(x,y,.1),(x,y,2.45),.11,M['walnut'])
for x in [45.7,48.5,51.3]:
    for y,sign in [(23.7,-1),(28.9,1)]:
        box('Dining chair upholstered seat',(x,y,1.5),(1.65,1.55,.22),M['fabric'],.12)
        box('Dining chair curved back',(x,y+sign*.65,2.35),(1.67,.18,1.23),M['walnut'],.15)
        for dx in [-.6,.6]:
            for dy in [-.55,.55]:rod('Chair leg',(x+dx,y+dy,.04),(x+dx*.9,y+dy*.9,1.45),.045,M['black'])
box('Living woven rug',(44,37,.025),(16,10,.05),M['fabric'],.08)
box('Low walnut sofa base',(43.5,41,.6),(11,3.4,.4),M['walnut'],.12)
box('Oatmeal sofa back',(43.5,42.4,1.72),(11,.5,1.95),M['fabric'],.25)
for x in [39.7,43.5,47.3]:box('Sofa cushion',(x,40.9,1.12),(3.6,2.9,.58),M['fabric'],.23)
for x in [38.1,48.9]:box('Sofa arm',(x,41,1.37),(.45,3.4,1.5),M['fabric'],.17)
box('Walnut coffee table',(44,36.8,1.1),(6,2.9,.2),M['walnut'],.4)
for x in [42,46]:box('Coffee table support',(x,36.8,.53),(.25,2,.95),M['walnut'],.02)
box('Sculptural hearth',(29.1,38.4,1),(1.6,8,2),M['stone'],.04)
box('Hearth firebox',(30,38.4,1.22),(.03,4,1.2),M['black'],.01)
cyl('Dining pendant',(48.5,26.3,6.65),1.05,.22,M['black'])
rod('Dining pendant cable',(48.5,26.3,8.9),(48.5,26.3,6.75),.018,M['black'])
area('Dining light',(48.5,26.3,6.4),(48.5,26.3,2),100,2)

collection('05 Private rooms | bedroom and bath fitout')
for label,x,y,w in [('Bedroom 02',8,5.7,5),('Bedroom 03',8,25,5),('Primary',8,37,6.4)]:
    box(label+' bed frame',(x,y,.62),(w+.35,6.9,.4),M['walnut'],.12)
    box(label+' mattress',(x,y,1.07),(w,6.6,.55),M['fabric'],.18)
    box(label+' headboard',(x,y+3.35,1.8),(w+.8,.22,2.8),M['walnut'],.09)
    for dx in [-w*.24,w*.24]:box(label+' pillow',(x+dx,y+2.1,1.5),(w*.43,1.55,.25),M['white'],.18)
    box(label+' folded sage blanket',(x,y-1.8,1.43),(w+.02,2.1,.12),M['sage'],.05)
    for dx in [-w/2-1,w/2+1]:box(label+' bedside',(x+dx,y+2.4,1),(1.4,1.4,1.8),M['walnut'],.045)
def bathroom(label,x,y,w,d):
    box(label+' tile floor',(x+w/2,y+d/2,.03),(w-.3,d-.3,.055),M['stone'],.015)
    box(label+' vanity',(x+w*.65,y+d-1.1,1.65),(3.4,1.8,2.4),M['walnut'],.025)
    box(label+' vanity top',(x+w*.65,y+d-1.1,2.9),(3.5,2,.12),M['stone'],.02)
    sphere(label+' basin',(x+w*.65,y+d-1.1,3.0),(1,.6,.15),M['white'])
    box(label+' mirror',(x+w*.65,y+d-.22,5.2),(3,.06,2.8),M['steel'],.04)
    box(label+' shower tray',(x+2,y+2,.13),(3.5,3.5,.2),M['stone'],.02)
    box(label+' shower glass',(x+3.8,y+2,3.7),(.035,3.5,7.2),M['glass'])
    cyl(label+' rain shower',(x+2,y+1.2,7.6),.37,.06,M['steel'])
    rod(label+' shower riser',(x+.3,y+1.2,4),(x+.3,y+1.2,7.6),.04,M['steel'])
    box(label+' WC cistern',(x+1,y+d-1,1.7),(1.3,.6,2.4),M['white'],.2)
    sphere(label+' WC bowl',(x+1,y+d-2,1.13),(.67,1,.57),M['white'])
bathroom('Bath 02',8,12,10,8);bathroom('Bath 03',22,0,8,8);bathroom('Primary ensuite',18,34,10,10)
for y in [1.6,4.2]:box('Laundry appliance',(39.6,y,1.5),(2.6,2.4,3),M['white'],.06)

collection('06 Landscape | atrium and terrace')
box('Ground',(30,20,-.65),(180,150,.8),M['soil'],.08)
box('East terrace',(67,24,-.2),(14,47,.35),M['concrete'],.04)
box('Atrium gravel bed',(30,17.5,-.12),(15.8,14.8,.17),M['stone'],.04)
for y in [11.7,14.7,17.7,20.7,23.7]:box('Atrium stepping slab',(34,y,.015),(4.8,2.5,.12),M['concrete'],.03)
box('Atrium planting bed',(26.3,18,.02),(6.3,9,.17),M['soil'],.15)
def tree(x,y,z=0,scale=1):
    rod('Olive trunk',(x,y,z),(x+.16*scale,y+.1*scale,z+6*scale),.15*scale,M['fir'])
    vertices=[];faces=[]
    for i in range(9):
        a=i*2.399;xx=x+math.cos(a)*2*scale;yy=y+math.sin(a)*2*scale;zz=z+(5.2+random.random()*2)*scale
        rod('Olive branch',(x,y,z+3.3*scale),(xx,yy,zz),.035*scale,M['fir'])
        for j in range(140):
            center=Vector((xx+random.uniform(-.9,.9)*scale,yy+random.uniform(-.8,.8)*scale,zz+random.uniform(-.7,.7)*scale))
            angle=random.random()*math.tau;tilt=random.uniform(-.8,.8)
            u=Vector((math.cos(angle),math.sin(angle),tilt)).normalized();v=u.cross(Vector((0,0,1))).normalized()
            length=random.uniform(.11,.21)*scale;width=length*.23;base=len(vertices)
            vertices.append(tuple((center+Vector((0,0,.02*scale)))*F))
            for k in range(8):
                a=math.tau*k/8;vertices.append(tuple((center+u*math.cos(a)*length+v*math.sin(a)*width)*F))
            for k in range(8):faces.append((base,base+1+k,base+1+(k+1)%8))
    mesh=bpy.data.meshes.new('Olive leaf canopy');mesh.from_pydata(vertices,[],faces);mesh.materials.append(M['leaves'])
    obj=bpy.data.objects.new('Olive leaf canopy',mesh);g.ACTIVE.objects.link(obj)
tree(26.5,18,scale=.9)
for x,y,s in [(73,39,1.6),(-12,30,1.6),(-9,-7,1.25),(70,-8,1.25),(40,57,1.5)]:tree(x,y,scale=s)
for i in range(85):
    x=random.uniform(23.4,29);y=random.uniform(14,22)
    sphere('Atrium river pebble',(x,y,.08),(.10,.075,.055),M['concrete'])
for y in [-5,-10,-15]:box('Entry approach',(33,y,-.15),(6,4,.3),M['concrete'],.04)

collection('10 Lighting and cameras')
world=bpy.data.worlds.new('Daylight atmosphere');bpy.context.scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(32);sky.sun_rotation=math.radians(135);sky.sun_intensity=.5;sky.altitude=.1
l.new(sky.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.3
d=bpy.data.lights.new('Late afternoon sun','SUN');d.energy=2;d.angle=.06;o=bpy.data.objects.new(d.name,d);g.ACTIVE.objects.link(o);o.rotation_euler=(math.radians(28),math.radians(-32),math.radians(-25))
area('East glazing daylight',(63,16,7),(48,10,2),850,18,(.80,.89,1),shape='RECTANGLE',size_y=7)
area('Atrium soft daylight',(30,17,12),(46,10,3),650,10,(1,.92,.8))
area('Kitchen camera fill',(40,22,7),(53,6,3),260,9,(1,.93,.84))
cams={name:camera(name,*data) for name,data in CAMERAS.items()}
scene=bpy.context.scene;scene.camera=cams['01 Kitchen hero'];scene.unit_settings.system='IMPERIAL';scene.unit_settings.length_unit='FEET';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
scene.cycles.max_bounces=8;scene.cycles.transparent_max_bounces=8
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for device in prefs.devices:device.use=(device.type=='METAL')
    scene.cycles.device='GPU'
except Exception as e:print('GPU setup:',e)
scene.render.resolution_x=1600;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.65
scene.render.film_transparent=False
scene['design_stage']='Architectural concept; not construction documents'
scene['enclosed_gross_area_sqft']=GROSS_AREA;scene['bedrooms']=3;scene['bathrooms']=3
scene['area_formula']='60 x 44 - 16 x 15 = 2400 sqft; includes walls, excludes atrium'
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/atrium-01.blend'))
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(HOME/'model/atrium-01.blend'))
# Text manifest is generated from the same measured design.
manifest={'schema_version':1,'id':'atrium-01','name':'Atrium 01','status':'concept','units':'meters','display_units':'feet-inches','target_area_sqft':2400,'gross_enclosed_area_sqft':GROSS_AREA,'area_basis':scene['area_formula'],'bedrooms':3,'bathrooms':3,'software':{'blender':bpy.app.version_string,'bonsai':'0.8.5'},'asset_dependencies':[{'id':'materials/sage-fluted-tile','version':'v001','path':'../../library/materials/sage-fluted-tile/v001/sage-fluted-tile.blend'}],'deliverables':{'presentation_model':'model/atrium-01.blend','architectural_model':'model/atrium-01.ifc','floor_plan':'drawings/floor-plan.svg','kitchen_render':'renders/01-kitchen.png'}}
(HOME/'project.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('MODEL_SAVED',len(scene.objects),'objects',GROSS_AREA,'sqft')
if '--render' in sys.argv:
    scene.render.filepath=str(HOME/'renders/01-kitchen.png');bpy.ops.render.render(write_still=True)
