"""Measured concept checks from evaluated native geometry; finite operating sweeps."""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from design import AREA,SLUG
F=.3048;HOME=ROOT/'homes'/SLUG;s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get()
checks=[];errors=[]
def check(name,measured,ok,basis):
 checks.append({'name':name,'measured':measured,'passed':bool(ok),'basis':basis})
 if not ok:errors.append(name)
def bb(o):
 e=o.evaluated_get(dg);pts=[e.matrix_world@Vector(v) for v in e.bound_box]
 return [min(p[i] for p in pts)/F for i in range(3)],[max(p[i] for p in pts)/F for i in range(3)]
def ibb(o):
 pts=[]
 def walk(c,transform):
  for child in c.objects:
   t=transform@child.matrix_world
   if child.type in {'MESH','CURVE'}:
    ev=child.evaluated_get(dg)
    mesh=ev.to_mesh();pts.extend(t@v.co for v in mesh.vertices);ev.to_mesh_clear()
   elif child.instance_type=='COLLECTION':walk(child.instance_collection,t)
  for sub in c.children:walk(sub,transform)
 walk(o.instance_collection,o.matrix_world)
 return [min(p[i] for p in pts)/F for i in range(3)],[max(p[i] for p in pts)/F for i in range(3)]
assets={o.name:(o,*ibb(o)) for o in s.objects if o.instance_type=='COLLECTION' and o.get('shared_asset_id','').split('/')[0] in {'furniture','cabinetry','appliances','fixtures'}}
floors=[o for o in s.objects if o.name in ['West wing floor','East wing floor','Front link floor','Rear link floor']]
actual_area=sum(o.dimensions.x*o.dimensions.y/(F*F) for o in floors)
check('Actual four floor plates planning area',round(actual_area,3),abs(actual_area-AREA)<.01,'Evaluated plate dimensions; includes planning wall allowances, not exterior cladding-face survey')
check('Dedicated bedrooms and flex guest',{'dedicated':sum(int(o.get('bed_count',0)) for o in s.objects),'guest':sum(int(o.get('guest_bed',0)) for o in s.objects)},sum(int(o.get('bed_count',0)) for o in s.objects)==2 and sum(int(o.get('guest_bed',0)) for o in s.objects)==1,'Actual instantiated beds, not room labels')
# Clear gallerywidth measuredfrom localfixedmesh bounds within routez0..7.
for side,x1,x2 in [('West',19,25),('East',43,49)]:
 objs=[o for o in s.objects if o.type=='MESH' and not o.library and (side+' gallery partition' in o.name or side+' gallery court mullion' in o.name)]
 walls=[bb(o) for o in objs if 'partition' in o.name and 'door' not in o.name and 'lintel' not in o.name]
 frames=[bb(o) for o in objs if 'mullion' in o.name]
 clearance=min(v[0][0] for v in frames)-max(v[1][0] for v in walls) if side=='West' else min(v[0][0] for v in walls)-max(v[1][0] for v in frames)
 check(side+' gallery clear width inches',round(clearance*12,2),clearance>=4,'Actual partition and courtyard mullion bounds; beam posts placed outside gallery glazing')
for off,label in [(0,'West'),(48,'East')]:
 bank1=[v for k,v in assets.items() if label+' WIC west' in k];bank2=[v for k,v in assets.items() if label+' WIC east' in k]
 aisle=min(v[1][0] for v in bank2)-max(v[2][0] for v in bank1)
 check(label+' WIC clear closed-pull aisle inches',round(aisle*12,2),aisle>=3,'Actual evaluated wardrobe geometry including pulls. Libraryleafwidth.95ft gives additional individualopen-doorcheck below.')
 check(label+' WIC single90degreeleaf remaining bypass inches',round((aisle-.95)*12,2),aisle-.95>=2,'Actual aisle minus.95ftlibraryleaf projection; oneleafoperated, opposingdoorsclosed; notaccessibilityapproval')
 # GeometryofactualWCpartitionwalls andbacks defineclearrectangle.
 front=[o for o in s.objects if o.name.startswith('Ensuite enclosed WC front') and abs(o.location.x/F-(off+10.25))<.1][0]
 east=[o for o in s.objects if o.name.startswith('Ensuite WC pocket') and 'recessed' not in o.name and 'lintel' not in o.name and abs(o.location.x/F-(off+12.4))<.1][0]
 width=bb(east)[0][0]-(off+8.125);depth=27.875-bb(front)[1][1]
 check(label+' WC clear feet',{'width':round(width,3),'depth':round(depth,3)},width>=4 and depth>=6,'Fixed mesh innerfaces; actual east-wall pocket entry, no inward leaf')
 linen=[v for k,v in assets.items() if label+' primary linen' in k][0];shower=[v for k,v in assets.items() if label+' primary separate shower' in k][0]
 check(label+' bath linen fitted beside shower',{'linen_bounds_ft':linen[1:],'shower_bounds_ft':shower[1:]},linen[1][0]>off+12.525 and linen[2][0]<shower[1][0] and linen[2][1]<27.875,'Actual closed linen cabinet and shower bounds; cabinet remains inside ensuite')
