"""Original coastal plant geometry; build with Blender --background --python this-file.
Five botanical families, three discrete forms each. All dimensions are meters.
"""
import argparse
import math
import random
import sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

TAU=math.tau

def vec(v): return Vector(v)
def unit(v):
    v=vec(v)
    return v.normalized() if v.length else vec((0,0,1))
def radial(a): return vec((math.cos(a),math.sin(a),0))
def path(a,b,bend=0.04):
    a,b=vec(a),vec(b)
    return [a,a.lerp(b,.35)+vec((bend,0,.05)),a.lerp(b,.7)+vec((0,bend,.05)),b]
def tube(builder,a,b,r): builder.tube(path(a,b),[r,r*.75,r*.45,r*.12],sides=7)
def blade(builder,point,direction,l,w,style='oval',roll=0):
    builder.leaf(tuple(point),tuple(direction),l,w,style=style,roll=roll)
def builders(prefix, mats): return [C.MeshBuilder(prefix+' '+name,mat) for name,mat in mats]
def finish(col,bs):
    for b in bs:
        obj=b.finish(col)
        if obj is None: continue
        # Root tube rings are sliced at grade rather than floating or extending below it.
        for vertex in obj.data.vertices:
            if vertex.co.z < 0: vertex.co.z = 0

def pine(idx):
    rng=random.Random(832+idx)
    names=['young-open','irregular-mature','wind-shaped']
    col=C.collection('shore-pine-'+names[idx])
    bark,needles,needlelight,cones=builders('Shore pine', [('bark',C.bark_material('Shore pine fissured bark',(.13,.085,.045))),('dark paired needles',C.material('Pine deep needles',(.04,.105,.025))),('new needles',C.material('Pine shoot tips',(.10,.20,.045))),('woody cones',C.material('Pine woody cones',(.23,.13,.065)))])
    h=[3.0,5.4,4.0][idx]; spread=[.9,1.9,1.7][idx]
    lean=[.12,.32,1.55][idx]
    trunk=[vec((lean*(k/11)**1.6+.035*math.sin(k*1.1),.07*math.sin(k*.7),h*k/11)) for k in range(12)]
    bark.tube(trunk,[max(.003,.075*(1-k/11)**1.35*(h/3)) for k in range(12)],sides=9)
    def foliate(attach,tip,amount=42):
        axis=unit(tip-attach)
        tube(bark,attach,tip,.006)
        side=unit(axis.cross(vec((0,0,1)))) if abs(axis.z)<.96 else vec((1,0,0))
        other=unit(side.cross(axis))
        for fasc in range(amount):
            along=.08+.92*(fasc/(amount-1))
            root=attach.lerp(tip,along)
            theta=fasc*2.399+rng.random()*.2
            out=unit((side*math.cos(theta)+other*math.sin(theta))*.88+axis*.5)
            for pair in [-1,1]:
                nd=unit(out+side*(pair*.10))
                length=rng.uniform(.078,.122)
                dest=root+nd*length
                (needlelight if fasc>amount*.85 else needles).tube([root,root.lerp(dest,.58)+axis*.007,dest],[.0022,.0016,.0001],sides=3)
    for tier in range(11):
        z=h*(.17+tier*.072+rng.uniform(-.018,.018))
        for branch in range(4):
            a=branch*TAU/4+tier*1.4+rng.uniform(-.4,.4)
            wind=vec((1.15 if idx==2 else 0,0,0))
            d=unit(radial(a)+wind)
            reach=spread*(.62+.35*math.sin(math.pi*(tier+.5)/11))*rng.uniform(.7,1.18)
            zbranch=z+h*rng.uniform(-.038,.038)
            base=vec((lean*(zbranch/h)**1.6+.035*math.sin(zbranch/h*11*1.1),.07*math.sin(zbranch/h*11*.7),zbranch))
            end=base+d*reach+vec((0,0,rng.uniform(-.05,.25)+reach*.18))
            tube(bark,base,end,.025*(1-tier*.067)*h/4)
            # Many actual ramified leafy shoots create a continuous lobed bough.
            for shoot in range(12):
                t=.22+shoot*.069
                attach=base.lerp(end,t)
                sd=unit(d*.55+radial(a+(-1 if shoot%2 else 1)*1.15)*.75+vec((0,0,rng.uniform(.35,1.5))))
                tip=attach+sd*(.30+reach*.21)*rng.uniform(.8,1.3)
                foliate(attach,tip,68)
            foliate(end,end+unit(d*.3+vec((0,0,1)))*.43,64)
            if tier<4 and branch%2==0:
                cp=end-vec((0,0,.04))
                for sc in range(6):
                    for ro in range(5):
                        aa=sc*TAU/6+ro*.7
                        p=cp+radial(aa)*(.014*math.sin(math.pi*(ro+1)/6))+vec((0,0,ro*.008))
                        cones.ellipsoid(p,(.010,.009,.007),segments=6,rings=4)
    # Foliage covers the tapered terminal leader rather than ending in a bare pole.
    for i in range(12):
        attach=trunk[-1]-vec((0,0,.35*i/12))
        tip=attach+unit(radial(i*2.399)*.8+vec((0,0,.8)))*rng.uniform(.15,.30)
        foliate(attach,tip,40)
    finish(col,[bark,needles,needlelight,cones]); return names[idx],col,['Young open crown with visible branching and paired needles.','Irregular mature open crown with woody cones.','Wind-shaped leaning trunk and asymmetric spread; stylized coastal exposure.'][idx]

