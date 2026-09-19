"""Dimensioned pavilion shells, openings, positive roof drainage, and circulation."""
import math,json
import bpy
from mathutils import Vector
from common import geometry as g
from common.library import linked_collection
from utils import *
import design as d
OPENINGS=[]

def wall(name,a,b,z,h,mat,th=.24,level='Ground floor'):
 v=Vector(b)-Vector(a);o=box(name,((a[0]+b[0])/2,(a[1]+b[1])/2,z+h/2),(v.length,th,h),mat,.008);o.rotation_euler.z=math.atan2(v.y,v.x)
 return tag(o,'IfcWall',level)

def cut(obj,rect,z0,z1,M):
 x0,y0,x1,y1=rect;c=box('Temporary opening cutter',((x0+x1)/2,(y0+y1)/2,(z0+z1)/2),(x1-x0,y1-y0,z1-z0),M['dark'])
 bpy.context.view_layer.objects.active=obj;m=obj.modifiers.new('Actual aperture','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c
 bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)

def panel_wall(name,a,b,z,h,M,panels,level):
 o=wall(name,a,b,z,h,M['stone'],.26,level)
 v=Vector(b)-Vector(a);length=v.length;u=v/length;norm=Vector((-u.y,u.x));ang=math.atan2(u.y,u.x)
 # Catalog modules on outward facing finish; perimeter cuts retain physical size.
 pitchx=1.225296;pitchz=.615696
 for row in range(math.ceil(h/pitchz)):
  zh=min(.6096,h-row*pitchz)
  for k in range(math.ceil(length/pitchx)):
   w=min(1.2192,length-k*pitchx)
   if min(w,zh)<.03:continue
   mid=Vector(a)+u*(k*pitchx+w/2)+norm*.131
   if abs(w-1.2192)<.001 and abs(zh-.6096)<.001:
    q=instance(name+' linked limestone',panels,(mid.x,mid.y,z+row*pitchz),ang);tag(q,'IfcCovering',level)
   else:
    q=box(name+' perimeter-cut limestone',(mid.x+norm.x*.019,mid.y+norm.y*.019,z+row*pitchz+zh/2),(w,.0381,zh),M['stone'],.0024);q.rotation_euler.z=ang;tag(q,'IfcCovering',level)
 return o

def frame(name,a,b,z,h,M,win,level):
 length=math.dist(a,b);n=max(1,round(length/2.4));u=(Vector(b)-Vector(a))/length
 for i in range(n):
  p=Vector(a)+u*(i+.5)*length/n
  obj=instance(name+' linked glazing',win,(p.x,p.y,z),math.atan2(u.y,u.x),(length/n/2.4,1,h/2.4));tag(obj,'IfcWindow',level)
  obj['approximate_resizing']='Nonuniform concept aperture adaptation; frame sightlines vary from library nominal.'

def facade(name,a,b,z,h,ops,M,win,panels,level='Ground floor',cedar=False):
 length=math.dist(a,b);u=(Vector(b)-Vector(a))/length;cur=0
 def segment(s,e,bottom,top):
  if e-s<.015 or top-bottom<.015:return
  aa=Vector(a)+u*s;bb=Vector(a)+u*e
  if cedar:
   wall(name+' cedar backing',aa,bb,z+bottom,top-bottom,M['cedar'],.24,level)
   normal=Vector((-u.y,u.x))
   wall(name+' interior lining',aa-normal*.135,bb-normal*.135,z+bottom,top-bottom,M['plaster'],.025,level)
   for j in range(math.ceil((e-s)/.145)):
    w=min(.137,e-s-j*.145)
    p=aa+u*(j*.145+w/2)+normal*.13
    obj=box(name+' cedar board',(p.x,p.y,z+bottom+(top-bottom)/2),(w,.025,top-bottom),M['cedar'],.002);obj.rotation_euler.z=math.atan2(u.y,u.x);tag(obj,'IfcCovering',level)
  else:panel_wall(name+' limestone',aa,bb,z+bottom,top-bottom,M,panels,level)
 for start,width,sill,height,kind in sorted(ops):
  segment(cur,start,0,h);segment(start,start+width,0,sill);segment(start,start+width,sill+height,h)
  aa=Vector(a)+u*start;bb=aa+u*width
  OPENINGS.append({'name':name,'a':list(aa),'b':list(bb),'z':z+sill,'height':height,'kind':kind,'level':level})
  if kind=='window':frame(name,aa,bb,z+sill,height,M,win,level)
  elif kind=='door':
   # Door leaf stands ajar and rotates into room with a real clear aperture.
   n=Vector((-u.y,u.x));hinge=aa+u*.05;dv=(u*math.cos(.22)+n*math.sin(.22));p=hinge+dv*(width-.1)/2
   o=box(name+' entry door',(p.x,p.y,z+height/2),(width-.1,.07,height-.04),M['cedar'],.012);o.rotation_euler.z=math.atan2(dv.y,dv.x);tag(o,'IfcDoor',level)
   p2=hinge+dv*(width-.25)+n*.06
   rod('Door pull',(p2.x,p2.y,z+.85),(p2.x,p2.y,z+1.65),.013,M['bronze'])
  cur=start+width
 segment(cur,length,0,h)

