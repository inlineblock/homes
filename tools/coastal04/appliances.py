"""Coordinated shared appliance bays, original kitchen cabinetry and pantry."""
import bpy,math
from common.geometry import box,collection,F
from common.shared_assets import place

def complete_kitchen(M,shared):
    for o in list(bpy.context.scene.objects):
        remove=o.name.startswith(('Induction glass','Induction zone','Concealed extraction','Integrated fridge','Fridge pull','Fridge housing','East countertop','Island cabinet carcass'))
        if o.name.startswith(('East oak cabinetry','East drawer face')) and any(abs(o.location.y/F-y)<.1 for y in [23,25.6,33.4]):remove=True
        if o.name.startswith(('Island drawer front','Island finger recess')) and any(abs(o.location.x/F-x)<.1 for x in [50.75,53.25]):remove=True
        if remove:bpy.data.objects.remove(o,do_unlink=True)
    collection('03 Kitchen | coordinated shared appliances')
    box('East continuous stone counter',(66.45,32.15,3.02),(2.85,12.3,.16),M['counter'],.02)
    place('Shared induction cooktop',shared['cooktop'],(66.3,33.4,3.14),rotation=-math.pi/2)
    place('Shared built-in oven',shared['oven'],(66.25,33.4,.5),rotation=-math.pi/2)
    box('Oven base support',(66.25,33.4,.24),(2,2.5,.48),M['oak'],.02)
    place('Shared concealed hood',shared['hood'],(66.8,33.4,5.85),rotation=-math.pi/2)
    # Concept duct rises into the attic; final exterior termination, sizing and setbacks are unresolved.
    box('Hood vertical duct allowance',(67.0,33.4,9.55),(.60,.65,2.4),M['steel'],.02)
    place('Shared wide panel-ready fridge',shared['fridge'],(66.4,24,0),rotation=-math.pi/2)
    box('Fridge upper storage',(66.4,24,7.85),(2.5,4,1.6),M['oak'],.025)
    # Island carcass has actual space for sink, drawers, waste and dishwasher.
    for x in [49.54,59.46]:box('Island cabinet side panel',(x,29.5,1.6),(.08,2.45,2.62),M['oak'],.01)
    box('Island cabinet back panel',(54.5,28.32,1.6),(9.84,.09,2.62),M['oak'],.01)
    box('Island cabinet bottom',(54.5,29.5,.38),(9.84,2.4,.08),M['oak'],.01)
    place('Shared dishwasher beside sink',shared['dishwasher'],(53.25,29.75,0),rotation=math.pi)
    o=bpy.data.objects.get('Kitchen waste pullout cabinet front')
    if o:o.location.x=50.75*F;o.dimensions.x=2.43*F
    for i,o in enumerate([o for o in bpy.data.objects if o.name.startswith('Kitchen waste recycling bin')]):o.location.x=(50.30+i*.9)*F
    # Tall pantry against a solid rear pier leaves the glazed openings untouched.
    for x in [44.1,46.1]:place('Kitchen full-height pantry',shared['wardrobe'],(x,38.3,0))
    for z in [1.5,3,4.5,6]:
        for x in [44.1,46.1]:box('Pantry shelf insert',(x,38.3,z),(1.8,1.8,.055),M['oak'],.005)