# Exact counteredges and applianceforefronts.
work=bpy.data.objects['East cooking continuous stone'];island=bpy.data.objects['Island preparation and social stone']
clear=bb(work)[0][0]-bb(island)[1][0]
check('Kitchen counter working aisle inches',round(clear*12,2),clear>=4,'Measured modeled stone edges, applianceopeningschecked separately')
# Full hingeddoorgeometry sampled0..90degrees vs actual furniture/equipment bounds.
def rect_overlap(poly,lo,hi):
 other=[(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])]
 for pts in [poly,other]:
  for i in range(4):
   a,b=pts[i],pts[(i+1)%4];axis=(-(b[1]-a[1]),b[0]-a[0]);p=[x*axis[0]+y*axis[1] for x,y in poly];q=[x*axis[0]+y*axis[1] for x,y in other]
   if max(p)<=min(q)+.005 or max(q)<=min(p)+.005:return False
 return True
collisions=[]
for door in [o for o in s.objects if 'hinge_xy_ft' in o]:
 hx,hy=door['hinge_xy_ft'];w=door['door_width_ft']
 for deg in range(0,91,5):
  a=door['closed_angle']+door['swing_sign']*math.radians(deg);u=(math.cos(a),math.sin(a));v=(-u[1],u[0]);poly=[(hx+u[0]*x+v[0]*y,hy+u[1]*x+v[1]*y) for x,y in [(0,-.065),(w,-.065),(w,.065),(0,.065)]]
  for name,(o,lo,hi) in assets.items():
   if hi[2]<.10 or lo[2]>8.5 or any(k in name.lower() for k in ['lever','pendant','downlight']):continue
   if rect_overlap(poly,lo,hi):collisions.append({'door':door.name,'angle_degrees':deg,'obstacle':name});break
  if collisions and collisions[-1]['door']==door.name:break
check('Hinged doors sampled full90degree operation',collisions,not collisions,'5degree samples of realwidth/thickness against evaluated furniture/appliance AABBs; does not certify manufacturer clearance')
# Conservative manufacturer-independent concept operating envelopes for actual installations.
for asset_slug,label in [('smoked-oak-panel-ready-fridge-48in','Refrigerator110degree leaves'),('smoked-oak-panel-ready-dishwasher-24in','Dishwasher90degree drop panel')]:
 host=next(o for o in s.objects if o.get('shared_asset_id')=='appliances/'+asset_slug)
 meta=json.loads((ROOT/'library/appliances'/asset_slug/'v001/asset.json').read_text());env=meta['installation']['operating_envelope']['door_sweep_bounds_m']
 pts=[host.matrix_world@Vector((x,y,z)) for x in [env['min'][0],env['max'][0]] for y in [env['min'][1],env['max'][1]] for z in [env['min'][2],env['max'][2]]]
 lo=[min(p[i] for p in pts)/F for i in range(3)];hi=[max(p[i] for p in pts)/F for i in range(3)]
 hits=[]
 for name,(obj,other_lo,other_hi) in assets.items():
  if obj==host or any(k in name.lower() for k in ['hood','sink and mixer','pendant','downlight']):continue
  if all(min(hi[i],other_hi[i])-max(lo[i],other_lo[i])>.015 for i in range(3)):hits.append(name)
 # Finishedisland orwallstone surfacesareseparate localobjects.
 for obj in [work,island]:
  other_lo,other_hi=bb(obj)
  if all(min(hi[i],other_hi[i])-max(lo[i],other_lo[i])>.015 for i in range(3)):hits.append(obj.name)
 check(label,{'sweep_bounds_ft':[lo,hi],'obstructions':hits},not hits,'Pinned asset conservative sweep transformed by actual native installation; one appliance operated at a time')
