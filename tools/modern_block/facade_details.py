"""Room-specific projecting façade details; repeated screens remain linked assets."""
from common import geometry as g
from common.library import linked_collection
from utils import box, tag, instance
import design as d


def build_facade_details(root,M,panels):
 from envelope import panel_wall
 g.collection('01 Architecture | arrival and privacy depth')
 # The occupied upper projection shelters the entrance. Its continuous cedar
 # soffit is authored with the envelope; this portal has no separate roof.
 portal_depth=-d.UPPER_FRONT
 portal_head_height=.22
 portal_clear=d.GROUND_CLEAR-portal_head_height
 tag(box('Arrival limestone portal header',
         (20.6,d.UPPER_FRONT/2,d.GROUND_CLEAR-portal_head_height/2),
         (2.8,portal_depth,portal_head_height),M['stone'],.012),'IfcBeam')
 panel_wall('Arrival east stone return',(21.89,d.UPPER_FRONT),(21.89,0),
            0,portal_clear,M,panels,'Ground floor')
 # The west edge remains open toward the living-room garden.
 tag(box('Arrival supported level landing',(20.45,-.7,-.265),(3.1,1.4,.53),M['stone'],.008),'IfcSlab')
 for prefix,cx,back,width in [('Entry',20.45,-1.4,3.1),('Lanai',5,0,8.8)]:
  for i in range(3):
   top=-.53+(i+1)*(.53/3)
   obj=box(prefix+' equal-riser garden step',(cx,back-1.2+(i+.5)*.4,(-.53+top)/2),(width,.4,top+.53),M['stone'],.006)
   obj['riser_m']=.53/3;obj['tread_depth_m']=.4
 # Deep external bedroom reveals preserve the full room footprint.
 for x in [10.50,16.60]:
  box('Bedroom cedar reveal jamb',(x,d.UPPER_FRONT-.225,d.UPPER+1.58),(.20,.45,2.86),M['cedar'],.006)
 for z in [d.UPPER+.15,d.UPPER+2.96]:
  box('Bedroom dark reveal edge',(13.55,d.UPPER_FRONT-.225,z),(6.30,.45,.10),M['dark'],.006)
 screen=linked_collection(root,'openings','angled-cedar-privacy-screen-2000x2800','v001')
 for x in [18.5,20.5]:
  obj=instance('Primary bath fixed privacy screen',screen,(x,d.UPPER_FRONT-.60,d.UPPER+.05))
  obj['service_gap_m']=.35;tag(obj,'IfcShadingDevice','Upper floor')
 for x in [17.5,19.5,21.5]:
  for z in [d.UPPER+.09,d.UPPER+2.81]:box('Privacy screen demountable bracket',(x,d.UPPER_FRONT-.28,z),(.045,.39,.045),M['dark'],.004)
 # Functional exterior stone pier carries the flue past the occupied upper WC.
 x0,y0,x1,y1=d.EAST_FLUE_PIER
 pier_base=-.53
 pier_top=d.UPPER_ROOF_Z+.28
 pier_height=pier_top-pier_base
 tag(box('East flue pier core',((x0+x1)/2,(y0+y1)/2,(pier_base+pier_top)/2),(x1-x0,y1-y0,pier_height),M['stone']),'IfcWall')
 for a,b in [((x1,y1),(x1,y0)),((x1,y0),(x0,y0)),((x0,y1),(x1,y1))]:
  panel_wall('East flue pier cladding',a,b,pier_base,pier_height,M,panels,'Ground floor')
 # Cap top is 360mm above the upper roof datum, seated on the pier core.
 box('East flue pier dark cap',((x0+x1)/2,(y0+y1)/2,d.UPPER_ROOF_Z+.32),(.92,2.10,.08),M['dark'],.008)
 # Slim projecting surrounds align the two stair windows; floor band stays legible.
 for z,h in [(.1,3.45),(d.UPPER+.45,2.4)]:
  for y in [8.32,12.28]:box('Stair bay bronze jamb',(22.18,y,z+h/2),(.40,.12,h+.14),M['dark'],.005)
  for zz in [z-.06,z+h+.06]:box('Stair bay bronze head sill',(22.18,10.3,zz),(.40,4.08,.12),M['dark'],.005)
