"""Raised, genuinely vaulted coastal pavilion and two lower draining wings.

This is coordinated concept geometry. Timber-clad engineered frames express
load paths; member sizing, connections and roof products remain unengineered.
"""
import math

from coastal04.roof_design import *


def build(M):
    from common.geometry import box, rod, collection
    from common.architecture import mesh, beam
    from common.timber_materials import grain_uv

    collection('09 Roof | raised coastal pavilion and stepped wings')
    wood = M['accent_oak']
    metal = M['roof_metal']
    exterior = M.get('exterior_plaster', M['plaster'])

    def classify(obj, cls, note=None):
        obj['ifc_class'] = cls
        if note:
            obj['concept_intent'] = note
        return obj

    def timber(name, a, b, width, depth, cls='IfcBeam'):
        obj = classify(beam(name, a, b, width, depth, wood), cls,
                       'Exposed driftwood timber finish; engineered core, bearing and fixings unresolved')
        grain_uv(obj)
        return obj

    def solid_panels(name, patches, thickness, mat, cls):
        """Closed solids for coplanar adjoining patches; feet to common mesh."""
        vertices, faces = [], []
        for poly in patches:
            n = len(poly)
            base = len(vertices)
            vertices.extend(poly)
            vertices.extend((x, y, z - thickness) for x, y, z in poly)
            faces.extend([tuple(base + i for i in range(n)), tuple(base + n + i for i in reversed(range(n)))])
            faces.extend((base + i, base + (i + 1) % n, base + n + (i + 1) % n, base + n + i) for i in range(n))
        obj = classify(mesh(name, vertices, faces, mat), cls)
        if mat == wood:
            grain_uv(obj)
        return obj

    def plane(name, rect, height, thickness, mat, cls='IfcRoof'):
        x1, y1, x2, y2 = rect
        return solid_panels(name, [[(x1, y1, height(x1, y1)), (x2, y1, height(x2, y1)),
                                   (x2, y2, height(x2, y2)), (x1, y2, height(x1, y2))]], thickness, mat, cls)

    def vertical(name, poly, axis, thickness, mat, cls='IfcWall'):
        n = len(poly)
        vertices = list(poly)
        for point in poly:
            other = list(point)
            other[axis] += thickness
            vertices.append(tuple(other))
        faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
        faces.extend((i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n))
        return classify(mesh(name, vertices, faces, mat), cls)

    # Finite roof skins, with a real .70 ft roof-to-interior ceiling reserve.
    plane('Pavilion west 3 in 12 roof', (-3, 18, 22, 43), lambda x, y: pavilion_roof_height(x), ROOF_SKIN_THICKNESS, metal)
    plane('Pavilion east 3 in 12 roof', (22, 18, 47, 43), lambda x, y: pavilion_roof_height(x), ROOF_SKIN_THICKNESS, metal)
    plane('Front wing 1 in 12 roof', FRONT_ROOF_BOUNDS, lambda x, y: front_roof_height(y), ROOF_SKIN_THICKNESS, metal)
    plane('Kitchen wing 1 in 12 roof', KITCHEN_ROOF_BOUNDS, lambda x, y: kitchen_roof_height(x), ROOF_SKIN_THICKNESS, metal)
    for i in range(18):
        y = 18 + i * 25 / 17
        for end_x in (-3, 47):
            classify(beam('Pavilion standing seam', (22, y, PAVILION_RIDGE + .035),
                          (end_x, y, pavilion_roof_height(end_x) + .035), .035, .065, metal), 'IfcMember')
    for i in range(49):
        x = -2 + i * 1.5
        classify(beam('Front wing standing seam', (x, -3.75, front_roof_height(-3.75) + .035),
                      (x, 20, LOW_WING_HIGH + .035), .035, .065, metal), 'IfcMember')
    for i in range(17):
        y = 20 + i * 23 / 16
        classify(beam('Kitchen wing standing seam', (44, y, LOW_WING_HIGH + .035),
                      (71, y, kitchen_roof_height(71) + .035), .035, .065, metal), 'IfcMember')
    classify(box('Pavilion ridge weather cap', (22, 30.5, PAVILION_RIDGE + .025), (.42, 25.15, .10), metal, .015), 'IfcMember')

    # Sloped timber soffits are outside the thermal enclosure, not fake ceilings.
    eave_patches = [(-3, 18, 22, 20), (22, 18, 47, 20), (-3, 40, 22, 43),
                   (22, 40, 47, 43), (-3, 20, 0, 40), (44, 20, 47, 40)]
    for index, rect in enumerate(eave_patches):
        plane('Pavilion deep timber eave %02d' % index, rect, lambda x, y: pavilion_roof_height(x) - .30,
              .10, wood, 'IfcCovering')
    for y in (18., 43.):
        for a, b in [(-3., 22.), (22., 47.)]:
            timber('Pavilion sculpted timber gable edge', (a, y, pavilion_roof_height(a) - .20),
                   (b, y, pavilion_roof_height(b) - .20), .16, .40, 'IfcMember')
    for x in (-3., 47.):
        timber('Pavilion long timber eave edge', (x, 18, pavilion_roof_height(x) - .20),
               (x, 43, pavilion_roof_height(x) - .20), .14, .40, 'IfcMember')
    for rect in [(-2, -3.75, 70, 0), (-2, 0, 0, 20), (68, 0, 70, 20)]:
        plane('Front wing timber-lined eave', rect, lambda x, y: front_roof_height(y) - .30, .10, wood, 'IfcCovering')
    for rect in [(68, 20, 71, 43), (44, 40, 68, 43)]:
        plane('Kitchen wing timber-lined eave', rect, lambda x, y: kitchen_roof_height(x) - .30, .10, wood, 'IfcCovering')

    # Only the protected program regions retain a flat ceiling.
    flat_patches = [[(x1, y1, FLAT_CEILING + CEILING_THICKNESS), (x2, y1, FLAT_CEILING + CEILING_THICKNESS),
                     (x2, y2, FLAT_CEILING + CEILING_THICKNESS), (x1, y2, FLAT_CEILING + CEILING_THICKNESS)]
                    for x1, y1, x2, y2 in FLAT_RECTS]
    solid_panels(FLAT_CEILING_NAME, flat_patches, CEILING_THICKNESS, M['ceiling'], 'IfcCovering')
    for side, low, high, name in [('west', 0, 22, WEST_CEILING_NAME), ('east', 22, 44, EAST_CEILING_NAME)]:
        patches = []
        for x1, y1, x2, y2 in VAULT_RECTS:
            a, b = max(x1, low), min(x2, high)
            if b > a:
                z = lambda x: pavilion_roof_height(x) - VAULT_ASSEMBLY_DEPTH + CEILING_THICKNESS
                patches.append([(a, y1, z(a)), (b, y1, z(b)), (b, y2, z(b)), (a, y2, z(a))])
        solid_panels(name, patches, CEILING_THICKNESS, M['plaster'], 'IfcCovering')

    # Enclose the raised volume and the stepped roofs, avoiding open attic voids.
    for x in (0., 44.):
        ztop = pavilion_roof_height(x) - ROOF_SKIN_THICKNESS
        vertical('Pavilion raised side wall', [(x - .12, 20, 10.5), (x - .12, 40, 10.5),
                 (x - .12, 40, ztop), (x - .12, 20, ztop)], 0, .24, exterior)
    for x in (0., 68.):
        vertical('Front wing sloping attic side', [(x - .10, 0, 10.5), (x - .10, 20, 10.5),
                 (x - .10, 20, front_roof_height(20) - ROOF_SKIN_THICKNESS),
                 (x - .10, 0, front_roof_height(0) - ROOF_SKIN_THICKNESS)], 0, .20, exterior)
    classify(box('Front wing attic front closure', (34, .1, (10.5 + front_roof_height(0) - ROOF_SKIN_THICKNESS) / 2),
                 (68, .20, front_roof_height(0) - ROOF_SKIN_THICKNESS - 10.5), exterior, .012), 'IfcWall')
    vertical('Kitchen rear sloping attic closure', [(44, 39.9, 10.5), (68, 39.9, 10.5),
             (68, 39.9, kitchen_roof_height(68) - ROOF_SKIN_THICKNESS),
             (44, 39.9, kitchen_roof_height(44) - ROOF_SKIN_THICKNESS)], 1, .20, exterior)
    classify(box('Kitchen east attic closure', (67.9, 30, (10.5 + kitchen_roof_height(68) - ROOF_SKIN_THICKNESS) / 2),
                 (.20, 20, kitchen_roof_height(68) - ROOF_SKIN_THICKNESS - 10.5), exterior, .01), 'IfcWall')
    vertical('Lower wings real roof-step riser', [(44, 19.95, 13), (70, 19.95, 13),
             (70, 19.95, kitchen_roof_height(70))], 1, .15, exterior)
    # Concealed bath corner is closed against the high room above its own ceiling.
    vertical('Primary bath upper privacy return', [(18, 20, FLAT_CEILING), (18, 26, FLAT_CEILING),
             (18, 26, pavilion_roof_height(18) - VAULT_ASSEMBLY_DEPTH),
             (18, 20, pavilion_roof_height(18) - VAULT_ASSEMBLY_DEPTH)], 0, .16, M['plaster'])
    vertical('Primary bath upper living return', [(0, 26, FLAT_CEILING), (18, 26, FLAT_CEILING),
             (18, 26, pavilion_roof_height(18) - VAULT_ASSEMBLY_DEPTH),
             (0, 26, pavilion_roof_height(0) - VAULT_ASSEMBLY_DEPTH)], 1, .16, M['plaster'])

    # Rear glazing sees the real vaulted public room. Front glazing begins over
    # the open foyer/dining zone, not the retained bath ceiling/attic at x<18.
    def gable_band(name, x1, x2, y, bottom, top):
        return vertical(name, [(x1, y, bottom), (x2, y, bottom),
                              (x2, y, top(x2)), (x1, y, top(x1))], 1, .20, exterior)
    ceiling_profile = lambda x: pavilion_roof_height(x) - VAULT_ASSEMBLY_DEPTH
    gable_band('Rear pavilion upper header band', 0, 44, 39.90, 10.5, lambda x: 11.10)
    gable_band('Front pavilion entry transition band', 0, 44, 19.90, 10.5, lambda x: 13.8)
    gable_band('Front pavilion private gable field', 0, 18, 19.90, 13.8, ceiling_profile)
    gable_band('Front pavilion east gable field', 42, 44, 19.90, 13.8, ceiling_profile)
    for label, y, sill, breaks in [('rear', 40.02, 11.10, [.40, 5.5, 11, 16.5, 22, 27.5, 33, 38.5, 43.6]),
                                    ('front', 20.02, 13.80, [18, 22, 27, 32, 37, 42])]:
        for a, b in zip(breaks, breaks[1:]):
            top_a, top_b = ceiling_profile(a) - .10, ceiling_profile(b) - .10
            assert min(top_a, top_b) > sill + .12
            vertical(UPPER_GLAZING_PREFIX + ' ' + label,
                     [(a + .07, y, sill + .08), (b - .07, y, sill + .08),
                      (b - .07, y, ceiling_profile(b - .07) - .10),
                      (a + .07, y, ceiling_profile(a + .07) - .10)], 1, .035, M['glass'], 'IfcWindow')
            classify(beam('Pavilion upper glazing sloped frame', (a, y, top_a), (b, y, top_b), .10, .12, M['bronze']), 'IfcMember')
        for x in breaks:
            top = ceiling_profile(x) - .10
            classify(box('Pavilion upper glazing vertical frame', (x, y + .015, (sill + top) / 2),
                         (.12, .13, top - sill), M['bronze'], .005), 'IfcMember')
        classify(box('Pavilion upper glazing sill rail', ((breaks[0] + breaks[-1]) / 2, y + .015, sill + .025),
                     (breaks[-1] - breaks[0], .16, .13), M['bronze'], .006), 'IfcMember')
    # Small terminal wall returns close between glazing frames and side walls.
    for a, b in [(0, .4), (43.6, 44)]:
        gable_band('Rear pavilion gable end return', a, b, 39.90, 11.10, ceiling_profile)
    # Close the real roof assembly above each gable: no exposed attic slot
    # between the glazing/ceiling edge and the underside of the roof deck.
    for y in (20., 40.10):
        for a, b in [(0., RIDGE_X), (RIDGE_X, 44.)]:
            timber('Pavilion timber gable assembly closure',
                   (a, y, pavilion_roof_height(a) - .54),
                   (b, y, pavilion_roof_height(b) - .54), .28, .55, 'IfcCovering')

    # Timber-clad engineered portal frames follow the roof, with real posts at
    # side walls, never through the 30 ft slider or its retractable pocket.
    frame_offset = FRAME_DEPTH * math.sqrt(1 + PAVILION_PITCH ** 2) / 2
    for y in FRAME_Y:
        for x in FRAME_POST_X:
            top = pavilion_roof_height(x) - VAULT_ASSEMBLY_DEPTH - FRAME_DEPTH
            wet_zone = x == FRAME_POST_X[0] and y == FRAME_Y[0]
            name = 'Pavilion encased wet-zone structural frame post' if wet_zone else 'Pavilion driftwood structural frame post'
            finish = M['stone'] if wet_zone else wood
            intent = ('Stone-clad engineered frame column in primary wet zone; waterproofing and connection design unresolved'
                      if wet_zone else 'Timber-clad engineered frame column; connections and foundations unengineered')
            obj = classify(box(name, (x, y, top / 2), (FRAME_POST_WIDTH, FRAME_WIDTH, top), finish, .025), 'IfcColumn', intent)
            obj['wet_zone_encased'] = wet_zone
            if not wet_zone:
                grain_uv(obj)
        for a, b in [(FRAME_POST_X[0], RIDGE_X), (RIDGE_X, FRAME_POST_X[1])]:
            timber('Pavilion exposed driftwood sloping rafter',
                   (a, y, pavilion_roof_height(a) - VAULT_ASSEMBLY_DEPTH - frame_offset),
                   (b, y, pavilion_roof_height(b) - VAULT_ASSEMBLY_DEPTH - frame_offset), FRAME_WIDTH, FRAME_DEPTH)
    timber('Pavilion exposed driftwood ridge beam', (RIDGE_X, 20, PAVILION_RIDGE - VAULT_ASSEMBLY_DEPTH - RIDGE_BEAM_DEPTH / 2),
           (RIDGE_X, 40, PAVILION_RIDGE - VAULT_ASSEMBLY_DEPTH - RIDGE_BEAM_DEPTH / 2), RIDGE_BEAM_WIDTH, RIDGE_BEAM_DEPTH)

    # Roof-to-wall counterflashings follow the lower roofs. No hidden valleys.
    classify(box('Front wing pavilion wall flashing', (22, 19.93, 13.20), (44, .06, .50), metal, .004), 'IfcMember')
    classify(box('Kitchen wing pavilion wall flashing', (44.08, 30, 13.20), (.06, 20, .50), metal, .004), 'IfcMember')
    classify(beam('Lower wings step counterflashing', (44, 20.12, 13.18),
                  (70, 20.12, kitchen_roof_height(70) + .18), .05, .40, metal), 'IfcMember')

    def gutter(name, a, b, cross_axis):
        # a,b mark bottom-center elevations; each run has explicit positive fall.
        for offset in (-.16, .16):
            aa, bb = list(a), list(b)
            aa[cross_axis] += offset; bb[cross_axis] += offset
            aa[2] += .13; bb[2] += .13
            classify(beam(name + ' upstand', aa, bb, .025, .26, metal), 'IfcFlowSegment')
        classify(beam(name + ' base', a, b, .32, .025, metal), 'IfcFlowSegment')

    def downpipe(name, x, y, top):
        classify(rod(name, (x, y, top), (x, y, .08), .065, metal), 'IfcFlowSegment')
        classify(rod(name + ' conceptual buried conveyance', (x, y, -.28), (x + (8 if x > 34 else -8), y, -.28), .10, metal), 'IfcFlowSegment')
        box(name + ' inspection grate', (x, y, -.005), (.60, .60, .04), M['dark'], .01)

    # Pavilion gutters fall rearward so there are no downpipes through rooms.
    for x in (-3.17, 47.17):
        top = pavilion_roof_height(-3) - .29
        rear = top - 25 / 192
        gutter('Pavilion external side gutter', (x, 18, top), (x, 43, rear), 0)
        downpipe('Pavilion rainwater downpipe', x, 43, rear)
    for edge in (-2, 70):
        top = front_roof_height(-3.75) - .29
        end = top - 36 / 192
        gutter('Front wing external gutter', (34, -3.91, top), (edge, -3.91, end), 1)
        downpipe('Front wing rainwater downpipe', edge, -3.91, end)
    top = kitchen_roof_height(71) - .29
    rear = top - 23 / 192
    gutter('Kitchen wing east gutter', (71.17, 20, top), (71.17, 43, rear), 0)
    downpipe('Kitchen wing rainwater downpipe', 71.17, 43, rear)


