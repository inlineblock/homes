"""Furnished equal suites and complete cooking/storage program using library pins."""
import math
import bpy
from common import geometry as g
from common.geometry import box,rod,area,F
from common.timber_materials import grain_uv
from assets import put
from architecture import woodbox

def counter(name,rect,M,holes=(),z=3):
 x1,y1,x2,y2=rect;o=box(name,((x1+x2)/2,(y1+y2)/2,z-.06),(x2-x1,y2-y1,.12),M['stone'])
 for x,y,w,d in holes:
  cutter=box('Temporary fitted worktop cutout',(x,y,z),(w,d,.5));m=o.modifiers.new('Real equipment mounting cutout','BOOLEAN');m.operation='DIFFERENCE';m.object=cutter
  bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
 b=o.modifiers.new('Eased stone edge','BEVEL');b.width=.003;b.segments=3
 return o

def build(M):
 g.collection('03 Kitchen | complete shared appliances and cabinetry')
 # Front of east-wall equipment faces west.48infridge south of island.
 put('Wide integrated refrigerator freezer','appliances','smoked-oak-panel-ready-fridge-48in',(66.35,44.35,0),-math.pi/2)
 put('Cooking landing drawers south','cabinetry','smoked-oak-drawer-base-2ft',(66.65,47.65,0),-math.pi/2)
 put('Cooking oven base cabinet','cabinetry','smoked-oak-oven-base-36in',(66.65,50.15,0),-math.pi/2)
 put('Built-in cooking oven','appliances','built-in-oven-30in',(66.65,50.15,.14/F),-math.pi/2)
 for y in [52.65,54.65,56.65]:put('Cooking wall storage drawers','cabinetry','smoked-oak-drawer-base-2ft',(66.65,y,0),-math.pi/2)
 counter('East cooking continuous stone',(65.45,46.5,67.75,57.8),M,[(66.65,50.15,1.62,2.88)])
 put('Induction stove36inch','appliances','induction-cooktop-36in',(66.65,50.15,3.02),-math.pi/2)
 put('Extraction hood36inch','appliances','wall-hood-36in',(66.77,50.15,5.55),-math.pi/2)
 box('Hood exhaust riser conceptual',(67.25,50.15,10.2),(.75,1.1,4.35),M['dark'],.02)
 box('Honed stone cooking backsplash',(67.71,51.9,4.25),(.10,11.3,2.5),M['stone'],.01)
 area('Hood task light',(66.0,50.15,5.45),(66.65,50.15,3),32,2.6,(1,.86,.65))
 # Island working face east;4.5ft aisle measuredcountertocounter, stoolroutewest.
 # Length10ft provides sink3ft,DW2ft,waste1.5ft+drawer2ft.
 for name,slug,y in [('Island sink cabinet','smoked-oak-sink-base-36in',51.3),('Island dishwasher','smoked-oak-panel-ready-dishwasher-24in',48.8),('Island waste recycling','smoked-oak-waste-pullout-18in',47.05),('Island deep drawers','smoked-oak-drawer-base-2ft',53.8)]:
  category='appliances' if 'dishwasher' in slug else 'cabinetry';put(name,category,slug,(59.7,y,0),math.pi/2)
 counter('Island preparation and social stone',(57.3,45.95,61.0,55.1),M,[(59.7,51.3,.464/F,.664/F)])
 put('Island sink and mixer','fixtures','kitchen-sink-mixer-650',(59.7,51.3,3),math.pi/2,version='v002')
 woodbox('Island finished back',(57.6,50.5,1.44),(.08,8.9,2.76),M['oak'])
 for y in [46,55.05]:woodbox('Island fitted supporting end',(59.2,y,1.44),(3.65,.08,2.76),M['oak'])
 for y in [47.35,50.4,53.45]:put('Island walnut counter seat','furniture','walnut-counter-stool',(55.85,y,0),-math.pi/2)
 for y in [48,52.8]:
  put('Kitchen opal feature pendant','fixtures','opal-globe-pendant',(59.1,y,11.8))
  area('Kitchen pendant illumination',(59.1,y,8.4),(59.1,y,3),90,1.1,(1,.82,.59))
 # Pantry accessed directly from kitchen,6ftclearcentralaisle.
 g.collection('03 Pantry | food and household storage')
 for y in [34.5,36.5,38.5,40.5]:
  put('Pantry west food shelf','cabinetry','smoked-oak-pantry-shelf-2ft',(58.75,y,0),math.pi/2)
  put('Pantry east food shelf','cabinetry','smoked-oak-pantry-shelf-2ft',(67.25,y,0),-math.pi/2)
 # Pantry south service strip stays clear for mechanical access panels.

 g.collection('04 Furnishings | equal primary suites and office')
 for name,cx,rot in [('West primary',8,-math.pi/2),('East primary',60,math.pi/2)]:
  bed=put(name+' king bed','furniture','oak-linen-king-bed',(cx,7.4,0),rot);bed['bed_count']=1
  for y in [2.9,11.9]:put(name+' nightstand','furniture','oak-open-nightstand',(cx+(-2.7 if cx<20 else 2.7),y,0),rot)
 # Opposing2ftdeepwardrobe fronts;4ftgrossmiddle beforehandles.
 for offset,label in [(0,'West'),(48,'East')]:
  for y in [17.5,19.5,21.5,23.5,25.5]:
   put(label+' WIC west hanging bay','cabinetry','oak-wardrobe-2ft',(offset+(1.3 if offset==0 else 1.45),y,0),math.pi/2)
   put(label+' WIC east hanging bay','cabinetry','oak-wardrobe-2ft',(offset+6.85,y,0),-math.pi/2)
 # Office is explicit flexguest room withactualqueen andseparatestorage.
 bed=put('Office guest queen bed','furniture','oak-linen-queen-bed',(4.2,33.8,0),-math.pi/2);bed['guest_bed']=1
 put('Office writing desk','furniture','oak-writing-desk',(7,40.6,0))
 put('Office desk chair','furniture','oak-upholstered-dining-chair',(7,38.3,0),math.pi)
 for y in [29.4,31.4,33.4]:put('Office guest wardrobe','cabinetry','oak-wardrobe-2ft',(11.7,y,0),-math.pi/2)
 g.collection('04 Furnishings | public living and dining')
 put('Living tailored linen sofa','furniture','linen-three-seat-sofa',(7.2,48.4,0),-math.pi/2)
 put('Living rounded coffee table','furniture','oak-rounded-coffee-table',(12,49,0),math.pi/2)
 for y in [46.8,53.1]:put('Living conversation lounge chair','furniture','coastal-outdoor-lounge-chair',(17.2,y,0),math.pi/2)
 put('Living woven rug','furniture','woven-oatmeal-rug',(12,51,.015))
 put('Dining eight foot oak table','furniture','oak-dining-table-8ft',(34,50.2,0))
 for x in [31.1,34,36.9]:
  for y,rot in [(47.2,math.pi),(53.2,0)]:put('Dining upholstered chair','furniture','oak-upholstered-dining-chair',(x,y,0),rot)
 for x in [30.5,37.5]:
  put('Dining opal pendant','fixtures','opal-globe-pendant',(x,50.2,12.0))
  area('Dining warm pendant',(x,50.2,8.6),(x,50.2,2.5),80,1.1,(1,.82,.61))
 # Welcoming opaque-front entry with coat storage andbench at eitherend.
 for x in [25.4,27.4]:put('Entry coat wardrobe','cabinetry','oak-wardrobe-2ft',(x,1.4,0),math.pi)
 woodbox('Entry shoe drop bench',(40.1,2,1.45),(5.5,1.75,.24),M['oak'])
 for x in [38,42.2]:woodbox('Entry bench support',(x,2,.68),(.12,1.5,1.35),M['oak'])
 baths(M);laundry(M);lighting(M)

