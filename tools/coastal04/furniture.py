"""Detailed original joinery and soft furnishings; geometry in feet."""
import bpy,math,random
from common.furnishings import soft,bowl,chair,sofa,bed
from common import geometry as g
from common.geometry import box,cyl,sphere,rod,curve,F



def cabinet_run(name,x1,x2,y,front,M):
    width=x2-x1;count=round(width/2.4);unit=width/count
    box(name+' recessed plinth',((x1+x2)/2,y,.22),(width-.14,2.20,.42),M['dark'],.012)
    box(name+' cabinet carcass',((x1+x2)/2,y,1.6),(width,2.45,2.62),M['oak'],.02)
    for i in range(count):
        x=x1+(i+.5)*unit
        for z,h in [(2.58,.52),(1.91,.75),(.98,1.06)]:
            box(name+' drawer front',(x,y+front*1.255,z),(unit-.035,.09,h),M['oak'],.015)
            box(name+' finger recess',(x,y+front*1.31,z+h/2-.035),(unit-.20,.025,.035),M['dark'],.006)
    box(name+' stone counter',((x1+x2)/2,y,3.025),(width+.16,2.75,.15),M['counter'],.025)




def kitchen(M):
    g.collection('03 Kitchen | interior exterior joinery')
    cabinet_run('Interior serving',47.8,63.3,38.43,-1,M)
    cabinet_run('Exterior serving',47.8,63.3,41.61,1,M)
    counter=bpy.data.objects['Exterior serving stone counter'];counter.location.y=42.20*F;counter.dimensions.y=3.93*F
    # Stone bridge underneath the sliding sill, joining the two distinct cabinet runs.
    box('Continuous stone sill serving bridge',(55.55,40.02,3.025),(15.65,.61,.15),M['counter'],.012)
    # Island with true undermount sink opening.
    cabinet_run('Island',49.5,59.5,29.5,1,M)
    box('Island stool-side cabinet',(54.5,28.28,1.54),(10,.10,2.74),M['oak'],.018)
    # Replace run worktop with a deeper slab and sink cutout.
    bpy.data.objects.remove(bpy.data.objects['Island stone counter'],do_unlink=True)
    top=box('Island quartzite slab',(54.5,29.2,3.025),(10.25,4.4,.15),M['counter'],.025)
    cut=box('Temporary sink cutter',(56.5,29.6,3.02),(2.25,1.6,.8),M['steel'],.1)
    bpy.context.view_layer.objects.active=top;mod=top.modifiers.new('Real sink opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    box('Sink basin bottom',(56.5,29.6,2.4),(2.24,1.59,.06),M['steel'],.10)
    for dx in [-1.12,1.12]:box('Sink basin end',(56.5+dx,29.6,2.71),(.045,1.6,.60),M['steel'],.018)
    for dy in [-.80,.80]:box('Sink basin side',(56.5,29.6+dy,2.71),(2.24,.045,.60),M['steel'],.018)
    cyl('Sink drain',(56.5,29.6,2.44),.10,.015,M['dark'])
    curve('Swan-neck kitchen faucet',[(56.5,30.65,3.10),(56.5,30.65,4.2),(56.5,30.1,4.55),(56.5,29.6,4.13)],.045,M['steel'])
    rod('Mixer handle',(56.9,30.65,3.08),(56.9,30.65,3.47),.03,M['steel'])
    # East wall appliances leave a broad aisle to the island.
    for y in [23,25.6,28.2,30.8,33.4,36]:
        box('East oak cabinetry',(66.5,y,1.6),(2.5,2.55,2.7),M['oak'],.025)
        for z in [.85,1.8,2.6]:box('East drawer face',(65.20,y,z),(.10,2.48,.68),M['oak'],.013)
    box('East countertop',(66.45,30.1,3.02),(2.85,15.8,.16),M['counter'],.02)
    box('Induction glass',(66.3,32.5,3.12),(1.85,2.5,.04),M['dark'],.03)
    for y in [31.9,33.1]:
        for x in [65.9,66.7]:cyl('Induction zone',(x,y,3.146),.27,.004,M['steel'],64)
    box('Concealed extraction plaster hood',(66.85,32.5,7.05),(2.05,3.8,2.3),M['plaster'],.02)
    for y in [22.6,24.1]:
        box('Integrated fridge tall door',(65.06,y,4.3),(.15,1.44,8.55),M['oak'],.02)
        rod('Fridge pull',(64.94,y-.5,3.7),(64.94,y-.5,5),.023,M['bronze'])
    box('Fridge housing',(66.4,23.35,4.3),(2.7,3.05,8.6),M['oak'],.025)
    # Shelf and carefully sparse styling.
    box('East floating oak shelf',(66.6,36.8,5.4),(2,4.2,.14),M['oak'],.016)
    bowl('Serving fruit bowl',50,38.1,3.12,.65,M['porcelain'])
    for i in range(5):sphere('Fresh green pear',(49.7+(i%3)*.25,38+(i//3)*.22,3.31),(.16,.16,.22),M['leaf'])
    box('Oak cutting board',(51.2,29.4,3.13),(1.45,1.05,.08),M['oak'],.1)
    bowl('Breakfast ceramic',52.3,29.2,3.12,.35,M['porcelain'])
    for x in [50.4,53.9,57.4]:
        cyl('Island pendant canopy',(x,29.2,10.33),.18,.12,M['bronze'])
        rod('Island pendant cord',(x,29.2,10.27),(x,29.2,6.3),.009,M['dark'])
        sphere('Pendant opal globe',(x,29.2,6.23),(.31,.31,.31),M['porcelain'])
        # shallow disc shade
        cyl('Wide champagne pendant shade',(x,29.2,6.40),.62,.055,M['bronze'],64)


def rooms(M):
    g.collection('04 Furnishings | living dining bedrooms')
    # Library-owned living/dining geometry; local room dimensions remain here.
    from pathlib import Path
    from comfort import living_dining
    living_dining(Path(__file__).resolve().parents[2],M)
    from design import BEDS
    for name,x,y,w in BEDS:bed(name,x,y,w,M)
    # Bath fixtures, clear door zones, and wardrobe/Laundry.
    for prefix,x,y in [('Primary',0,16),('Guest',60,0)]:
        box(prefix+' shower tray',(x+2.6,y+6.3,.07),(4.3,3.0,.12),M['stone'],.02)
        from common.architecture import glass_wall
        glass_wall(prefix+' shower screen',(x+.5,y+4.75),(x+2.2,y+4.75),7.5,M['glass'],M['bronze'])
        rod(prefix+' shower riser',(x+.7,y+7.6,3),(x+.7,y+7.6,7.0),.035,M['steel'])
        cyl(prefix+' shower head',(x+1.0,y+7.5,7.0),.3,.05,M['steel'])
        box(prefix+' vanity',(x+6.5,y+6.65,1.45),(2.2,2.2,2.7),M['oak'],.03)
        bowl(prefix+' basin',x+6.5,y+6.65,2.86,.73,M['porcelain'])
        sphere(prefix+' WC bowl',(x+(8.2 if prefix=='Primary' else 6.5),y+(2.0 if prefix=='Primary' else 2.6),1.1),(.60,.92,.50),M['porcelain'])
        box(prefix+' WC cistern',(x+(8.2 if prefix=='Primary' else 6.5),y+(1.35 if prefix=='Primary' else 1.95),1.7),(1.15,.55,1.7),M['porcelain'],.12)
    box('Dressing wardrobe',(16.7,20.3,4.4),(2.2,6.6,8.8),M['oak'],.03)
    box('Dressing rear wardrobe',(12.65,22.75,4.4),(4.9,2.2,8.8),M['oak'],.03)
    for x in [63,66]:
        box('Laundry appliance',(x,14.3,1.55),(2.65,2.5,3.1),M['porcelain'],.06)
        o=cyl('Laundry round door',(x,13.02,1.7),.8,.08,M['dark'],64);o.rotation_euler.x=math.pi/2
    box('Laundry oak worktop',(64.5,14.3,3.17),(5.85,2.7,.16),M['oak'],.02)
