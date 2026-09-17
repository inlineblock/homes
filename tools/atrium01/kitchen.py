"""Kitchen-focused joinery, appliances, and the reusable original ceramic tile."""
import bpy, math, json
from common.geometry import box,cyl,sphere,rod,curve,area,collection,F

def tile_library(root,M):
    folder=root/'library/materials/sage-fluted-tile/v001';folder.mkdir(parents=True,exist_ok=True)
    path=folder/'sage-fluted-tile.blend'
    if path.exists():
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[src.collections[0]]
        return dst.collections[0]
    c=collection('Sage fluted tile | 3 x 12 in | v001')
    box('Ceramic tile body',(0,0,0),(.24,.045,.99),M['sage'],.008)
    for i in range(6):cyl('Glazed vertical flute',(-.1+i*.04,.019,0),.018,.976,M['sage'],12)
    bpy.data.libraries.write(str(path),{c},fake_user=True)
    for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.collections.remove(c)
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[src.collections[0]]
    # Library links are made repository-relative when the house is saved.
    data={'schema_version':1,'id':'materials/sage-fluted-tile','version':'v001','name':'Sage fluted ceramic','units':'meters','dimensions_m':[.073152,.0181356,.301752],'nominal_module_inches':[3,12],'grout_inches':.12,'source':{'kind':'original','author':'Homes project','generator':'tools/atrium01/kitchen.py:tile_library'},'license':'CC-BY-4.0','rights':'Original project asset; CC BY 4.0; attribution: Homes project contributors','files':{'blender':'sage-fluted-tile.blend'},'dependencies':[]}
    (folder/'asset.json').write_text(json.dumps(data,indent=2)+'\n')
    return dst.collections[0]

def cabinet(name,x,y,w,d,h,M,front='north'):
    box(name+' carcass',(x,y,h/2+.35),(w,d,h),M['walnut'],.025)
    # A thin recessed toe kick grounds the joinery.
    box(name+' plinth',(x,y,.2),(w-.12,d-.18,.4),M['black'],.01)
    if front=='north':
        for dz,hz in [(2.48,.72),(1.62,.88),(.7,.85)]:
            box(name+' drawer',(x,y+d/2+.025,dz),(w-.045,.075,hz),M['walnut'],.018)
            box(name+' pull',(x,y+d/2+.09,dz+hz/2-.09),(w*.44,.05,.045),M['black'],.01)
    else:
        for dz,hz in [(2.48,.72),(1.62,.88),(.7,.85)]:
            box(name+' drawer',(x-d/2-.025,y,dz),(.075,w-.045,hz),M['walnut'],.018)
            box(name+' pull',(x-d/2-.09,y,dz+hz/2-.09),(.05,w*.44,.045),M['black'],.01)

