"""Original reusable proxies; no manufacturer CAD or third-party meshes."""
import bpy,json,math
from pathlib import Path
from common import geometry as g
from common.geometry import box,cyl,sphere,rod,collection,F,material
from common.library import linked_collection
from design import PLATFORM_WIDTH,PLATFORM_LENGTH,PLATFORM_SPACING,POOL_PLAY

def publish(root,category,slug,make,metadata):
    folder=root/'library'/category/slug/'v001';path=folder/f'{slug}.blend'
    if not path.exists():
        folder.mkdir(parents=True,exist_ok=True);c=collection(slug+' | original v001');make()
        bpy.data.libraries.write(str(path),{c},fake_user=True)
        metadata.update({'schema_version':1,'id':category+'/'+slug,'version':'v001','units':'meters','origin':'Floor/driveway level at plan center','license':'CC-BY-4.0','rights':'Original project asset; CC BY 4.0; attribution: Homes project contributors','source':{'kind':'original','generator':'tools/garage03/assets.py'},'files':{'blender':path.name},'dependencies':[]})
        (folder/'asset.json').write_text(json.dumps(metadata,indent=2)+'\n')
        for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c)
    return linked_collection(root,category,slug)

def lift_asset(root,M):
    def make():
        # Movable double-width carriage at upper deck level 0; columns live in the building.
        for level,z in [('upper',0),('lower',-PLATFORM_SPACING)]:
            box('Parking '+level+' full platform',(0,0,z-.1),(PLATFORM_WIDTH,PLATFORM_LENGTH,.2),M['steel'],.025)
            for x in [-PLATFORM_WIDTH/2,PLATFORM_WIDTH/2]:
                box(level+' side beam',(x,0,z-.17),(.22,PLATFORM_LENGTH,.44),M['black'],.015)
                rod(level+' edge rail',(x,-PLATFORM_LENGTH/2,z+.25),(x,PLATFORM_LENGTH/2,z+.25),.035,M['steel'])
            for i in range(55):
                y=-PLATFORM_LENGTH/2+.15+i*(PLATFORM_LENGTH-.3)/54
                box(level+' deck rib',(0,y,z+.012),(PLATFORM_WIDTH-.3,.025,.022),M['steel'])
            for x in [-4.65,4.65]:box(level+' wheel stop',(x,PLATFORM_LENGTH/2-.7,z+.11),(4.5,.16,.22),M['black'],.018)
        for x in [-PLATFORM_WIDTH/2-.15,PLATFORM_WIDTH/2+.15]:
            for y in [-1.5,1.5]:box('Moving carriage upright',(x,y,-PLATFORM_SPACING/2),(.25,.25,PLATFORM_SPACING+.3),M['black'],.01)
    return publish(root,'fixtures','double-pit-parking-carriage',make,{'name':'Double pit parking carriage | schematic','dimensions_m':[PLATFORM_WIDTH*F,PLATFORM_LENGTH*F,(PLATFORM_SPACING+.5)*F],'planning_reference':'KLAUS MultiBase 2072i DP, original simplified proxy; not manufacturer geometry','clear_platform_width_m':5.4,'platform_spacing_m':PLATFORM_SPACING*F,'limitations':'No certified mechanism, anchors, rated loads, or fabricated details. Fixed guide columns are separate building placeholders.'})

def pool_asset(root,M):
    def make():
        felt=material('Deep petrol billiard cloth',(.018,.15,.14),.92)
        for x in [-1.65,1.65]:
            for y in [-3.1,3.1]:box('Billiard tapered leg',(x,y,1.25),(.48,.55,2.5),M['walnut'],.12)
        box('Billiard cabinet',(0,0,2.1),(4.55,8.05,.72),M['walnut'],.13)
        box('Billiard slate trim',(0,0,2.54),(4.7,8.35,.2),M['black'],.05)
        box('Billiard playing field',(0,0,2.68),(POOL_PLAY[0],POOL_PLAY[1],.12),felt,.035)
        for x in [-2.1,2.1]:box('Billiard walnut rail',(x,0,2.7),(.5,8.35,.24),M['walnut'],.075)
        for y in [-3.92,3.92]:box('Billiard walnut rail',(0,y,2.7),(4.7,.5,.24),M['walnut'],.075)
        for x in [-1.81,1.81]:
            for y in [-3.62,0,3.62]:cyl('Billiard pocket',(x,y,2.766),.19,.028,M['black'])
        for x in [-2.1,2.1]:
            for y in [-2.6,-1.3,1.3,2.6]:sphere('Ivory rail sight',(x,y,2.825),(.028,.065,.012),M['white'])
        colors=[(.82,.64,.08),(.02,.13,.5),(.65,.035,.015),(.32,.03,.42),(.86,.23,.02),(.025,.25,.08)]
        for i,(x,y) in enumerate([(.15,-1.3),(.75,1.4),(-.6,2),(.25,1.95),(-.55,-.7),(.1,.7)]):sphere('Pool ball',(x,y,2.845),(.095,)*3,material('Ball pigment '+str(i),colors[i],.19))
        sphere('Cue ball',(-.55,-2.35,2.845),(.095,)*3,M['white'])
    return publish(root,'furniture','walnut-eight-foot-pool-table',make,{'name':'Walnut eight-foot pool table','dimensions_m':[4.7*F,8.35*F,2.94*F],'playing_surface_m':[POOL_PLAY[0]*F,POOL_PLAY[1]*F],'cue_length_m':58*.0254,'dimensions_basis':'Original visualization design; 44 x 88 inch playing surface; not a purchasable product'})

def car(name,x,y,z,paint,M):
    """Original sports coupe, 15.2 x 6.15 x 4.65 feet; wheels rest on z."""
    from common.architecture import mesh
    box(name+' body',(x,y,z+1.38),(5.85,15.2,1.34),paint,.55)
    box(name+' sill',(x,y,z+.68),(5.7,13.9,.42),M['black'],.15)
    # Sloped glazed cabin with a separate painted roof.
    verts=[(x-2.52,y-4.1,z+2),(x+2.52,y-4.1,z+2),(x+2.1,y-2.05,z+4.38),(x-2.1,y-2.05,z+4.38),(x-2.52,y+4.35,z+2),(x+2.52,y+4.35,z+2),(x+2.1,y+2.2,z+4.38),(x-2.1,y+2.2,z+4.38)]
    mesh(name+' tinted cabin',verts,[(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(3,2,6,7)],M['car-glass'])
    box(name+' roof',(x,y+.08,z+4.51),(4.18,4.3,.28),paint,.12)
    for side in [-1,1]:
        for yy in [-4.65,4.65]:
            wheel=cyl(name+' tire',(x+side*2.78,y+yy,z+1.02),1.02,.6,M['rubber'],48);wheel.rotation_euler.y=math.pi/2
            rim=cyl(name+' alloy wheel',(x+side*3.09,y+yy,z+1.02),.69,.035,M['steel'],48);rim.rotation_euler.y=math.pi/2
            hub=cyl(name+' wheel hub',(x+side*3.12,y+yy,z+1.02),.18,.045,M['black']);hub.rotation_euler.y=math.pi/2
        box(name+' headlamp',(x+side*1.96,y-7.56,z+1.55),(1.2,.06,.2),M['glow'],.045)
        box(name+' rear lamp',(x+side*1.95,y+7.56,z+1.55),(1.2,.06,.16),M['red'],.04)
        box(name+' door handle',(x+side*2.94,y+.55,z+2),(.055,.6,.07),M['steel'],.02)
    return [o for o in g.ACTIVE.objects if o.name.startswith(name)]
