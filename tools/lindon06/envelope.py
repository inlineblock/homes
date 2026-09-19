"""Listing-derived massing with an original red-brick and broad-window remodel."""
import math
from pathlib import Path
import bpy
from mathutils import Vector
from common import geometry as g
from common.library import linked_collection
from utils import box,rod,beam,mesh,prism,instance,tag,cyl

OPENING_SCHEDULE=[]
WINDOW_COLLECTION=None

def poly_area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2

def wall_piece(name,a,b,z0,z1,mat,depth=.32):
    if z1-z0<.001 or math.dist(a,b)<.002:return
    d=Vector(b)-Vector(a)
    obj=box(name,((a[0]+b[0])/2,(a[1]+b[1])/2,(z0+z1)/2),(d.length,depth,z1-z0),mat,.008)
    obj.rotation_euler.z=math.atan2(d.y,d.x)
    return obj

def window(root, name, a,b,base,height,M,depth_offset=-.06):
    global WINDOW_COLLECTION
    delta=Vector(b)-Vector(a);length=delta.length;ang=math.atan2(delta.y,delta.x)
    mid=(Vector(a)+Vector(b))/2
    # CCW perimeter has its interior on local +Y. The glazing is recessed
    # 100 mm behind the 320 mm host wall's outer face, not pasted onto it.
    mid+=Vector((-delta.y,delta.x)).normalized()*depth_offset
    if WINDOW_COLLECTION is None:
        path=root/'library/openings/slim-dark-window/v002/slim-dark-window.blend'
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=['Slim bronze window | 2400 x 2400 mm | v002']
        WINDOW_COLLECTION=dst.collections[0]
    coll=WINDOW_COLLECTION
    # Deliberate broad picture units use a parametric size adaptation. The
    # immutable source remains linked; exact product and sash design are open.
    obj=instance(name,coll,(mid.x,mid.y,base),ang,(length/2.4,1,height/2.4))
    obj['ifc_class']='IfcWindow';obj['opening_width_m']=length;obj['opening_height_m']=height
    return obj

