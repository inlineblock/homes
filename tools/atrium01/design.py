"""Atrium 01 measured concept: meters internally; feet only at input/display.

All room rectangles are planning zones. Wall centerlines and their thicknesses,
opening offsets, and furniture footprints determine finished clear dimensions.
Southwest outer footprint corner is (0, 0); floor finish datum is z=0.
"""
from math import dist
FT = 0.3048

def ft(value):
    return value * FT

def p(x, y):
    return (ft(x), ft(y))

def box(x1, y1, x2, y2):
    return tuple(ft(v) for v in (x1, y1, x2, y2))

WIDTH, DEPTH = ft(60), ft(44)
HEIGHT = ft(10.5)  # Finished ceiling, not wall/roof assembly height.
BEAM_CLEAR = ft(9.5)
SERVICE_CLEAR = ft(9)
FLOOR_DATUM = 0.0
ROOF_BOUNDS = box(-2, -2, 62, 46)
ATRIUM = box(25, 13, 41, 28)
GROSS_AREA = WIDTH * DEPTH - (ATRIUM[2]-ATRIUM[0])*(ATRIUM[3]-ATRIUM[1])
GROSS_AREA_SQFT = round(GROSS_AREA / FT**2)

ROOMS = [
 ('bedroom-2',box(0,0,13,14.2),'BEDROOM 02'),
 ('bath-2',box(13,0,20,8),'ENSUITE 02'),
 ('wardrobe-2',box(13,8,20,10.25),'WARDROBE 02'),
 ('bedroom-2-entry',box(13,10.25,20,14.2),'BEDROOM 02 ENTRY'),
 ('bedroom-3',box(0,14.2,13,28.2),'BEDROOM 03'),
 ('laundry',box(13,14.2,20,22),'LAUNDRY'),
 ('wardrobe-3',box(13,22,20,24.25),'WARDROBE 03'),
 ('bedroom-3-entry',box(13,24.25,20,28.2),'BEDROOM 03 ENTRY'),
 ('gallery',box(20,0,25,28.2),'PRIVATE GALLERY'),
 ('primary',box(0,28.2,14,44),'PRIMARY BEDROOM'),
 ('primary-vestibule',box(14,28.2,25,32),'PRIVATE VESTIBULE'),
 ('primary-bath',box(14,32,25,44),'PRIMARY BATH'),
 ('primary-wc',box(21.5,32,25,37.65),'ENCLOSED WC'),
 ('bath-3',box(25,0,33,8),'SHARED BATH'),
 ('entry',box(33,0,41,8),'FOYER / COATS'),
 ('cross-gallery',box(25,8,41,13),'INDOOR CROSS-GALLERY'),
 ('pantry',box(41,0,49,8),'PANTRY'),
 ('utility',box(49,0,60,8),'UTILITY / BULK'),
 ('kitchen',box(41,8,60,28),'KITCHEN'),
 ('dining',box(25,28,41,44),'DINING'),
 ('living',box(41,28,60,44),'LIVING'),
]

def wall(name, a, b, thickness=.35, openings=()):
    return (name, p(*a), p(*b), ft(thickness),
            [tuple(ft(v) for v in opening[:4]) + (opening[4],) for opening in openings])