def leafy_shrub(idx,species):
    silktassel=species=='coast-silktassel'
    names=['leafy-screen','winter-male-catkins','open-small-tree'] if silktassel else ['natural-multistem','dwarf-yaupon-nana','fruiting-female']
    rng=random.Random((221 if silktassel else 514)+idx)
    col=C.collection(species+'-'+names[idx])
    bark,leaf,light,feature=builders(species,[('branches',C.bark_material(species+' bark',(.21,.17,.12))),('leaf upper',C.material(species+' glossy evergreen',(.07,.15,.075) if silktassel else (.035,.12,.055),roughness=.37)),('leaf variation',C.material(species+' new foliage',(.17,.25,.12),roughness=.46)),('catkins' if silktassel else 'berries',C.material(species+' display detail',(.58,.61,.33) if silktassel else (.58,.027,.015),roughness=.55))])
    h=([2.2,2.8,3.8] if silktassel else [4.2,1.0,3.2])[idx]
    spread=([1.2,1.45,1.55] if silktassel else [1.65,.9,1.35])[idx]
    for stem in range(6 if silktassel else 8):
        a=stem*TAU/(6 if silktassel else 8)+rng.random()*.5
        d=radial(a)
        top=d*spread*.55+vec((0,0,h*rng.uniform(.69,.83)))
        tube(bark,vec((0,0,0)),top,.035 if h>2 else .013)
        for b in range(7):
            t=(.36 if idx==2 and silktassel else .12)+b*(.102 if idx==2 and silktassel else .142)
            origin=top*t
            ba=a+b*2.3
            branchend=origin+radial(ba)*spread*(.44+.2*math.sin(math.pi*b/6))+vec((0,0,h*.16))
            tube(bark,origin,branchend,.012*(1-b*.08) if h>2 else .005)
            for twig in range(12 if silktassel else 24):
                attach=origin.lerp(branchend,.18+.82*twig/(11 if silktassel else 23))
                td=unit(radial(ba+(-1 if twig%2 else 1)*rng.uniform(.7,1.65))+vec((0,0,rng.uniform(.25,.75))))
                tip=attach+td*rng.uniform(.32,.53)*(h/2.5)**.3
                tube(bark,attach,tip,.005)
                count=11 if silktassel else 21
                for n in range(count):
                    p=attach.lerp(tip,.15+.8*n/count)
                    la=ba+n*2.1
                    # Garrya opposing leathery leaves; holly smaller alternating leaves.
                    for side in [-1,1] if silktassel else [1]:
                        ld=unit(radial(la)*side+vec((0,0,.25)))
                        ll=rng.uniform(.085,.12) if silktassel else rng.uniform(.035,.055)
                        blade(leaf if n%4 else light,p+ld*ll*.36,ld,ll,ll*(.52 if silktassel else .6),roll=rng.uniform(-.5,.5))
                if silktassel and idx==1 and twig in [1,3]:
                    # Long pendulous winter male catkins with individual bracts.
                    cl=rng.uniform(.11,.23)
                    feature.tube([tip,tip+vec((.012,0,-cl*.5)),tip+vec((.02,0,-cl))],[.003,.003,.001],sides=5)
                    for bead in range(15):
                        p=tip+vec((.02*bead/15,0,-cl*bead/15))
                        for side in [-1,1]:
                            feature.ellipsoid(p+vec((side*.004,0,0)),(.007,.005,.007),segments=6,rings=4)
                if not silktassel and idx==2 and twig%4==0:
                    for berry in range(3):
                        p=tip-td*(.03+berry*.035)+vec((0,0,-.012))
                        feature.ellipsoid(p,(.0048,.0048,.0048),segments=8,rings=5)
    finish(col,[bark,leaf,light,feature])
    desc=(['Dense leafy evergreen screen.','Winter male flowering specimen with pendulous catkins.','Pruned small tree with visible lower stems.'] if silktassel else ['Natural multi-stem evergreen small tree.','Compact mounded form representing dwarf cultivar Nana; no fruit claim.','Female fruiting specimen; red berries imply compatible pollination, not guaranteed yield.'])[idx]
    return names[idx],col,desc

