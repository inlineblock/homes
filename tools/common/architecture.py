import bpy,math
from mathutils import Vector
from . import geometry as g
from .geometry import box,rod,F
def mesh(name,vertices,faces,mat):
    d=bpy.data.meshes.new(name);d.from_pydata([[v*F for v in co] for co in vertices],[],faces);d.materials.append(mat);o=bpy.data.objects.new(name,d);g.ACTIVE.objects.link(o);return o
def pitched_plate(name,x1,x2,y1,y2,z1,z2,mat,thickness=.22):
    v=[(x1,y1,z1),(x2,y1,z2),(x2,y2,z2),(x1,y2,z1)]
    return mesh(name,v+[(x,y,z-thickness) for x,y,z in v],[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],mat)
def beam(name,a,b,width,depth,mat):
    delta=Vector(b)-Vector(a);o=box(name,(Vector(a)+Vector(b))/2,(width,depth,delta.length),mat,.018);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o
def glass_wall(name,a,b,head,glass,frame,sill=.1,panels=None):
    length=math.dist(a,b);n=panels or max(1,round(length/4));dx=b[0]-a[0];dy=b[1]-a[1]
    for i in range(n+1):
        x=a[0]+dx*i/n;y=a[1]+dy*i/n;box(name+' mullion',(x,y,(head+sill)/2),(.13,.13,head-sill),frame,.005)
    for z in [sill,head]:beam(name+' rail',(*a,z),(*b,z),.12,.12,frame)
    for i in range(n):
        cx=a[0]+dx*(i+.5)/n;cy=a[1]+dy*(i+.5)/n
        box(name+' glazing',(cx,cy,(head+sill)/2),(abs(dx)/n-.12 if dx else .022,abs(dy)/n-.12 if dy else .022,head-sill-.14),glass)
def interior_wall(name,a,b,openings,mat,height=9):
    length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length;cursor=0
    def part(start,end,z,h):
        if end<=start:return
        mid=(start+end)/2;box(name,(a[0]+ux*mid,a[1]+uy*mid,z+h/2),((end-start) if ux else .35,(end-start) if uy else .35,h),mat,.01)
    for off,w in openings:
        part(cursor,off,0,height);part(off,off+w,7.5,height-7.5);cursor=off+w
    part(cursor,length,0,height)
