"""Original generic kitchen appliances and closed-glass fireplace insert.

Authoring units feet. These are editable visual planning envelopes, not a
manufacturer's CAD, installation requirements or certified working products.
"""
import bpy
import math
from pathlib import Path
from . import geometry as g
from .geometry import box, rod, cyl, F
from .architecture import mesh

DESCRIPTIONS = {
    'oven': ('Original 30-inch built-in oven', 'Bottom-center origin, front -Y. Nominal 30W x 24D x 28H inches; handle extends about two inches beyond front. Glass door, inner cavity, two racks and control fascia. Host cabinetry must provide the actual clear appliance opening; no solid carcass or drawer behind the face.'),
    'dishwasher': ('Original 24-inch dishwasher', 'Floor-center origin, front -Y. Nominal 24W x 24D x 34H inches; handle projects beyond front. Provide adjacent sink services and unobstructed downward door opening in host design.'),
    'cooktop': ('Original 36-inch induction cooktop', 'Top face at Z=0, centered XY, controls toward -Y. Nominal 36W x 21D inches, five induction zones. Host worktop opening and electrical services remain project-specific.'),
    'hood': ('Original 36-inch wall hood', 'Bottom-center origin, front -Y, rear +Y toward wall. Nominal 36W x 22D x 30H inches. Filters, task lights and chimney cover included. Host supplies a continuous exhaust route and product-specific installation height.'),
    'fireplace': ('Original 48-inch closed-glass fireplace insert', 'Bottom-center origin, front -Y. Nominal 48W x 18D x 32H inches plus top flue collar and handle projection. Glass enclosure and original log bed; no active flame. Host supplies noncombustible surround, hearth, continuous conceptual flue and local engineering review. Fuel, listed product and clearances unselected.'),
    'fridge': ('Original 48-inch panel-ready refrigerator', 'Floor-center origin, front -Y. Nominal 48W x 30D x 84H inches; handles project about 1.7 inches beyond front. Two original white-oak door panels with narrow reveals, discreet handles and recessed lower ventilation grille. Generic refrigeration envelope; compartment arrangement, selected product, vent area and installation clearances remain unverified.'),
}


def materials():
    M = {'steel': g.material('Original appliance brushed stainless',(.39,.42,.43),.29,.85),
         'dark': g.material('Original appliance graphite enamel',(.021,.026,.03),.27,.15),
         'rubber': g.material('Original appliance black gasket',(.012,.013,.014),.85),
         'ceramic': g.material('Original induction black ceramic',(.012,.021,.026),.15,.2),
         'marks': g.material('Original appliance etched control marks',(.30,.34,.34),.38,.4),
         'log': g.material('Original unlit fireplace log',(.060,.036,.023),.9),
         'glass': g.material('Original appliance low-tint glass',(.72,.78,.81),.045)}
    p=M['glass'].node_tree.nodes.get('Principled BSDF')
    p.inputs['Transmission Weight'].default_value=.94
    p.inputs['IOR'].default_value=1.46
    return M


def _ring(name,x,y,z,r,mat):
    bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=6,major_radius=r*F,
                                   minor_radius=.003*F,location=(x*F,y*F,z*F))
    o=g.move(bpy.context.object);o.name=name;o.data.materials.append(mat)
    return o


