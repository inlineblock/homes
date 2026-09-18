"""Generous primary suite: independent bathing, dressing, WC and sleeping zones."""
import bpy,math
from mathutils import Matrix,Vector
from common import geometry as g
from common.geometry import box,cyl,rod,curve,sphere,collection,F
from common.architecture import glass_wall,mesh
from common.furnishings import bed,bowl
from common.shared_assets import place

BED_TERMS=['bed frame','mattress','upholstered headboard','duvet','pillow','blue folded throw','bedside']

def premium_suite(M,shared):
    for o in list(bpy.context.scene.objects):
        if (o.name.startswith('Primary ') and any(t in o.name for t in BED_TERMS+['shower','vanity','basin','WC bowl','WC cistern'])) or o.name.startswith(('Dressing wardrobe','Dressing rear wardrobe')):
            bpy.data.objects.remove(o,do_unlink=True)
    collection('04 Furnishings | premium primary suite')
    before=set(bpy.context.scene.objects);bed('Primary',6,5.5,6.5,M)
    center=Vector((6*F,5.5*F,0));rot=Matrix.Rotation(-math.pi/2,4,'Z')
    for o in set(bpy.context.scene.objects)-before:o.matrix_world=Matrix.Translation(center)@rot@Matrix.Translation(-center)@o.matrix_world
    for y in [13.2,15.2]:place('Primary dressing wardrobe',shared['wardrobe'],(1.15,y,0),rotation=math.pi/2)
    place('Primary dressing wardrobe',shared['wardrobe'],(4.8,16.8,0))
    # Five-foot shower with an open three-foot side entry, rain fitting and hand shower.
    box('Primary shower recessed tray',(3.05,21.95,.06),(5.2,7.4,.10),M['stone'],.04)
    glass_wall('Primary shower fixed return',(5.65,23.5),(5.65,25.65),8,M['glass'],M['bronze'],.10,1)
    rod('Primary shower riser',(.70,23,3),(.70,23,7.6),.035,M['steel'])
    rod('Primary overhead shower arm',(.70,23,7.6),(2.0,23,7.6),.035,M['steel'])
    cyl('Primary rain shower head',(2,23,7.55),.5,.05,M['steel'],64)
    place('Primary separate soaking tub',shared['bathtub'],(9,24.2,0))
    curve('Primary floor tub filler',[(9,25.65,.0),(9,25.65,2.7),(9,25.35,2.9),(9,24.95,2.7)],.055,M['steel'])
    # A 5 ft 7 in dual vanity faces a generous central bathing area.
    box('Primary dual vanity cabinet',(16.55,23,1.40),(2.2,5.6,2.75),M['oak'],.03)
    box('Primary dual vanity stone top',(16.50,23,2.86),(2.4,5.75,.15),M['counter'],.025)
    for y in [21.5,24.5]:
        bowl('Primary vanity basin',16.4,y,2.94,.70,M['porcelain'])
        curve('Primary vanity faucet',[(17.35,y,2.98),(17.35,y,3.55),(16.95,y,3.60),(16.80,y,3.4)],.03,M['steel'])
        for z in [.65,1.55,2.4]:box('Primary vanity drawer front',(15.405,y,z),(.08,2.7,.65),M['oak'],.014)
        box('Primary framed vanity mirror',(17.75,y,5.6),(.06,2.35,3.3),M['bronze'],.05)
        box('Primary vanity mirror',(17.70,y,5.6),(.02,2.23,3.18),M['glass'],.035)
    place('Primary enclosed shared toilet',shared['toilet'],(16,16.5,0))
    for o in list(bpy.context.scene.objects):
        if o.name.startswith(('Guest WC bowl','Guest WC cistern')):bpy.data.objects.remove(o,do_unlink=True)
    place('Guest shared toilet',shared['toilet'],(66.15,3.3,0),rotation=-math.pi/2)
    box('Guest vanity stone top',(66.5,6.65,2.86),(2.25,2.25,.15),M['counter'],.02)
    curve('Guest basin faucet',[(67.3,6.65,2.96),(67.3,6.65,3.55),(66.95,6.65,3.62),(66.80,6.65,3.42)],.03,M['steel'])
    # Bath towels have a dedicated shallow linen niche near the dressing room.
    box('Primary towel niche backing',(6.18,17,5.1),(.12,1.2,3.0),M['oak'],.018)
    for z in [4.0,5.2,6.4]:box('Primary towel niche shelf',(6.4,17,z),(.5,1.2,.07),M['oak'],.012)
