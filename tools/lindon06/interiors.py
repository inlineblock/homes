"""Proposed light-oak furnishings within the approximate sourced Lindon plan.

Pure placement schedules can be imported by plan drawings without Blender.
Positions and dimensions are meters, rotations are radians about +Z. Library
assets are rigid instances; bespoke worktops/chases fit this house's layout.
"""
from pathlib import Path
import math,json
from design import LEVELS, FIXTURE_CENTERS

ROOT=Path(__file__).resolve().parents[2]
FURNITURE=[]
FIXTURES=[]

def add(target,level,name,kind,category,slug,x,y,rotation=0,z=None,version='v001'):
    manifest=ROOT/'library'/category/slug/version/'asset.json'
    dims=json.loads(manifest.read_text())['dimensions_m'] if manifest.exists() else [1,1,1]
    row={'level':level,'name':name,'kind':kind,'asset':category+'/'+slug,'version':version,
         'location':[x,y,LEVELS[level]['z'] if z is None else z],
         'dimensions':dims,'rotation':rotation}
    target.append(row);return row

def furniture(level,name,kind,slug,x,y,rotation=0):
    return add(FURNITURE,level,name,kind,'furniture',slug,x,y,rotation)

def fixture(level,name,kind,category,slug,x,y,rotation=0,z=None,version='v001'):
    return add(FIXTURES,level,name,kind,category,slug,x,y,rotation,z,version)

# Bed positions intentionally avoid the traced closet and bedroom-door zones.
BED_LAYOUT=[(1,'upper',14.85,9.05,-math.pi/2,'king'),(2,'upper',5.72,10.45,-math.pi/2,'queen'),
 (3,'upper',9.45,1.40,0,'queen'),(4,'upper',22.85,2.60,math.pi/4,'queen'),
 (5,'upper',26.30,-.20,math.pi/4,'queen'),(6,'basement',2.00,7.15,math.pi,'queen'),
 (7,'basement',1.42,1.95,-math.pi/2,'queen')]
for number,level,x,y,angle,size in BED_LAYOUT:
    furniture(level,f'Bedroom {number} shared bed frame','bed','oak-linen-'+size+'-bed',x,y,angle)
    for sign in [-1,1]:
        dx=(1.32 if size=='king' else 1.13)*sign;dy=-.72
        furniture(level,f'Bedroom {number} bedside {sign}','nightstand','oak-open-nightstand',
                  x+dx*math.cos(angle)-dy*math.sin(angle),y+dx*math.sin(angle)+dy*math.cos(angle),angle)

def wardrobe(level,name,x,y,angle=0):
    fixture(level,name,'wardrobe','cabinetry','oak-wardrobe-2ft',x,y,angle)

for x in [11.80,12.41,13.02]:wardrobe('upper','Primary closet north hanging',x,10.38)
for x in [10.45,11.06,11.67]:wardrobe('upper','Primary closet south hanging',x,7.39,math.pi)
for y in [10.18,10.79,11.40]:wardrobe('upper','Bedroom 2 closet',8.53,y,-math.pi/2)
for x in [9.18,9.79]:wardrobe('upper','Bedroom 3 closet',x,4.13)
for i in range(4):wardrobe('upper','Bedroom 4 angled closet',20.36+i*.4313,4.00+i*.4313,math.pi/4)
for i in range(3):wardrobe('upper','Bedroom 5 walk-in closet',23.62+i*.4313,-3.49+i*.4313,math.pi/4)
for x in [.62,1.23]:wardrobe('basement','Bedroom 6 closet',x,3.88,math.pi)
for x in [4.30,4.91,5.52,6.13,6.74]:wardrobe('basement','Bedroom 7 walk-in closet',x,3.10,math.pi)
wardrobe('main','Garage entry shared coat wardrobe',12.10,3.50,math.pi/2)
for x in [8.2,8.81,9.42]:wardrobe('basement','General linen and household storage',x,.52,math.pi)

def dining(level,name,x,y,angle=0):
    furniture(level,name+' table','table','oak-dining-table-8ft',x,y,angle)
    for side in [-1,1]:
        for dx in [-.82,0,.82]:
            dy=side*.97
            furniture(level,name+' chair','chair','oak-upholstered-dining-chair',
                x+dx*math.cos(angle)-dy*math.sin(angle),y+dx*math.sin(angle)+dy*math.cos(angle),
                angle+(0 if side>0 else math.pi))
dining('main','Formal dining',9.47,2.22,math.pi/2)
dining('main','Breakfast dining',14.2,14.05)
furniture('basement','Second kitchen dining table','table','oak-round-dining-table-1000',7.0,9.55)
for dx,dy,angle in [(-.94,0,-math.pi/2),(.94,0,math.pi/2),(0,-.94,math.pi),(0,.94,0)]:
    furniture('basement','Second kitchen dining chair','chair','oak-upholstered-dining-chair',7+dx,9.55+dy,angle)
