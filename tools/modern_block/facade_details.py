"""Room-specific projecting façade details; repeated screens remain linked assets."""
from common import geometry as g
from common.library import linked_collection
from utils import box, tag, instance
import design as d


def build_facade_details(root,M,panels):
 from envelope import panel_wall
 g.collection('01 Architecture | arrival and privacy depth')
 # Entry remains on its original line; the sheltered outdoor room projects.
 tag(box('Arrival limestone canopy',(20.6,-.675,3.27),(2.8,1.35,.30),M['stone'],.012),'IfcRoof')
 canopy=box('Arrival positive fall roof',(20.6,-.675,3.445),(2.8,1.35,.05),M['roof'])
 for v in canopy.data.vertices:
  if v.co.z>0:v.co.z+=(-v.co.y+.675)/80
 box('Arrival cedar soffit',(20.6,-.675,3.108),(2.36,1.29,.025),M['cedar'],.003)
 panel_wall('Arrival east stone return',(21.89,-1.35),(21.89,0),0,3.12,M,panels,'Ground floor')
 # The west edge remains open toward the living-room garden.
 tag(box('Arrival supported level landing',(20.45,-.7,-.265),(3.1,1.4,.53),M['stone'],.008),'IfcSlab')
 for prefix,cx,back,width in [('Entry',20.45,-1.4,3.1),('Lanai',5,0,8.8)]:
  for i in range(3):
   top=-.53+(i+1)*(.53/3)
   obj=box(prefix+' equal-riser garden step',(cx,back-1.2+(i+.5)*.4,(-.53+top)/2),(width,.4,top+.53),M['stone'],.006)
   obj['riser_m']=.53/3;obj['tread_depth_m']=.4
 # Deep external bedroom reveals preserve the full room footprint.
 for x in [10.50,16.60]:
  box('Bedroom cedar reveal jamb',(x,-.225,5.18),(.20,.45,2.86),M['cedar'],.006)
 for z in [3.75,6.56]:
  box('Bedroom dark reveal edge',(13.55,-.225,z),(6.30,.45,.10),M['dark'],.006)
 screen=linked_collection(root,'openings','angled-cedar-privacy-screen-2000x2800','v001')
 for x in [18.5,20.5]:
  obj=instance('Primary bath fixed privacy screen',screen,(x,-.60,3.65))
  obj['service_gap_m']=.35;tag(obj,'IfcShadingDevice','Upper floor')
 for x in [17.5,19.5,21.5]:
  for z in [3.69,6.41]:box('Privacy screen demountable bracket',(x,-.28,z),(.045,.39,.045),M['dark'],.004)
 # Functional exterior stone pier carries the flue past the occupied upper WC.
 x0,y0,x1,y1=d.EAST_FLUE_PIER
 tag(box('East flue pier core',((x0+x1)/2,(y0+y1)/2,3.21),(x1-x0,y1-y0,7.48),M['stone']),'IfcWall')
 for a,b in [((x1,y1),(x1,y0)),((x1,y0),(x0,y0)),((x0,y1),(x1,y1))]:
  panel_wall('East flue pier cladding',a,b,-.53,7.48,M,panels,'Ground floor')
 box('East flue pier dark cap',(22.42,3.55,6.97),(.92,2.10,.08),M['dark'],.008)
 # Slim projecting surrounds align the two stair windows; floor band stays legible.
 for z,h in [(.1,3.1),(4.05,2.4)]:
  for y in [8.32,12.28]:box('Stair bay bronze jamb',(22.18,y,z+h/2),(.40,.12,h+.14),M['dark'],.005)
  for zz in [z-.06,z+h+.06]:box('Stair bay bronze head sill',(22.18,10.3,zz),(.40,4.08,.12),M['dark'],.005)
