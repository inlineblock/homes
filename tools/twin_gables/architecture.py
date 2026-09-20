"""Continuous paired gables, honest openings and exact-fit envelope."""
import math
import bpy
from common import geometry as g
from common.geometry import box,rod,F
from common.architecture import mesh,pitched_plate,beam,glass_wall,interior_wall
from common.timber_materials import grain_uv
from assets import put
PLAN_WALLS=[]
POCKETS=[]
from design import DEPTH,EAVE,RIDGE,CEILING_EAVE,CEILING_RIDGE,ROOMS,WALLS

def woodbox(name,loc,size,mat):
 o=box(name,loc,size,mat,.012);grain_uv(o);return o

def facade(name,a,b,openings,M,height=12.2):
 """Openings along an axis wall as (start,end,sill,head), no buried glazing."""
 PLAN_WALLS.append({'name':name,'a':a,'b':b,'openings':[{'offset':q[0],'width':q[1]-q[0],'sill':q[2],'head':q[3],'type':'window'} for q in openings]})
 length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
 def panel(l,r,z1,z2):
  if r-l<.005 or z2-z1<.005:return
  mid=(l+r)/2;cx=a[0]+ux*mid;cy=a[1]+uy*mid
  box(name+' insulated wall',(cx,cy,(z1+z2)/2),(r-l if ux else .42,r-l if uy else .42,z2-z1),M['plaster'],.009)
  # Outside face on west/east/front; rear wall is mostly glass.
  outside=-1 if name.startswith(('West','Front')) else 1
  count=max(1,math.ceil((r-l)/.48));step=(r-l)/count
  for i in range(count):
   t=l+(i+.5)*step;x=a[0]+ux*t;y=a[1]+uy*t
   if ux:y+=outside*.24
   else:x+=outside*.24
   woodbox(name+' cedar board',(x,y,(z1+z2)/2),(step-.018 if ux else .07,step-.018 if uy else .07,z2-z1),M['cedar'])
 cursor=0
 for lo,hi,sill,head in sorted(openings):
  panel(cursor,lo,0,height);panel(lo,hi,0,sill);panel(lo,hi,head,height)
  glass_wall(name+' window',(a[0]+ux*lo,a[1]+uy*lo),(a[0]+ux*hi,a[1]+uy*hi),head,M['glass'],M['dark'],sill)
  cursor=hi
 panel(cursor,length,0,height)

def door(name,a,b,M,height=8.5):
 # Open leaf hinged at a,45deg; true opening remains in partition.
 ax,ay=a;bx,by=b;dx=bx-ax;dy=by-ay;width=math.hypot(dx,dy)
 if 'mechanical access' in name:
  for dx in [-2,2]:woodbox(name+' removable service panel',((ax+bx)/2+dx,ay,height/2),(3.94,.10,height),M['oak'])
  return
 if 'WC pocket' in name or (abs(ax-19.75)<.01 and 29.9<ay<30.1) or (abs(ax-48.25)<.01 and 33.9<ay<34.1):
  leaf=woodbox(name+' recessed sliding leaf',(ax,by+width/2-.12,height/2),(.12,width-.08,height),M['oak']);POCKETS.append(leaf)
  return
 ang=math.atan2(dy,dx)+math.radians(-55 if abs(ax-48.25)<.01 or 'Pantry kitchen' in name else 55)
 cx=ax+math.cos(ang)*width/2;cy=ay+math.sin(ang)*width/2
 o=woodbox(name+' open door',(cx,cy,height/2),(width-.08,.13,height),M['oak']);o.rotation_euler.z=ang
 o['ifc_class']='IfcDoor'
 o['hinge_xy_ft']=[ax,ay];o['door_width_ft']=width-.08;o['closed_angle']=math.atan2(dy,dx);o['swing_sign']=-1 if abs(ax-48.25)<.01 or 'Pantry kitchen' in name else 1
 # Lever shares same local operation axis; generic pinned hardware.
 hx=ax+math.cos(ang)*(width-.3);hy=ay+math.sin(ang)*(width-.3)
 normal=(-math.sin(ang),math.cos(ang))
 front=put(name+' lever','hardware','door-lever-satin-bronze',(hx-normal[0]*.07,hy-normal[1]*.07,3.15),ang)
 front.rotation_euler.y=math.pi;front['door_owner']=o.name
 back=put(name+' opposite lever','hardware','door-lever-satin-bronze',(hx+normal[0]*.07,hy+normal[1]*.07,3.15),ang+math.pi)
 back['door_owner']=o.name
 rod(name+' conceptual latch spindle',(hx-normal[0]*.07,hy-normal[1]*.07,3.15),(hx+normal[0]*.07,hy+normal[1]*.07,3.15),.022,M['dark'])

