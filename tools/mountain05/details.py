"""Shared hardware, real recessed light apertures and lighting schedule."""
import math,bpy
from common import geometry as g
from common.geometry import F,box
from common.architecture import mesh
from common.lighting_assets import load,place
from common.hardware_assets import place as hardware

def install(ROOT,M):
    C=load(ROOT,keys=['downlight','taskbar','linear'])
    g.collection('12 Lighting fixtures | recessed task and focal')
    # One coherent main ceiling; the cavity above is reserved for lighting/services.
    ceiling=bpy.data.objects['Main continuous ceiling']
    positions=[(6,6),(18,6),(6,18),(18,18),(28,3),(28,9),(37,4),(37,12),(37,20),(44,16),(44,20),(43,9),(48,8),(54,7),(58,7),(51,16),(57,16),(51,23),(57,23),(5,34),(12,34),(19,34),(26,30),(39,30),(44,36),(53,36)]
    # Multiple disjoint cylindrical cutters, one Boolean operation on the ceiling.
    verts=[];faces=[];radius=1.70/12;N=32
    for x,y in positions:
        base=len(verts)
        for z in [9.98,10.55]:
            verts.extend((x+radius*math.cos(i*math.tau/N),y+radius*math.sin(i*math.tau/N),z) for i in range(N))
        for i in range(N):faces.append((base+i,base+(i+1)%N,base+N+(i+1)%N,base+N+i))
        faces.append(tuple(base+i for i in reversed(range(N))));faces.append(tuple(base+N+i for i in range(N)))
    cutter=mesh('Temporary coordinated light cutouts',verts,faces,M['dark']);bpy.context.view_layer.objects.active=ceiling
    mod=ceiling.modifiers.new('Actual recessed fixture cutouts','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    for x,y in positions:place('Shared recessed main downlight',C['downlight'],'downlight',(x,y,10.10),power=4)
    # A single focal fixture over dining; no decorative pendants scattered over every room.
    place('Shared dining linear focal light',C['linear'],'linear',(33,32.3,10.10),power=14)
    # Task bar under a real shallow counter shelf, separate from the daylight window.
    box('Kitchen side task shelf',(59.0,31.5,5.5),(1.0,4.3,.12),M['oak'],.015)
    place('Shared kitchen task bar',C['taskbar'],'taskbar',(58.8,31.5,5.44),rotation=math.pi/2,power=6)
    g.collection('11 Details | shared hardware and joinery')
    # Host supplies both sides of every door lever and an actual latch body.
    for o in list(bpy.context.scene.objects):
        if o.type!='MESH' or 'open door' not in o.name:continue
        x,y,z=[v/F for v in o.location];w=o.dimensions.x/F;d=o.dimensions.y/F
        if w>d:
            px=x+w/2-.28;py=y
            hardware(ROOT,'door-lever','matte-black',o.name+' inside lever',(px,py-d/2,z-.75),0)
            hardware(ROOT,'door-lever','matte-black',o.name+' outside lever',(px,py+d/2,z-.75),math.pi)
            box(o.name+' latch body',(px,py,z-.75),(.18,d,.10),M['steel'],.01)
        else:
            px=x;py=y+d/2-.28
            hardware(ROOT,'door-lever','matte-black',o.name+' inside lever',(px+w/2,py,z-.75),math.pi/2)
            hardware(ROOT,'door-lever','matte-black',o.name+' outside lever',(px-w/2,py,z-.75),-math.pi/2)
            box(o.name+' latch body',(px,py,z-.75),(w,.18,.10),M['steel'],.01)
    for x in [51,53]:hardware(ROOT,'bar-pull','matte-black','Shared sink cabinet pull',(x,37.35,2.45))
    hardware(ROOT,'bar-pull','matte-black','Shared waste pullout pull',(51,32.91,2.5),math.pi)
    for x in [45,53]:
        for z in [.98,1.88,2.72]:hardware(ROOT,'bar-pull','matte-black','Shared island drawer pull',(x,32.9,z),math.pi)