def aperture_wall(root,name,a,b,z,height,openings,M,level,brick=True):
    d=Vector(b)-Vector(a);L=d.length;u=d/L;cursor=0
    # The traced house footprints run CCW, while the garage perimeter is CW.
    # Only the actual inward broad wall face receives the interior finish.
    # Jambs and exposed perimeter ends retain the selected exterior finish.
    inward_sign=-1 if name.startswith('Garage side') else 1
    def point(t):return tuple(Vector(a)+u*t)
    def exterior_material(mid):
        if not brick:return M['plaster']
        if name.startswith('main facade'):
            face=int(name.rsplit(' ',1)[1])
            if face==7 and 8.31-.01<=mid[0]<=11.08+.01:return M['panel']
            if face in [2,3,4,10,11,12]:return M['facade_plaster']
        elif name.startswith('upper facade'):
            face=int(name.rsplit(' ',1)[1])
            if face==3 and 8.31<=mid[0]<=11.08:return M['panel']
            if face in [7,8,9]:return M['panel']
            if face in [1,2,4,5,6,14]:return M['facade_plaster']
        return M['brick']
    def part(t1,t2,sill,head,mat=None):
        # Split a continuous wall at the tall charcoal insert's edges so brick
        # side cheeks remain solid masonry. The window aperture stays real.
        stops=[t1,t2]
        if name in ['main facade 7','upper facade 3'] and abs(u.x)>.99:
            stops += [(x-a[0])/u.x for x in [8.31,11.08] if t1<(x-a[0])/u.x<t2]
        stops=sorted(set(stops))
        for start,end in zip(stops,stops[1:]):
            obj=wall_piece(name,point(start),point(end),z+sill,z+head,mat or exterior_material(point((start+end)/2)))
            if obj:
                obj.data.materials.append(M['plaster'])
                for face in obj.data.polygons:
                    if face.normal.y*inward_sign>.5:face.material_index=1
                tag(obj,'IfcWall',level)
    for i,op in enumerate(sorted(openings,key=lambda o:o['offset'])):
        off,w=op['offset'],op['width'];sill,h=op.get('sill',.7),op.get('height',2.1)
        if off<cursor-.001 or off+w>L+.001:continue
        part(cursor,off,0,height);part(off,off+w,0,sill);part(off,off+w,sill+h,height)
        kind=op.get('kind','window')
        if kind in ['entry','passage']:
            # Sidelights flank a genuine hinged leaf and empty passage width.
            leaf=min(1.18,w);side=max(0,(w-leaf)/2)
            if side>.1:
                window(root,name+' entry sidelight left',point(off),point(off+side),z+sill,h,M,depth_offset=-.06*inward_sign)
                window(root,name+' entry sidelight right',point(off+side+leaf),point(off+w),z+sill,h,M,depth_offset=-.06*inward_sign)
            pa=Vector(point(off+side));pb=Vector(point(off+side+leaf))
            door=wall_piece(name+' timber door',tuple(pa),tuple(pb),z+sill,z+sill+h,M['cedar'],.075)
            tag(door,'IfcDoor',level)
            pull=pa.lerp(pb,.88);n=Vector((u.y,-u.x))
            rod(name+' door pull',(pull.x+n.x*.07,pull.y+n.y*.07,z+1.0),(pull.x+n.x*.07,pull.y+n.y*.07,z+1.78),.012,M['bronze'])
        elif kind=='glazed_door':
            # A project-width rear door assembly, with glazing, heads and a
            # separate daily passage leaf. Shown closed; not operation-certified.
            panels=max(2,round(w/1.15));pw=w/panels
            for j in range(panels):
                pa=Vector(point(off+j*pw));pb=Vector(point(off+(j+1)*pw));mid=(pa+pb)/2
                pane=wall_piece(name+' clear door pane',tuple(pa+u*.034),tuple(pb-u*.034),z+.085,z+h-.055,M['glass'],.012)
                tag(pane,'IfcDoor',level)
                for p in [pa,pb]:beam(name+' door stile',(p.x,p.y,z+.025),(p.x,p.y,z+h),.038,.068,M['dark'])
                for zz in [z+.05,z+h-.025]:beam(name+' door rail',(pa.x,pa.y,zz),(pb.x,pb.y,zz),.046,.055,M['dark'])
            p=Vector(point(off+w-.16));rod(name+' daily door pull',(p.x,p.y-.065,z+1.0),(p.x,p.y-.065,z+1.43),.012,M['dark'])
        else:
            win=window(root,name+f' | dark window {i+1}',point(off),point(off+w),z+sill,h,M,depth_offset=-.06*inward_sign)
            win['ifc_storey']=level
        if kind=='window':
            zh=z+sill-.035
            # One restrained sill; no raised dark stripe across every head.
            trim=wall_piece(name+' | thin bronze sill',point(off-.025),point(off+w+.025),zh,zh+.035,M['dark'],.35)
            tag(trim,'IfcMember',level)
        OPENING_SCHEDULE.append({'level':level,'name':name,'kind':kind,'start_m':point(off),'end_m':point(off+w),'sill_m':sill,'height_m':h,'design':{'window':'Rectangular fixed center with casement-style side panels, shown closed','entry':'Timber entry leaf with sidelights where width permits','passage':'Timber passage leaf','glazed_door':'Glazed door assembly with proposed daily passage leaf, shown closed'}.get(kind,kind)+'; concept geometry, product and operation unverified'})
        cursor=off+w
    part(cursor,L,0,height)

def guard(name,a,b,base,M):
    d=Vector(b)-Vector(a);L=d.length;u=d/L
    beam(name+' continuous slender top rail',(*a,base+1.06),(*b,base+1.06),.033,.037,M['dark'])
    beam(name+' glazing base channel',(*a,base+.07),(*b,base+.07),.045,.06,M['dark'])
    n=math.ceil(L/1.7)
    for i in range(n+1):
        p=Vector(a)+d*i/n
        box(name+' slender glazing post',(p.x,p.y,base+.54),(.03,.03,1.08),M['dark'],.003)
    for i in range(n):
        start=Vector(a)+u*(i*L/n+.027);end=Vector(a)+u*((i+1)*L/n-.027)
        pane=wall_piece(name+' clear concept guard panel',tuple(start),tuple(end),base+.105,base+1.035,M['glass'],.012)
        tag(pane,'IfcRailing','Upper floor' if base>1 else 'Ground floor')

def roof_face(name,verts,M):
    # Both roof slopes must face upward so thickness grows into the building,
    # rather than covering the standing seams on the opposite slope.
    if (Vector(verts[1])-Vector(verts[0])).cross(Vector(verts[2])-Vector(verts[0])).z<0:verts=list(reversed(verts))
    obj=mesh(name,verts,[tuple(range(len(verts)))],M['roof'])
    sol=obj.modifiers.new('Folded roof thickness','SOLIDIFY');sol.thickness=.09
    tag(obj,'IfcRoof','Upper floor')
    return obj

