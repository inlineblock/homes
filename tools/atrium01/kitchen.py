"""Measured walnut kitchen, using rigid, pinned shared equipment collections.

All native coordinates are meters. One-off counters and installation fillers are
host geometry; cabinets, appliances, tile, stools and lighting stay linked.
"""
import math
import design as d

F = d.FT
TOP = .9144
TOP_THICK = .0381


def build(root, M, asset, box, rod, cyl, area):
    from api import host_footprint
    records = {'equipment': [], 'clearances': [], 'counter_openings': []}

    def put(cat, slug, name, x, y, z=0, rotation=0, version='v001'):
        ob = asset(cat, slug, name, (x*F, y*F, z), math.radians(rotation), version)
        if cat == 'appliances' or 'sink' in slug:
            records['equipment'].append({'name': name, 'asset': f'{cat}/{slug}/{version}',
                                         'origin_m': [x*F,y*F,z], 'rotation_degrees': rotation})
        return ob

    def top(name, rect, holes=(), z=TOP, thickness=TOP_THICK):
        """Partition a rectangular slab around actual rectangular installation holes."""
        x0,y0,x1,y1 = rect
        xs = sorted(set([x0,x1]+[v for h in holes for v in [h[0],h[2]]]))
        ys = sorted(set([y0,y1]+[v for h in holes for v in [h[1],h[3]]]))
        for a,b in zip(xs,xs[1:]):
            for c,e in zip(ys,ys[1:]):
                if any(h[0] < (a+b)/2 < h[2] and h[1] < (c+e)/2 < h[3] for h in holes):
                    continue
                box(name,((a+b)/2,(c+e)/2,z-thickness/2),(b-a,e-c,thickness),M['stone'])
        host_footprint(name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],'counter')
        for h in holes:
            records['counter_openings'].append({'counter': name, 'bounds_m': list(h), 'top_m': z})

    # South cooking wall. Pantry access remains west of the first cabinet.
    for x in [47.75,52.75]:
        put('cabinetry','walnut-drawer-base-2ft','Kitchen cooking landing drawers',x,9.4,rotation=180)
    put('cabinetry','walnut-oven-base-36in','Kitchen open oven housing',50.25,9.4,rotation=180)
    put('appliances','built-in-oven-30in','Kitchen oven 30 inch',50.25,9.4,.14,180)
    cook_x,cook_y=50.25*F,9.4*F
    cook_hole=(cook_x-.44,cook_y-.2475,cook_x+.44,cook_y+.2475)
    top('Kitchen cooking worktop',d.box(46.74,8.32,53.85,10.65),[cook_hole])
    put('appliances','induction-cooktop-36in','Kitchen induction 36 inch',50.25,9.4,TOP,180)
    put('appliances','wall-hood-36in','Kitchen extraction hood 36 inch',50.25,9.25,1.70,180)
    # A continuous hollow duct connects the hood chimney to an open-sided cowl.
    # The architecture module cuts the actual340×300mm roof/ceiling bore around
    # this320×280mm outer envelope. Flow, fire protection and product sizing are
    # unresolved engineering decisions, not inferred from the visual route.
    ex,ey=50.25*F,8.78*F
    duct_bottom,duct_top,wall=2.455,3.66,.003
    for side,xoff,yoff,wid,dep in [('west',-.16+wall/2,0,wall,.28),
                                 ('east',.16-wall/2,0,wall,.28),
                                 ('south',0,-.14+wall/2,.32-2*wall,wall),
                                 ('north',0,.14-wall/2,.32-2*wall,wall)]:
        ob=box('Kitchen dedicated exhaust duct '+side,(ex+xoff,ey+yoff,(duct_bottom+duct_top)/2),
               (wid,dep,duct_top-duct_bottom),M['steel'])
        ob['concept_system_role']='continuous_kitchen_exhaust_duct'
    # Four flashing strips form a genuine central opening instead of a sealed box.
    for side,xoff,yoff,wid,dep in [('west',-.206,0,.088,.47),('east',.206,0,.088,.47),
                                 ('south',0,-.1885,.324,.093),('north',0,.1885,.324,.093)]:
        box('Kitchen exhaust flashing '+side,(ex+xoff,ey+yoff,3.58),(wid,dep,.018),M['dark'])
    for dx in [-.222,.222]:
        for dy in [-.207,.207]:
            box('Kitchen exhaust cowl corner support',(ex+dx,ey+dy,3.68075),(.018,.018,.1835),M['dark'],.002)
    box('Kitchen roof exhaust rain cap',(ex,ey,3.79),(.52,.49,.035),M['dark'],.008)
    records['exhaust']={
        'center_m':[ex,ey], 'roof_bore_m':[.34,.30],
        'outer_duct_rectangle_m':[ex-.16,ey-.14,ex+.16,ey+.14],
        'inner_duct_rectangle_m':[ex-.157,ey-.137,ex+.157,ey+.137],
        'continuous_duct_z_m':[duct_bottom,duct_top],
        'hood_chimney_top_m':1.70+.762,
        'hood_to_duct_overlap_m':1.70+.762-duct_bottom,
        'cowl_cap_underside_m':3.7725, 'open_side_outlet_height_m':3.7725-duct_top,
        'route':'Hood capture and chimney; continuous open-ended four-wall riser through reserved roof bore; four open lateral outlets below rain cap.',
        'status':'Modeled concept route; selected product, exhaust sizing, makeup air, flashings and weather/fire performance unresolved.'}
    area('Cooking task illumination',(50.25*F,9.25*F,1.68),(50.25*F,9.4*F,TOP),65,.75)
    # Immovable 48-inch fridge has its own landing and door-use bay.
    put('appliances','walnut-panel-ready-fridge-48in','Kitchen refrigerator freezer 48 inch',56.6,9.55,rotation=180)
    # An exposed space between cold and hot equipment gives hinge relief; no filler
    # crosses the refrigerator leaf sweep. The cooking top provides its landing.
    for x in [46.78,53.81]:
        box('Cooking counter support cheek',(x*F,9.42*F,.438),(.022,2.2*F,.876),M['walnut'],.004)

    # East cleanup run: full-size sink, dishwasher and separate waste pullout.
    east_x=58.4
    for y in [24.5,26.5]:
        put('cabinetry','walnut-drawer-base-2ft','Kitchen east drawer storage',east_x,y,rotation=-90)
    put('cabinetry','walnut-sink-base-36in',
        'Kitchen accessible sink cabinet',east_x,17.5,rotation=-90)
    put('appliances','walnut-panel-ready-dishwasher-24in','Kitchen integrated dishwasher',east_x,20.05,rotation=-90)
    put('cabinetry','walnut-waste-pullout-18in','Kitchen waste and recycling',east_x,21.90,rotation=-90)
    # Nominal sink mounting offset is30mm toward the cabinet front.
    sink_x=east_x*F-.03; sink_y=17.5*F
    sink_hole=(sink_x-.232,sink_y-.332,sink_x+.232,sink_y+.332)
    top('Kitchen cleanup worktop',d.box(57.3,15.85,59.48,27.6),[sink_hole])
    asset('fixtures','kitchen-sink-mixer-650','Kitchen real bowl and mixer',(sink_x,sink_y,TOP),-math.pi/2,'v002')
    records['equipment'].append({'name':'Kitchen real bowl and mixer','asset':'fixtures/kitchen-sink-mixer-650/v002','origin_m':[sink_x,sink_y,TOP],'rotation_degrees':-90})
    for y in [15.90,27.57]:
        box('Cleanup counter end support',(58.4*F,y*F,.438),(2.1*F,.022,.876),M['walnut'],.004)
    # Small installation gaps remain visible as deliberate walnut filler panels.
    for y,w in [(21.10,.05),(23.125,.75)]:
        box('Cleanup run fitted spacer',(58.4*F,y*F,.436),(2*F,w*F,.872),M['walnut'],.003)

    # A single coherent field reaches the refrigerator's2.134m top datum.
    # Whole original3×12in tiles remain rigidly linked. Four rows terminate at
    #2.131m; equal18mm plaster reveals finish the two worktop ends.
    tile_top=TOP+.301752+3*.3048
    box('Sage ceramic backing bed',(50.295*F,8.2075*F,(TOP+tile_top)/2),
        (7.11*F,.065*F,tile_top-TOP),M['plaster'])
    for row in range(4):
        for col in range(28):
            put('materials','sage-fluted-tile','Sage fluted cooking tile',46.92+col*.25,8.25,TOP+.150876+row*.3048)
    # The hood sits forward of the ceramic face instead of intersecting tiles.
    # Two installation stand-offs connect its chimney to wall backing; appliance
    # fixings, loads and the selected commercial installation remain unresolved.
    for x in [49.9,50.6]:
        box('Hood concealed mounting stand-off',(x*F,8.26*F,2.31),(.035,.17*F,.12),M['steel'],.003)

    # Four working-side cabinet modules leave a generous15-inch-plus knee recess.
    ix0,iy0,ix1,iy1=d.KITCHEN_ISLAND
    cab_x=ix1-.36
    for i in range(4):
        cy=iy0+(.5+i*2+1)*F
        asset('cabinetry','walnut-drawer-base-2ft','Island working drawers',(cab_x,cy,0),math.pi/2)
    top('Island pale stone worktop',d.KITCHEN_ISLAND)
    # Site-specific continuous rear/end panels are the island host, not new cabinets.
    box('Island walnut back',(cab_x-.325,(iy0+iy1)/2,.436),(.027,iy1-iy0-.10,.872),M['walnut'],.006)
    for yy in [iy0+.05,iy1-.05]:
        box('Island fitted walnut end',(cab_x,yy,.436),(.66,.028,.872),M['walnut'],.005)
    for i in range(4):
        # The historic shared stool's bent back is at-X; its original orientation
        # already faces the island from its west side.
        sy=iy0+(.5+i*2.5+.75)*F
        asset('furniture','walnut-counter-stool','Courtyard facing walnut counter seat',(ix0-1.2*F,sy,0))
    for yy in [iy0+2*F,(iy0+iy1)/2,iy1-2*F]:
        asset('fixtures','opal-globe-pendant','Island opal globe',( (ix0+ix1)/2,yy,d.HEIGHT))
        area('Island warm task pool',((ix0+ix1)/2,yy,2.08),((ix0+ix1)/2,yy,TOP),55,.85)

    # The pantry L keeps its southwest corner open so each shelf has its own
    # standing approach; three full two-foot bays retain useful dry-food capacity.
    for x in [44.55]:
        put('cabinetry','walnut-pantry-shelf-2ft','Pantry dry food shelves',x,1.02,rotation=180)
    for y in [3.0,5.05]:
        put('cabinetry','walnut-pantry-shelf-2ft','Pantry west food shelves',41.74,y,rotation=90)
    # A separate landing supports deep portable appliances; pantry shelves are not
    # falsely counted as full-depth appliance counters.
    put('cabinetry','walnut-drawer-base-2ft','Pantry small appliance drawers',47.55,1.50,rotation=180)
    top('Pantry appliance landing',d.box(46.48,.52,48.63,2.62))

    records['clearances']=[
        {'name':'East working aisle','measured_m':57.3*F-ix1,'basis':'Stone edge to island stone; closed fixtures'},
        {'name':'Oven full door plus operator','measured_m':iy0-10.65*F,'required_m':1.52,'basis':'Concept0.72m open leaf plus0.8m operator'},
        {'name':'West route behind stools','measured_m':ix0-1.2*F-.75*F-41*F,'required_m':1.1176,'basis':'Stool conservative back envelope to courtyard glazing'},
        {'name':'Island seating width per place','measured_m':2.5*F,'required_m':.6096,'basis':'Four fixed place centers'},
        {'name':'Island knee depth','measured_m':cab_x-.338-ix0,'required_m':.381,'basis':'Stone edge to rear panel face'},
    ]
    records['sage_wall']={'tile_top_m':tile_top,'rows':4,'columns':28,'hood_rear_plane_m':(9.25-11/12)*F,'tile_front_plane_m':8.287*F,'minimum_hood_to_tile_m':(9.25-11/12-8.287)*F,'basis':'Original tile collection and measured hood rear plane; mounting stand-offs above tile field.'}
    records['sink_cutout_m']=[.464,.664]
    records['sink_service']={'cabinet_open_cavity':True,'drain_trap_routes':'Reserved within linked open sink base; product rough-in unresolved'}
    records['refrigerator_operation']={'origin_m':[56.6*F,9.55*F,0],'rotation_degrees':180,
        'leaf_angle_degrees':110,'basis':'Published concept swept geometry; verify native host before acceptance'}
    return records