def baths(M):
 g.collection('05 Bathrooms | dual suites and private toilets')
 for off,label in [(0,'West primary'),(48,'East primary')]:
  # Equal12x13ft bathrooms: west vanity, south tub, northeast shower, northwest WC.
  for y in [16.25,18.25,20.25]:put(label+' vanity drawers','cabinetry','oak-drawer-base-2ft',(off+9.35,y,0),math.pi/2)
  counter(label+' double vanity stone',(off+8.25,15.2,off+10.5,21.3),M)
  for y in [16.7,19.7]:put(label+' basin mixer and mirror','fixtures','vanity-basin-mixer-mirror',(off+9.4,y,3),math.pi/2)
  put(label+' separate72inch bathtub','fixtures','freestanding-tub-72in',(off+16.5,17,0))
  rod(label+' tub filler stem',(off+16.5,19.0,0),(off+16.5,19.0,2.8),.042,M['dark']);rod(label+' tub filler spout',(off+16.5,19,2.8),(off+16.5,18.4,2.8),.04,M['dark'])
  put(label+' separate shower','fixtures','shower-tray-screen-1500x1200',(off+17.15,25.4,0))
  put(label+' enclosed toilet','fixtures','toilet-elongated',(off+10.25,26.35,0))
  put(label+' linen closet inside bath','cabinetry','oak-linen-cabinet-2ft',(off+13.57,26.7,0))
  box(label+' bath floor',(off+14,21.5,.012),(11.65,12.65,.024),M['stone'])
 # Full third bath fromgallery, nearofficeandpublicspace.
 put('Guest bathroom shower','fixtures','shower-tray-screen-900',(18.1,34.1,0))
 put('Guest bathroom toilet','fixtures','toilet-elongated',(14.55,34.3,0))
 put('Guest bathroom vanity drawers','cabinetry','oak-drawer-base-2ft',(14.6,29.5,0),math.pi)
 counter('Guest bathroom vanity',(13.45,28.35,15.75,30.6),M)
 put('Guest bathroom basin','fixtures','vanity-basin-mixer-mirror',(14.6,29.5,3),math.pi)