def roof(name,r,z,M,level='Ground floor',hole=None):
 x0,y0,x1,y1=r
 o=tag(prism(name+' roof insulation fall',d.rect_poly(r),z,z+.18,M['roof']),'IfcRoof',level)
 # 1:80 fall along Y, high at front, rear collection edge. Not an occupiable terrace.
 for v in o.data.vertices:
  if v.co.z>z+.1:v.co.z+=(y1-v.co.y)/80
 if hole:cut(o,hole,z-.3,z+1,M)
 ceil=tag(box(name+' ceiling',((x0+x1)/2,(y0+y1)/2,z-.065),(x1-x0,y1-y0,.13),M['ceiling']),'IfcCovering',level)
 if hole:cut(ceil,hole,z-.5,z+.5,M)
 for a,b in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:
  tag(wall(name+' slim fascia',a,b,z-.1,.3,M['dark'],.09,level),'IfcMember',level)
 # Rear gutter and drain to planted infiltration strip, conceptual sizing.
 tag(box(name+' rear collection channel',((x0+x1)/2,y1,z+.1),(x1-x0,.18,.1),M['dark']),'IfcBuildingElementProxy',level)
 for xx in [x0+.2,x1-.2]:rod(name+' downpipe',(xx,y1+.08,z+.1),(xx,y1+.08,-.1),.045,M['dark'])
 return ceil