# Openings: offset from a, nominal width, finished sill, finished head, kind.
# The door opening width is a nominal frame opening, not certified leaf clearance.
WALLS = [
 wall('south',(0,.25),(60,.25),.5,[(2,9,2.75,9.25,'window'),(34,4,0,8.5,'entry'),(43,4,6.5,8.5,'window'),(51,6,6.5,8.5,'window')]),
 wall('west',(.25,0),(.25,44),.5,[(3,7,2.75,9.25,'window'),(17,7,2.75,9.25,'window'),(34,8,.3,9.25,'glass')]),
 wall('north',(0,43.75),(60,43.75),.5,[(2,10,.3,9.25,'glass'),(16,7,6.5,9.25,'window'),(26,13,0,9.25,'slider'),(43,14,0,9.25,'glass')]),
 wall('east',(59.75,0),(59.75,44),.5,[(11,14,3.6,9.25,'window'),(30,11,0,9.25,'glass')]),
 wall('bedroom-gallery',(20,0),(20,28.2),.35,[(10.4,3.2,0,8,'door'),(16.2,3.2,0,8,'door'),(24.4,3.2,0,8,'door')]),
 wall('secondary-divider',(0,14.2),(20,14.2)),
 wall('ensuite-2-west',(13,0),(13,8),.35,[(3.4,3.2,0,8,'door')]),
 wall('ensuite-2-north',(13,8),(20,8)),
 wall('laundry-west',(13,14.2),(13,22)),
 wall('laundry-north',(13,22),(20,22)),
 wall('primary-south',(0,28.2),(25,28.2),.35,[(20.4,3.4,0,8,'door')]),
 wall('primary-east',(14,28.2),(14,44),.35,[(.4,3.0,0,8,'door')]),
 wall('primary-bath-south',(14,32),(25,32),.35,[(3.35,3.0,0,8,'door')]),
 wall('primary-suite-east',(25,28),(25,44)),
 wall('primary-wc-west',(21.5,32),(21.5,37.65),.35,[(.6,2.8,0,8,'door')]),
 wall('primary-wc-north',(21.5,37.65),(25,37.65)),
 wall('shared-bath-west',(25,0),(25,8)),
 wall('shared-bath-east',(33,0),(33,8)),
 wall('shared-bath-north',(25,8),(33,8),.35,[(1.3,3.2,0,8,'door')]),
 wall('pantry-west',(41,0),(41,8)),
 wall('pantry-east',(49,0),(49,8),.35,[(2.4,3.2,0,8,'door')]),
 wall('service-north',(41,8),(60,8),.35,[(2.5,3.2,0,8,'door')]),
]

COURTYARD_GLAZING = [
 ('atrium-west',p(25,13),p(25,28)),
 ('atrium-east',p(41,13),p(41,28)),
 ('atrium-south',p(25,13),p(41,13)),
 ('atrium-north',p(25,28),p(41,28)),
]
# Slider reservation: offset and full assembly width; half the assembly is movable.
COURTYARD_SLIDERS = {'atrium-east': (ft(6),ft(8)), 'atrium-north': (ft(7),ft(8))}
# Keys index only door/entry openings within each wall, excluding windows.
# Rotation is relative to the wall tangent, in degrees. Pocket/slider exceptions
# are explicit so the plan never presents their leaves as hinged geometry.
DOOR_SWINGS = {
 ('south',0): 90,
 ('bedroom-gallery',0): 90, ('bedroom-gallery',1): 90, ('bedroom-gallery',2): 90,
 ('ensuite-2-west',0): 90,
 ('primary-south',0): 90,
 ('primary-east',0): 90,
 ('primary-bath-south',0): 'pocket',
 ('primary-wc-west',0): -90,
 ('shared-bath-north',0): 'pocket',
 ('service-north',0): -90, ('pantry-east',0): -90,
}
DOOR_HINGES = {('bedroom-gallery',1): 'end', ('primary-south',0): 'end'}
# -1 stores toward wall start; +1 stores toward wall end.
POCKET_DIRECTIONS = {('primary-bath-south',0): -1}

SLABS = [box(0,0,60,13),box(0,13,25,28),box(41,13,60,28),box(0,28,60,44)]
SERVICE_ZONES = [box(13,0,20,8),box(13,14.2,20,22),box(25,0,33,8),box(41,0,60,8)]
CARPORT = box(0,-27,24,-5)
PARKING_BAYS = [box(1,-25,11,-7),box(13,-25,23,-7)]
SHELTERED_WALK = box(0,-5,41,0)
FRONT_LANDING = box(31,-6,41,0)
REAR_TERRACE = box(25,44,60,55)
SITE_BOUNDS = box(-14,-48,77,65)
KITCHEN_ISLAND = (ft(48)-.10, ft(15.75), ft(52.25)-.10, ft(25.75))
# Planning reservations; actual installed assets are recorded separately.
CLEARANCE_TARGETS = {'gallery':ft(4.65), 'south_cross_gallery':ft(4.65),
                     'kitchen_work_aisle':1.62, 'island_south_aisle':ft(5.1)}


def validate_layout():
    assert GROSS_AREA_SQFT == 2400
    for name,a,b,t,opens in WALLS:
        length=dist(a,b); end=0
        for offset,width,sill,head,kind in sorted(opens):
            assert offset >= end - 1e-8, (name,'overlap')
            assert offset + width <= length + 1e-8, (name,'outside wall')
            assert 0 <= sill < head <= HEIGHT, (name,'vertical opening')
            end=offset+width
    return True

validate_layout()
