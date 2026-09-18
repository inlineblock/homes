"""Listing-derived massing with an original red-brick and broad-window remodel."""
import math
import bpy
from mathutils import Vector
from common import geometry as g
from common.library import linked_collection
from utils import box,rod,beam,mesh,prism,instance,tag

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

def window(root, name, a,b,base,height,M,depth_offset=0):
    global WINDOW_COLLECTION
    delta=Vector(b)-Vector(a);length=delta.length;ang=math.atan2(delta.y,delta.x)
    mid=(Vector(a)+Vector(b))/2
    if WINDOW_COLLECTION is None:
        path=root/'library/openings/slim-dark-window/v001/slim-dark-window.blend'
        with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=['Slim dark window | 2400 x 2400 mm']
        WINDOW_COLLECTION=dst.collections[0]
    coll=WINDOW_COLLECTION
    # Deliberate broad picture units use a parametric size adaptation. The
    # immutable source remains linked; exact product and sash design are open.
    obj=instance(name,coll,(mid.x,mid.y,base),ang,(length/2.4,1,height/2.4))
    obj['ifc_class']='IfcWindow';obj['opening_width_m']=length;obj['opening_height_m']=height
    return obj

def aperture_wall(root,name,a,b,z,height,openings,M,level,brick=True):
    d=Vector(b)-Vector(a);L=d.length;u=d/L;cursor=0
    def point(t):return tuple(Vector(a)+u*t)
    def part(t1,t2,sill,head,mat=None):
        obj=wall_piece(name,point(t1),point(t2),z+sill,z+head,mat or M['brick' if brick else 'plaster'])
        if obj:tag(obj,'IfcWall',level)
    for i,op in enumerate(sorted(openings,key=lambda o:o['offset'])):
        off,w=op['offset'],op['width'];sill,h=op.get('sill',.7),op.get('height',2.1)
        if off<cursor-.001 or off+w>L+.001:continue
        part(cursor,off,0,height);part(off,off+w,0,sill);part(off,off+w,sill+h,height)
        kind=op.get('kind','window')
        if kind in ['entry','passage']:
            # Sidelights flank a genuine hinged leaf and empty passage width.
            leaf=min(1.18,w);side=max(0,(w-leaf)/2)
            if side>.1:
                window(root,name+' entry sidelight left',point(off),point(off+side),z+sill,h,M)
                window(root,name+' entry sidelight right',point(off+side+leaf),point(off+w),z+sill,h,M)
            pa=Vector(point(off+side));pb=Vector(point(off+side+leaf))
            door=wall_piece(name+' timber door',tuple(pa),tuple(pb),z+sill,z+sill+h,M['oak'],.075)
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
            win=window(root,name+f' | dark window {i+1}',point(off),point(off+w),z+sill,h,M)
            win['ifc_storey']=level
        for zh in [z+sill-.045,z+sill+h+.04]:
            trim=wall_piece(name+' | thin cast sill / lintel',point(off-.06),point(off+w+.06),zh,zh+.065,M['dark'],.40)
            tag(trim,'IfcMember',level)
        OPENING_SCHEDULE.append({'level':level,'name':name,'kind':kind,'start_m':point(off),'end_m':point(off+w),'sill_m':sill,'height_m':h,'design':{'window':'Rectangular fixed center with casement-style side panels, shown closed','entry':'Timber entry leaf with sidelights where width permits','passage':'Timber passage leaf','glazed_door':'Glazed door assembly with proposed daily passage leaf, shown closed'}.get(kind,kind)+'; concept geometry, product and operation unverified'})
        cursor=off+w
    part(cursor,L,0,height)

def guard(name,a,b,base,M):
    d=Vector(b)-Vector(a);L=d.length;u=d/L
    for z in [base+.13,base+1.06]:beam(name+' continuous rail',(*a,z),(*b,z),.035,.04,M['dark'])
    for i in range(math.ceil(L/1.7)+1):
        p=Vector(a)+d*i/math.ceil(L/1.7)
        box(name+' post',(p.x,p.y,base+.54),(.055,.055,1.08),M['dark'],.004)
    for i in range(1,math.ceil(L/.11)):
        p=Vector(a)+u*i*L/math.ceil(L/.11)
        box(name+' straight baluster',(p.x,p.y,base+.57),(.014,.014,.93),M['dark'],.002)

def roof_face(name,verts,M):
    # Both roof slopes must face upward so thickness grows into the building,
    # rather than covering the standing seams on the opposite slope.
    if (Vector(verts[1])-Vector(verts[0])).cross(Vector(verts[2])-Vector(verts[0])).z<0:verts=list(reversed(verts))
    obj=mesh(name,verts,[tuple(range(len(verts)))],M['roof'])
    sol=obj.modifiers.new('Folded roof thickness','SOLIDIFY');sol.thickness=.09
    tag(obj,'IfcRoof','Upper floor')
    return obj

