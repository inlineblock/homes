"""Deterministic estate-edge planting and a connected, supported arrival drive.

Coordinates are illustrative concept choices, not a surveyed landscape. Repeated
plants remain rigid linked library instances; only their site placement is local.
"""
import math
import random

import bpy
from mathutils import Vector

from common import geometry as g
from utils import instance, mesh


def _plant_bounds(obj):
    """World XY bounds of a linked plant, including its real foliage extent."""
    points = []
    if obj.instance_collection:
        for child in obj.instance_collection.all_objects:
            if child.type == 'MESH':
                transform = obj.matrix_world @ child.matrix_world
                points.extend(transform @ Vector(p) for p in child.bound_box)
    if not points:
        return (obj.location.x, obj.location.y) * 2
    return (min(p.x for p in points), min(p.y for p in points),
            max(p.x for p in points), max(p.y for p in points))


def _overlaps(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def enrich_site(ROOT, M, assets):
    """Call after base planting; adds no new asset dependencies or native output."""
    g.collection('12 Landscape | connected arrival and wooded garden edge')
    bpy.context.view_layer.update()

    # The road top is -0.54 m; the existing garage apron top is -0.125 m.
    # A single 19.9 m run rises gently between them, overlapping each endpoint.
    # Its deep closed volume bears into the existing ground, without a floating
    # paving sheet. The first 1.05 m lies within the road's existing footprint.
    x0, x1, y0, y1 = -15.0, -11.0, -11.8, 8.1
    z0, z1, bottom = -.54, -.125, -.76
    drive = mesh('Connected side arrival drive', [
        (x0,y0,bottom), (x1,y0,bottom), (x1,y1,bottom), (x0,y1,bottom),
        (x0,y0,z0), (x1,y0,z0), (x1,y1,z1), (x0,y1,z1),
    ], [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),
        (2,3,7,6),(3,0,4,7)], M['stone'])
    drive['design_role'] = 'Illustrative supported driveway, road to garage apron'
    drive['concept_slope'] = (z1-z0)/(y1-y0)
    drive['site_status'] = 'Unsurveyed concept alignment; civil drainage unresolved'

    # Clear real shrub/grass extents, not just their origins, from the vehicle
    # route and a narrow verge. Existing architecture and the mature trees stay.
    clearance = (x0-.25, y0-.15, x1+.25, y1+.15)
    apron = (-17.45,8,-7.95,22)
    removed = 0
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith('Forecourt native concept planting'):
            if _overlaps(_plant_bounds(obj), clearance) or _overlaps(_plant_bounds(obj), apron):
                bpy.data.objects.remove(obj, do_unlink=True)
                removed += 1

    # Six offset crowns establish depth behind the architecture. The principal
    # street view stays open and the elevated review camera passes above them.
    trees = [(-19,23,.90,.65), (-5,29,1.04,2.1), (10,31,.94,3.4),
             (28,28,1.08,1.3), (30,11,.91,4.5), (-18,-2,.92,5.2)]
    for index, (x,y,scale,angle) in enumerate(trees, 1):
        tree = instance('Garden edge canopy %02d' % index, assets['tree'],
                        (x,y,-.53), angle, scale)
        tree['placement_role'] = 'Illustrative background canopy; existing asset'

    # Irregular overlapping drifts form garden edges, instead of a uniform
    # scatter over the whole site. Nothing is introduced within the courtyard.
    rng = random.Random(2026091902)
    drifts = [(-20,20,3.4,5.4), (-6,26,5.0,2.5), (8,27,5.2,2.6),
              (26,25,4.2,3.0), (27,9,2.3,5.1), (-19,-2,2.6,4.2),
              (10,-7.0,3.0,1.7)]
    added = 0
    for group, (cx,cy,rx,ry) in enumerate(drifts, 1):
        for j in range(24):
            angle = rng.random()*math.tau
            radial = math.sqrt(rng.random())
            x = cx + math.cos(angle)*rx*radial
            y = cy + math.sin(angle)*ry*radial
            if _overlaps((x-.7,y-.7,x+.7,y+.7), clearance) or _overlaps((x-.7,y-.7,x+.7,y+.7), apron):
                continue
            if -8.8 < x < 22.7 and -.7 < y < 20.8:
                continue
            if y < 0 and (abs(x-4.2)<1.1 or abs(x-20.45)<1.2):
                continue
            kind = 'shrub' if j % 3 else 'grass'
            plant = instance('Garden edge drift %02d' % group, assets[kind],
                             (x,y,-.53), rng.random()*math.tau,
                             rng.uniform(.78,1.16))
            plant['placement_role'] = 'Grouped garden edge underplanting'
            added += 1
    return {'background_trees':len(trees), 'grouped_plants':added,
            'driveway_plants_removed':removed, 'drive_width_m':4.0,
            'drive_slope':(z1-z0)/(y1-y0)}