def partition(name,a,b,openings,M):
 # Height10, door8.5ft, no hidden transom void.
 PLAN_WALLS.append({'name':name,'a':a,'b':b,'openings':[{'offset':q[0],'width':q[1],'type':'removable panels' if 'mechanical access' in name else 'pocket' if 'WC pocket' in name or ('West gallery' in name and q[0]==29.75) or ('East gallery' in name and q[0]==33.75) else 'door','angle_degrees':-55 if name.startswith('East gallery') or name=='Pantry kitchen' else 55} for q in openings]})
 length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length;cursor=0
 for off,w in openings+[(length,0)]:
  if off>cursor:
   mid=(cursor+off)/2;box(name,(a[0]+ux*mid,a[1]+uy*mid,5),(off-cursor if ux else .25,off-cursor if uy else .25,10),M['plaster'],.01)
  if w:
   mid=off+w/2;box(name+' lintel',(a[0]+ux*mid,a[1]+uy*mid,9.25),(w if ux else .25,w if uy else .25,1.5),M['plaster'])
   door(name, (a[0]+ux*off,a[1]+uy*off),(a[0]+ux*(off+w),a[1]+uy*(off+w)),M)
  cursor=off+w

def sliding(name,a,b,head,M,panels=5,open_panel=None):
 """One sliding leaf is parked over its adjacent fixed leaf; frame gap stays open."""
 PLAN_WALLS.append({'name':name,'a':a,'b':b,'openings':[{'offset':0,'width':math.dist(a,b),'type':'sliding glazing'}]})
 length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length;step=length/panels
 chosen=panels//2 if open_panel is None else open_panel
 for i in range(panels):
  start=i*step
  if i==chosen:start-=step
  # Parked moving leaf has separate track depth, no coincident panes.
  depth=.16 if i==chosen else 0
  aa=(a[0]+ux*start-uy*depth,a[1]+uy*start+ux*depth)
  bb=(aa[0]+ux*step,aa[1]+uy*step)
  glass_wall(name+(' open parked leaf' if i==chosen else ' fixed glazed leaf'),aa,bb,head,M['glass'],M['dark'],.08,panels=1)
  if i==chosen:
   hx=aa[0]+ux*(step-.25);hy=aa[1]+uy*(step-.25)
   rod(name+' sliding handle',(hx,hy,3),(hx,hy,4.2),.025,M['dark'])
 beam(name+' continuous upper track',(*a,head+.08),(*b,head+.08),.20,.12,M['dark'])
 # Architectural concept threshold, drainage selection unresolved.
 beam(name+' recessed lower track',(*a,.02),(*b,.02),.12,.04,M['dark'])

