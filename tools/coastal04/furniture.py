"""Detailed original joinery and soft furnishings; geometry in feet."""
import bpy,math,random
from common import geometry as g
from common.geometry import box,cyl,sphere,rod,curve,F

def soft(name,loc,size,mat,r=.12):
    o=box(name,loc,size,mat,r)
    for mod in o.modifiers:
        if mod.type=='BEVEL':mod.segments=8;mod.harden_normals=True
    for face in o.data.polygons:face.use_smooth=True
    return o

def bowl(name,x,y,z,r,mat):
    # Lathed ceramic shell, including a real concave interior.
    profile=[(0,0),(.55,.01),(.9,.16),(1,.42),(.97,.47),(.88,.43),(.78,.18),(.40,.09),(0,.09)]
    verts=[];faces=[];N=64
    for rr,zz in profile:
        for i in range(N):a=i*math.tau/N;verts.append(((x+rr*r*math.cos(a))*F,(y+rr*r*math.sin(a))*F,(z+zz*r)*F))
    for j in range(len(profile)-1):
        for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.materials.append(mat);o=bpy.data.objects.new(name,mesh);g.ACTIVE.objects.link(o)
    for f in mesh.polygons:f.use_smooth=True
    return o

def cabinet_run(name,x1,x2,y,front,M):
    width=x2-x1;count=round(width/2.4);unit=width/count
    box(name+' recessed plinth',((x1+x2)/2,y,.22),(width-.14,2.20,.42),M['dark'],.012)
    box(name+' cabinet carcass',((x1+x2)/2,y,1.6),(width,2.45,2.62),M['oak'],.02)
    for i in range(count):
        x=x1+(i+.5)*unit
        for z,h in [(2.58,.52),(1.91,.75),(.98,1.06)]:
            box(name+' drawer front',(x,y+front*1.255,z),(unit-.035,.09,h),M['oak'],.015)
            box(name+' finger recess',(x,y+front*1.31,z+h/2-.035),(unit-.20,.025,.035),M['dark'],.006)
    box(name+' stone counter',((x1+x2)/2,y,3.025),(width+.16,2.75,.15),M['counter'],.025)

def chair(name,x,y,angle,M):
    objs=[];before=set(bpy.context.scene.objects)
    soft(name+' upholstered seat',(x,y,1.55),(1.75,1.75,.23),M['linen'],.12)
    # Thin arced back with two uprights, actual separate cushions.
    curve(name+' curved oak back',[(x-.85,y+.55,2.55),(x,y+.80,2.68),(x+.85,y+.55,2.55)],.085,M['oak'])
    for dx in [-.70,.70]:
        rod(name+' rear leg',(x+dx,y+.6,0),(x+dx,y+.65,2.55),.06,M['oak'])
        rod(name+' front leg',(x+dx,y-.64,0),(x+dx,y-.60,1.5),.06,M['oak'])
    # Rotate as a group about the chair center.
    from mathutils import Matrix,Vector
    c=Vector((x*F,y*F,0));R=Matrix.Rotation(angle,4,'Z')
    for o in set(bpy.context.scene.objects)-before:o.matrix_world=Matrix.Translation(c)@R@Matrix.Translation(-c)@o.matrix_world

def sofa(name,x,y,M):
    soft(name+' upholstered base',(x,y,.65),(11.4,3.5,.68),M['linen'],.20)
    soft(name+' rounded back',(x,y-1.42,1.60),(11.4,.55,1.70),M['linen'],.23)
    for dx in [-5.40,5.40]:soft(name+' curved arm',(x+dx,y,1.28),(.6,3.45,1.55),M['linen'],.24)
    for i in range(3):
        xx=x+(i-1)*3.45
        soft(name+' seat cushion',(xx,y+.08,1.08),(3.34,2.75,.40),M['linen'],.18)
        soft(name+' back cushion',(xx,y-1,1.88),(3.35,.53,1.38),M['linen'],.18)
        curve(name+' cushion welt',[(xx-1.55,y-1.12,1.20),(xx-1.55,y+1.35,1.20),(xx+1.55,y+1.35,1.20),(xx+1.55,y-1.12,1.20)],.012,M['linen'])
    for dx in [-4.4,4.4]:
        o=soft(name+' accent pillow',(x+dx,y-.4,1.84),(1.7,.46,1.65),M['blue'],.21);o.rotation_euler=(.15,.13,(-.13 if dx<0 else .13))
    for dx in [-4.8,4.8]:
        for yy in [y-1.1,y+1.1]:cyl(name+' concealed foot',(x+dx,yy,.18),.09,.3,M['oak'])

