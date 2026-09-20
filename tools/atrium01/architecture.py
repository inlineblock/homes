"""Metric enclosure and illustrative landscape for the sheltered courtyard ring.

The glazing is bespoke post-and-beam infill coordinated to this home's openings;
plants, pavers and hardware are immutable linked library collections. Roof member
depths and drainage paths are concept reservations, not engineered assemblies.
"""
import math
import random

import bpy
from common import geometry as g
import design as d

FT = 0.3048


def build(root, M, asset, box, rod, cyl):
    """Build the measured shell and site; return inspectable operating metadata."""
    height = d.HEIGHT
    beam_clear = d.BEAM_CLEAR
    service_clear = d.SERVICE_CLEAR
    door_states = []
    f = lambda value: value * FT

    def block(name, rect, bottom, top, material, bevel=.008):
        x0, y0, x1, y1 = rect
        return box(name, ((x0+x1)/2, (y0+y1)/2, (bottom+top)/2),
                   (x1-x0, y1-y0, top-bottom), material, bevel=bevel)

    def segment(name, a, b, bottom, top, thickness, material, bevel=.004):
        if top <= bottom + .001 or math.dist(a, b) <= .001:
            return None
        horizontal = abs(a[1]-b[1]) < .001
        obj = box(name, ((a[0]+b[0])/2, (a[1]+b[1])/2, (bottom+top)/2),
                  (abs(b[0]-a[0]) if horizontal else thickness,
                   thickness if horizontal else abs(b[1]-a[1]), top-bottom),
                  material, bevel=bevel)
        return obj

    def tagged(obj, kind):
        if obj:
            obj['ifc_class'] = kind
        return obj

    def pane(name, a, b, sill, head, offset=0):
        """One closed framed light. Glass stays inside its frame."""
        length = math.dist(a, b)
        ux, uy = (b[0]-a[0])/length, (b[1]-a[1])/length
        nx, ny = -uy, ux
        p = (a[0]+nx*offset, a[1]+ny*offset)
        q = (b[0]+nx*offset, b[1]+ny*offset)
        frame = .042
        for point in (p, q):
            tagged(box(name+' jamb', (point[0], point[1], (sill+head)/2),
                       (.055, .055, head-sill), M['dark'], bevel=.003), 'IfcMember')
        for z in (sill+frame/2, head-frame/2):
            segment(name+' rail', p, q, z-frame/2, z+frame/2, .055, M['dark'])
        pa = (p[0]+ux*frame, p[1]+uy*frame)
        pb = (q[0]-ux*frame, q[1]-uy*frame)
        tagged(segment(name+' glass', pa, pb, sill+frame, head-frame, .018, M['glass'], 0), 'IfcWindow')

    def glazing(name, a, b, sill, head):
        length = math.dist(a, b)
        count = max(1, round(length/f(4)))
        for i in range(count):
            p = (a[0]+(b[0]-a[0])*i/count, a[1]+(b[1]-a[1])*i/count)
            q = (a[0]+(b[0]-a[0])*(i+1)/count, a[1]+(b[1]-a[1])*(i+1)/count)
            pane(name+f' bay {i+1:02}', p, q, sill, head)

    def sliding_pair(name,a,b,sill,head):
        length=math.dist(a,b)
        ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
        mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
        pane(name+' fixed backing leaf',mid,b,sill,head)
        # Moving jambs need real stop clearance at both travel endpoints;
        # fixed jambs may sit at the rough-opening reveal.
        moving_a=(mid[0]+ux*.0325,mid[1]+uy*.0325)
        moving_b=(b[0]-ux*.0325,b[1]-uy*.0325)
        pane(name+' parked moving leaf',moving_a,moving_b,sill,head,offset=-.072)
        for delta in (-.035,.035):
            segment(name+' threshold track',(a[0]-uy*delta,a[1]+ux*delta),
                    (b[0]-uy*delta,b[1]+ux*delta),-.01,.012,.017,M['dark'],0)
        segment(name+' head track',a,b,head-.03,head+.015,.15,M['dark'])
        hx,hy=mid[0]+ux*.15+uy*.115,mid[1]+uy*.15-ux*.115
        rod(name+' sliding pull',(hx,hy,.95),(hx,hy,1.30),.013,M['dark'])
        door_states.append({'id':name,'type':'exterior sliding pair',
                            'modeled_state':'first half open; second half fixed and parked',
                            'clear_opening_m':length/2-.075,'track_width_m':.15,
                            'clear_start_m':[a[0]+ux*.04,a[1]+uy*.04],
                            'clear_end_m':[mid[0]-ux*.035,mid[1]-uy*.035]})

    def hinged_door(name, a, b, head, wall_thickness, entry=False, swing=90, hinge_end=False):
        length = math.dist(a, b)
        ux, uy = (b[0]-a[0])/length, (b[1]-a[1])/length
        width = length-.065
        hinge = (b[0]-ux*.035,b[1]-uy*.035) if hinge_end else (a[0]+ux*.035,a[1]+uy*.035)
        angle = math.atan2(uy, ux)+(math.pi if hinge_end else 0)
        open_angle = math.radians(70 if entry else swing)*(-1 if hinge_end else 1)
        leaf_angle = angle+open_angle
        lx, ly = math.cos(leaf_angle), math.sin(leaf_angle)
        nx, ny = -ly, lx
        leaf = box(name+' walnut door leaf',
                   (hinge[0]+lx*width/2, hinge[1]+ly*width/2, head/2),
                   (width, .045, head-.035), M['walnut'], bevel=.006)
        leaf.rotation_euler.z = leaf_angle
        leaf['ifc_class'] = 'IfcDoor'
        leaf['door_id'] = name
        leaf['hinge_x_m'], leaf['hinge_y_m'] = hinge
        leaf['leaf_width_m'] = width
        leaf['closed_rotation_rad'] = angle
        leaf['open_rotation_rad'] = leaf_angle
        leaf['modeled_state'] = f'{math.degrees(open_angle):g} degrees open'
        leaf['hinge_at_wall_end']=hinge_end
        for side in (-1, 1):
            hx, hy = hinge[0]+lx*(width-.15)+nx*.024*side, hinge[1]+ly*(width-.15)+ny*.024*side
            asset('hardware', 'door-lever-matte-black', name+f' lever {side:+}',
                  (hx, hy, 1.02), rotation=leaf_angle+(math.pi if side>0 else 0))
        for point in (a, b):
            box(name+' timber jamb', (point[0], point[1], head/2),
                (.065, .065, head), M['walnut'], bevel=.004)
        segment(name+' timber head', a, b, head-.025, head+.04,
                wall_thickness+.035, M['walnut'])
        door_states.append({'id': name, 'type': 'hinged', 'width_m': width,
                            'hinge_m': list(hinge), 'height_m': head-.035,
                            'closed_rotation_rad': angle, 'angle_degrees': math.degrees(open_angle)})

    g.collection('01 Architecture | walls and glazing')
    for name, a, b, thickness, openings in d.WALLS:
        length = math.dist(a, b)
        ux, uy = (b[0]-a[0])/length, (b[1]-a[1])/length
        point = lambda distance: (a[0]+ux*distance, a[1]+uy*distance)
        # Pre-reserve both forward and backward pockets before emitting any
        # solid wall, so a west-storing leaf never passes through an opaque wall.
        pockets=[]
        pocket_door_index=0
        for po,pw,ps,ph,pk in sorted(openings):
            if pk not in ('door','entry'):
                continue
            if d.DOOR_SWINGS.get((name,pocket_door_index),90)=='pocket':
                direction=getattr(d,'POCKET_DIRECTIONS',{}).get((name,pocket_door_index),1)
                start=po-pw-.04 if direction<0 else po+pw
                end=po if direction<0 else po+2*pw+.04
                assert start>=-.001 and end<=length+.001,(name,'pocket outside wall',start,end,length)
                pockets.append((max(0,start),min(length,end),ph))
            pocket_door_index+=1
        def solid(start,end):
            cuts=sorted({start,end,*[v for po,pe,ph in pockets for v in (po,pe) if start<v<end]})
            for left,right in zip(cuts,cuts[1:]):
                midpoint=(left+right)/2
                pocket=next((p for p in pockets if p[0]<=midpoint<=p[1]),None)
                pa,pb=point(left),point(right)
                if pocket:
                    for side in (-1,1):
                        shift=side*(thickness/2-.012)
                        sa=(pa[0]-uy*shift,pa[1]+ux*shift)
                        sb=(pb[0]-uy*shift,pb[1]+ux*shift)
                        tagged(segment(name+' pocket wall skin',sa,sb,0,height,.024,M['plaster']),'IfcWall')
                    tagged(segment(name+' pocket wall head',pa,pb,pocket[2],height,thickness,M['plaster']),'IfcWall')
                else:
                    tagged(segment(name+' solid',pa,pb,0,height,thickness,M['plaster']),'IfcWall')
        cursor = 0
        door_index = 0
        for index, (offset, width, sill, head, kind) in enumerate(sorted(openings)):
            opening_id = f'{name} opening {index+1:02}'
            if offset > cursor:
                solid(cursor,offset)
            pa, pb = point(offset), point(offset+width)
            if sill > 0:
                tagged(segment(opening_id+' sill wall', pa, pb, 0, sill,
                               thickness, M['plaster']), 'IfcWall')
            tagged(segment(opening_id+' header wall', pa, pb, head, height,
                           thickness, M['plaster']), 'IfcWall')
            if kind in ('window', 'glass'):
                glazing(opening_id, pa, pb, sill+.025, head-.015)
            elif kind == 'slider':
                sliding_pair(opening_id,pa,pb,.025,head-.015)
            elif kind in ('door', 'entry'):
                swing = d.DOOR_SWINGS.get((name,door_index),90)
                if swing == 'pocket':
                    # Pocket leaf is shown closed; adjacent wall has an actual
                    # cavity and return skins for the reserved sliding state.
                    leaf=segment(opening_id+' closed pocket leaf',pa,pb,.015,head-.025,.040,M['walnut'])
                    leaf['door_id']=opening_id
                    leaf['ifc_class']='IfcDoor'
                    leaf['modeled_state']='closed pocket door'
                    direction=getattr(d,'POCKET_DIRECTIONS',{}).get((name,door_index),1)
                    travel=direction*(width+.02)
                    leaf['pocket_travel_m']=width+.02
                    leaf['pocket_direction']=direction
                    leaf['leaf_width_m']=width
                    leaf['closed_rotation_rad']=math.atan2(uy,ux)
                    leaf['open_rotation_rad']=math.atan2(uy,ux)
                    leaf['hinge_x_m'],leaf['hinge_y_m']=pa
                    leaf['pocket_translation_m']=[ux*travel,uy*travel,0]
                    leaf['closed_location_m']=list(leaf.location)
                    # Place the finger cup at the trailing edge for either
                    # storage direction, with a real recess in the leaf.
                    pull_distance=width-.15 if direction<0 else .15
                    cutter=box('Pocket finger cup recess cutter',
                               (pa[0]+ux*pull_distance-uy*.013,pa[1]+uy*pull_distance+ux*.013,1.02),
                               (.03683,.024,.11938),None,bevel=0)
                    cutter.rotation_euler.z=math.atan2(uy,ux)
                    modifier=leaf.modifiers.new('Actual recessed finger cup pocket','BOOLEAN')
                    modifier.operation='DIFFERENCE';modifier.object=cutter
                    bpy.context.view_layer.objects.active=leaf
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
                    bpy.data.objects.remove(cutter,do_unlink=True)
                    asset('hardware','flush-pull-matte-black',opening_id+' pocket pull',
                          (pa[0]+ux*pull_distance-uy*.024,pa[1]+uy*pull_distance+ux*.024,1.02),rotation=math.atan2(uy,ux)+math.pi)
                    door_states.append({'id':opening_id,'type':'pocket','modeled_state':'closed',
                                        'width_m':width,'reserved_travel_m':width+.04,
                                        'signed_translation_m':[ux*travel,uy*travel,0]})
                else:
                    hinged_door(opening_id,pa,pb,head,thickness,kind=='entry',swing,
                                getattr(d,'DOOR_HINGES',{}).get((name,door_index),'start')=='end')
                door_index+=1
            cursor = max(cursor,offset+width)
        if cursor < length:
            solid(cursor,length)

    # Selected doors have two tracks and a real open aperture. Fixed infill is
    # separate; sliders park over one stationary leaf rather than disappearing.
    court_head = beam_clear-.04
    for name, a, b in d.COURTYARD_GLAZING:
        length=math.dist(a,b)
        ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
        point=lambda distance:(a[0]+ux*distance,a[1]+uy*distance)
        slider=d.COURTYARD_SLIDERS.get(name)
        if not slider:
            glazing(name,a,b,.025,court_head)
            continue
        offset,width=slider
        if offset>.05:
            glazing(name+' fixed approach',a,point(offset),.025,court_head)
        parked_a,parked_b=point(offset+width/2),point(offset+width)
        pane(name+' fixed backing leaf',parked_a,parked_b,.025,court_head)
        pane(name+' parked moving leaf',parked_a,parked_b,.025,court_head,offset=-.072)
        if offset+width<length-.05:
            glazing(name+' fixed end',point(offset+width),b,.025,court_head)
        p=point(offset+width/2+.15)
        rod(name+' sliding pull',(p[0]+uy*.115,p[1]-ux*.115,.95),
            (p[0]+uy*.115,p[1]-ux*.115,1.30),.013,M['dark'])
        for delta in (-.035,.035):
            p,q=point(offset),point(offset+width)
            segment(name+' continuous threshold track',(p[0]-uy*delta,p[1]+ux*delta),
                    (q[0]-uy*delta,q[1]+ux*delta),-.01,.012,.017,M['dark'],0)
        segment(name+' supported head track',point(offset),point(offset+width),
                court_head-.03,court_head+.015,.15,M['dark'])
        door_states.append({'id':name,'type':'one moving and one fixed sliding light',
                            'modeled_state':'first half open; moving leaf parked over second half',
                            'clear_opening_m':width/2-.075,'track_width_m':.15,
                            'clear_start_m':list(point(offset+.04)),
                            'clear_end_m':list(point(offset+width/2-.035))})

    g.collection('02 Architecture | enclosed floors')
    for index, rect in enumerate(d.SLABS):
        slab = block('Enclosed floor '+str(index+1), rect, -.16, 0, M['stone'])
        slab['ifc_class'] = 'IfcSlab'
        slab['floor_area_role'] = 'conditioned'

    # Roof has a single datum, 24-inch eaves and a reserved insulated build-up.
    # Its inner edge follows the court: no beam or roof closes the open sky.
    g.collection('09 Roof | hide for cutaway')
    w, depth = d.WIDTH, d.DEPTH
    cx0, cy0, cx1, cy1 = d.ATRIUM
    eave = f(2)
    roof_rects = [(-eave,-eave,w+eave,cy0), (-eave,cy0,cx0,cy1),
                  (cx1,cy0,w+eave,cy1), (-eave,cy1,w+eave,depth+eave)]
    # One shared height field and one welded mesh cover all four roof wings.
    # Every common edge therefore has identical vertices/elevations; separate
    # strip slopes previously exposed pale triangular gaps at their junctions.
    def roof_grid(stops):
        values=[]
        for start,end in zip(stops,stops[1:]):
            cells=max(1,math.ceil((end-start)/.8))
            values.extend(start+(end-start)*i/cells for i in range(cells))
        return values+[stops[-1]]
    xs=roof_grid((-eave,cx0,cx1,w+eave))
    ys=roof_grid((-eave,cy0,cy1,depth+eave))
    fall_run=min(w+2*eave,depth+2*eave)/2
    def membrane_z(x,y):
        perimeter_distance=max(0,min(x+eave,w+eave-x,y+eave,depth+eave-y))
        return height+.285+.055*perimeter_distance/fall_run
    verts=[]
    indices={}
    def roof_vertex(ix,iy):
        key=(ix,iy)
        if key not in indices:
            indices[key]=len(verts)
            verts.append((xs[ix],ys[iy],membrane_z(xs[ix],ys[iy])))
        return indices[key]
    top_faces=[]
    for iy in range(len(ys)-1):
        for ix in range(len(xs)-1):
            midpoint=((xs[ix]+xs[ix+1])/2,(ys[iy]+ys[iy+1])/2)
            if cx0<midpoint[0]<cx1 and cy0<midpoint[1]<cy1:
                continue
            a,b,c,e=(roof_vertex(ix,iy),roof_vertex(ix+1,iy),
                     roof_vertex(ix+1,iy+1),roof_vertex(ix,iy+1))
            top_faces.extend(((a,b,c),(a,c,e)))
    top_count=len(verts)
    verts.extend((x,y,z-.012) for x,y,z in list(verts))
    faces=list(top_faces)
    faces.extend(tuple(v+top_count for v in reversed(face)) for face in top_faces)
    edge_uses={}
    for face in top_faces:
        for a,b in zip(face,face[1:]+face[:1]):
            edge_uses.setdefault(tuple(sorted((a,b))),[]).append((a,b))
    for uses in edge_uses.values():
        if len(uses)==1:
            a,b=uses[0]
            faces.append((a,a+top_count,b+top_count,b))
    mesh=bpy.data.meshes.new('Continuous tapered roof membrane mesh')
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    mesh.materials.append(M['dark'])
    membrane=bpy.data.objects.new('Tapered roof membrane toward perimeter',mesh)
    g.ACTIVE.objects.link(membrane)
    membrane['fall_basis']='Continuous nearest-perimeter height field; up to55mm concept fall; drainage sizing unresolved'
    membrane['mesh_basis']='Welded shared vertices; closed outer and courtyard edges; open atrium omitted'

    for index, rect in enumerate(roof_rects):
        tagged(block('Roof insulated assembly '+str(index+1), rect, height+.035,
                     height+.275,M['plaster']), 'IfcRoof')
        x0,y0,x1,y1 = rect
        count = math.ceil((x1-x0)/.20)
        pitch = (x1-x0)/count
        for i in range(count):
            block('Pale tongue-and-groove ceiling',
                  (x0+i*pitch+.002,y0,x0+(i+1)*pitch-.002,y1),
                  height,height+.032,M['plaster'],.002)
    edges = [((-eave,-eave),(w+eave,-eave)), ((w+eave,-eave),(w+eave,depth+eave)),
             ((w+eave,depth+eave),(-eave,depth+eave)), ((-eave,depth+eave),(-eave,-eave)),
             ((cx0,cy0),(cx1,cy0)), ((cx1,cy0),(cx1,cy1)),
             ((cx1,cy1),(cx0,cy1)), ((cx0,cy1),(cx0,cy0))]
    for a,b in edges:
        segment('Continuous walnut fascia',a,b,height-.055,height+.25,.11,M['walnut'])
        segment('Dark roof drip edge',a,b,height+.26,height+.355,.13,M['dark'])
    # Services use a deliberate lower plane, never an accidental room-wide beam.
    for index,rect in enumerate(d.SERVICE_ZONES):
        block('Service zone ceiling '+str(index+1),rect,service_clear,service_clear+.045,M['plaster'])

    g.collection('08 Structure | hide for cutaway')
    beam_top = height
    # Member breaks expose the bearing logic; the wing widths are engineering
    # drivers. They are never represented as one uninterrupted 60-foot timber.
    for y_ft in (0,13,28,44):
        y=f(.35 if y_ft==0 else y_ft)
        for left,right in ((0,25),(25,41),(41,60)):
            segment('Primary bay beam', (f(left)-(.12 if left==0 else 0),y),
                    (f(right)+(.12 if right==60 else 0),y),beam_clear,beam_top,
                    .18,M['walnut'])
    for x_ft in (0,25,41,60):
        x=f(x_ft)
        for ya,yb in ((0,13),(13,28),(28,44)):
            segment('Longitudinal support beam',(x,f(ya)),(x,f(yb)),
                    beam_clear,beam_top,.18,M['walnut'])
    # Posts occupy wall edges/court corners; external glass bays receive their
    # own aligned intermediate supports without blocking the central passage.
    post_positions={(0,0),(25,0),(41,0),(60,0),(0,13),(25,13),(41,13),(60,13),
                    (0,28),(25,28),(41,28),(60,28),(0,44),(25,44),(41,44),(60,44),
                    (60,36),(49,44),(33,44)}
    for x_ft,y_ft in sorted(post_positions):
        y_ft=.35 if y_ft==0 else y_ft
        obj=box('Timber bearing post',(f(x_ft),f(y_ft),beam_clear/2),
                (.18,.18,beam_clear),M['walnut'],bevel=.006)
        tagged(obj,'IfcColumn')
        block('Post shoe', (f(x_ft)-.105,f(y_ft)-.105,f(x_ft)+.105,f(y_ft)+.105),
              .015,.10,M['dark'],.003)

    g.collection('10 Site | terraces courtyard and arrival')
    # Level terrain is illustrative. It is lower than interior finish; channels
    # remain visible instead of pretending a flush threshold is waterproof.
    block('Illustrative level site', (f(-75),f(-70),f(125),f(110)), -.40,-.15,M['soil'],0)
    courtyard_grade=-.045
    block('Courtyard pale gravel and paving base',(cx0,cy0,cx1,cy1),-.14,-.06,M['stone'],0)
    planting=(f(27),f(19),f(34.5),f(25.5))
    block('Courtyard planted soil bed',planting,-.061,-.035,M['soil'],.04)
    asset('landscape','olive-tree','Courtyard olive specimen',(f(30.5),f(22),-.035))
    # Full shared pavers form an uninterrupted southern and eastern walking edge.
    for ix in range(4):
        asset('surfaces','honed-limestone-paver-4ft','Court south paver '+str(ix),
              (f(27.01+ix*4.02),f(15.03),courtyard_grade))
    for iy in range(2):
        asset('surfaces','honed-limestone-paver-4ft','Court east paver '+str(iy),
              (f(38.96),f(19.08+iy*4.02),courtyard_grade))
    for side in (cx0+.085,cx1-.085):
        segment('Court threshold drain channel',(side,cy0+.10),(side,cy1-.10),
                -.052,-.035,.07,M['dark'],0)
    segment('Court south threshold drain',(cx0+.10,cy0+.085),(cx1-.10,cy0+.085),
            -.052,-.035,.07,M['dark'],0)
    # Bespoke garden seat follows the planter edge; it is a masonry landscape
    # wall/cap, not a private copied reusable furnishing family.
    block('Courtyard stone seat wall',(f(27),f(25.5),f(34.5),f(27)),
          courtyard_grade,f(1.3),M['plaster'],.025)
    block('Courtyard walnut seat cap',(f(26.9),f(25.45),f(34.6),f(27.05)),
          f(1.3),f(1.46),M['walnut'],.02)
    for x,y in ((27.9,20.3),(33.2,20),(28,24.3)):
        asset('landscape','ornamental-grass-clump','Court grass',(f(x),f(y),-.035),version='v002')

    # Carport southwest of the home; drive meets the illustrative road shown on
    # the site sheet. This geometry makes no claim about legal highway access.
    carport=d.CARPORT
    block('Two car parking pad',carport,-.22,-.08,M['stone'],.015)
    block('Drive approach',(carport[0],f(-35),carport[2],carport[1]),-.25,-.10,M['stone'],.01)
    road=(d.SITE_BOUNDS[0],d.SITE_BOUNDS[1],d.SITE_BOUNDS[2],f(-35))
    block('Illustrative connecting road',road,-.26,-.10,M['dark'],.01)
    for x_ft in (6,18):
        for side in (-4.5,4.5):
            segment('Parking bay guide',(f(x_ft+side),f(-25)),(f(x_ft+side),f(-7)),
                    -.077,-.071,.035,M['dark'],0)
        block('Parking wheel stop',(f(x_ft-2),f(-6.8),f(x_ft+2),f(-6.4)),
              -.08,.04,M['dark'],.02)
    # Five-foot clear covered path: supports sit outside the paving envelope.
    walk=d.SHELTERED_WALK
    block('Covered arrival walkway',walk,-.15,-.04,M['stone'],.006)
    block('Entry landing',d.FRONT_LANDING,-.15,-.015,M['stone'],.006)
    for i in range(10):
        asset('surfaces','honed-limestone-paver-4ft','Arrival shared paver '+str(i),
              (f(2.02+i*4.02),f(-2.5),-.03))
    # Full shared paving and perimeter cuts are kept at their actual dimensions.
    terrace=d.REAR_TERRACE
    block('Rear terrace base',terrace,-.15,-.06,M['stone'])
    for iy in range(2):
        for ix in range(8):
            asset('surfaces','honed-limestone-paver-4ft','Rear terrace shared paver',
                  (f(27.02+ix*4.02),f(46.05+iy*4.02),-.04))

    g.collection('09 Roof | arrival and terrace canopies')
    for name,rect,z in [('Carport roof',carport,height),
                        ('Covered daily route',(walk[0]-.12,walk[1]-.20,walk[2]+.15,walk[3]+.2),height),
                        ('Entry shelter',(f(32),f(-6.9),f(42),0),height),
                        ('Rear shelter',(f(28),f(44),f(60),f(51)),height)]:
        tagged(block(name,rect,z,z+.20,M['walnut']),'IfcRoof')
        block(name+' dark weather edge',(rect[0]-.035,rect[1]-.035,rect[2]+.035,rect[3]+.035),
              z+.20,z+.245,M['dark'])
    g.collection('08 Structure | canopy supports')
    canopy_post_centers=[(.5,-26.5),(23.5,-26.5),(.5,-5.5),(23.5,-5.5),(32,-5.45),(41,-5.45),
                         (28,50.7),(44,50.7),(60,50.7)]
    for x_ft,y_ft in canopy_post_centers:
        tagged(box('Canopy timber support',(f(x_ft),f(y_ft),(height-.10)/2),
                   (.18,.18,height+.10),M['walnut'],bevel=.008),'IfcColumn')

    g.collection('11 Roof and site drainage | concept reservations')
    for x,y in ((-.22,f(1)),(-.22,f(43)),(w+.22,f(2)),(w+.22,f(43))):
        exterior_x=-eave+.04 if x<0 else w+eave-.04
        exterior_y=-eave+.04 if y<depth/2 else depth+eave-.04
        # Each downpipe explicitly meets its collecting edge through horizontal
        # branches within the eave zone, rather than floating below the roof.
        rod('Gutter collector branch',(exterior_x,exterior_y,height+.29),
            (x,exterior_y,height+.29),.05,M['dark'])
        rod('Gutter to downpipe connection',(x,exterior_y,height+.29),
            (x,y,height+.29),.05,M['dark'])
        rod('Roof downpipe',(x,y,height+.29),(x,y,.12),.04,M['dark'])
        rod('Roof discharge elbow',(x,y,.12),(x+(-.22 if x<0 else .22),y,-.10),.04,M['dark'])
    for y in (-eave+.04,depth+eave-.04):
        segment('Roof edge collection gutter',(-eave+.04,y),(w+eave-.04,y),
                height+.24,height+.34,.13,M['dark'],.003)
    for x in (-eave+.04,w+eave-.04):
        segment('Roof side collection gutter',(x,-eave+.04),(x,depth+eave-.04),
                height+.24,height+.34,.13,M['dark'],.003)
    for x in (-eave+.04,w+eave-.04):
        rod('Visible emergency overflow reservation',(x,-eave+.04,height+.32),
            (x,-eave-.30,height+.30),.04,M['dark'])
    for x in (cx0+.12,cx1-.12):
        block('Courtyard accessible drain sump',(x-.07,cy0+.06,x+.07,cy0+.20),-.055,-.025,M['dark'],.003)

    g.collection('12 Landscape | linked library planting')
    rng=random.Random(101)
    for i,(x,y) in enumerate(((-45,18),(-24,60),(20,79),(105,78),(88,39),(93,-6),(-25,-40))):
        asset('landscape','broad-canopy-oak',f'Garden canopy {i+1}',(f(x),f(y),-.15),rotation=rng.uniform(0,math.tau))
    for i,(x,y) in enumerate(((31,-18),(56,-18),(73,10),(-10,30))):
        asset('landscape','olive-tree',f'Garden olive {i+1}',(f(x),f(y),-.15),rotation=rng.uniform(0,math.tau))
    plant_positions=[]
    for x in range(2,61,4):
        if x<44: continue
        plant_positions.append((x,-11+rng.uniform(-1,1)))
    for y in range(4,49,4):
        plant_positions.extend([(-6+rng.uniform(-1,1),y),(66+rng.uniform(-1,1),y)])
    for x in range(3,61,4):
        plant_positions.append((x,59+rng.uniform(-1,1)))
    for index,(x,y) in enumerate(plant_positions):
        species='sage-shrub' if index%3==0 else 'ornamental-grass-clump'
        asset('landscape',species,f'Layered garden planting {index+1}',
              (f(x),f(y),-.15),rotation=rng.uniform(0,math.tau),version='v002')

    # Editable, hidden-from-beauty QA solids: these are dimensional reserves,
    # deliberately not cosmetic cars or manufacturer meshes. The shared IFC
    # exporter excludes this unclassified collection; no ifc_class is assigned.
    qa=g.collection('99 QA | parking and sheltered route envelopes')
    qa.hide_render=True
    qa['scope']='Illustrative full-size vehicle/access envelopes; no turning-path certification'
    vehicle_records=[]
    vehicle_rects=[]
    door_rects=[]
    front_access=.80
    rear_access=.80
    side_door_travel=.75
    def reserve(name,rect,bottom,top,role):
        obj=block(name,rect,bottom,top,M['dark'],0)
        obj.display_type='WIRE'
        obj.hide_render=True
        obj['qa_only']=True
        obj['qa_role']=role
        obj['exclude_from_ifc']=True
        obj['rect_m']=list(rect)
        return obj
    for index,bay in enumerate(d.PARKING_BAYS,1):
        x0,y0,x1,y1=bay
        center=((x0+x1)/2,(y0+y1)/2)
        body=(center[0]-.95,center[1]-2.4,center[0]+.95,center[1]+2.4)
        vehicle_rects.append(body)
        car=reserve(f'QA vehicle {index} body 1900x4800x1600',body,-.08,1.52,'vehicle_body')
        car['width_m']=1.9;car['length_m']=4.8;car['height_m']=1.6
        car['facing']='positive Y toward sheltered walk'
        for side,rect in [('left',(body[0]-.75,body[1],body[0],body[3])),
                          ('right',(body[2],body[1],body[2]+.75,body[3]))]:
            reserve(f'QA vehicle {index} {side} door sweep reserve',rect,-.08,1.32,'vehicle_side_door_reserve')
            door_rects.append(rect)
        reserve(f'QA vehicle {index} front access reserve',
                (body[0],body[3],body[2],body[3]+front_access),-.08,1.92,'vehicle_front_access')
        reserve(f'QA vehicle {index} rear access reserve',
                (body[0],body[1]-rear_access,body[2],body[1]),-.08,1.92,'vehicle_rear_access')
        vehicle_records.append({'id':index,'body_rect_m':list(body),'bay_rect_m':list(bay),
                                'body_size_m':[1.9,4.8,1.6],'side_door_reserve_m':side_door_travel,
                                'front_access_m':front_access,'rear_access_m':rear_access,
                                'bay_side_margin_m':min(body[0]-x0,x1-body[2]),
                                'bay_end_margin_m':min(body[1]-y0,y1-body[3]),
                                'carport_front_margin_m':carport[3]-body[3],
                                'carport_rear_margin_m':body[1]-carport[1],
                                'body_to_sheltered_walk_m':walk[1]-body[3]})
    reserve('QA five-foot continuous sheltered route',walk,-.04,2.06,'sheltered_walk_clearance')
    def overlap(a,b):
        return min(a[2],b[2])-max(a[0],b[0])>1e-6 and min(a[3],b[3])-max(a[1],b[1])>1e-6
    post_rects=[(f(x)-.09,f(y)-.09,f(x)+.09,f(y)+.09) for x,y in canopy_post_centers]
    assert not any(overlap(walk,r) for r in vehicle_rects+door_rects+post_rects), 'Sheltered walk obstruction'
    assert not any(overlap(r,p) for r in door_rects for p in post_rects), 'Vehicle side-door reserve meets post'
    assert not overlap(door_rects[1],door_rects[2]), 'Adjacent door reserves overlap'
    route_clearance={'walk_width_m':walk[3]-walk[1],
                     'minimum_canopy_post_gap_m':min(walk[1]-r[3] for r in post_rects if r[3]<walk[1]),
                     'vehicle_body_gap_m':vehicle_rects[1][0]-vehicle_rects[0][2],
                     'simultaneous_inner_door_reserve_gap_m':door_rects[2][0]-door_rects[1][2],
                     'front_access_to_walk_gap_m':min(v['body_to_sheltered_walk_m']-front_access for v in vehicle_records),
                     'checked':'Axis-aligned vehicle, side-door, canopy-post and covered-walk geometry',
                     'limits':'0.75m conservative side clearance envelopes; exact vehicle door arcs, turning, road access and grades require selected vehicles and site design'}

    return {'door_states':door_states,
            'ceiling_plane_m':height,'beam_clear_m':beam_clear,'service_clear_m':service_clear,
            'roof_top_m':height+.355,'eave_projection_m':eave,
            'carport_rect_m':list(carport),'covered_walk_rect_m':list(walk),
            'parking_reserves_m':[list(rect) for rect in d.PARKING_BAYS],
            'vehicle_clearance_records':vehicle_records,'sheltered_route_clearance':route_clearance,
            'illustrative_road_rect_m':list(road),
            'site_basis':'Illustrative level terrain; no surveyed parcel or climate claim',
            'glazing_basis':'Bespoke host post-and-beam infill; court east and north doors half open',
            'drainage_basis':'Concept roof collection/downpipes, court channels and accessible sumps; sizing and discharge unresolved'}
