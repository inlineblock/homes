"""Complete furnished Atrium01 program; meter-native pinned library placement."""
import math
import design as d
import kitchen
F=d.FT


def build(root, M, asset, box, rod, cyl, area):
    from api import host_footprint
    result={'kitchen':kitchen.build(root,M,asset,box,rod,cyl,area),
            'bedrooms':[], 'bathrooms':[], 'storage':[], 'ceiling_cutouts':[]}

    def put(cat,slug,name,x,y,z=0,rotation=0):
        return asset(cat,slug,name,(x*F,y*F,z),math.radians(rotation))

    def stone(name,x0,y0,x1,y1,top=.750):
        box(name,((x0+x1)/2*F,(y0+y1)/2*F,top-.015),((x1-x0)*F,(y1-y0)*F,.03),M['stone'])
        host_footprint(name,[(x0*F,y0*F),(x1*F,y0*F),(x1*F,y1*F),(x0*F,y1*F)],'vanity')

    def vanity(name,x,y,rotation=0):
        put('cabinetry','walnut-vanity-base-24in',name+' cabinet',x,y,rotation=rotation)
        theta=math.radians(rotation)
        # Fixture mirror back +.3475m minus the42.7mm mounting offset aligns
        # exactly with the cabinet's304.8mm rear mounting plane.
        sx=x*F+.0427*math.sin(theta);sy=y*F-.0427*math.cos(theta)
        asset('fixtures','vanity-basin-mixer-mirror',name+' basin and mirror',(sx,sy,.75),theta)
        # Cabinet fronts stay at their real scale; basin waste needs an actual
        # clearance through the top rather than a solid slab under the drain.
        r=.045; a=.324;b=.325
        # Four simple pieces frame a90mmsquare service opening around the drain.
        for xa,xb,ya,yb in [(-a,-r,-b,b),(r,a,-b,b),(-r,r,-b,-r),(-r,r,r,b)]:
            cx=(xa+xb)/2;cy=(ya+yb)/2-.0427
            ob=box(name+' stone worktop',(x*F+cx*math.cos(theta)-cy*math.sin(theta),
                y*F+cx*math.sin(theta)+cy*math.cos(theta),.735),(xb-xa,yb-ya,.03),M['stone'])
            ob.rotation_euler.z=theta
        corners=[]
        for xx,yy in [(-a,-b-.0427),(a,-b-.0427),(a,b-.0427),(-a,b-.0427)]:
            corners.append((x*F+xx*math.cos(theta)-yy*math.sin(theta),y*F+xx*math.sin(theta)+yy*math.cos(theta)))
        host_footprint(name+' stone worktop',corners,'vanity')
        return {'name':name,'counter_top_m':.75,'basin_origin_m':[sx,sy,.75],
                'rotation_degrees':rotation,'drain_opening_m':.09}

    # Bedrooms keep actual queen/king sizes. The primary headboard meets the
    # solid bathroom wall, leaving north/west garden glazing unobstructed.
    for number,cy in [(2,5.5),(3,19.5)]:
        put('furniture','oak-linen-queen-bed',f'Bedroom {number} queen bed',6.5,cy)
        for x in [2.60,10.40]:
            put('furniture','oak-open-nightstand',f'Bedroom {number} bedside table',x,cy-3.2,rotation=180)
        wy=9.25 if number==2 else 23.25
        for x in [14.3,16.4,18.5]:
            put('cabinetry','walnut-wardrobe-2ft',f'Bedroom {number} wardrobe',x,wy,rotation=180)
        result['bedrooms'].append({'bedroom':number,'bed':'queen','wardrobe_bays':3,
            'wardrobe_origin_y_m':wy*F,'nominal_storage_width_m':6*F,
            'wardrobe_front_clear_m':(14.2 if number==2 else 28.2)*F-.175*F-(wy*F+.3334512),
            'usable_rail_note':'Six feet nominal bay frontage; actual internal rails exclude shared side panels.'})
    put('furniture','oak-linen-king-bed','Primary king bed',9.65,37.7,rotation=90)
    for y in [33.25,42.15]:
        put('furniture','oak-open-nightstand','Primary bedside table',11.8,y,rotation=-90)
    for x in [1.6,3.7,5.8,7.9]:
        put('cabinetry','walnut-wardrobe-2ft','Primary wardrobe',x,29.45,rotation=180)
    result['bedrooms'].append({'bedroom':'primary','bed':'king','wardrobe_bays':4,
        'nominal_storage_width_m':8*F,'wardrobe_front_clear_m':37.7*F-1.06426-(29.45*F+.3334512),
        'headboard':'Faces solid east bathroom wall; garden glazing remains alongside bed.'})
    # A useful quiet work corner is included in bedroom03 without obstructing its
    # bed-to-wardrobe path; the full-size desk is never compressed to fit.
    put('furniture','oak-writing-desk','Bedroom 3 quiet desk',1.80,25,rotation=90)
    put('furniture','oak-upholstered-dining-chair','Bedroom 3 desk chair',3.8,25,rotation=-90)

    # Secondary ensuite: south vanity, northeast shower, northwest WC. Its door
    # opens toward the sleeping room, clear of the wet fixtures.
    vanity2=vanity('Ensuite 02 vanity',14.175,1.62,90)
    put('fixtures','toilet-elongated','Ensuite 02 toilet',14.70,6.565)
    put('fixtures','shower-tray-screen-900','Ensuite 02 shower',18.28,6.34)
    result['bathrooms'].append({'name':'Ensuite 02','vanity':vanity2,
        'shower_approach':'South of tray;900mmtray original concept, no accessibility claim'})
    # Guest bath is available from the indoor cross-gallery without entering a room.
    vanity3=vanity('Shared bath vanity',26.175,6.70,90)
    put('fixtures','toilet-elongated','Shared bath toilet',28.0,1.76,rotation=180)
    put('fixtures','shower-tray-screen-900','Shared bath shower',31.25,2.00,rotation=180)
    result['bathrooms'].append({'name':'Shared bath','vanity':vanity3})

    # Primary bathing suite: dual separate storage vanities, a genuine72in bath,
    # larger1500×1200 shower with west entry, and a separately enclosed toilet.
    primary_vanities=[vanity('Primary south vanity',15.175,33.30,90),
                      vanity('Primary north vanity',15.175,36.30,90)]
    # Bridge the two cabinet tops with a fitted shallow continuous stone strip;
    # the individual drain cutouts remain open in the basin zones.
    stone('Primary vanity connecting landing',14.2,34.37,16.34,35.23)
    put('fixtures','freestanding-tub-72in','Primary separate bathtub',16.3,40.45,rotation=90)
    put('fixtures','shower-tray-screen-1500x1200','Primary generous shower',22.85,41.0,rotation=-90)
    put('fixtures','toilet-elongated','Primary enclosed toilet',23.25,36.18)
    # A one-off wall-fed bath filler is an installation extension of the wet wall,
    # not an unverified commercial fixture. The small original pipe route is
    # exposed as conceptual plumbing and explicitly recorded for product selection.
    rod('Primary bath wall filler',(14.19*F,40.1*F,.77),(15.23*F,40.1*F,.77),.018,M['steel'])
    rod('Primary bath filler outlet',(15.23*F,40.1*F,.77),(15.23*F,40.1*F,.69),.018,M['steel'])
    mixer=cyl('Primary bath mixer allowance',(14.23*F,39.65*F,.80),.038,.018,M['steel'])
    mixer.rotation_euler.y=math.pi/2
    result['bathrooms'].append({'name':'Primary','vanities':primary_vanities,
        'basin_centers_m':3*F,'shower_approach_m':(22.85-16.3-1.5)*F-.602,
        'toilet_front_clear_m':36.18*F-.376428-32.175*F,
        'bath_filler':'Bespoke conceptual wall-fed spout; commercial controls, rough-in and certification unresolved.'})

    # Dedicated laundry: both machines retain real600mm bodies and a rear service
    # gap; baskets/operators occupy the measured central area, not the entry.
    for x,label in [(14.8,'washer'),(16.87,'heat pump dryer')]:
        put('appliances','front-loading-laundry-600','Laundry '+label,x,15.65,rotation=180)
    stone('Laundry folding worktop',13.7,14.45,17.98,17.02,top=.92)
    for x in [13.73,17.95]:
        box('Laundry counter support cheek',(x*F,15.735*F,.445),(.022,2.54*F,.89),M['walnut'],.004)
    for x in [14.6,16.65]:
        put('cabinetry','walnut-pantry-shelf-2ft','Laundry linen shelves',x,21.25)
    # Wet-item hanging belongs over the folding counter, outside linen and
    # machine standing zones. Ceiling hangers preserve a usable1113mm rail.
    rod('Laundry over-counter drying rail',(14.0*F,15.9*F,1.9),(17.65*F,15.9*F,1.9),.015,M['steel'])
    for x in [14.0,17.65]:
        rod('Laundry drying rail ceiling support',(x*F,15.9*F,1.9),(x*F,15.9*F,d.SERVICE_CLEAR),.012,M['steel'])
    result['laundry']={'front_operator_and_basket_m':20.75*F-(15.65*F+.4025),
        'machine_origins_m':[[14.8*F,15.65*F,0],[16.87*F,15.65*F,0]],
        'rear_hose_clearance_m':15.65*F-.32-14.375*F,
        'drying_rail_m':{'start':[14.0*F,15.9*F,1.9],'end':[17.65*F,15.9*F,1.9],'location':'Over folding counter; ceiling supported'},
        'dryer':'Heat-pump concept; condensate route to laundry drain reserved; performance and selected installation unresolved.'}

    # Give the south end of the private gallery a purpose: dedicated cleaning and
    # linen storage, facing north and wholly below the bedroom entrance routes.
    put('cabinetry','walnut-cleaning-cabinet-2ft','Gallery cleaning and vacuum cabinet',21.35,1.50,rotation=180)
    put('cabinetry','walnut-pantry-shelf-2ft','Gallery spare bedding shelves',23.55,1.02,rotation=180)
    # Foyer coats are kept along the east wall, away from the front door and its
    # four-foot leaf sweep; two full-size bays hold coats and shoes.
    for y in [2.0,4.1]:
        put('cabinetry','walnut-wardrobe-2ft','Foyer coats and shoes',39.825,y,rotation=-90)
    put('furniture','oak-open-nightstand','Foyer keys and bag landing',39.5,6.5,rotation=-90)
    # Utility/bulk room uses shallow storage with a separate service reservation.
    for x in [50.5,52.55,54.60]:
        put('cabinetry','walnut-pantry-shelf-2ft','Utility household bulk shelves',x,1.02,rotation=180)
    for x in [50.5,52.6]:
        put('cabinetry','walnut-wardrobe-2ft','Utility seasonal hanging storage',x,6.65)
    put('cabinetry','walnut-cleaning-cabinet-2ft','Utility maintenance cupboard',54.7,6.65)
    # Transparent planning volumes are deliberately not fake HVAC/water-heater
    # products. Their existence reserves service and replacement space in the plan.
    for name,rect in [('Mechanical equipment reservation',d.box(57,1,59.4,3.6)),
                      ('Hot water equipment reservation',d.box(57,4.6,59.4,7.2))]:
        x0,y0,x1,y1=rect
        ob=box(name,((x0+x1)/2,(y0+y1)/2,.95),(x1-x0,y1-y0,1.9),M['dark'],.025)
        ob.hide_render=True;ob.display_type='WIRE';ob['concept_allowance_only']=True
        host_footprint(name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],'service-reservation')
    result['storage']=[{'role':'Bedroom clothes','modules':10,'nominal_frontage_m':20*F},
        {'role':'Entry coats and shoes','modules':2,'nominal_frontage_m':4*F},
        {'role':'Linen and spare bedding','modules':3,'nominal_shelf_depth_m':.278},
        {'role':'Cleaning and vacuum','modules':2,'asset':'cabinetry/walnut-cleaning-cabinet-2ft/v001'},
        {'role':'Bulk and seasonal storage','modules':5,'location':'Utility; independent of reserved equipment footprints'}]

    # Six-place dining and a relaxed living group; actual fixed furniture sizes
    # leave a continuous east garden route and an open connection to the kitchen.
    put('furniture','oak-dining-table-8ft','Dining table for six',33.5,36.2,rotation=90)
    for y in [33.8,36.2,38.6]:
        put('furniture','oak-upholstered-dining-chair','Dining west chair',30.3,y,rotation=90)
        put('furniture','oak-upholstered-dining-chair','Dining east chair',36.7,y,rotation=-90)
    for y in [34.5,38.0]:
        put('fixtures','opal-globe-pendant','Dining opal globe',33.5,y,d.HEIGHT)
        area('Dining warm pool',(33.5*F,y*F,2.08),(33.5*F,y*F,.76),50,.85)
    put('furniture','linen-three-seat-sofa','Living linen sofa',50.5,31.5)
    put('furniture','oak-rounded-coffee-table','Living rounded coffee table',50.5,35.9)
    for x in [46.8,54.2]:
        put('furniture','coastal-outdoor-lounge-chair','Living oak lounge chair',x,40.0,rotation=180)
    # A short walnut credenza beside the sofa separates the seating group from
    # dining without blocking the garden glass. Drawers face the generous west
    # approach; the two standard modules retain their actual operating envelopes.
    for y in [33.0,35.05]:
        put('cabinetry','walnut-drawer-base-2ft','Living walnut storage drawers',43.5,y,rotation=-90)
    box('Living credenza walnut top',(43.465*F,34.025*F,.88622),
        (2.19*F,4.17*F,.03),M['walnut'],.006)
    host_footprint('Living credenza walnut top',
        [(42.37*F,31.94*F),(44.56*F,31.94*F),(44.56*F,36.11*F),(42.37*F,36.11*F)],'storage')
    # The reading corner uses an existing companion table and ceiling-mounted
    # globe; no new floor-lamp geometry or circulation obstruction is introduced.
    put('furniture','oak-open-nightstand','Living reading side table',44.25,40.0,rotation=90)
    put('fixtures','opal-globe-pendant','Living reading globe',44.25,40.0,d.HEIGHT)
    area('Living focused reading pool',(44.25*F,40*F,2.08),(46.35*F,40*F,.85),38,.65)
    result['living']={'east_route_clear_m':(59.5-50.5)*F-1.73736,
        'dining_west_chair_back_to_wall_m':(30.3-25.175)*F-.26712,
        'living_storage':'Two linked walnut drawer bays with a continuous walnut top; fronts face west toward the dining approach.',
        'living_storage_operator_target_m':1.3,
        'living_storage_closed_front_to_dining_chair_m':(43.5-36.7)*F-.33655-.26712,
        'reading_corner':'Shared side table and opal pendant beside the west lounge chair.',
        'rug':'Large20ftlibraryrug deliberately omitted because it exceeds this19ftlivingzone; no scaled substitute.'}

    # Layered lighting: actual fixtures with explicit ceiling cutouts returned to
    # architecture. These are housing reservations, not photometric certification.
    lights=[('Entry',36.0,4.5,d.HEIGHT),('Cross gallery',29.0,10.5,d.HEIGHT),
            ('Bedroom 02',6.5,10.9,d.HEIGHT),('Bedroom 03',7.0,25.4,d.HEIGHT),
            ('Primary bedroom',7.0,35.0,d.HEIGHT),('Ensuite 02',16.5,4.3,d.SERVICE_CLEAR),
            ('Shared bath',29.2,4.8,d.SERVICE_CLEAR),('Laundry',16.5,18.7,d.SERVICE_CLEAR),
            ('Pantry',44.5,4.0,d.SERVICE_CLEAR),('Utility',56.0,4.1,d.SERVICE_CLEAR),
            ('Primary bath',19.1,36.0,d.HEIGHT),('Kitchen cleanup',55.2,18.2,d.HEIGHT),
            ('Kitchen north',55.2,25.0,d.HEIGHT),('Living east',57.8,35.8,d.HEIGHT)]
    for name,x,y,z in lights:
        put('fixtures','lighting-recessed-downlight-3in',name+' recessed light',x,y,z)
        result['ceiling_cutouts'].append({'name':name,'center_m':[x*F,y*F,z],
                                         'radius_m':.08636/2,'housing_depth_m':.096})
        area(name+' illumination',(x*F,y*F,z-.045),(x*F,y*F,0),45,.9)
    return result