def bed(name,x,y,w,M):
    box(name+' bed frame',(x,y,.52),(w+.35,7.3,.62),M['oak'],.08)
    soft(name+' mattress',(x,y,1.0),(w,7,.65),M['linen'],.22)
    soft(name+' upholstered headboard',(x,y-3.55,2.02),(w+.65,.26,3.5),M['linen'],.12)
    soft(name+' duvet',(x,y+.45,1.38),(w+.13,5.85,.24),M['linen'],.15)
    for dx in [-w*.25,w*.25]:soft(name+' pillow',(x+dx,y-2.25,1.52),(w*.43,1.6,.35),M['porcelain'],.18)
    soft(name+' blue folded throw',(x,y+2.1,1.57),(w+.18,1.6,.10),M['blue'],.07)
    for dx in [-w/2-1,w/2+1]:
        box(name+' bedside chest',(x+dx,y-2.5,1.0),(1.55,1.7,1.95),M['oak'],.06)
        cyl(name+' bedside lamp base',(x+dx,y-2.5,2.10),.28,.25,M['porcelain'])
        soft(name+' bedside lamp shade',(x+dx,y-2.5,2.6),(.8,.8,.65),M['linen'],.3)

def kitchen(M):
    g.collection('03 Kitchen | interior exterior joinery')
    cabinet_run('Interior serving',47.8,63.3,38.43,-1,M)
    cabinet_run('Exterior serving',47.8,63.3,41.61,1,M)
    counter=bpy.data.objects['Exterior serving stone counter'];counter.location.y=42.20*F;counter.dimensions.y=3.93*F
    # Stone bridge underneath the sliding sill, joining the two distinct cabinet runs.
    box('Continuous stone sill serving bridge',(55.55,40.02,3.025),(15.65,.61,.15),M['counter'],.012)
    # Island with true undermount sink opening.
    cabinet_run('Island',49.5,59.5,29.5,1,M)
    box('Island stool-side cabinet',(54.5,28.28,1.54),(10,.10,2.74),M['oak'],.018)
    # Replace run worktop with a deeper slab and sink cutout.
    bpy.data.objects.remove(bpy.data.objects['Island stone counter'],do_unlink=True)
    top=box('Island quartzite slab',(54.5,29.2,3.025),(10.25,4.4,.15),M['counter'],.025)
    cut=box('Temporary sink cutter',(56.5,29.6,3.02),(2.25,1.6,.8),M['steel'],.1)
    bpy.context.view_layer.objects.active=top;mod=top.modifiers.new('Real sink opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    box('Sink basin bottom',(56.5,29.6,2.4),(2.24,1.59,.06),M['steel'],.10)
    for dx in [-1.12,1.12]:box('Sink basin end',(56.5+dx,29.6,2.71),(.045,1.6,.60),M['steel'],.018)
    for dy in [-.80,.80]:box('Sink basin side',(56.5,29.6+dy,2.71),(2.24,.045,.60),M['steel'],.018)
    cyl('Sink drain',(56.5,29.6,2.44),.10,.015,M['dark'])
    curve('Swan-neck kitchen faucet',[(56.5,30.65,3.10),(56.5,30.65,4.2),(56.5,30.1,4.55),(56.5,29.6,4.13)],.045,M['steel'])
    rod('Mixer handle',(56.9,30.65,3.08),(56.9,30.65,3.47),.03,M['steel'])
    # East wall appliances leave a broad aisle to the island.
    for y in [23,25.6,28.2,30.8,33.4,36]:
        box('East oak cabinetry',(66.5,y,1.6),(2.5,2.55,2.7),M['oak'],.025)
        for z in [.85,1.8,2.6]:box('East drawer face',(65.20,y,z),(.10,2.48,.68),M['oak'],.013)
    box('East countertop',(66.45,30.1,3.02),(2.85,15.8,.16),M['counter'],.02)
    box('Induction glass',(66.3,32.5,3.12),(1.85,2.5,.04),M['dark'],.03)
    for y in [31.9,33.1]:
        for x in [65.9,66.7]:cyl('Induction zone',(x,y,3.146),.27,.004,M['steel'],64)
    box('Concealed extraction plaster hood',(66.85,32.5,7.05),(2.05,3.8,2.3),M['plaster'],.02)
    for y in [22.6,24.1]:
        box('Integrated fridge tall door',(65.06,y,4.3),(.15,1.44,8.55),M['oak'],.02)
        rod('Fridge pull',(64.94,y-.5,3.7),(64.94,y-.5,5),.023,M['bronze'])
    box('Fridge housing',(66.4,23.35,4.3),(2.7,3.05,8.6),M['oak'],.025)
    # Shelf and carefully sparse styling.
    box('East floating oak shelf',(66.6,37,5.4),(2,3.6,.14),M['oak'],.016)
    bowl('Serving fruit bowl',50,38.1,3.12,.65,M['porcelain'])
    for i in range(5):sphere('Fresh green pear',(49.7+(i%3)*.25,38+(i//3)*.22,3.31),(.16,.16,.22),M['leaf'])
    box('Oak cutting board',(51.2,29.4,3.13),(1.45,1.05,.08),M['oak'],.1)
    bowl('Breakfast ceramic',52.3,29.2,3.12,.35,M['porcelain'])
    for x in [50.4,53.9,57.4]:
        cyl('Island pendant canopy',(x,29.2,10.33),.18,.12,M['bronze'])
        rod('Island pendant cord',(x,29.2,10.27),(x,29.2,6.3),.009,M['dark'])
        sphere('Pendant opal globe',(x,29.2,6.23),(.31,.31,.31),M['porcelain'])
        # shallow disc shade
        cyl('Wide champagne pendant shade',(x,29.2,6.40),.62,.055,M['bronze'],64)


def rooms(M):
    g.collection('04 Furnishings | living dining bedrooms')
    # Large tactile rug and lower furniture keep the glazing visually dominant.
    box('Living wool rug',(13,31.6,.025),(20,12,.04),M['linen'],.03)
    # Small physical fringes rather than a flat monotone rectangle.
    for i in range(80):
        x=3.1+i*.25
        for yy in [25.52,37.68]:rod('Rug fringe',(x,yy-.12,.04),(x+.01,yy+.12,.04),.009,M['linen'])
    sofa('Living sofa',13,27.7,M)
    soft('Living chaise cushion',(7.7,31.6,1.07),(3.5,5.3,.42),M['linen'],.22)
    soft('Living chaise base',(7.7,31.6,.66),(3.5,5.3,.6),M['linen'],.20)
    box('Low limestone coffee table',(14,32.7,1.10),(5.8,3.4,.23),M['stone'],.48)
    for x in [12.3,15.7]:box('Coffee table pedestal',(x,32.7,.54),(.65,2.3,1.0),M['stone'],.12)
    box('Coffee table art book',(14.2,32.9,1.25),(1.3,1,.08),M['blue'],.015)
    bowl('Coffee table ceramic',12.8,32.7,1.22,.40,M['porcelain'])
    # Dining table with a thick rounded solid-oak edge.
    soft('Dining oval oak tabletop',(35,29.1,2.48),(8.5,3.8,.20),M['oak'],.50)
    for x in [32.2,37.8]:box('Dining sculptural trestle',(x,29.1,1.21),(.5,2.35,2.42),M['oak'],.10)
    for x in [32.4,35,37.6]:
        chair('Dining chair',x,26.25,math.pi,M);chair('Dining chair',x,31.95,0,M)
    bowl('Dining centerpiece',35,29.1,2.6,.72,M['porcelain'])
    for name,x,y,w in [('Primary',8.6,6.9,6.5),('Guest 02',30.5,6.7,5),('Guest 03',47.5,6.7,5)]:bed(name,x,y,w,M)
    # Bath fixtures, clear door zones, and wardrobe/Laundry.
    for prefix,x,y in [('Primary',0,16),('Guest',60,0)]:
        box(prefix+' shower tray',(x+2.6,y+6.0,.07),(4.3,3.6,.12),M['stone'],.02)
        from common.architecture import glass_wall
        glass_wall(prefix+' shower screen',(x+.5,y+4.15),(x+2.4,y+4.15),7.5,M['glass'],M['bronze'])
        rod(prefix+' shower riser',(x+.7,y+7.6,3),(x+.7,y+7.6,7.0),.035,M['steel'])
        cyl(prefix+' shower head',(x+1.0,y+7.5,7.0),.3,.05,M['steel'])
        box(prefix+' vanity',(x+6.5,y+6.65,1.45),(2.2,2.2,2.7),M['oak'],.03)
        bowl(prefix+' basin',x+6.5,y+6.65,2.86,.73,M['porcelain'])
        sphere(prefix+' WC bowl',(x+(8.2 if prefix=='Primary' else 6.5),y+(2.0 if prefix=='Primary' else 2.6),1.1),(.60,.92,.50),M['porcelain'])
        box(prefix+' WC cistern',(x+(8.2 if prefix=='Primary' else 6.5),y+(1.35 if prefix=='Primary' else 1.95),1.7),(1.15,.55,1.7),M['porcelain'],.12)
    box('Dressing wardrobe',(16.7,20.3,4.4),(2.2,6.6,8.8),M['oak'],.03)
    box('Dressing rear wardrobe',(12.65,22.75,4.4),(4.9,2.2,8.8),M['oak'],.03)
    for x in [63,66]:
        box('Laundry appliance',(x,14.3,1.55),(2.65,2.5,3.1),M['porcelain'],.06)
        o=cyl('Laundry round door',(x,13.02,1.7),.8,.08,M['dark'],64);o.rotation_euler.x=math.pi/2
    box('Laundry oak worktop',(64.5,14.3,3.17),(5.85,2.7,.16),M['oak'],.02)