def _oven(M):
    w,h=2.5,28/12
    # Hollow enclosure with inset cavity; the window is not laid over a solid cube.
    for x in [-1.20,1.20]:box('Oven steel side casing',(x,0,h/2),(.10,2,h),M['steel'],.015)
    box('Oven insulated rear',(0,.94,h/2),(2.30,.12,h),M['dark'],.02)
    for z in [.06,h-.06]:box('Oven top or bottom casing',(0,0,z),(2.30,2,.12),M['dark'],.015)
    box('Oven control fascia',(0,-1.01,2.11),(2.5,.09,.446),M['steel'],.018)
    for x in [-1.19,1.19]:box('Oven door side stile',(x,-1.025,1.05),(.12,.08,1.92),M['dark'],.018)
    for z in [.11,1.90]:box('Oven door top or bottom stile',(0,-1.025,z),(2.28,.08,.17),M['dark'],.015)
    box('Oven transparent viewing window',(0,-1.018,1.02),(2.18,.025,1.62),M['glass'],.014)
    rod('Oven full-width door handle',(-1.01,-1.17,1.75),(1.01,-1.17,1.75),.036,M['steel'])
    for x in [-.99,.99]:rod('Oven handle bracket',(x,-1.03,1.75),(x,-1.17,1.75),.035,M['steel'])
    for x in [-.91,.91]:
        o=cyl('Oven selector dial',(x,-1.085,2.11),.092,.045,M['dark'],32);o.rotation_euler.x=math.pi/2
        box('Oven dial indicator',(x,-1.113,2.15),(.012,.006,.044),M['marks'],.002)
    box('Oven dark display',(0,-1.065,2.11),(.72,.009,.17),M['dark'],.015)
    for x in [-.22,0,.22]:
        for z in [2.06,2.11,2.16]:box('Oven subtle display segment',(x,-1.073,z),(.12,.005,.008),M['marks'],.002)
    for z in [.55,1.13]:
        for x in [-1.04,1.04]:rod('Oven rack side',(x,-.88,z),(x,.75,z),.014,M['steel'])
        for i in range(15):
            y=-.85+i*.11
            rod('Oven rack rail',(-1.04,y,z),(1.04,y,z),.011,M['steel'])


def _dishwasher(M):
    box('Dishwasher appliance enclosure',(0,.03,1.42),(1.96,1.94,2.81),M['dark'],.03)
    box('Dishwasher brushed front',(0,-.995,1.51),(1.975,.09,2.62),M['steel'],.024)
    box('Dishwasher upper control strip',(0,-1.049,2.69),(1.89,.02,.17),M['dark'],.012)
    rod('Dishwasher door handle',(-.78,-1.16,2.40),(.78,-1.16,2.40),.033,M['steel'])
    for x in [-.75,.75]:rod('Dishwasher handle bracket',(x,-1.04,2.40),(x,-1.16,2.40),.03,M['steel'])
    box('Dishwasher recessed toe kick',(0,-.84,.13),(1.84,.08,.26),M['rubber'],.012)
    for x in [-.67,-.45,-.23]:box('Dishwasher program mark',(x,-1.064,2.69),(.09,.007,.012),M['marks'],.003)
    box('Dishwasher status display',(.50,-1.064,2.69),(.34,.007,.08),M['marks'],.006)


def _cooktop(M):
    box('Cooktop below-counter casing',(0,0,-.082),(2.85,1.59,.16),M['dark'],.035)
    box('Induction ceramic glass surface',(0,0,-.025),(3,1.75,.05),M['ceramic'],.027)
    for x,y,r in [(-.96,-.36,.31),(-.96,.38,.30),(.96,-.36,.31),(.96,.38,.30),(0,.12,.36)]:
        _ring('Induction etched cooking zone',x,y,.001,r,M['marks'])
        rod('Induction zone center horizontal',(x-.035,y,.005),(x+.035,y,.005),.002,M['marks'])
        rod('Induction zone center vertical',(x,y-.035,.005),(x,y+.035,.005),.002,M['marks'])
    for x in [-.48,-.24,0,.24,.48]:
        box('Induction touch control',(x,-.70,.003),(.12,.015,.004),M['marks'],.002)


