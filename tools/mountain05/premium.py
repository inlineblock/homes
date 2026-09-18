"""Premium program: complete kitchen, private bathroom and optional fireplace."""
import bpy,math
from common import geometry as g
from common.geometry import box,cyl,rod,curve,sphere,F
from common.architecture import glass_wall
from common.furnishings import bowl
from common.shared_assets import place

def kitchen(M,C):
    g.collection('03 Kitchen | shared appliances and fitted joinery')
    for x in [43,45,47,49]:place('Rear shared drawer module',C['base_cabinet'],(x,38.45,0))
    # Custom four-foot sink carcass is an appliance-specific cut module, not a solid drawer block.
    for x in [50.04,53.96]:box('Sink cabinet side',(x,38.45,1.56),(.08,2,2.6),M['oak'],.01)
    for x in [51,53]:box('Sink cabinet hinged front',(x,37.40,1.55),(1.96,.08,2.55),M['oak'],.015)
    place('Shared integrated dishwasher',C['dishwasher'],(55,38.45,0))
    top=box('Rear quartzite worktop',(49,38.4,2.98),(14.3,2.8,.18),M['counter'],.025)
    cut=box('Sink opening cutter',(52,38.4,3),(2.5,1.65,.9),M['steel'],.08)
    bpy.context.view_layer.objects.active=top;mod=top.modifiers.new('Real undermount basin opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    box('Sink basin bottom',(52,38.4,2.36),(2.48,1.63,.06),M['steel'],.06)
    for x in [50.75,53.25]:box('Sink basin end',(x,38.4,2.67),(.04,1.65,.60),M['steel'],.015)
    for y in [37.575,39.225]:box('Sink basin side',(52,y,2.67),(2.5,.04,.60),M['steel'],.015)
    curve('Sink mixer faucet',[(52,39.35,3.1),(52,39.35,4.2),(52,38.9,4.5),(52,38.4,4.1)],.045,M['steel'])
    for x in [45,53]:place('Island shared drawer module',C['base_cabinet'],(x,31.8,0),math.pi)
    # Oven has its own full-width cavity; no drawer carcass runs through it.
    place('Shared 30 inch oven',C['oven'],(48,31.8,.38),math.pi)
    for x in [46.35,49.65]:box('Oven side filler',(x,31.8,1.5),(.70,2,2.8),M['oak'],.018)
    box('Island back finish',(49,30.745,1.5),(10,.09,2.8),M['oak'],.01)
    box('Island quartzite worktop',(49,31.8,2.98),(10.3,3.2,.18),M['counter'],.035)
    place('Shared 36 inch induction cooktop',C['cooktop'],(48,31.8,3.09),math.pi)
    place('Shared induction extraction hood',C['hood'],(48,31.8,6.1),math.pi)
    box('Hood vertical duct enclosure',(48,31.8,10.6),(1.1,1.0,4.1),M['dark'],.03)
    cyl('Hood roof exhaust duct',(48,31.8,13.1),.33,1.3,M['dark'])
    cyl('Hood weather cap',(48,31.8,13.8),.52,.13,M['dark'])
    # Dedicated waste pullout beside prep/oven: two bins behind a tall door.
    for x in [50.2,51.8]:box('Waste pullout side',(x,31.8,1.45),(.06,1.9,2.6),M['oak'])
    box('Waste and recycling pullout front',(51,32.86,1.48),(1.95,.08,2.65),M['oak'],.015)
    for y in [31.35,32.25]:box('Waste recycling removable bin',(51,y,1.35),(1.55,.80,1.75),M['dark'],.05)
    for y in [34,36]:place('Shared tall food pantry',C['wardrobe'],(58.5,y,0),-math.pi/2)
    place('Shared 48 inch panel ready refrigerator',C['fridge'],(56.75,27.6,0),math.pi)
    bowl('Counter ceramic bowl',44,38.4,3.10,.65,M['porcelain'])
    box('Preparation cutting board',(53,31.8,3.10),(1.6,1.2,.06),M['oak'],.09)

def primary_bath(M,C):
    g.collection('05 Fixtures | premium primary bath')
    place('Shared freestanding soaking tub',C['bathtub'],(55.5,2.35,0))
    rod('Tub floor mounted filler',(59,2.4,0),(59,2.4,3),.055,M['steel'])
    rod('Tub filler spout',(59,2.4,3),(58.2,2.4,3),.04,M['steel'])
    box('Separate primary shower tray',(48,2.65,.08),(4.8,4.8,.15),M['stone'],.025)
    glass_wall('Primary shower west screen',(45.6,.25),(45.6,5.05),8,M['glass'],M['dark'],.15,1)
    glass_wall('Primary shower east screen',(50.4,.25),(50.4,5.05),8,M['glass'],M['dark'],.15,1)
    glass_wall('Primary shower front fixed glass',(45.6,5.05),(47.2,5.05),8,M['glass'],M['dark'],.15,1)
    rod('Primary shower riser',(48,.5,3),(48,.5,7.6),.04,M['steel']);cyl('Primary rain head',(48,1,7.6),.40,.07,M['steel'])
    # Seven-foot double vanity, two real bowls at four-foot centers.
    for x in [53,55,57]:place('Primary double vanity shared module',C['base_cabinet'],(x,10.8,0))
    box('Primary double vanity stone',(55,10.8,2.98),(6.4,2.6,.16),M['counter'],.02)
    for x in [53,57]:
        bowl('Primary double vanity basin',x,10.8,3.08,.74,M['porcelain'])
        rod('Primary vanity faucet',(x,11.55,3.1),(x,11.55,3.9),.035,M['steel'])
        box('Primary vanity mirror',(x,11.78,5.75),(2.8,.06,3.1),M['steel'],.07)
    # Toilet is inside the actual separate 5 x 6 ft room defined in design.py.
    place('Primary enclosed shared WC',C['toilet'],(42.5,1.95,0),math.pi)

def fireplace(M,C):
    g.collection('08 Structure | fireplace concept and flue allowance')
    box('Noncombustible fireplace chase',(0.6,28.5,6.7),(2.0,6.6,13.4),M['rock'],.04)
    # Opening is a shallow front recess; insert sits in front of the noncombustible chase.
    place('Shared closed glass fireplace',C['fireplace'],(1.3,28.5,1.55),math.pi/2)
    box('Fireplace hearth',(1.4,28.5,.13),(3.0,7.0,.26),M['stone'],.035)
    cyl('Concept fireplace flue',(0.6,28.5,14.1),.4,1.5,M['dark'])
    cyl('Fireplace weather cap',(0.6,28.5,14.9),.65,.12,M['dark'])
