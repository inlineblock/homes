"""Original reusable furniture authoring primitives; feet in, meters stored."""
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
