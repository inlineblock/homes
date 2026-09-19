"""Original metric asset geometry; publish a new version rather than overwriting adoption."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'tools'))
from common import geometry as g
from common.geometry import material
from common.materials import noise_material
bpy.ops.wm.read_factory_settings(use_empty=True)
def box(name,loc,size,mat,bevel=0):return g.box(name,[v/.3048 for v in loc],[v/.3048 for v in size],mat,bevel/.3048)
def rod(name,a,b,r,mat):return g.rod(name,[v/.3048 for v in a],[v/.3048 for v in b],r/.3048,mat)
def mesh(name,verts,faces,mat):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.materials.append(mat);d.update();o=bpy.data.objects.new(name,d);g.ACTIVE.objects.link(o);return o
ID='landscape/flowering-perennial-clump';NAME='Lilac and ivory flowering perennial clump'
import random
rng=random.Random(610681)
coll=g.collection('Flowering perennial clump | shared v001')
stemmat=material('Perennial green stems',(.13,.20,.07),.8)
leafmat=noise_material('Perennial soft green leaves',(.10,.16,.045),(.23,.30,.095),30,.84,.0003)
purple=material('Perennial lilac petals',(.46,.28,.57),.7)
ivory=material('Perennial pale ivory petals',(.82,.80,.68),.72)
leafv=[];leaff=[];bloomv=[[],[]];bloomf=[[],[]]
def add_leaf(base,tip,width):
    a=Vector(base);b=Vector(tip);axis=b-a;side=axis.cross(Vector((0,0,1))).normalized()*width
    mid=a+axis*.52;start=len(leafv)
    leafv.extend([tuple(a),tuple(mid+side),tuple(b),tuple(mid-side),tuple(mid+Vector((0,0,.007)))])
    leaff.extend([(start,start+1,start+4),(start+1,start+2,start+4),(start+2,start+3,start+4),(start+3,start,start+4)])
def flower(center,size,kind,angle):
    # Five cupped petals, physically joined at the flower throat.
    center=Vector(center);v=bloomv[kind];f=bloomf[kind]
    for k in range(5):
        a=angle+k*math.tau/5;direction=Vector((math.cos(a),math.sin(a),.15));side=Vector((-math.sin(a),math.cos(a),0));start=len(v)
        v.extend([tuple(center),tuple(center+direction*size*.55+side*size*.36),tuple(center+direction*size+Vector((0,0,.003))),tuple(center+direction*size*.55-side*size*.36)])
        f.append((start,start+1,start+2,start+3))
for i in range(27):
    angle=rng.uniform(0,math.tau);radius=rng.uniform(.015,.25);height=rng.uniform(.34,.66)
    start=Vector((math.cos(angle)*radius,math.sin(angle)*radius,0));lean=Vector((math.cos(angle)*.055,math.sin(angle)*.055,0));end=start+lean+Vector((0,0,height))
    rod('Connected perennial stem',start,end,.0024,stemmat)
    for j in range(4):
        base=start+(end-start)*(.12+j*.14)
        for sign in [-1,1]:
            a=angle+sign*1.2+j*.65;length=.08*(1-j*.10)
            add_leaf(base,base+Vector((math.cos(a)*length,math.sin(a)*length,.025)),.019)
    for j in range(8):
        h=height-.15+j*.019;base=start+lean*(h/height)+Vector((0,0,h));rad=.019*(1-j*.055)
        for k in range(4):
            a=k*math.tau/4+j*.55;point=base+Vector((math.cos(a)*rad,math.sin(a)*rad,0))
            flower(point,rng.uniform(.010,.014)*(1-j*.025),1 if i%5==0 else 0,a)
# Connected low rosette leaves give the clump a grounded base, rather than bare sticks.
for i in range(40):
    a=i*2.39996;r=rng.uniform(.14,.31)
    add_leaf((math.cos(a)*.03,math.sin(a)*.03,.012),(math.cos(a)*r,math.sin(a)*r,rng.uniform(.06,.16)),rng.uniform(.012,.026))
mesh('Perennial attached lanceolate leaves',leafv,leaff,leafmat)
mesh('Lilac cupped perennial flowers',bloomv[0],bloomf[0],purple)
mesh('Ivory cupped perennial flowers',bloomv[1],bloomf[1],ivory)
meta={'placement':{'origin':'Ground-contact base Z=0; centered XY; upright Z','front_direction':'Radial planting clump','allowed_variation':'Uniform scale 0.8 to 1.4 and arbitrary Z rotation; no nonuniform stretching'},'mounting':'Place base on actual soil or grade, with free space around foliage.','clearances':{'neighbor_center_spacing_m':.6,'basis':'Illustrative planting massing, not botanical growth or climate suitability guidance.','host_checked':False},'source_notes':'Original generic flowering perennial silhouette with connected stems, attached leaves and modeled cupped petals; no imported geometry or botanical species claim.','product_status':'Illustrative original landscape geometry; no commercial plant specification.'}
bpy.context.view_layer.update()
pts=[o.matrix_world@Vector(c) for o in coll.all_objects if o.type=='MESH' for c in o.bound_box]
lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
coll['asset_id']=ID;coll['asset_version']='v001'
folder=Path(__file__).parent;native=folder/(ID.split('/')[-1]+'.blend')
assert not native.exists(),'Published versions are immutable; choose a new version.'
bpy.data.libraries.write(str(native),{coll},fake_user=True)
meta.update({'schema_version':1,'id':ID,'version':'v001','name':NAME,'units':'meters','dimensions_m':[round(b-a,6) for a,b in zip(lo,hi)],'bounds_m':{'min':lo,'max':hi},'dependencies':[],'source':{'kind':'original','generator':str(Path(__file__).relative_to(ROOT)),'command':'blender --background --factory-startup --python '+str(Path(__file__).relative_to(ROOT))},'license':'CC-BY-4.0','rights':'Original geometry and embedded procedural materials; attribution Homes project contributors','software':{'blender':bpy.app.version_string},'files':{'blender':native.name,'preview':'preview.png','validation':'validation.json','preview_renderer':'review.py'}})
(folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
print('ASSET_PUBLISHED',ID,len(coll.all_objects),meta['dimensions_m'])