def strawberry(idx):
    rng=random.Random(662+idx); names=['glossy-low-mat','white-flowering','runner-edge-colony']
    col=C.collection('beach-strawberry-'+names[idx])
    stems,leaves,petals,centers=builders('Beach strawberry',[('petioles and stolons',C.material('Strawberry stems',(.12,.20,.045))),('glossy leaflets',C.material('Strawberry waxy green',(.025,.11,.035),roughness=.35)),('five white petals',C.material('Strawberry white petals',(.93,.93,.81))),('flower centers',C.material('Strawberry yellow anthers',(.75,.48,.045)))])
    def petiole(root,tip,r=.0015):
        points=[root.lerp(tip,k/6)+vec((0,0,.009*math.sin(math.pi*k/6))) for k in range(7)]
        stems.tube(points,[r*(1-.55*k/6) for k in range(7)],sides=5)
    def leaflet(center,direction,length,width):
        # Fine serrations retain an obovate rounded outline; these are not lobed maple blades.
        axis=unit(direction); side=unit(axis.cross(vec((0,0,1)))); normal=unit(side.cross(axis)); n=20;offset=len(leaves.vertices)
        for i in range(n+1):
            t=i/n;w=width*.5*(math.sin(math.pi*t)**.63)*(1+.055*((-1)**i))
            mid=center+axis*((t-.5)*length)+normal*(.005*math.sin(math.pi*t))
            leaves.vertices.extend([tuple(mid-side*w-normal*w*.07),tuple(mid),tuple(mid+side*w-normal*w*.07)])
        for i in range(n):
            a=offset+3*i;leaves.faces.extend([(a,a+1,a+4,a+3),(a+1,a+2,a+5,a+4)])
    count=[48,43,28][idx]
    for plant in range(count):
        a=plant*2.399; r=.066*math.sqrt(plant);root=radial(a)*r
        for pet in range(4):
            angle=a+pet*TAU/4+rng.uniform(-.25,.25)
            head=root+radial(angle)*rng.uniform(.025,.052)+vec((0,0,rng.uniform(.035,.067)))
            petiole(root,head)
            for lf in range(3):
                la=angle+(lf-1)*1.20
                d=unit(radial(la)+vec((0,0,rng.uniform(-.08,.12))))
                ll=.065 if lf==1 else .057
                attach=head+d*(.010 if lf==1 else .005)
                petiole(head,attach,.0007)
                leaflet(attach+d*ll*.5,d,ll,ll*.74)
        if idx==1 and plant%3==0:
            fp=root+vec((.01,-.03,.105));petiole(root,fp,.0013)
            for pet in range(5):
                d=radial(pet*TAU/5);blade(petals,fp+d*.008,d,.016,.012)
            centers.ellipsoid(fp+vec((0,0,.002)),(.005,.005,.003),segments=10,rings=5)
        if idx==2 and plant%3==0:
            dest=root+radial(a)*rng.uniform(.17,.26)
            points=[root.lerp(dest,k/7)+vec((0,0,.007*math.sin(math.pi*k/7))) for k in range(8)]
            stems.tube(points,[.0013]*8,sides=5)
            head=dest+vec((0,0,.024));petiole(dest,head)
            for lf in range(3):
                d=radial(a+(lf-1)*1.2);leaflet(head+d*.026,d,.042,.031)
    finish(col,[stems,leaves,petals,centers]);return names[idx],col,['Dense low mat of visibly separate rounded, finely serrated three-part leaves.','White five-petal flowers over a dense trifoliate mat.','Trailing colony with ground-hugging runners and rooted juvenile trifoliate rosettes.'][idx]

