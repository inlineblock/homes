"""Shared detailed hardware and a restrained, layered household lighting layout."""
import bpy,math
from common.geometry import collection,cyl,F
from common.lighting_assets import load as load_lights,place as place_light
from common.hardware_assets import place as hardware,dependencies as hardware_dependencies
LIGHT_KEYS=['downlight','taskbar']
HARDWARE=[('bar-pull','satin-bronze'),('door-lever','satin-bronze')]

def details(ROOT):
    collection('11 Details | shared hardware and lighting')
    for o in list(bpy.context.scene.objects):
        if o.type!='MESH':continue
        x,y,z=[v/F for v in o.location];dx,dy,dz=[v/F for v in o.dimensions]
        if 'drawer front' in o.name and not o.library:
            if dx<.3:loc=(x-dx/2-.003,y,z);rot=-math.pi/2
            else:
                sign=-1 if o.name.startswith('Interior serving') else 1
                loc=(x,y+sign*(dy/2+.003),z);rot=0 if sign<0 else math.pi
            hardware(ROOT,'bar-pull','satin-bronze',o.name+' shared pull',loc,rotation_z=rot)
        if 'open oak door leaf' in o.name:
            if dx<.3:
                yy=y+dy/2-.35 if o.name.startswith('Primary WC west') else y-dy/2+.35
                for side in [-1,1]:hardware(ROOT,'door-lever','satin-bronze',o.name+' lever',(x+side*(dx/2+.005),yy,3.1),rotation_z=-math.pi/2 if side<0 else math.pi/2)
            else:
                sign=-1 if o.name.startswith(('Primary east','Bath closet partition','Primary bath front')) else 1
                xx=x+sign*(dx/2-.35)
                for side in [-1,1]:hardware(ROOT,'door-lever','satin-bronze',o.name+' lever',(xx,y+side*(dy/2+.005),3.1),rotation_z=0 if side<0 else math.pi)
    lights=load_lights(ROOT,keys=LIGHT_KEYS)
    positions=[(6,28),(20,28),(6,35),(20,35),(29,24),(40,24),(29,35),(40,35),(47,34),(61,34),(62,26),(22,8),(22,16),(9,16),(13.5,19),(9,22),(3,21),(5,5),(33,7),(48,8),(64,4),(63,11),(16,15),(3.5,14),(65,18)]
    ceiling=bpy.data.objects['Continuous warm white ceiling']
    cutters=[]
    mat=next(m for m in bpy.data.materials if m.name.startswith('Graphite hardware'))
    for x,y in positions:
        cutters.append(cyl('Temporary downlight ceiling cut',(x,y,10.59),1.7/12,.52,mat,24))
        place_light('Shared recessed downlight',lights['downlight'],'downlight',(x,y,10.45),power=5)
    bpy.ops.object.select_all(action='DESELECT')
    for o in cutters:o.select_set(True)
    bpy.context.view_layer.objects.active=cutters[0];bpy.ops.object.join();cut=cutters[0]
    mod=ceiling.modifiers.new('Real downlight service openings','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=ceiling;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    # Concealed task lighting beneath the east floating shelf, directed at preparation surface.
    place_light('Shared preparation task strip',lights['taskbar'],'taskbar',(66.5,36.8,5.31),rotation=math.pi/2,power=7)

def dependencies():
    return hardware_dependencies(HARDWARE)+[{'id':'fixtures/'+slug,'version':'v001','path':'../../library/fixtures/'+slug+'/v001/'} for slug in ['lighting-recessed-downlight-3in','lighting-undercabinet-bar-4ft']]