def build(root,M):
    tiles=tile_library(root,M);collection('03 Kitchen | detailed joinery')
    # South cooking wall; modules are 30 inches wide.
    for i in range(5):cabinet('South cabinet %02d'%i,45.4+i*2.5,1.4,2.5,2.3,2.45,M)
    box('South limestone worktop',(51.3,1.45,3.01),(13.6,2.6,.16),M['stone'],.035)
    for row in range(3):
        for col in range(53):
            o=bpy.data.objects.new('Sage tile %02d-%02d'%(row,col),None);o.instance_type='COLLECTION';o.instance_collection=tiles
            bpy.data.collections['03 Kitchen | detailed joinery'].objects.link(o);o.location=( (44.7+col*.25)*F, .55*F, (3.64+row)*F)
    box('Walnut floating display shelf',(51.25,.78,6.6),(13.5,1.15,.15),M['walnut'],.03)
    # Thin concealed range extraction rather than a bulky dropped hood.
    box('Slim integrated range canopy',(51.1,1.05,6.47),(3.4,1.6,.17),M['black'],.04)
    box('Induction glass cooktop',(51.1,1.48,3.115),(2.8,1.78,.035),M['black'],.035)
    for x in [50.42,51.8]:
        for y in [1.05,1.91]:
            bpy.ops.mesh.primitive_torus_add(major_radius=.25*F,minor_radius=.008*F,location=(x*F,y*F,3.14*F));o=bpy.context.object;o.name='Induction ring';o.data.materials.append(M['steel'])
    # East wall: appliance bank, prep drawers and an undermount sink.
    for y,label in [(2.4,'Integrated refrigerator'),(5.6,'Oven tower')]:
        box(label,(58.7,y,4.2),(2.3,3,8),M['walnut'],.035)
        for z,h in [(2.45,3.8),(6.45,3.8)]:box(label+' front',(57.49,y,z),(.10,2.94,h),M['walnut'],.018)
        rod(label+' handle',(57.35,y-1.12,3.5),(57.35,y-1.12,5),.025,M['black'])
    for z in [3.4,5.1]:
        box('Wall oven glass',(57.40,5.6,z),(.08,2.62,1.35),M['black'],.04)
        rod('Oven handle',(57.27,4.48,z+.44),(57.27,6.72,z+.44),.045,M['steel'])
    for y in [8.45,11.05,13.65,16.25,18.85]:cabinet('East drawer module',58.7,y,2.6,2.3,2.45,M,'west')
    # Separate stone pieces leave a real sink opening.
    for ya,yb in [(7.1,11.8),(14.3,20.2)]:box('East worktop',(58.7,(ya+yb)/2,3.01),(2.65,yb-ya,.16),M['stone'],.025)
    for x in [57.52,59.87]:box('Sink surround',(x,13.05,3.01),(.30,2.5,.16),M['stone'],.02)
    box('Sink basin bottom',(58.68,13.05,2.52),(1.94,2.45,.07),M['steel'],.13)
    for x in [57.73,59.64]:box('Sink side',(x,13.05,2.75),(.07,2.45,.5),M['steel'],.045)
    for y in [11.86,14.25]:box('Sink end',(58.68,y,2.75),(1.96,.07,.5),M['steel'],.045)
    cyl('Drain',(58.68,13.05,2.565),.12,.02,M['black'])
    curve('Gooseneck faucet',[(59.62,13.1,3.1),(59.62,13.1,4.25),(59.4,13.1,4.45),(58.96,13.1,4.4),(58.91,13.1,4.06)],.05,M['steel'])
    rod('Faucet lever',(59.63,13.42,3.2),(59.63,13.42,3.55),.035,M['steel'])
    # 10 x 4 ft island. West overhang and four seats face the courtyard.
    box('Island recessed plinth',(50.35,11,.23),(2.95,9.5,.46),M['black'],.02)
    box('Island walnut core',(50.35,11,1.67),(3.15,9.7,2.58),M['walnut'],.035)
    for y in [7.35,9.79,12.23,14.67]:
        for z in [.92,2.13]:box('Island working drawer',(51.96,y,z),(.08,2.4,1.13),M['walnut'],.014)
    box('Island limestone top',(50,11,3.04),(4.3,10.1,.20),M['stone'],.045)
    for y in [6.02,15.98]:box('Island stone waterfall',(50,y,1.51),(4.3,.18,3.02),M['stone'],.025)
    for y in [7.3,9.75,12.2,14.65]:
        cyl('Walnut stool seat',(46.8,y,2.05),.69,.16,M['walnut'])
        for dx,dy in [(-.42,-.4),(-.42,.4),(.42,-.4),(.42,.4)]:rod('Stool leg',(46.8+dx,y+dy,.08),(46.8+dx*.78,y+dy*.78,2),.045,M['black'])
        rod('Stool footrest',(46.38,y-.4,.72),(47.22,y-.4,.72),.025,M['black'])
        curve('Stool bentwood back',[(46.22,y-.5,2.17),(46.14,y-.48,2.73),(46.14,y,2.91),(46.14,y+.48,2.73),(46.22,y+.5,2.17)],.065,M['walnut'])
    for y in [7.6,11,14.4]:
        rod('Pendant cable',(50,y,8.9),(50,y,6.7),.014,M['black'])
        cyl('Pendant cap',(50,y,6.77),.12,.18,M['black'])
        sphere('Opal globe pendant',(50,y,6.33),(.49,.49,.49),M['glow'])
        area('Pendant pool',(50,y,6),(50,y,2.8),45,1.1)
    area('Under-shelf wash',(51,1.2,6.45),(51,.25,4.1),95,10,shape='RECTANGLE',size_y=.25)
    # Human-scale countertop and shelf objects.
    cyl('Serving bowl foot',(50,12,3.2),.33,.08,M['white'])
    sphere('Low stoneware fruit bowl',(50,12,3.29),(.68,.68,.20),M['terracotta'])
    for x,y,z in [(49.75,11.85,3.5),(50.18,12.15,3.51),(50.08,11.79,3.52)]:sphere('Orange',(x,y,z),(.18,.18,.18),M['orange'])
    box('Linen board',(49.8,8.6,3.18),(1.6,.9,.065),M['walnut'],.13)
    for x in [49.5,50.1]:cyl('Ceramic espresso cup',(x,8.6,3.35),.13,.28,M['white'])
    for x,h in [(46.1,.58),(47,.87),(55.1,.65),(56.3,.47)]:
        cyl('Shelf ceramic vessel',(x,.78,6.72+h/2),.19,h,M['white'])
    for i in range(4):box('Cookbook',(53.7+i*.12,.75,7.11),(.10,.62,.84),M['terracotta'] if i%2 else M['fabric'],.012)
    cyl('Utensil crock',(55.9,1.15,3.5),.27,.70,M['white'])
    for dx in [-.11,0,.12]:rod('Walnut utensil',(55.9+dx,1.15,3.52),(56+dx,1.11,4.13),.032,M['walnut'])
