"""Sheltered dune garden composition, using pinned shared planting only.

Authoring coordinates are feet. Plant identities remain illustrative rather
than a coastal species specification. Architecture and circulation stay clear.
"""
import math
import random

from common import geometry as g
from common.shared_assets import place


def dune_height(x, y):
    """Visible ground height from the same dune formula as build.py.

    The flat sand foundation overlaps the dune mesh through Y=80: planting
    cannot be placed on the buried portion of that surface.
    """
    if y < 55:
        return -.12
    fade = max(0., min(1., (y - 57.) / 10.))
    z = -.6 + fade * (.8 * math.sin(x * .11 + y * .17)
                      + .32 * math.sin(x * .31 - y * .12))
    if y > 82:
        z -= ((y - 82.) / 53.) * 2.5
    return max(-.12, z) if y <= 80 else z


def _intersects(x, y, radius, rect):
    x1, y1, x2, y2 = rect
    return x + radius > x1 and x - radius < x2 and y + radius > y1 and y - radius < y2


def _clear(x, y, radius):
    # Conservative whole-plant footprint exclusion, not just origin checks.
    protected = [
        (-.4, -.25, 68.4, 40.4),  # house and glazing
        (-3., 40., 71., 58.),      # entire furnished terrace
        (17., -45., 23., -.25),    # six-foot front pedestrian walk
        (17., -4.25, 86., -.25),   # four-foot parking-to-entry crosswalk
        (72.6, -45., 99.4, -2.),   # two-car driveway/carport and edges
        (16., -7., 28., 2.),       # new entry porch and its approach
        (-200., -67., 200., -45.), # road
    ]
    return not any(_intersects(x, y, radius, rect) for rect in protected)


def build(M, shared):
    """Build 130 grasses, 45 shrubs and six trees in coherent garden rooms.

    M is accepted for the home assembly interface; every plant keeps its linked
    library materials. No asset is regenerated or copied into this home.
    """
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree

    rng = random.Random(240918)
    g.collection('16 Garden rooms | linked dune planting and entry court')

    # Use the actual tessellated dune surface when it exists, rather than
    # floating roots above the sampled mesh. The pure formula is a fallback.
    terrain = bpy.data.objects.get('Soft original coastal dune topography')
    dune_bvh = BVHTree.FromObject(terrain, bpy.context.evaluated_depsgraph_get()) if terrain else None

    def grade(x, y):
        if y < 55 or dune_bvh is None:
            return dune_height(x, y)
        origin = Vector((x * g.F, y * g.F, 30 * g.F))
        local_origin = terrain.matrix_world.inverted() @ origin
        hit, _, _, _ = dune_bvh.ray_cast(local_origin, Vector((0, 0, -1)))
        if hit is None:
            return dune_height(x, y)
        z = (terrain.matrix_world @ hit).z / g.F
        return max(-.12, z) if y <= 80 else z

    # Each tuple describes one shaped drift, not random planting across the
    # whole site. The central ocean outlook and all furnished zones stay open.
    drifts = [
        ('Entry west inner', 11.2, -12.5, 3.1, 5.0, 15, 6),
        ('Entry west approach', 9.5, -29., 4.3, 9.0, 18, 5),
        ('Entry east inner', 32.2, -12.5, 3.4, 5.0, 15, 6),
        ('Entry east garden', 41., -28., 9.0, 11., 20, 8),
        ('West side garden', -7., -15., 4.0, 10., 10, 4),
        ('Terrace west shelter', -8., 48., 3.5, 8.0, 14, 5),
        ('Terrace east shelter', 77., 49., 3.5, 9.0, 14, 5),
        ('West dune crescent', -5., 65.5, 7.0, 5.5, 12, 3),
        ('East dune crescent', 77., 67., 7.0, 6.0, 12, 3),
        ('Low central dune west', 25., 65., 10., 4., 20, 2),
        ('Low central dune east', 52., 72., 12., 5., 20, 4),
    ]
    counts = {'grass': 0, 'shrub': 0, 'olive': 0}
    for label, cx, cy, rx, ry, grass_count, shrub_count in drifts:
        for kind, count in [('shrub', shrub_count), ('grass', grass_count)]:
            placed = []
            for index in range(count):
                for _ in range(300):
                    angle = rng.uniform(0, math.tau)
                    distance = math.sqrt(rng.random())
                    # Slight bend gives the beds flowing, tapered boundaries.
                    y = cy + math.sin(angle) * ry * distance
                    x = cx + math.cos(angle) * rx * distance + .12 * (y - cy)
                    scale = rng.uniform(.72, 1.06) if kind == 'grass' else rng.uniform(.72, 1.0)
                    radius = (1.4 if kind == 'grass' else 1.55) * scale
                    spacing = .85 if kind == 'grass' else 1.45
                    if _clear(x, y, radius) and all(math.hypot(x-a, y-b) > spacing for a, b in placed):
                        break
                else:
                    raise ValueError('No clear planting position for ' + label + ' ' + kind)
                placed.append((x, y))
                obj = place(label + ' | shared ' + kind, shared[kind],
                            (x, y, grade(x, y) - .015),
                            rotation=rng.uniform(0, math.tau), scale=scale)
                obj['garden_zone'] = label
                obj['circulation_footprint_radius_ft'] = radius
                counts[kind] += 1

    # Asymmetric published olive bounds need up to 6.3 ft at full scale.
    # Keep the complete canopy outside walkways, roof edges and parking.
    for label, x, y, scale in [
        ('Entry west canopy', 8.5, -20.5, .88),
        ('Entry east canopy', 49., -20., .85),
        ('West side canopy', -9., 29., .92),
        ('East side canopy', 79., 29., .92),
        ('West dune framing canopy', -12., 70., .85),
        ('East dune framing canopy', 88., 71., .82),
    ]:
        assert _clear(x, y, 6.3 * scale), label + ' intrudes on a protected route or terrace'
        # Linked olive mesh root minimum is -0.0030199 m below its origin.
        # Lift by that scaled amount so roots touch the real sand surface.
        root_offset_ft = .003019925905391574 / g.F * scale
        obj = place(label + ' | shared olive', shared['olive'],
                    (x, y, grade(x, y) + root_offset_ft),
                    rotation=rng.uniform(0, math.tau), scale=scale)
        obj['garden_zone'] = label
        obj['circulation_footprint_radius_ft'] = 6.3 * scale
        counts['olive'] += 1
    return counts