furniture('main','Formal living sofa','sofa','linen-three-seat-sofa',2.18,1.20)
furniture('main','Formal living coffee table','table','oak-rounded-coffee-table',2.18,2.80)
for x in [1.1,3.15]:furniture('main','Formal living accent chair','chair','oak-upholstered-dining-chair',x,4.30)
furniture('main','Family room south sofa','sofa','linen-three-seat-sofa',14.35,8.25)
furniture('main','Family room north sofa','sofa','linen-three-seat-sofa',14.35,11.20,math.pi)
furniture('main','Family room coffee table','table','oak-rounded-coffee-table',14.35,9.7)
furniture('basement','Walkout sitting sofa','sofa','linen-three-seat-sofa',10.55,12.00,-math.pi/2)
furniture('basement','Walkout sitting coffee table','table','oak-rounded-coffee-table',11.98,12.00,math.pi/2)
furniture('basement','Recreation sofa','sofa','linen-three-seat-sofa',14.3,8.0)
furniture('basement','Recreation coffee table','table','oak-rounded-coffee-table',14.3,9.8)
add(FURNITURE,'basement','Shared eight-foot billiards table','pool','furniture','walnut-eight-foot-pool-table',16.03,14.09,math.pi/2,version='v002')

# Complete kitchen equipment, oriented into the relevant working aisle.
for x in [5.6,6.21,8.32]:fixture('main','Rear kitchen shared drawer cabinet','cabinet','cabinetry','oak-drawer-base-2ft',x,11.56)
for x in [7.06,7.67,8.28]:fixture('main','Island shared drawer cabinet','cabinet','cabinetry','oak-drawer-base-2ft',x,9.45)
fixture('main','Main oven in dedicated cavity','oven','appliances','built-in-oven-30in',7.54,11.56,z=.12)
fixture('main','Main induction cooktop','cooktop','appliances','induction-cooktop-36in',7.54,11.56,z=.962)
fixture('main','Main extraction hood','hood','appliances','wall-hood-36in',7.54,11.56,z=1.75)
fixture('main','Main panel-ready wide refrigerator','fridge','appliances','panel-ready-fridge-48in',10.08,11.48)
wardrobe('main','Main food pantry',8.96,11.56)
fixture('main','Main integrated dishwasher','dishwasher','appliances','dishwasher-24in',4.80,9.74,math.pi/2)
fixture('main','Main powder cabinet','vanity','cabinetry','oak-drawer-base-2ft',11.72,7.18)
fixture('main','Main powder toilet','toilet','fixtures','toilet-elongated',12.49,7.03)
fixture('main','Family living closed glass fireplace','fireplace','fixtures','closed-glass-fireplace-48in',18.80,8.90,-math.pi/2,z=.50)
for y in [8.18,10.95]:fixture('basement','Second kitchen west drawers','cabinet','cabinetry','oak-drawer-base-2ft',4.80,y,math.pi/2)
for x in [6.15,8.53]:fixture('basement','Second kitchen north drawers','cabinet','cabinetry','oak-drawer-base-2ft',x,11.55)
fixture('basement','Second kitchen oven','oven','appliances','built-in-oven-30in',4.8,9.61,math.pi/2,z=-3.03)
fixture('basement','Second kitchen induction','cooktop','appliances','induction-cooktop-36in',4.8,9.61,math.pi/2,z=-2.188)
fixture('basement','Second kitchen extraction hood','hood','appliances','wall-hood-36in',4.8,9.61,math.pi/2,z=-1.40)
fixture('basement','Second kitchen dishwasher','dishwasher','appliances','dishwasher-24in',7.91,11.55)
fixture('basement','Second kitchen wide refrigeration','fridge','appliances','panel-ready-fridge-48in',8.29,8.10,-math.pi/2)
for y in [13.13,11.38]:fixture('upper','Primary shared vanity','vanity','cabinetry','oak-drawer-base-2ft',9.37,y,math.pi/2)
fixture('upper','Primary tub','tub','fixtures','freestanding-tub-72in',10.32,14.75)
fixture('upper','Primary enclosed toilet','toilet','fixtures','toilet-elongated',12.57,13.10)
fixture('upper','Shared upper bathroom vanity','vanity','cabinetry','oak-drawer-base-2ft',7.39,7.40,math.pi)
fixture('upper','Shared upper bathroom WC','toilet','fixtures','toilet-elongated',6.78,7.43,math.pi)
fixture('upper','Shared upper bathroom tub','tub','fixtures','freestanding-tub-72in',5.43,7.76,0)
fixture('upper','Wing bathroom vanity','vanity','cabinetry','oak-drawer-base-2ft',18.35,5.01,math.pi/4)
fixture('upper','Wing bathroom WC','toilet','fixtures','toilet-elongated',19.17,5.82,math.pi/4)
fixture('basement','Basement shared vanity','vanity','cabinetry','oak-drawer-base-2ft',9.78,6.98)
fixture('basement','Basement bathroom WC','toilet','fixtures','toilet-elongated',10.53,5.10)