def verify_geometry(scene):
    """Check saved actual geometry without claiming structural performance."""
    from mathutils import Vector
    F = .3048

    def bounds(obj):
        pts = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
        return [min(p[a] for p in pts) / F for a in range(3)] + [max(p[a] for p in pts) / F for a in range(3)]

    objects = scene.objects
    west = bounds(objects['Pavilion west 3 in 12 roof'])
    east = bounds(objects['Pavilion east 3 in 12 roof'])
    assert abs(west[5] - PAVILION_RIDGE) < .01 and abs(east[5] - PAVILION_RIDGE) < .01
    for name, func, axis in [('Pavilion west 3 in 12 roof', pavilion_roof_height, 0),
                             ('Pavilion east 3 in 12 roof', pavilion_roof_height, 0),
                             ('Front wing 1 in 12 roof', front_roof_height, 1),
                             ('Kitchen wing 1 in 12 roof', kitchen_roof_height, 0)]:
        obj = objects[name]
        pts = [obj.matrix_world @ vertex.co / F for vertex in obj.data.vertices]
        assert all(min(abs(p.z - func(p[axis])), abs(p.z - func(p[axis]) + ROOF_SKIN_THICKNESS)) < .01 for p in pts), name
    flat = objects[FLAT_CEILING_NAME]
    # Inspect actual horizontal ceiling polygons: no old flat sheet across vault.
    for face in flat.data.polygons:
        if abs(face.normal.z) < .9:
            continue
        center = flat.matrix_world @ face.center / F
        assert not is_vault(center.x, center.y), ('flat ceiling covers vault', tuple(center))
    for name in (WEST_CEILING_NAME, EAST_CEILING_NAME):
        obj = objects[name]
        assert bounds(obj)[5] > 18
        assert any(abs(face.normal.x) > .2 and abs(face.normal.z) > .9 for face in obj.data.polygons), 'vault must actually slope'
    glazing = [o for o in objects if o.name.startswith(UPPER_GLAZING_PREFIX)]
    assert len(glazing) == 13 and all(o.get('ifc_class') == 'IfcWindow' for o in glazing)
    assert min(bounds(o)[2] for o in glazing) > 11 and max(bounds(o)[5] for o in glazing) > 18
    rafters = [o for o in objects if o.name.startswith('Pavilion exposed driftwood sloping rafter')]
    posts = [o for o in objects if o.name.startswith(('Pavilion driftwood structural frame post', 'Pavilion encased wet-zone structural frame post'))]
    assert len(rafters) == 6 and len(posts) == 6
    public_posts = [o for o in posts if not o.get('wet_zone_encased')]
    wet_posts = [o for o in posts if o.get('wet_zone_encased')]
    assert len(public_posts) == 5 and len(wet_posts) == 1
    assert all(o.data.materials[0] == objects['Verandah timber column'].data.materials[0] for o in rafters + public_posts)
    assert wet_posts[0].data.materials[0] != objects['Verandah timber column'].data.materials[0], 'wet-zone post must be encased, not exposed wood'
    for post in posts:
        pb = bounds(post)
        assert abs(pb[2]) < .01, 'frame post must bear at the floor datum'
        matching = [bounds(r) for r in rafters if abs((bounds(r)[1] + bounds(r)[4]) / 2 - (pb[1] + pb[4]) / 2) < .01
                    and min(bounds(r)[3], pb[3]) > max(bounds(r)[0], pb[0])]
        assert any(abs(pb[5] - rb[2]) < .03 for rb in matching), ('frame post does not meet rafter foot', post.name)
    ridge = objects['Pavilion exposed driftwood ridge beam']
    assert ridge.data.materials[0] == objects['Verandah timber column'].data.materials[0]
    assert abs(bounds(ridge)[5] - (PAVILION_RIDGE - VAULT_ASSEMBLY_DEPTH)) < .01
    downpipes = [o for o in objects if o.name in ('Pavilion rainwater downpipe', 'Pavilion rainwater downpipe.001',
                 'Front wing rainwater downpipe', 'Front wing rainwater downpipe.001', 'Kitchen wing rainwater downpipe')]
    assert len(downpipes) == 5
    return {'design': metadata(), 'actual_roof_planes': 4, 'upper_glazing_panels': len(glazing),
            'exposed_sloping_rafters': len(rafters), 'side_frame_posts': len(posts),
            'stone_encased_wet_zone_posts': len(wet_posts),
            'actual_frame_post_to_rafter_contact_checked': True,
            'actual_ceiling_slopes_checked': True, 'no_flat_ceiling_across_vault': True,
            'same_timber_as_pergola': True, 'modeled_roof_downpipes': len(downpipes),
            'limits': 'Geometry and material checks only; no structural, roof-product, flashing, drainage-capacity or local approval.'}
