"""Coastal pavilion roof design in feet; pure data shared by plan and lighting.

All levels are concept dimensions, not engineered sections or product minima.
"""
import math

PAVILION = (0., 20., 44., 40.)  # x1,y1,x2,y2 at building walls
RIDGE_X = 22.
PAVILION_PITCH = 3 / 12
PAVILION_BEARING = 14.5
PAVILION_RIDGE = 20.
PAVILION_ROOF_BOUNDS = (-3., 18., 47., 43.)
ROOF_SKIN_THICKNESS = .28
VAULT_ASSEMBLY_DEPTH = .70
FLAT_CEILING = 10.45
CEILING_THICKNESS = .08
FRONT_ROOF_BOUNDS = (-2., -3.75, 70., 20.)
KITCHEN_ROOF_BOUNDS = (44., 20., 71., 43.)
LOW_WING_HIGH = 13.
LOW_WING_PITCH = 1 / 12
VAULT_RECTS = ((0., 26., 18., 40.), (18., 20., 44., 40.))
FLAT_RECTS = ((0., 0., 68., 20.), (0., 20., 18., 26.), (44., 20., 68., 40.))
FRAME_Y = (20.5, 32., 39.5)
FRAME_WIDTH = .48
FRAME_DEPTH = .75
FRAME_POST_X = (.45, 43.55)
FRAME_POST_WIDTH = .60
RIDGE_BEAM_WIDTH = .60
RIDGE_BEAM_DEPTH = .90
FLAT_CEILING_NAME = 'Continuous warm white ceiling'
WEST_CEILING_NAME = 'Pavilion west sloping ceiling'
EAST_CEILING_NAME = 'Pavilion east sloping ceiling'
UPPER_GLAZING_PREFIX = 'Pavilion real upper glazing'


def is_vault(x, y):
    return any(x1 <= x <= x2 and y1 <= y <= y2 for x1, y1, x2, y2 in VAULT_RECTS)


def pavilion_roof_height(x):
    return PAVILION_RIDGE - abs(x - RIDGE_X) * PAVILION_PITCH


def ceiling_height(x, y):
    """Actual visible underside in feet, including the genuine vault."""
    return pavilion_roof_height(x) - VAULT_ASSEMBLY_DEPTH if is_vault(x, y) else FLAT_CEILING


def ceiling_slope(x, y):
    """dz/dx, dz/dy for the visible ceiling; flat regions return zero."""
    if not is_vault(x, y):
        return (0., 0.)
    return (PAVILION_PITCH if x < RIDGE_X else -PAVILION_PITCH, 0.)


def ceiling_normal(x, y):
    """Upward unit normal: align a ceiling-mounted fixture's local +Z here."""
    sx, sy = ceiling_slope(x, y)
    length = math.sqrt(1 + sx * sx + sy * sy)
    return (-sx / length, -sy / length, 1 / length)


def ceiling_mesh_name(x, y):
    if not is_vault(x, y):
        return FLAT_CEILING_NAME
    return WEST_CEILING_NAME if x < RIDGE_X else EAST_CEILING_NAME


def ceiling_surface(x, y):
    return ceiling_height(x, y), ceiling_normal(x, y), ceiling_mesh_name(x, y)


def front_roof_height(y):
    return LOW_WING_HIGH - (20. - y) * LOW_WING_PITCH


def kitchen_roof_height(x):
    return LOW_WING_HIGH - (x - 44.) * LOW_WING_PITCH


def near_exposed_frame(x, y, clearance=.20):
    return is_vault(x, y) and (abs(x - RIDGE_X) < .30 + clearance or
                              any(abs(y - frame_y) < FRAME_WIDTH / 2 + clearance for frame_y in FRAME_Y))


def metadata():
    return {'main_pavilion': {'wall_bounds_ft': list(PAVILION), 'pitch': '3:12',
            'bearing_ft': PAVILION_BEARING, 'ridge_ft': PAVILION_RIDGE,
            'ridge_axis': 'front-to-rear at x=22 ft', 'roof_bounds_ft': list(PAVILION_ROOF_BOUNDS)},
            'lower_wings': {'pitch': '1:12', 'front_roof_bounds_ft': list(FRONT_ROOF_BOUNDS),
                            'kitchen_roof_bounds_ft': list(KITCHEN_ROOF_BOUNDS),
                            'front_drainage': 'south', 'kitchen_drainage': 'east'},
            'ceiling': {'flat_ft': FLAT_CEILING, 'vault_rectangles_ft': [list(r) for r in VAULT_RECTS],
                        'vault_underside_offset_from_roof_ft': VAULT_ASSEMBLY_DEPTH,
                        'exposed_frame_y_ft': list(FRAME_Y), 'frame_post_x_ft': list(FRAME_POST_X),
                        'rafter_width_depth_ft': [FRAME_WIDTH, FRAME_DEPTH],
                        'ridge_beam_width_depth_ft': [RIDGE_BEAM_WIDTH, RIDGE_BEAM_DEPTH]},
            'roof_skin_thickness_ft': ROOF_SKIN_THICKNESS,
            'drainage': {'high_pavilion': 'Side gutters fall rearward to external downpipes; no valley into lower wings',
                         'downpipe_xy_ft': [[-3.17, 43], [47.17, 43], [-2, -3.91], [70, -3.91], [71.17, 43]],
                         'roof_steps': 'Flashed vertical abutments and a front/kitchen roof-step riser'},
            'limits': 'Original concept geometry. Roof assemblies, spans, uplift, connections, condensation control and drainage capacity are unengineered.'}


def roof_metadata():
    return metadata()