furniture('main','Office writing desk','desk','oak-writing-desk',2.1,7.75)
furniture('main','Office chair','chair','oak-upholstered-dining-chair',2.1,6.98,math.pi)
fixture('main','Main undermount sink and mixer','sink','fixtures','kitchen-sink-mixer-650',4.80,10.70,math.pi/2,z=.956)
fixture('basement','Second kitchen sink and mixer','sink','fixtures','kitchen-sink-mixer-650',7.16,11.55,z=-2.194)
for level,x,y,angle in [('main',11.72,7.18,0),('upper',9.37,13.13,math.pi/2),('upper',9.37,11.38,math.pi/2),('upper',7.39,7.40,math.pi),('upper',18.35,5.01,math.pi/4),('basement',9.78,6.98,0)]:
    fixture(level,'Shared basin faucet and mirror','basin','fixtures','vanity-basin-mixer-mirror',x,y,angle,z=LEVELS[level]['z']+.94)
for level,x,y,angle in [('upper',12.53,14.78,0),('upper',20.45,6.10,math.pi/4),('basement',8.07,5.02,0)]:
    fixture(level,'Shared shower tray and screen','shower','fixtures','shower-tray-screen-900',x,y,angle)
for level,x,y,angle in [('upper',12.10,2.90,math.pi/2),('upper',12.10,2.20,math.pi/2),('basement',4.60,7.60,math.pi/2),('basement',4.60,6.90,math.pi/2)]:
    fixture(level,'Shared front-loading laundry','laundry','appliances','front-loading-laundry-600',x,y,angle)

FITTED_GEOMETRY=[]
def fitted(level,name,loc,size,material,kind='counter',rotation=0,bevel=.012):
    FITTED_GEOMETRY.append({'level':level,'name':name,'kind':kind,'location':list(loc),'dimensions':list(size),'rotation':rotation,'material':material,'bevel':bevel})
fitted('main','Main kitchen island quartzite',(7.67,9.56,.934),(2.06,1.14,.045),'counter',bevel=.018)
fitted('main','Main rear worktop',(6.8,11.55,.934),(3.66,.72,.045),'counter')
fitted('main','Main sink worktop',(4.80,10.70,.934),(.72,1.25,.045),'counter')
fitted('basement','Second kitchen west top',(4.80,9.58,-2.216),(.72,3.50,.045),'counter')
fitted('basement','Second kitchen north top',(7.20,11.55,-2.216),(3.55,.72,.045),'counter')
fitted('main','Family room noncombustible chase',(19.06,8.90,1.50),(.50,2.15,3.0),'stone','chase')
fitted('main','Family room stone hearth',(18.71,8.90,.07),(1.05,2.55,.14),'stone','hearth',bevel=.022)
fitted('main','Main hood duct enclosure',(7.54,11.70,2.74),(.34,.30,.48),'dark','hood')
fitted('basement','Second kitchen hood duct enclosure',(4.66,9.61,-.425),(.30,.34,.37),'dark','hood')
for level,x,y,angle in [('main',11.72,7.18,0),('upper',9.37,13.13,math.pi/2),('upper',9.37,11.38,math.pi/2),('upper',7.39,7.40,math.pi),('upper',18.35,5.01,math.pi/4),('basement',9.78,6.98,0)]:
    fitted(level,'Vanity stone top',(x,y,LEVELS[level]['z']+.923),(.66,.65,.034),'counter',rotation=angle)
RECESSED_LIGHTS=[(x,y,2.98) for x in [6.1,8.65,13.5,16.7] for y in [8.0,10.3]]
RECESSED_LIGHTS += [(x,y,6.23) for x in [15.0,17.5] for y in [8.1,10.8]]
RECESSED_LIGHTS += [(x,y,-.24) for x in [14.6,17.6] for y in [8.0,10.6]]
INTERIOR_CAMERAS={
 '05-kitchen':((10.30,7.40,1.65),(6.7,10.7,1.20),25),
 '06-family-room':((11.35,11.40,1.65),(17.35,8.70,1.30),25),
}