def gable(name,origin,u,v,length,width,eave,ridge,M):
    o=Vector(origin);u=Vector(u);v=Vector(v)
    def p(x,y,z):q=o+u*x+v*y;return(q.x,q.y,z)
    for sign in [-1,1]:
        roof_face(name+' standing-seam slope',[p(0,sign*width/2,eave),p(length,sign*width/2,eave),p(length,0,ridge),p(0,0,ridge)],M)
        n=math.ceil(length/.45)
        for i in range(n+1):
            x=i*length/n
            beam(name+' raised seam',p(x,sign*width/2,eave+.045),p(x,0,ridge+.045),.017,.024,M['roof'])
        beam(name+' eave fascia',p(0,sign*width/2,eave),p(length,sign*width/2,eave),.15,.16,M['dark'])
        # A half-round concept gutter is a visible collection path. Discharge
        # sizing and concealed connections await an actual survey/design.
        rod(name+' gutter',p(0,sign*(width/2+.055),eave-.035),p(length,sign*(width/2+.055),eave-.035),.05,M['dark'])
    for x in [0,length]:
        mesh(name+' brick gable', [p(x,-width/2,eave),p(x,width/2,eave),p(x,0,ridge)],[(0,1,2)],M['brick'])
        for sign in [-1,1]:beam(name+' verge',p(x,sign*width/2,eave),p(x,0,ridge),.14,.16,M['dark'])
    beam(name+' folded ridge cap',p(0,0,ridge+.04),p(length,0,ridge+.04),.10,.05,M['roof'])

def build_roof(M):
    g.collection('09 Roof | charcoal metal, clear pitches and restrained profiles')
    # Dominant simple roof replaces the original busy combination of hips,
    # decorative arches and paired small dormers. Its footprint retains the
    # recognized core and 45-degree garage / bedroom wing.
    # Hip roof over the actual occupied upper core, leaving the rear upper
    # terrace open to sky. The original house also has a dominant hip volume.
    x0,x1,y0,y1,eave,ridge=3.98,19.66,2.5,12.46,6.23,9.55
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
    for a,b in [((x0,y0,eave),(x1,y0,eave)),((x1,y1,eave),(x0,y1,eave)),((x0,y1,eave),(x0,y0,eave)),((x1,y0,eave),(x1,y1,eave))]:beam('Main restrained eave fascia',a,b,.12,.18,M['dark'])
    gable('Front bedroom gable',(9.58,-.32),(0,1),(1,0),5.5,4.78,6.23,8.10,M)
    gable('Rear bathing pavilion',(11.06,11.9),(0,1),(1,0),4.01,4.82,6.23,8.20,M)
    # Left single-storey study / formal sitting wing.
    gable('Low front study wing',(2.20,-.37),(0,1),(1,0),9.46,4.95,3.05,4.65,M)
    # Garage wing has an occupied full-height floor with a quieter roof profile.
    # The source loft is interpreted with higher knee walls, explicitly a
    # proposed exterior change rather than an undocumented as-built condition.
    gable('Angled garage bedroom wing',(17.25,5.10),(.70710678,-.70710678),(.70710678,.70710678),12.2,8.45,6.23,8.65,M)
    for x,y in [(4.00,.0),(19.85,15.9),(0.0,8.4),(28.4,.2)]:
        box('Rainwater leader',(x,y,1.45),(.065,.065,2.9),M['dark'],.009)

def build_decks(M):
    g.collection('08 Structure | two rear decks and exposed walkout')
    for z in [0,3.25]:
        rects=[(8.78,16.1,19.43,19.39)] if z==0 else [(8.78,15.60,19.43,19.39),(13.20,12.12,19.43,15.60)]
        for x0,y0,x1,y1 in rects:
            box('Rear terrace structural slab',((x0+x1)/2,(y0+y1)/2,z-.16),(x1-x0,y1-y0,.32),M['dark'],.018)
            count=math.ceil((y1-y0)/.145)
            for i in range(count):box('Rear terrace ash decking',((x0+x1)/2,y0+(i+.5)*(y1-y0)/count,z+.009),(x1-x0-.012,(y1-y0)/count-.009,.028),M['deck'],.003)
        guard('Rear terrace guard',(8.78,19.39),(19.43,19.39),z,M)
        guard('West return guard',(8.78,16.1 if z==0 else 15.60),(8.78,19.39),z,M)
        guard('East return guard',(19.43,16.1 if z==0 else 12.12),(19.43,19.39),z,M)
    for x in [8.9,14.12,19.32]:
        box('Continuous rear brick pier',(x,19.12,.075),(.38,.38,6.45),M['brick'],.006)
        box('Pier stone coping',(x,19.12,3.36),(.47,.47,.10),M['stone'],.005)
    # Rectangular geometry replaces the scalloped/bowed historical deck line.
    # Rear patio and stair back to the lawn are supplied by the site module.

def build_entry(M):
    g.collection('05 Arrival | sheltered timber entrance')
    box('Thin folded entry canopy',(6.08,2.07,3.02),(3.52,1.86,.14),M['dark'],.015)
    for x in [4.5,7.6]:box('Entry timber canopy upright',(x,1.30,1.43),(.13,.13,2.86),M['cedar'],.009)
