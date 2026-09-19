"""Quiet large limestone courses using a shared panel and explicit edge cuts."""
import bpy
from mathutils import Vector
from common.geometry import F, move
from common.library import linked_collection, instance

PANEL_ID = 'surfaces/honed-limestone-wall-panel-4x2'
PIERS = ((0., 4.5), (40.3, 47.7), (63.4, 68.))
JOINT = .025


def build(root):
    panel = linked_collection(root, 'surfaces', 'honed-limestone-wall-panel-4x2', 'v001')
    source = next(o for o in panel.all_objects if o.type == 'MESH')
    whole, cuts = 0, 0
    for a, b in PIERS:
        width = b - a
        for row in range(6):
            bottom = .02 + row * (2 + JOINT)
            height = min(2., 10.48 - bottom)
            # Broad balanced cuts at narrow piers; never leave a thin sliver.
            first = 4. if width > 6 else (width - JOINT) / 2 + (.35 if row % 2 else -.35)
            widths = [first, width - JOINT - first]
            if row % 2: widths.reverse()
            start = a
            for w in widths:
                center = start + w / 2
                if abs(w - 4) < .001 and abs(height - 2) < .001:
                    obj = instance('Shared limestone facade full panel', panel, (center, 40.63, bottom))
                    whole += 1
                else:
                    # Trim copies of actual published mesh, with no object scale
                    # or shader stretching. Full module remains immutable.
                    obj = source.copy(); obj.data = source.data.copy()
                    obj.name = 'Limestone facade bespoke perimeter cut'
                    for v in obj.data.vertices:
                        point = source.matrix_world @ v.co
                        point.x = max(-w * F / 2, min(w * F / 2, point.x))
                        point.z = max(0., min(height * F, point.z))
                        v.co = point
                    obj.matrix_world.identity()
                    obj.location = Vector((center, 40.63, bottom)) * F
                    bpy.context.scene.collection.objects.link(obj); move(obj)
                    obj['cut_from_asset'] = PANEL_ID + '@v001'
                    obj['cut_size_ft'] = [w, .125, height]
                    cuts += 1
                obj['ifc_class'] = 'IfcCovering'
                obj['installation_status'] = 'Concept stone facing; anchors, cavity and waterproofing unengineered'
                start += w + JOINT
    return {'asset': PANEL_ID, 'version': 'v001', 'full_linked_panels': whole,
            'bespoke_edge_cuts': cuts, 'nominal_course_height_ft': 2., 'joint_ft': JOINT}