def sea_oats(idx):
    rng=random.Random(916+idx);names=['young-dune-clump','green-seed-panicles','tan-flattened-seedheads']
    col=C.collection('sea-oats-'+names[idx])
    stem,leaf,seeds=builders('Sea oats',[('culms',C.material('Sea oats culm',(.28,.34,.105) if idx<2 else (.5,.38,.16))),('strap leaves',C.material('Sea oats leaf',(.18,.28,.085))),('flattened spikelets',C.material('Sea oats spikelets',(.31,.40,.13) if idx<2 else (.67,.49,.23)))])
    for n in range([26,35,37][idx]):
        a=n*2.399;rad=rng.uniform(.02,.18); root=radial(a)*rad
        h=rng.uniform(.55,.8) if idx==0 else rng.uniform(1.1,1.8)
        lean=radial(a)*rng.uniform(.1,.32)
        tip=root+lean+vec((0,0,h))
        stem.tube([root,root+lean*.2+vec((0,0,h*.4)),tip],[.0035,.003,.0012],sides=6)
        for k in range(5):
            start=root+lean*(k/7)+vec((0,0,h*(.08+k*.11)))
            d=radial(a+k*2.6)
            length=rng.uniform(.26,.5)
            # Long arching narrow strap blades are built as bent tapered ribbons.
            pts=[start,start+d*length*.35+vec((0,0,.11)),start+d*length*.75+vec((0,0,.10)),start+d*length+vec((0,0,.035))]
            for seg in range(3):
                delta=pts[seg+1]-pts[seg]
                blade(leaf,(pts[seg]+pts[seg+1])*.5,delta,delta.length*1.1,.022*(1-seg*.28),'lance',roll=.5)
        if idx:
            for spray in range(5):
                attach=tip-vec((0,0,.03+spray*.028))
                d=radial(a+spray*2.25)
                end=attach+d*(.07+spray*.02)+vec((0,0,-.02-spray*.008))
                tube(stem,attach,end,.0012)
                # Flattened oat spikelet, overlapping pointed florets on a central rachis.
                for floret in range(7):
                    fp=end+vec((0,0,.012*(floret-3)))
                    for side in [-1,1]:
                        sd=unit(d*side+vec((0,0,.5)))
                        blade(seeds,fp+sd*.006,sd,.025,.009,'lance',roll=a)
    finish(col,[stem,leaf,seeds]);return names[idx],col,['Young dune grass clump without mature seedheads.','Summer green flattened spikelet panicles.','Late-season tan flattened spikelets above green to straw culms.'][idx]

SOURCES={
'shore-pine':('Pinus contorta var. contorta','Cool Pacific coastal exposure; not a universal warm-beach tree.','https://landscapeplants.oregonstate.edu/plants/pinus-contorta-var-contorta'),
'coast-silktassel':('Garrya elliptica','Mild Pacific gardens; sheltered siting unless exposure is verified.','https://landscapeplants.oregonstate.edu/plants/garrya-elliptica'),
'beach-strawberry':('Fragaria chiloensis','Cool Pacific coastal groundcover; no crop production promise.','https://depts.washington.edu/propplnt/Plants/fragariachiloensis.htm'),
'sea-oats':('Uniola paniculata','Warm Atlantic and Gulf dune planting; nursery material and local restoration rules apply.','https://plants.ces.ncsu.edu/plants/uniola-paniculata/common-name/sea-oats/'),
'yaupon-holly':('Ilex vomitoria','Warm southeastern coastal garden; fruiting requires female stock and compatible pollination.','https://plants.ces.ncsu.edu/plants/ilex-vomitoria/')}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--assets",nargs="+")
    parser.add_argument("--repair-foliage",action="store_true")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    for slug,func in [('shore-pine',pine),('coast-silktassel',lambda i:leafy_shrub(i,'coast-silktassel')),('beach-strawberry',strawberry),('sea-oats',sea_oats),('yaupon-holly',lambda i:leafy_shrub(i,'yaupon-holly'))]:
        if args.assets and slug not in args.assets: continue
        if args.repair_foliage and slug not in ['shore-pine','coast-silktassel','yaupon-holly']: continue
        C.reset(); variants=[func(i) for i in range(3)]
        botanical,climate,url=SOURCES[slug]
        C.save_family(slug,slug.replace('-',' ').title(),variants,{'botanical_name':botanical,'climate_notes':climate,'reference_urls':[url],'generator':'tools/library/plants/coastal.py','category_tags':['coastal','landscape'],'limitations':['Original architectural visualization geometry; no botanical survey or horticultural specification.','Modeled dimensions describe this specimen; not guaranteed mature size.','No site adoption claimed; preview and host review recorded separately.']})
        print('COASTAL_PLANT_BUILT',slug,flush=True)
if __name__=='__main__': main()