def laundry(M):
 g.collection('05 Services | laundry and dimensional reservations')
 for x,label in [(50,'washer'),(52.4,'dryer')]:put('Laundry '+label,'appliances','front-loading-laundry-600',(x,40.3,0))
 for y in [35,37]:put('Laundry household shelves','cabinetry','oak-shelving-2ft',(56.7,y,0),-math.pi/2)
 counter('Laundry folding worktop',(48.8,38.9,54,41.6),M,z=3.2)
 # Mechanicalspacevolumes areexplicitreservations, notselected/sizedequipment.
 for name,loc,size in [('Air handler allowance',(61,30,3),(2.5,2.8,6)),('Hot water allowance',(65.7,30,2.8),(2.2,2.2,5.6))]:
  o=box(name,loc,size,M['dark'],.08);o['equipment_status']='dimensioned service reservation only'

def lighting(M):
 g.collection('10 Lighting | restrained architectural fixtures')
 for x,y,z in [(22,4,10),(22,12,10),(22,22,10),(22,32,10),(46,4,10),(46,14,10),(46,24,10),(46,34,10),(34,3,12),(30,50,12),(38,50,12),(5,20,10),(53,20,10),(14,21,10),(62,21,10),(54,35,10),(63,37,10),(7,37,10)]:
  # Actual3.4infixturecutout through each intersecting flatceiling host.
  for host in list(bpy.context.scene.objects):
   if host.type!='MESH' or 'ceiling' not in host.name.lower() or host.library:continue
   if abs((host.location.z-host.dimensions.z/2)/F-z)>.03:continue
   if abs(host.location.x/F-x)>host.dimensions.x/F/2 or abs(host.location.y/F-y)>host.dimensions.y/F/2:continue
   bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=(3.4/12)*F/2,depth=.5*F,location=(x*F,y*F,(z+.12)*F))
   tool=bpy.context.object;mod=host.modifiers.new('Recessed light real ceiling aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.object=tool
   bpy.context.view_layer.objects.active=host;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(tool,do_unlink=True)
  put('Recessed architectural downlight','fixtures','lighting-recessed-downlight-3in',(x,y,z))
  area('Soft recessed illumination',(x,y,z-.12),(x,y,0),45,1,(1,.87,.70))
 for x in [12,56]:
  for y in [6,46,56]:area('Vault indirect soft light',(x,y,12),(x,y,0),100,6,(1,.86,.70))