def build_envelope(root,M):
 win=linked_collection(root,'openings','slim-dark-window','v002');panels=linked_collection(root,'surfaces','honed-limestone-wall-panel-4x2','v001')
 g.collection('02 Architecture | occupied slabs')
 for name,r,z in [('Main',d.MAIN,0),('Guest',d.GUEST,0),('Upper',d.UPPER_RECT,3.6),('Garage',d.GARAGE,-.10)]:
  o=tag(prism(name+' occupied slab',d.rect_poly(r),z-.24,z,M['stone'] if name!='Upper' else M['oak']),'IfcSlab','Upper floor' if name=='Upper' else 'Ground floor')
  o['floor_area_role']='garage' if name=='Garage' else 'occupied'
  if name=='Upper':cut(o,d.STAIR_VOID,z-.5,z+.5,M)
 g.collection('01 Architecture | exterior envelope')
 # Faces counter-clockwise with their limestone finish oriented toward outside.
 facade('Main street',(22,0),(10,0),0,3.3,[(.8,1.6,0,3.0,'door'),(3.3,4.5,.06,3.12,'window'),(10,2,.06,3.12,'window')],M,win,panels)
 facade('Main courtyard',(10,0),(10,20),0,3.3,[(.3,1.5,.06,3.12,'window'),(2,1.3,0,3.1,'door'),(3.5,3.3,.06,3.12,'window'),(7,1.3,0,3.1,'door'),(8.5,11.2,.06,3.12,'window')],M,win,panels)
 facade('Main east',(22,20),(22,0),0,3.3,[(.4,2,1.4,1.5,'window'),(6.5,2.5,.7,2.4,'window'),(11,2.1,.7,2.4,'window'),(18.3,1.4,.1,3,'window')],M,win,panels)
 facade('Main rear',(10,20),(22,20),0,3.3,[(.5,2,1.5,1.5,'window'),(7.3,1.1,.9,2.1,'window'),(10,1.4,0,2.6,'door')],M,win,panels)
 facade('Guest street',(0,0),(-8,0),0,3.3,[(2.2,4.8,.06,3.12,'window')],M,win,panels)
 facade('Guest court',(0,12),(0,0),0,3.3,[(.4,3.5,.06,3.12,'window'),(5.2,1.2,0,3.0,'door'),(7.3,1.3,.06,3.12,'window'),(8.8,1.2,0,3,'door'),(10.2,1.3,.06,3.12,'window')],M,win,panels)
 facade('Guest west',(-8,0),(-8,12),0,3.3,[(1,2.4,.7,2.4,'window'),(6,2.4,.7,2.4,'window'),(10.3,1.3,1.7,1.3,'window')],M,win,panels)
 facade('Garage rear',(-8,20),(0,20),-.1,3.4,[(6.3,1.1,0,2.6,'door')],M,win,panels)
 facade('Garage court',(0,20),(0,12),-.1,3.4,[(4.8,1.2,0,2.6,'door')],M,win,panels)
 wall('Garage guest divider',(-8,12),(0,12),0,3.3,M['plaster'])
 # Two actual west door apertures, sectional doors shown closed.
 facade('Garage west',(-8,12),(-8,20),-.1,3.4,[(.6,2.9,0,2.7,'garage'),(4.4,2.9,0,2.7,'garage')],M,win,panels)
 for y in [14.05,17.85]:
  for i in range(5):tag(box('Garage sectional door',(-8,y,-.1+(i+.5)*.54),(.09,2.88,.53),M['cedar'],.007),'IfcDoor')
 for name,a,b,L in [('Upper street',(22,0),(10,0),12),('Upper court',(10,0),(10,17),17),('Upper east',(22,17),(22,0),17),('Upper rear',(10,17),(22,17),12)]:
  if 'street' in name:ops=[(.5,2.9,.25,2.65,'window'),(4.2,3,.25,2.65,'window'),(8,3.5,.25,2.65,'window')]
  elif 'court' in name:ops=[(.8,4.7,.45,2.4,'window'),(8,1.8,1,1.8,'window'),(12.2,1.2,0,2.9,'door'),(13.6,2.2,.45,2.4,'window')]
  elif 'east' in name:ops=[(.7,2.5,.45,2.4,'window'),(6.4,2,.9,1.9,'window'),(13.5,2.5,1.5,1.3,'window')]
  else:ops=[(.6,3.7,.45,2.4,'window'),(7.4,3.8,.45,2.4,'window')]
  facade(name,a,b,3.6,3.0,ops,M,win,panels,'Upper floor',True)
 g.collection('06 Architecture | partitions with door openings')
 for lev,ws in d.PARTITIONS.items():
  z=0 if lev=='ground' else 3.6;level='Ground floor' if lev=='ground' else 'Upper floor';h=3.3 if lev=='ground' else 3
  for name,a,b,ops in ws:
   u=(Vector(b)-Vector(a)).normalized();length=math.dist(a,b);cur=0
   for start,width in ops:
    if start>cur:wall(name,Vector(a)+u*cur,Vector(a)+u*start,z,h,M['plaster'],.14,level)
    wall(name+' lintel',Vector(a)+u*start,Vector(a)+u*(start+width),z+2.35,h-2.35,M['plaster'],.14,level)
    # Open perpendicular leaf stops outside principal clear opening.
    hinge=Vector(a)+u*start;n=Vector((-u.y,u.x));p=hinge+n*(width-.05)/2
    obj=box(name+' open door',(p.x,p.y,z+1.16),(width-.05,.04,2.32),M['oak'],.006);obj.rotation_euler.z=math.atan2(n.y,n.x);tag(obj,'IfcDoor',level)
    cur=start+width
   if length>cur:wall(name,Vector(a)+u*cur,b,z,h,M['plaster'],.14,level)
 g.collection('09 Roof | falls gutters and rooflights')
 # Main lower ceiling is the upper slab except for the rear roof strip.
 ceil=box('Main ceiling below upper', (16,8.5,3.285),(12,17,.03),M['ceiling']);cut(ceil,d.STAIR_VOID,3.0,4,M)
 roof('Main rear single-story', (9.8,17,22.2,20.3),3.3,M,hole=(11.4,17.5,14.9,19.3))
 roof('Cedar upper bar',(9.8,-.2,22.2,17.2),6.65,M,'Upper floor',hole=(17.5,8.2,18.7,12.5))
 roof('Guest pavilion',(-8.2,-.2,.2,12),3.3,M)
 roof('Garage',(-8.2,12,.2,20.2),3.3,M)
 roof('Lanai',(0,-.3,10,5.2),3.3,M)
 for nm,r,z in [('Kitchen rooflight',(11.4,17.5,14.9,19.3),3.6),('Gallery rooflight',(17.5,8.2,18.7,12.5),6.9)]:
  x0,y0,x1,y1=r;box(nm+' glass',((x0+x1)/2,(y0+y1)/2,z),(x1-x0,y1-y0,.018),M['glass'])
  for a,b in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:wall(nm+' curb',a,b,z-.3,.32,M['dark'],.07)
 # Slatted oak kitchen ceiling with the rooflight genuinely cut out.
 for ix in range(60):
  x=10.1+ix*.098
  if x>15.85:break
  if 11.4<x<14.9:segs=[(13.2,17.5),(19.3,19.8)]
  else:segs=[(13.2,19.8)]
  for y0,y1 in segs:box('Kitchen oak ceiling slat',(x,(y0+y1)/2,3.19),(.055,y1-y0,.12),M['oak'],.004)
 # Front stepped thresholds sit on the lower forecourt.
 g.collection('10 Stairs | interior and entry')
 for i in range(3):box('Broad front entry step',(20.4,-(3-i)*.40,-.48+i*.16),(3.1,.42,.16),M['stone'],.008)
 for i in range(3):box('Lanai garden step',(5,-(3-i)*.4,-.48+i*.16),(8.8,.42,.16),M['stone'],.008)
 # Two eleven-riser flights; lower clear landing and upper landing south of opening.
 riser=3.6/22;tread=.28
 for i in range(11):
  box('Lower stair oak tread',(19.7,8.2+(i+.5)*tread,(i+1)*riser-.04),(1.2,tread,.08),M['oak'],.009)
  if i<11:box('Upper stair oak tread',(21.1,11.28-(i+.5)*tread,(12+i)*riser-.04),(1.2,tread,.08),M['oak'],.009)
 box('Stair half landing',(20.4,11.89,1.8-.06),(2.6,1.22,.12),M['oak'],.009)
 for x in [19.18,20.22]:beam('Lower stair steel stringer',(x,8.2,.04),(x,11.3,1.8),.06,.14,M['dark'])
 for x in [20.58,21.62]:beam('Upper stair steel stringer',(x,11.28,1.8),(x,8.2,3.6),.06,.14,M['dark'])
 # Glass guards protect opening edges without blocking upper landing at south.
 for a,b in [((19,8.2),(19,12.5)),((19,12.5),(21.8,12.5)),((21.8,12.5),(21.8,8.2))]:
  wall('Upper stair glass guard',a,b,3.6,1.05,M['glass'],.018,'Upper floor');rod('Guard cap',(a[0],a[1],4.66),(b[0],b[1],4.66),.018,M['bronze'])
 for x,y,z,yy,zz in [(19.06,8.2,1.0,11.28,2.8),(21.74,11.28,2.8,8.2,4.6)]:rod('Stair handrail',(x,y,z),(x,yy,zz),.018,M['bronze'])
 return OPENINGS