def _hood(M):
    # Tapered closed canopy rising to an actual chimney cover.
    vertices=[(-1.5,-11/12,0),(1.5,-11/12,0),(1.5,11/12,0),(-1.5,11/12,0),
              (-.72,-.42,.63),(.72,-.42,.63),(.72,11/12,.63),(-.72,11/12,.63)]
    mesh('Wall hood tapered steel canopy',vertices,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],M['steel'])
    box('Wall hood chimney cover',(0,.39,1.56),(1.12,1.04,1.88),M['steel'],.016)
    box('Hood recessed underside filter',(0,0,-.006),(2.45,1.27,.018),M['dark'],.015)
    for i in range(17):box('Hood washable baffle',(i*.13-1.04,0,-.021),(.025,1.15,.025),M['steel'],.008)
    for x in [-1.25,1.25]:cyl('Hood task light lens',(x,-.54,-.018),.075,.02,M['marks'],32)
    for x in [-.12,0,.12]:box('Hood control button',(x,-11/12-.006,.10),(.05,.015,.034),M['dark'],.006)


def _fireplace(M):
    h=32/12
    box('Fireplace rear enclosure',(0,.69,h/2),(4,.12,h),M['dark'],.015)
    for x in [-1.95,1.95]:box('Fireplace steel side',(x,0,h/2),(.10,1.50,h),M['dark'],.012)
    for z in [.06,h-.06]:box('Fireplace top or bottom enclosure',(0,0,z),(3.8,1.5,.12),M['dark'],.012)
    for x in [-1.86,1.86]:box('Fireplace front stile',(x,-.755,h/2),(.28,.08,h),M['dark'],.018)
    for z in [.16,h-.16]:box('Fireplace front top or sill',(0,-.755,z),(3.50,.08,.32),M['dark'],.018)
    box('Fireplace sealed glass',(0,-.757,h/2),(3.50,.035,h-.59),M['glass'],.01)
    rod('Fireplace access handle',(1.79,-.84,1.12),(1.79,-.84,1.62),.028,M['dark'])
    for x in [-1.2,-.6,0,.6,1.2]:rod('Fireplace grate',(x,-.5,.38),(x,.45,.38),.022,M['steel'])
    for a,b,r in [((-1.30,-.18,.49),(1.05,.22,.65),.12),((-1.00,.28,.67),(1.20,-.27,.65),.13),((-.50,-.10,.75),(.65,.18,.91),.105)]:
        rod('Original unlit firewood log',a,b,r,M['log'])
    cyl('Fireplace conceptual flue collar',(0,.28,h+.075),.29,.15,M['dark'],48)


def _fridge(M):
    box('Refrigerator concealed appliance enclosure',(0,.02,3.5),(3.92,2.44,6.96),M['dark'],.025)
    for x in [-1.97,1.97]:box('Integrated refrigerator oak side',(x,0,3.5),(.06,2.5,7),M['oak'],.009)
    box('Integrated refrigerator oak top',(0,0,6.97),(3.88,2.5,.06),M['oak'],.008)
    for x in [-.978,.978]:
        box('Refrigerator editable oak door panel',(x,-1.217,3.65),(1.94,.065,6.54),M['oak'],.013)
        handle_x = -.13 if x<0 else .13
        rod('Refrigerator discreet warm-metal pull',(handle_x,-1.365,3.55),(handle_x,-1.365,5.05),.023,M['steel'])
        for z in [3.6,5.0]:rod('Refrigerator pull mount',(handle_x,-1.25,z),(handle_x,-1.365,z),.022,M['steel'])
    box('Refrigerator recessed ventilation opening',(0,-1.18,.18),(3.86,.06,.30),M['rubber'],.008)
    for z in [.07,.13,.19,.25,.31]:box('Refrigerator ventilation grille slat',(0,-1.22,z),(3.75,.028,.019),M['dark'],.004)


def build_appliance(key, root):
    M=materials()
    if key == 'fridge':
        path=Path(root)/'library/materials/coastal-white-oak/v001/coastal-white-oak.blend'
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.materials=[src.materials[0]]
        M['oak']=dst.materials[0]
    {'oven':_oven,'dishwasher':_dishwasher,'cooktop':_cooktop,'hood':_hood,'fireplace':_fireplace,'fridge':_fridge}[key](M)