def gable(name,origin,u,v,length,width,eave,ridge,M,outer_wall=None,soffit_cutout=None):
    o=Vector(origin);u=Vector(u);v=Vector(v)
    def p(x,y,z):q=o+u*x+v*y;return(q.x,q.y,z)
    for sign in [-1,1]:
        roof_face(name+' standing-seam slope',[p(0,sign*width/2,eave),p(length,sign*width/2,eave),p(length,0,ridge),p(0,0,ridge)],M)
        n=math.ceil(length/.45)
        for i in range(n+1):
            x=i*length/n
            beam(name+' raised seam',p(x,sign*width/2,eave+.045),p(x,0,ridge+.045),.017,.024,M['roof'])
        beam(name+' eave fascia',p(0,sign*width/2,eave),p(length,sign*width/2,eave),.09,.11,M['dark'])
        # A half-round concept gutter is a visible collection path. Discharge
        # sizing and concealed connections await an actual survey/design.
        rod(name+' gutter',p(0,sign*(width/2+.055),eave-.035),p(length,sign*(width/2+.055),eave-.035),.05,M['dark'])
    for x in [0,length]:
        if x==length and outer_wall is not None:
            # The roof overhang and the supported masonry end are different
            # extents. The traced upper garage facade is narrower and inset
            # from the roof edge; a full roof-width triangle floats outside it.
            a,b=[Vector(point) for point in outer_wall]
            direction=(b-a).normalized()
            outward=Vector((direction.y,-direction.x))
            a+=outward*.159;b+=outward*.159
            ta=(a-o).dot(v);tb=(b-o).dot(v)
            stations=[(0.,a),(1.,b)]
            if ta*tb<0:
                t=-ta/(tb-ta);stations.append((t,a.lerp(b,t)))
            stations.sort(key=lambda item:item[0])
            slope=(ridge-eave)/(width/2)
            roof_underside=.09*math.sqrt(1+slope*slope)
            def roof_z(point):
                return max(eave-.01,ridge-abs((point-o).dot(v))*slope-roof_underside)
            verts=[(a.x,a.y,eave-.01),(b.x,b.y,eave-.01)]
            verts += [(point.x,point.y,roof_z(point)) for _,point in reversed(stations)]
            # Collapse coincident lower/top corners at the outer eave.
            compact=[]
            for vertex in verts:
                if not compact or math.dist(vertex,compact[-1])>.0001:compact.append(vertex)
            if math.dist(compact[0],compact[-1])<.0001:compact.pop()
            infill=mesh(name+' supported outer brick gable',compact,[tuple(range(len(compact)))],M['brick'])
            solid=infill.modifiers.new('Supported gable masonry depth','SOLIDIFY');solid.thickness=.16;solid.offset=-1
            tag(infill,'IfcWall','Upper floor')
        else:
            mesh(name+' brick gable', [p(x,-width/2,eave),p(x,width/2,eave),p(x,0,ridge)],[(0,1,2)],M['brick'])
        for sign in [-1,1]:beam(name+' verge',p(x,sign*width/2,eave),p(x,0,ridge),.09,.11,M['dark'])
    beam(name+' folded ridge cap',p(0,0,ridge+.04),p(length,0,ridge+.04),.10,.05,M['roof'])
    if soffit_cutout is not None:
        outline=[p(0,-width/2,0)[:2],p(length,-width/2,0)[:2],p(length,width/2,0)[:2],p(0,width/2,0)[:2]]
        soffit=prism(name+' dark boxed overhang soffit',outline,eave-.04,eave-.015,M['dark'])
        cutter=prism('Temporary occupied-footprint soffit exclusion',soffit_cutout,eave-.2,eave+.2,M['dark'])
        bpy.context.view_layer.objects.active=soffit
        mod=soffit.modifiers.new('Keep soffit outside occupied upper rooms','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(cutter,do_unlink=True)
        tag(soffit,'IfcCovering','Upper floor')

def build_roof(M):
    g.collection('09 Roof | charcoal metal, clear pitches and restrained profiles')
    # Dominant simple roof replaces the original busy combination of hips,
    # decorative arches and paired small dormers. Its footprint retains the
    # recognized core and 45-degree garage / bedroom wing.
    # Hip roof over the actual occupied upper core, leaving the rear upper
    # terrace open to sky. The original house also has a dominant hip volume.
    x0,x1,y0,y1,eave,ridge=3.98,19.66,2.5,12.46,6.23,8.65
    r0,r1,ry=8.8,14.84,7.48
    faces=[[(x0,y0,eave),(x1,y0,eave),(r1,ry,ridge),(r0,ry,ridge)],
           [(x1,y1,eave),(x0,y1,eave),(r0,ry,ridge),(r1,ry,ridge)],
           [(x0,y1,eave),(x0,y0,eave),(r0,ry,ridge)],
           [(x1,y0,eave),(x1,y1,eave),(r1,ry,ridge)]]
    for i,verts in enumerate(faces):roof_face('Main charcoal hip '+str(i),verts,M)
    for a,b in [((x0,y0,eave),(r0,ry,ridge)),((x0,y1,eave),(r0,ry,ridge)),((x1,y0,eave),(r1,ry,ridge)),((x1,y1,eave),(r1,ry,ridge)),((r0,ry,ridge),(r1,ry,ridge))]:beam('Hip and ridge folded cap',a,b,.10,.05,M['roof'])
    # Physical seams on each pitched face, clipped at the hip intersection.
    for sign in [-1,1]:
        ey=y0 if sign<0 else y1
        for i in range(36):
            x=x0+(i+.5)*(x1-x0)/36
            t=min(1,(x-x0)/(r0-x0),(x1-x)/(x1-r1))
            end=(x,ey+(ry-ey)*t,eave+(ridge-eave)*t+.045)
            beam('Main hip standing seam',(x,ey,eave+.045),end,.017,.022,M['roof'])
    for ex,rx in [(x0,r0),(x1,r1)]:
        for i in range(23):
            y=y0+(i+.5)*(y1-y0)/23
            t=min((y-y0)/(ry-y0),(y1-y)/(y1-ry))
            beam('End hip standing seam',(ex,y,eave+.045),(ex+(rx-ex)*t,y,eave+(ridge-eave)*t+.045),.017,.022,M['roof'])
    for a,b in [((x0,y0,eave),(x1,y0,eave)),((x1,y1,eave),(x0,y1,eave)),((x0,y1,eave),(x0,y0,eave)),((x1,y0,eave),(x1,y1,eave))]:beam('Main restrained eave fascia',a,b,.09,.11,M['dark'])
    # Inboard ends continue beneath the lowered hip rather than terminating
    # as exposed triangular walls. Outer facade/gable positions are retained.
    gable('Front bedroom gable',(9.58,-.32),(0,1),(1,0),7.0,4.78,6.23,8.10,M)
    gable('Rear bathing pavilion',(11.06,8.1),(0,1),(1,0),7.81,4.82,6.23,8.20,M)
    # The low study becomes the quiet modern volume. Its roof falls rearward
    # beneath a level masonry parapet; this is not a drainage specification.
    low_outline=[(-.20,-.20),(4.57,-.20),(4.57,2.58),(4.10,2.58),(4.10,8.97),(-.20,8.97)]
    roof_face('Study concealed roof with positive fall',[(x,y,3.31-(y+.20)*.15/9.17) for x,y in low_outline],M)
    for a,b in [(low_outline[0],low_outline[1]),(low_outline[1],low_outline[2]),(low_outline[4],low_outline[5]),(low_outline[5],low_outline[0])]:
        tag(wall_piece('Study brick parapet',a,b,3.035,3.50,M['brick'],.20),'IfcWall','Ground floor')
        tag(wall_piece('Study thin folded coping',a,b,3.50,3.545,M['dark'],.23),'IfcRoof','Ground floor')
    box('Study rear rainwater outlet',(.06,9.015,3.19),(.16,.20,.105),M['dark'],.004)
    box('Study visible rear rainwater leader',(.06,9.08,1.59),(.075,.075,3.18),M['dark'],.005)
    # Garage wing has an occupied full-height floor with a quieter roof profile.
    # The source loft is interpreted with higher knee walls, explicitly a
    # proposed exterior change rather than an undocumented as-built condition.
    from design import LEVELS
    upper=LEVELS['upper']['footprint']
    gable('Angled garage bedroom wing',(14.84583695,7.50416305),(.70710678,-.70710678),(.70710678,.70710678),15.6,8.45,6.23,8.65,M,
          outer_wall=(upper[9],upper[10]),soffit_cutout=upper)
    for x,y in [(4.00,.0),(19.85,15.9),(0.0,8.4),(28.4,.2)]:
        box('Rainwater leader',(x,y,1.45),(.065,.065,2.9),M['dark'],.009)

def build_decks(M):
    g.collection('08 Structure | two rear decks and exposed walkout')
    for z in [0,3.25]:
        rects=[(8.78,16.1,19.43,19.39)] if z==0 else [(8.78,15.60,19.43,19.39),(13.20,12.12,19.43,15.60)]
        for x0,y0,x1,y1 in rects:
            box('Rear terrace structural slab',((x0+x1)/2,(y0+y1)/2,z-.11),(x1-x0,y1-y0,.22),M['dark'],.012)
            count=math.ceil((y1-y0)/.145)
            for i in range(count):box('Rear terrace ash decking',((x0+x1)/2,y0+(i+.5)*(y1-y0)/count,z+.009),(x1-x0-.012,(y1-y0)/count-.009,.028),M['deck'],.003)
        guard('Rear terrace guard',(8.78,19.39),(19.43,19.39),z,M)
        guard('West return guard',(8.78,16.1 if z==0 else 15.60),(8.78,19.39),z,M)
        guard('East return guard',(19.43,16.1 if z==0 else 12.12),(19.43,19.39),z,M)
    for x in [8.9,14.12,19.32]:
        box('Continuous rear brick pier',(x,19.12,.075),(.38,.38,6.45),M['brick'],.006)
        box('Pier slim charcoal coping',(x,19.12,3.3125),(.42,.42,.025),M['dark'],.003)
    # Rectangular geometry replaces the scalloped/bowed historical deck line.
    # Rear patio and stair back to the lawn are supplied by the site module.
    chaise=linked_collection(Path(__file__).resolve().parents[2],'furniture','slatted-outdoor-chaise','v001')
    for x in [15.40,17.30]:
        # Leave the bedroom doorway/return strip and 1.4 m front circulation
        # free. These are rigid library placements, not scaled furniture.
        instance('Shared upper terrace chaise',chaise,(x,17.02,3.273),0)

def build_entry(M):
    g.collection('05 Arrival | sheltered timber entrance')
    canopy=box('Thin folded entry canopy',(5.965,1.05,3.035),(4.06,3.40,.13),M['dark'],.010)
    soffit=box('Sheltered smoked oak entry soffit',(5.965,1.05,2.957),(3.96,3.30,.022),M['cedar'],.004)
    # Shared downlights sit in real pockets, leaving the top roof skin intact.
    # Their artistic illumination is not a wet-location product specification.
    from common import lighting_assets
    root=Path(__file__).resolve().parents[2]
    lights=lighting_assets.load(root,['downlight'])
    for y in [.15,1.2,2.25]:
        cutter=cyl('Temporary entry fixture pocket',(5.965,y,2.98),.044,.14,M['dark'])
        for host in [canopy,soffit]:
            bpy.context.view_layer.objects.active=host
            mod=host.modifiers.new('Actual recessed fixture pocket','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
            bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(cutter,do_unlink=True)
        lighting_assets.place('Shared entry recessed downlight',lights['downlight'],'downlight',(5.965/.3048,y/.3048,2.946/.3048),power=18,color=(1,.83,.63))
    tag(box('Single brick arrival pier',(4.35,-.30,1.475),(.32,.40,2.95),M['brick'],.009),'IfcColumn','Ground floor')
    # The source trace has a 341 mm setback between the stacked front windows.
    # A dark stepped spandrel joins their colour field without moving the
    # occupied floor or laying an opaque panel across either clear opening.
    # Keep its inter-storey return level: a sloped panel read as an accidental
    # awning instead of the intended continuous charcoal window composition.
    tag(mesh('Continuous charcoal front-window spandrel',[
        (8.31,-.515,2.75),(11.08,-.515,2.75),
        (11.08,-.515,3.025),(8.31,-.515,3.025),
        (11.08,-.175,3.025),(8.31,-.175,3.025),
        (11.08,-.175,3.85),(8.31,-.175,3.85)],
        [(0,1,2,3),(3,2,4,5),(5,4,6,7)],M['panel']),'IfcCovering','Ground floor')
