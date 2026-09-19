"""Coastal room placement and styling; reusable furnishings remain linked.

Coordinates are feet. Native assets are rigid, meter-scale collections. These
placements retain the existing circulation and appliance reservations.
"""
import math

import bpy

from common import geometry as g
from common.furnishings import bowl, soft
from common.geometry import box, cyl
from common.library import linked_collection
from common.shared_assets import place
from common.lighting_assets import load as load_lights, place as place_light
from common.timber_materials import grain_uv


FURNITURE = [
    'linen-three-seat-sofa',
    'oak-rounded-coffee-table',
    'oak-dining-table-8ft',
    'oak-upholstered-dining-chair',
    'woven-oatmeal-rug',
    'olive-linen-cushion',
]


def living_dining(root, M):
    """Swap local repeat furniture for pinned assets at the established origins."""
    assets = {slug: linked_collection(root, 'furniture', slug, 'v001')
              for slug in FURNITURE}
    g.collection('04 Furnishings | linked living dining furniture')
    place('Living woven oatmeal rug', assets['woven-oatmeal-rug'], (13, 32.6, .045))
    place('Living shared linen sofa', assets['linen-three-seat-sofa'], (13, 28.7, .04))
    # Retain the existing chaise and its footprint. It is an extension specific
    # to this room's seating composition, not a new duplicate library sofa.
    soft('Living chaise cushion', (7.7, 32.6, 1.07), (3.5, 5.3, .42), M['linen'], .22)
    soft('Living chaise base', (7.7, 32.6, .66), (3.5, 5.3, .6), M['linen'], .20)
    # Cushion origin is its bottom edge. Existing linked sofa accent pillows
    # remain at either arm; the new olive cushions sit forward and inward.
    for x, angle in [(11.1, -.12), (14.9, .12)]:
        cushion = place('Living olive linen cushion', assets['olive-linen-cushion'],
                        (x, 28.65, 1.30), rotation=angle)
        cushion.rotation_euler.x = math.radians(9)
    place('Living shared oak coffee table', assets['oak-rounded-coffee-table'], (14, 33.7, .04))
    box('Coffee table art book', (14.2, 33.9, 1.35), (1.3, 1, .08), M['blue'], .015)
    bowl('Coffee table ceramic', 12.8, 33.7, 1.31, .40, M['porcelain'])
    place('Dining shared eight foot oak table', assets['oak-dining-table-8ft'], (35, 29.1, .04))
    for x in [32.4, 35, 37.6]:
        # Published chair front is -Y; the south row faces north.
        place('Dining shared oak chair south', assets['oak-upholstered-dining-chair'],
              (x, 26.25, .04), rotation=math.pi)
        place('Dining shared oak chair north', assets['oak-upholstered-dining-chair'],
              (x, 31.95, .04))
    bowl('Dining centerpiece', 35, 29.1, 2.54, .72, M['porcelain'])


def build(root, M):
    """Run after appliances so all island finish panels receive the same finish."""
    g.collection('11 Details | warm coastal interior')
    # The source palette stays immutable. Change only the local island panels,
    # never linked equipment or the pale perimeter/serving cabinetry.
    island_prefixes = ('Island cabinet', 'Island stool-side cabinet',
                       'Island drawer front', 'Kitchen waste pullout cabinet front')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and not obj.library and obj.name.startswith(island_prefixes):
            for slot in obj.material_slots:
                if slot.material == M['oak']:
                    slot.material = M['accent_oak']
            grain_uv(obj)
    shelf = bpy.data.objects.get('Entry keys drop shelf')
    if shelf:
        shelf.data.materials.clear()
        shelf.data.materials.append(M['accent_oak'])
        grain_uv(shelf)

    # Wall-mounted entry composition above the existing shallow shelf. It stays
    # west of X=18.5 and north/south clear of the bedroom doorway at Y=8.5.
    backing = box('Entry mirror smoked oak backing', (18.25, 5.9, 5.7),
                  (.10, 2.8, 3.9), M['accent_oak'], .06)
    grain_uv(backing)
    mirror = g.material('Entry mirror | reflective neutral silver', (.80, .82, .81), .035, 1)
    box('Entry mirror recessed reflective face', (18.31, 5.9, 5.7),
        (.025, 2.55, 3.65), mirror, .03)

    # Original site-specific relief composition on the living partition. These
    # are deliberately simple original forms, not a downloaded art reproduction.
    frame = box('Living original coastal art oak frame', (13.4, 26.25, 6.1),
                (6.2, .13, 3.7), M['accent_oak'], .03)
    grain_uv(frame)
    box('Living original coastal art woven ground', (13.4, 26.33, 6.1),
        (5.96, .04, 3.46), M['linen'], .01)
    sun = cyl('Living original coastal art warm disc', (12.0, 26.38, 6.6),
              .82, .035, M['stone'], 64)
    sun.rotation_euler.x = math.pi / 2
    box('Living original coastal art low sea band', (13.9, 26.40, 5.25),
        (4.55, .03, .48), M['blue'], .14)
    box('Living original coastal art dune relief', (14.4, 26.42, 5.9),
        (3.0, .025, .52), M['counter'], .18)

    lights = load_lights(root, keys=['linear'])
    # Fixture origin is canopy top. A 31.848-inch fixed drop places its lens at
    # Z=7.796 ft from the real 10.45 ft ceiling; no stretching or floating canopy.
    place_light('Dining shared linear focal pendant', lights['linear'], 'linear',
                (35, 29.1, 10.45), power=22, color=(1, .80, .58))


def dependencies():
    """Direct adopted collections; material links are recorded by the parent."""
    ids = ['furniture/' + slug for slug in FURNITURE]
    ids.append('fixtures/lighting-linear-pendant-4ft')
    return [{'id': asset, 'version': 'v001', 'path': '../../library/' + asset + '/v001/'}
            for asset in ids]