def build_interiors(root,M):
    import bpy
    from common import geometry as g
    from common.library import linked_collection
    from utils import instance,box,camera,area,rod
    g.collection('04 Interiors | linked furniture and household fixtures')
    cache={};adopted=[]
    for row in FURNITURE+FIXTURES:
        category,slug=row['asset'].split('/');key=(category,slug,row['version'])
        if key not in cache:
            cache[key]=linked_collection(root,category,slug,row['version'])
            adopted.append({'id':row['asset'],'version':row['version'],'path':f'../../library/{row["asset"]}/{row["version"]}/'})
        obj=instance(row['name'],cache[key],row['location'],row['rotation']);obj['level']=row['level'];obj['ifc_storey']=LEVELS[row['level']]['name'];obj['program_kind']=row['kind']
        if row['kind']=='bed':obj['bed_count']=1
    # These exact-fit worktops and chase are intentionally house-specific.
    g.collection('04 Interiors | bespoke fitted worktops and fireplace chase')
    fitted_objects={}
    for row in FITTED_GEOMETRY:
        obj=box(row['name'],row['location'],row['dimensions'],M[row['material']],row['bevel']);obj.rotation_euler.z=row['rotation'];obj['ifc_storey']=LEVELS[row['level']]['name'];fitted_objects[row['name']]=obj
    # Real host apertures keep basins and cooktop casings below the worktop,
    # with the cooktop glass 5.5 mm proud of the finished stone.
    for name,loc,size in [('Main sink worktop',(4.8,10.7,.93),(.455,.655,.35)),('Second kitchen north top',(7.16,11.55,-2.21),(.655,.455,.35)),('Main rear worktop',(7.54,11.56,.934),(.885,.504,.35)),('Second kitchen west top',(4.8,9.61,-2.216),(.504,.885,.35))]:
        top=fitted_objects[name];cut=box('Temporary equipment aperture',loc,size)
        bpy.context.view_layer.objects.active=top;mod=top.modifiers.new('Equipment opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    # Dedicated cavity surrounding oven; support excludes the oven volume.
    for level,x,y,ang in [('main',7.54,11.56,0),('basement',4.80,9.61,math.pi/2)]:
        for dx in [-.412,.412]:
            px=x+dx*math.cos(ang);py=y+dx*math.sin(ang)
            obj=box('Oven carcass side',(px,py,LEVELS[level]['z']+.44),(.035,.62,.87),M['oak'],.004);obj.rotation_euler.z=ang
    # Sink supports and removable front are fitted to actual linked basin dimensions.
    for level,x,y,ang in [('main',4.80,10.7,math.pi/2),('basement',7.16,11.55,0)]:
        for dx in [-.44,.44]:
            obj=box('Sink carcass side',(x+dx*math.cos(ang),y+dx*math.sin(ang),LEVELS[level]['z']+.44),(.03,.62,.87),M['oak'],.004);obj.rotation_euler.z=ang
        obj=box('Sink removable access front',(x+.31*math.sin(ang),y-.31*math.cos(ang),LEVELS[level]['z']+.44),(.88,.025,.85),M['oak'],.007);obj.rotation_euler.z=ang
        handle_key=('hardware','bar-pull-brushed-steel','v001')
        if handle_key not in cache:
            cache[handle_key]=linked_collection(root,*handle_key)
            adopted.append({'id':'hardware/bar-pull-brushed-steel','version':'v001','path':'../../library/hardware/bar-pull-brushed-steel/v001/'})
        instance('Shared sink access pull',cache[handle_key],(x+.328*math.sin(ang),y-.328*math.cos(ang),LEVELS[level]['z']+.70),ang)
    # A restrained material field under seating; no circulation barriers.
    for level,x,y,w,d in [('main',14.35,9.7,4.4,4.4),('main',2.18,2.7,3.6,3.7),('basement',16.05,8.7,5.2,3.8)]:
        box('Wool seating rug',(x,y,LEVELS[level]['z']+.012),(w,d,.018),M['linen'],.015)
    g.collection('10 Interior lighting and cameras')
    from common.lighting_assets import load as load_lighting,place as place_light,CATALOG
    lights=load_lighting(root,['downlight','linear'])
    for i,loc in enumerate(RECESSED_LIGHTS):place_light('Shared recessed interior light '+str(i),lights['downlight'],'downlight',[v/.3048 for v in loc],power=7,color=(1,.92,.82))
    for name,loc,ang in [('Breakfast focal light',(14.2,14.05,2.98),0),('Formal dining focal light',(9.47,2.22,2.98),math.pi/2)]:
        place_light(name,lights['linear'],'linear',[v/.3048 for v in loc],rotation=ang,power=20,color=(1,.92,.82))
    for key in ['downlight','linear']:
        slug=CATALOG[key][0];adopted.append({'id':'fixtures/'+slug,'version':'v001','path':'../../library/fixtures/'+slug+'/v001/'})
    for name,args in INTERIOR_CAMERAS.items():camera(name,*args)
    area('Kitchen soft daylight bounce',(7.7,10.3,2.70),(7.7,9.2,.6),160,3.0,(1,.94,.86))
    area('Family room soft daylight bounce',(15.8,9.7,2.7),(15.5,8.0,.7),180,3.3,(1,.94,.87))
    return adopted
