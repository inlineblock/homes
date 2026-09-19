"""Site-specific Coastal shade structures; feet, not engineered assemblies.

Constants are importable by drawings/checks without importing Blender.
The attached pergola supplies slatted shade, not a waterproof roof.
Its ledger connects to a structural header in concept, never cladding alone.
"""

PERGOLA_BOUNDS = (9.0, 41.0, 40.85, 56.0)
PERGOLA_POSTS = ((9.0, 56.0), (41.0, 56.0))
PERGOLA_POST_WIDTH = .60
PERGOLA_BEAM_BOTTOM = 8.55
PERGOLA_BEAM_TOP = 10.05
PERGOLA_LEDGER_BOTTOM = 9.65
PERGOLA_LEDGER_TOP = 10.05
PERGOLA_LEDGER_DEPTH = .50
PERGOLA_SLAT_TOP = 10.25
PERGOLA_SLAT_COUNT = 45
SCREEN_X = -1.40
SCREEN_Y = (45.0, 56.0)
SCREEN_HEIGHT = 3.80
ENTRY_CANOPY_BOUNDS = (16.0, 28.0, -7.0, 2.0)
ENTRY_CANOPY_POSTS = ((16.45, -6.45), (27.55, -6.45))


def build(M):
    from common.geometry import box, collection
    from common.timber_materials import grain_uv

    collection('14 Verandah | supported timber shade and low side screen')
    wood = M['accent_oak']

    def timber(name, center, size, ifc_class='IfcBeam'):
        obj = box(name, center, size, wood, .025)
        obj['ifc_class'] = ifc_class
        obj['design_status'] = 'Concept geometry; structural connections and sizing unresolved'
        grain_uv(obj)
        return obj

    x1, x2, y1, y2 = PERGOLA_BOUNDS
    # Only two seaward supports: the house edge is carried by its header ledger.
    for x, y in PERGOLA_POSTS:
        shoe = box('Verandah bronze column shoe', (x, y, .20), (.70, .70, .40), M['bronze'], .015)
        shoe['ifc_class'] = 'IfcPlate'
        timber('Verandah timber column', (x, y, (.18 + PERGOLA_BEAM_BOTTOM) / 2),
               (PERGOLA_POST_WIDTH, PERGOLA_POST_WIDTH, PERGOLA_BEAM_BOTTOM - .18), 'IfcColumn')
    outer = timber('Verandah timber-clad steel outer beam',
                   ((x1 + x2) / 2, y2, (PERGOLA_BEAM_BOTTOM + PERGOLA_BEAM_TOP) / 2),
                   (x2 - x1 + .9, .60, PERGOLA_BEAM_TOP - PERGOLA_BEAM_BOTTOM))
    outer['assembly_intent'] = 'Timber-clad steel concept beam, 18 inch overall depth; steel section and span unengineered'
    ledger = timber('Verandah attached structural header ledger',
                    ((x1 + x2) / 2, y1, (PERGOLA_LEDGER_BOTTOM + PERGOLA_LEDGER_TOP) / 2),
                    (x2 - x1 + .9, PERGOLA_LEDGER_DEPTH, PERGOLA_LEDGER_TOP - PERGOLA_LEDGER_BOTTOM))
    ledger['attachment_intent'] = 'Connect to structural header above slider, not facade cladding; fixing and load path require engineering'
    for x in (x1, x2):
        timber('Verandah side beam', (x, (y1 + y2) / 2, (PERGOLA_LEDGER_BOTTOM + PERGOLA_BEAM_TOP) / 2),
               (.60, y2 - y1, PERGOLA_BEAM_TOP - PERGOLA_LEDGER_BOTTOM))
    # Open slats span from ledger to outer beam, below the existing roof soffit.
    for i in range(PERGOLA_SLAT_COUNT):
        x = x1 + i * (x2 - x1) / (PERGOLA_SLAT_COUNT - 1)
        obj = timber('Verandah open shade slat', (x, (y1 + y2) / 2 + .05, (PERGOLA_BEAM_TOP + PERGOLA_SLAT_TOP) / 2),
                     (.40, y2 - y1 + .5, PERGOLA_SLAT_TOP - PERGOLA_BEAM_TOP), 'IfcMember')
        obj['weather_protection'] = 'Open slatted shade only; not rainproof'

    # A low side edge behind the lounge, never in front of the rear glazing.
    for y in (SCREEN_Y[0], (SCREEN_Y[0] + SCREEN_Y[1]) / 2, SCREEN_Y[1]):
        timber('Verandah low screen post', (SCREEN_X, y, SCREEN_HEIGHT / 2), (.24, .24, SCREEN_HEIGHT), 'IfcMember')
        shoe = box('Verandah screen shoe', (SCREEN_X, y, .12), (.30, .30, .24), M['bronze'], .008)
        shoe['ifc_class'] = 'IfcPlate'
    for i in range(9):
        timber('Verandah low horizontal screen batten', (SCREEN_X, sum(SCREEN_Y) / 2, .35 + i * .40),
               (.18, SCREEN_Y[1] - SCREEN_Y[0], .24), 'IfcMember')