# Oven front90degree conceptualleaf derived fromactual28in frontheight.
oven=next(o for o in s.objects if o.get('shared_asset_id')=='appliances/built-in-oven-30in')
oven_front=assets[oven.name][1][0];oven_open_front=oven_front-.7112/F
check('Oven drop-door and operator gap inches',round((oven_open_front-bb(island)[1][0])*12,2),oven_open_front-bb(island)[1][0]>=2,'Conservative28inleaf projection fromactual closedfront;24in remaining operatorallowance; genericconcept, productunselected')
# Verify the stovetop is actually visible above the fitted worktop opening.
hit,loc,norm,index,obj,matrix=s.ray_cast(dg,Vector((66.65*F,50.15*F,4.5*F)),Vector((0,0,-1)),distance=3*F)
check('Visible induction ceramic surface',{'object':obj.name if hit else None,'height_ft':round(loc.z/F,4) if hit else None},hit and 'Induction' in obj.name,'Downward nativegeometry ray through the cooking center; no worktop covers appliance')
# All sharedcovermeshvertices remain below the actual pitched outerroofplanes.
penetration=0.0;cover_vertices=0
for o in s.objects:
 if o.get('shared_asset_id')!='assemblies/cedar-steel-beam-cover-300x400':continue
 for child in o.instance_collection.all_objects:
  if child.type!='MESH':continue
  for v in child.data.vertices:
   q=o.matrix_world@child.matrix_world@v.co;x,y,z=q.x/F,q.y/F,q.z/F
   if -3<=y<=63:
    cx=12 if x<34 else 56;roof=18.5-abs(x-cx)*(.4666666667)
    penetration=max(penetration,z-roof);cover_vertices+=1
check('Beam cover contained below outer roof',{'maximum_penetration_ft':round(penetration,5),'vertices_checked':cover_vertices},penetration<.005,'Actuallinkedcovermeshvertices transformed into pitchedroofsection; engineering notimplied')
drive=bpy.data.objects['Side driveway and parking'];road=bpy.data.objects['Road illustrative front'];gap=max(0,bb(drive)[0][1]-bb(road)[1][1])
check('Driveway road continuity',{'gap_ft':round(gap,5)},gap<.01,'Actualgroundslabedge bounds; turning/siteengineering unresolved')
# Ceilingrays use actualvisible geometry. Lowestfixedfixture maycontrol atsomepoints.
rays=[]
for name,x,y in [('Living center',12,50),('Living rafter bay',2,48),('Kitchen center',56,54),('West primary',12,6),('West bathroom',14,20),('East bathroom',62,20),('Entry',34,3),('Dining',34,51)]:
 hit,loc,norm,index,obj,matrix=s.ray_cast(dg,Vector((x*F,y*F,5.5*F)),Vector((0,0,1)),distance=30*F)
 rays.append({'position':name,'finished_height_ft':round(loc.z/F,3) if hit else None,'first_fixed_element':obj.name if hit else None})
check('Sampled finished headroom',rays,all(v['finished_height_ft'] is not None and v['finished_height_ft']>=9.95 for v in rays),'Upward rays from5.5ft eye level atnamed clearfloor points; beamcoverundersidescount')
report={'model_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'checks':checks,'debug_assets':{k:[lo,hi] for k,(o,lo,hi) in assets.items() if 'basin mixer' in k or 'Laundry household' in k},'failures':errors,'limitations':['Generic equipment and finite operating samples, not selected-product approval.','No structural, thermal, fire, localcode or site survey certification.','Roof/slab source geometry and clearances remain concept assumptions.']}
(HOME/'model/functional-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('TWIN_FUNCTIONAL',json.dumps({'checks':len(checks),'failures':errors}),flush=True)
if errors:raise RuntimeError(errors)