def build(M):
 g.collection('02 Architecture | floors')
 for name,loc,size in [('West wing',(12,30,-.3),(24,60,.6)),('East wing',(56,30,-.3),(24,60,.6)),('Front link',(34,3,-.3),(20,6,.6)),('Rear link',(34,51,-.3),(20,18,.6))]:box(name+' floor',loc,size,M['stone'],.01)
 g.collection('01 Architecture | walls and glazing')
 facade('West side',(0,0),(0,60),[(3,12,3,10),(17,26,8.5,10),(30,40,3,10),(44,58,.15,10)],M)
 facade('East side',(68,0),(68,60),[(3,12,3,10),(17,26,8.5,10),(34,40,7,10),(44,48,7,10),(54,58,7,10)],M)
 for x in [0,44]:
  facade('Front wing',(x,0),(x+24,0),[(8.7,15.3,.2,9.4)],M,height=10.2)
  put('Fixed front privacy screen','openings','angled-cedar-privacy-screen-2000x2800',(x+12,-1.6,.2))
  for ya,label in [(0,'Front'),(60,'Rear')]:
   if ya==60:sliding('Rear gable garden slider',(x+.45,ya),(x+23.55,ya),10.2,M,panels=5)
   mesh(label+' gable clerestory glass',[(x+.4,ya,10.3),(x+23.6,ya,10.3),(x+23.6,ya,12.0),(x+12,ya,17.3),(x+.4,ya,12.0)],[(0,1,2,3,4)],M['glass'])
   for a,b in [((x+.35,ya,10.25),(x+23.65,ya,10.25)),((x+.35,ya,12.05),(x+12,ya,17.4)),((x+12,ya,17.4),(x+23.65,ya,12.05)),((x+12,ya,10.25),(x+12,ya,17.4))]:beam(label+' gable bronze frame',a,b,.15,.15,M['dark'])
   for xx in [x+6,x+18]:beam(label+' clerestory vertical',(xx,ya,10.25),(xx,ya,14.65),.11,.11,M['dark'])
 for x1,x2 in [(24,32),(36,44)]:facade('Front entry',(x1,0),(x2,0),[],M,12)
 woodbox('Opaque entry pivot door',(34,-.04,4.5),(3.94,.24,9),M['cedar'])
 woodbox('Entry timber header',(34,-.02,10.5),(4,.48,3),M['cedar']);rod('Entry bronze pull',(35.2,-.24,3),(35.2,-.24,4.8),.035,M['dark'])
 sliding('Entry court reveal',(24,6),(44,6),10.8,M,panels=5)
 PLAN_WALLS.extend([{'name':'West court glazing','a':(24,6),'b':(24,42),'openings':[{'offset':0,'width':36,'type':'fixed glazing'}]},{'name':'East court glazing','a':(44,6),'b':(44,42),'openings':[{'offset':0,'width':36,'type':'fixed glazing'}]},{'name':'Opaque entry pivot door','a':(32,0),'b':(36,0),'openings':[{'offset':0,'width':4,'type':'door','state':'closed'}]}])
 glass_wall('West gallery court',(24,6),(24,42),10.2,M['glass'],M['dark'],.12,panels=9)
 glass_wall('East gallery court',(44,6),(44,42),10.2,M['glass'],M['dark'],.12,panels=9)
 sliding('Dining court opening',(24,42),(44,42),10.8,M,panels=5)
 sliding('Dining garden opening',(24,60),(44,60),10.8,M,panels=5)
 for name,a,b,openings in WALLS:partition(name,a,b,openings,M)
 for x in [8,56]:
  partition('Ensuite enclosed WC front',(x,21.5),(x+4.4,21.5),[],M)
  partition('Ensuite WC pocket',(x+4.4,21.5),(x+4.4,27.875),[(.5,3)],M)
 # Hollow pocketreservations around actuallyparked leaves; no leaf buried in solidwall.
 for leaf in POCKETS:
  cutter=box('Temporary door pocket cavity',(leaf.location.x/F,leaf.location.y/F,4.325),(.16,3.10,8.65))
  for wall in list(bpy.context.scene.objects):
   if wall.type!='MESH' or wall==cutter or wall==leaf or 'recessed sliding' in wall.name or wall.library:continue
   if not any(c.name=='01 Architecture | walls and glazing' for c in wall.users_collection):continue
   if abs(wall.location.x-leaf.location.x)>F*.3 or abs(wall.location.y-leaf.location.y)>F*3:continue
   if 'glazing' in wall.name or 'door' in wall.name or 'lever' in wall.name:continue
   mod=wall.modifiers.new('Actual hollow pocket reservation','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
   bpy.context.view_layer.objects.active=wall;bpy.ops.object.modifier_apply(modifier=mod.name)
  bpy.data.objects.remove(cutter,do_unlink=True)
 g.collection('09 Roof | continuous twin gables')
 for cx in [12,56]:
  for x1,x2,z1,z2 in [(cx-13.5,cx,EAVE-.70,RIDGE),(cx,cx+13.5,RIDGE,EAVE-.70)]:
   pitched_plate('Continuous standing seam roof',x1,x2,-3,63,z1,z2,M['roof'],.26)
   for i in range(45):
    y=-3+i*1.5;beam('Roof standing seam',(x1,y,z1+.045),(x2,y,z2+.045),.048,.065,M['roof'])
   for y in [-3,63]:beam('Gable dark fascia',(x1,y,z1-.08),(x2,y,z2-.08),.16,.37,M['roof'])
   for i in range(132):
    ya=-3+i*.5;yb=ya+.486
    o=pitched_plate('Continuous cedar roof lining',x1,x2,ya,yb,z1-.70,z2-.70,M['cedar'],.075);grain_uv(o)
  for x in [cx-13.25,cx+13.25]:
   box('External eave gutter',(x,30,EAVE-.9),(.35,66,.28),M['roof'],.03)
   for y in [1,59]:rod('Rainwater downpipe',(x,y,.3),(x,y,EAVE-.95),.085,M['roof'])
 for y1,y2 in [(-2.5,6.5),(41.5,62.5)]:
  pitched_plate('Low link roof',23.8,44.2,y1,y2,12.6,12.78,M['roof'],.3)
  box('Low link cedar ceiling',(34,(y1+y2)/2,12.09),(20.4,y2-y1,.18),M['cedar'])
  for y in [y1,y2]:box('Link roof front fascia',(34,y,12.55),(20.6,.15,.40),M['roof'])
 for name,(x1,y1,x2,y2),h in ROOMS:
  if h!=10:continue
  o=box(name+' finished flat ceiling',((x1+x2)/2,(y1+y2)/2,10.12),(x2-x1,y2-y1,.24),M['plaster']);o['finished_clear_height_ft']=10.
 g.collection('08 Structure | concealed steel concept with wood covers')
 from mathutils import Vector
 def covered(name,a,b):
  d=Vector(b)-Vector(a);length=d.length*F
  # Library bottom soffit datum follows beam lower chord. LocalX length only.
  o=put(name,'assemblies','cedar-steel-beam-cover-300x400',tuple((Vector(a)+Vector(b))/2))
  o.scale=(length,1,1);o.rotation_euler=d.to_track_quat('X','Z').to_euler();o['ifc_class']='IfcCovering'
  # Hidden conceptual steel fits actual hollow cover, not a solid timber fiction.
  inner=box(name+' concealed steel assumption',(0,0,0),(d.length,.20/F,.29/F),M['dark'])
  from mathutils import Matrix
  inner.matrix_world=o.matrix_world.normalized() @ Matrix.Translation((0,0,.195))
  for end in [-1,1]:
   cap=woodbox(name+' fitted end closure',(0,0,0),(.02/F,.30/F,.40/F),M['cedar'])
   cap.matrix_world=o.matrix_world.normalized() @ Matrix.Translation((end*length/2,0,.20))
  return o
 for cx in [12,56]:
  for y in [-2,8,18,28,38,48,58]:
   for a,b in [((cx-12.6,y,10.45),(cx,y,16.33)),((cx,y,16.33),(cx+12.6,y,10.45))]:covered('Cedar cover on assumed steel rafter',a,b)
   for x in [cx-12.35,cx+12.35]:woodbox('Concept wood-look post finish',(x,y,5.7),(.5,.5,11.4),M['cedar'])
  for ya,yb in [(-3,18),(18,40),(40,63)]:covered('Cedar cover on assumed ridge steel',(cx,ya,16.45),(cx,yb,16.45))
