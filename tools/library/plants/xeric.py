"""Original water-wise plant meshes; Blender --background --python this-file.

Five botanical families, three separate architecture/season collections each.
Geometry is generated at soil origin in meters; no photograph/texture downloads.
"""
from pathlib import Path
import sys
import math
import random

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from common import material, bark_material, MeshBuilder, collection, reset, save_family

TAU = math.tau


def point(a, radius, z=0):
    return Vector((math.cos(a)*radius, math.sin(a)*radius, z))


class Ribbons:
    """Curved folded ribbons, used for actual narrow grass blades and ray petals."""
    def __init__(self, name, mat):
        self.name, self.mat, self.vertices, self.faces = name, mat, [], []

    def blade(self, path, width, angle, tip=True):
        side = Vector((math.cos(angle), math.sin(angle), 0))
        start = len(self.vertices)
        n = len(path)
        for i, center in enumerate(path):
            t = i/(n-1)
            w = width * (0.12 + 0.88*math.sin(math.pi*(t*.85+.05)))
            if tip and i == n-1:
                w = .00006
            p = Vector(center)
            self.vertices.extend([tuple(p-side*w/2), tuple(p+Vector((0,0,width*.13))), tuple(p+side*w/2)])
        for j in range(n-1):
            for k in range(2):
                q=start+j*3+k
                self.faces.append((q,q+3,q+4,q+1))

    def finish(self, col):
        mesh=bpy.data.meshes.new(self.name)
        mesh.from_pydata(self.vertices,[],self.faces)
        mesh.materials.append(self.mat)
        obj=bpy.data.objects.new(self.name,mesh)
        col.objects.link(obj)
        for face in mesh.polygons:
            face.use_smooth=True
        return obj


def finish_nonempty(builder, col):
    """Do not publish absent seasonal features as empty native mesh objects."""
    if builder.vertices and builder.faces:
        return builder.finish(col)
    return None


def base_meta(botanical, sources, limitations, habitat):
    return dict(botanical_name=botanical, browse_tags=['xeriscape','water-wise'],
                sources=sources, source_notes='Original deterministic species-informed geometry; no external images or meshes.',
                visual_accuracy_limitations=limitations,
                site_selection=dict(climate_basis=habitat,sun='Full sun; verify actual site exposure',
                    soil='Well-drained; site-specific soil suitability requires local review',
                    water='Establishment irrigation required; ongoing needs depend on climate and soil',
                    salt_spray='unknown',saline_inundation='unknown',fire_safety='not evaluated'),
                generator='tools/library/plants/xeric.py',
                preferred_detail_variant='eyelash-seedheads' if botanical == 'Bouteloua gracilis' else None,
                modeled_size_basis='Dimensions measured from the native meshes; not a mature spacing recommendation.',
                rootstock='not applicable',cultivar='species-inspired unspecified seed strain unless variant states otherwise')


def build_grama():
    reset()
    variants=[]
    specs=[('young-green','Young green bunch; lower narrow arching blades, no mature seedheads.',.32,0,701),
           ('eyelash-seedheads','Mature arching blue-green bunch with one-sided comb-like eyelash seedheads.',.65,32,702),
           ('dormant-straw','Dormant straw bunch with splayed stems and retained dry asymmetric seedheads.',.57,26,703)]
    for vid,desc,height,heads,seed in specs:
        rng=random.Random(seed); col=collection('blue-grama__'+vid)
        dry=vid=='dormant-straw'
        mats=[material('Grama '+vid+str(i),(.40+i*.04,.28+i*.035,.12+i*.02) if dry else (.075+i*.025,.19+i*.023,.085+i*.018),.72,.05) for i in range(3)]
        blades=[Ribbons('Narrow arching blades '+str(i),m) for i,m in enumerate(mats)]
        culms=MeshBuilder('Fine seed culms',mats[1]); seeds=MeshBuilder('One-sided spikelets',material('Grama bronze seed',(.24,.18,.07),.8))
        for i in range(170 if heads else 115):
            a=rng.random()*TAU; length=height*rng.uniform(.42,.78); base=point(a,rng.random()*.085)
            reach=rng.uniform(.06,.22)*(height/.5)
            path=[base+point(a,reach*t*t,length*(1.5*t-.58*t*t)) for t in [0,.16,.34,.52,.7,.86,1]]
            blades[i%3].blade(path,rng.uniform(.0018,.0036),a+math.pi/2)
        for i in range(heads):
            a=rng.random()*TAU; end=point(a,rng.uniform(.04,.22),height*rng.uniform(.69,1)); root=point(a,rng.uniform(.006,.06))
            culms.tube([root,root.lerp(end,.5)-point(a,.025),end],[.0013,.001,.0006],5)
            lateral=point(a+1.1,1)
            for offset in ([0,.038] if i%4==0 else [0]):
                p=end-Vector((0,0,offset)); points=[p+lateral*.06*t+Vector((0,0,.009*math.sin(t*math.pi))) for t in [0,.25,.5,.75,1]]
                culms.tube(points,[.0007]*5,5)
                for j in range(24):
                    t=j/24; q=p+lateral*.06*t+Vector((0,0,.009*math.sin(t*math.pi)))
                    tip=q+point(a-.6,.006, -.009-rng.random()*.004)
                    seeds.tube([q,tip],[.0007,.00025],4)
                    seeds.tube([tip,tip+Vector((0,0,-.004))],[.00023,.00005],3)
        for b in blades:finish_nonempty(b, col)
        finish_nonempty(culms, col); finish_nonempty(seeds, col)
        col['deterministic_seed']=seed; variants.append((vid,col,desc))
    save_family('blue-grama','Blue grama',variants,base_meta('Bouteloua gracilis',[{'url':'https://extension.colostate.edu/resource/native-grasses-for-use-in-colorado-landscapes/','supports':'Prairie grass selection; narrow bunch habit and distinctive seedheads.'}], 'Species-informed silhouette; small spikelets simplified at submillimeter scale.', 'Sunny prairie and steppe; water-wise is a browse tag, not approval for every dry climate.'))


def build_bluestem():
    reset(); variants=[]
    specs=[('summer-blue','Upright blue-green summer tussock with narrow folded blades.',False,False,711),
           ('copper-autumn','Copper autumn clump with taller reddish jointed stems and developing racemes.',True,False,712),
           ('winter-seed','Open standing winter clump with tan blades and retained pale hairy seeds.',True,True,713)]
    for vid,desc,autumn,winter,seed in specs:
        rng=random.Random(seed); col=collection('little-bluestem__'+vid)
        colors=[(.21,.34,.30),(.14,.25,.22),(.32,.39,.27)] if not autumn else ([(.49,.36,.20),(.59,.43,.25),(.33,.24,.14)] if winter else [(.43,.17,.065),(.29,.12,.07),(.58,.27,.10)])
        mats=[material(vid+str(i),v,.72,.04) for i,v in enumerate(colors)]
        blades=[Ribbons('Folded upright blades '+str(i),m) for i,m in enumerate(mats)]
        stalks=MeshBuilder('Jointed culms',mats[1]); hairs=MeshBuilder('Raceme awns and silky hairs',material('Pale seed hairs',(.74,.66,.48),.9))
        for i in range(155):
            a=rng.random()*TAU; base=point(a,rng.random()*.12); h=rng.uniform(.40,.85); reach=rng.uniform(.055,.19)
            path=[base+point(a,reach*t*t,h*(1.24*t-.30*t*t)) for t in [0,.18,.36,.55,.73,.9,1]]
            blades[i%3].blade(path,rng.uniform(.003,.006),a+math.pi/2)
        for i in range(48):
            a=rng.random()*TAU; root=point(a,rng.uniform(0,.09)); top=point(a,rng.uniform(.04,.19),rng.uniform(.75,1.12)); stalks.tube([root,root.lerp(top,.48),top],[.0019,.0014,.0007],6)
            for level in [.3,.47,.65,.82]:
                p=root.lerp(top,level); side=point(a+.8,.10*(1-level),.12)
                blades[i%3].blade([p,p+side*.65,p+side],.004,a)
                if autumn:
                    q=p+point(a+.8,.042,.105)
                    stalks.tube([p,q],[.0007,.00025],5)
                    for k in range(10 if winter else 6):
                        s=p.lerp(q,.25+.7*k/10)
                        hairs.tube([s,s+point(a+k*.6,.007,.024)],[.00028,.00003],3)
                        if winter:
                            for j in range(3):hairs.tube([s,s+point(a+j*1.8,.009,.013)],[.00012,.00002],3)
        for b in blades:finish_nonempty(b, col)
        finish_nonempty(stalks, col); finish_nonempty(hairs, col); col['deterministic_seed']=seed
        variants.append((vid,col,desc))
    save_family('little-bluestem','Little bluestem',variants,base_meta('Schizachyrium scoparium',[{'url':'https://plants.ces.ncsu.edu/plants/schizachyrium-scoparium/','supports':'Upright bunchgrass; blue-green summer, copper seasonal change and persistent hairy seeds.'}], 'Awn/hair density simplified for architectural scene performance.', 'Sunny prairie garden with drainage; selection for region and soil remains site-specific.'))


def flower_tube(mesh,base,direction,length,radius):
    """Hollow curved fused corolla with an open five-lobed mouth, not a cylinder cap."""
    axis=Vector(direction).normalized(); side=axis.cross(Vector((0,0,1)))
    if side.length<.1:side=axis.cross(Vector((0,1,0)))
    side.normalize(); up=side.cross(axis).normalized()
    verts=[]; faces=[]
    for k in range(6):
        t=k/5; center=Vector(base)+axis*length*t+up*.002*t*t
        for j in range(15):
            a=TAU*j/15; r=radius*(.34+.52*t+.14*t*t)
            lobe=(.0018*math.cos(5*a)) if k==5 else 0
            verts.append(center+side*math.cos(a)*r+up*math.sin(a)*r+axis*lobe)
    for k in range(5):
        for j in range(15):faces.append((k*15+j,k*15+(j+1)%15,(k+1)*15+(j+1)%15,(k+1)*15+j))
    # Own mesh component appended to MeshBuilder via an isolated Blender mesh later.
    mesh[0].extend([tuple(v) for v in verts]); off=len(mesh[0])-len(verts); mesh[1].extend([tuple(off+x for x in f) for f in faces])


def mesh_object(name,data,mat,col):
    me=bpy.data.meshes.new(name); me.from_pydata(data[0],[],data[1]); me.materials.append(mat)
    ob=bpy.data.objects.new(name,me); col.objects.link(ob)
    for p in me.polygons:p.use_smooth=True
    return ob


def build_penstemon():
    reset(); variants=[]
    for n,(vid,desc,bloom) in enumerate([('needle-cushion','Low evergreen needle-leaf cushion without flower stems.',None),('orange-red-bloom','Loose orange-red tubular flower spikes above a needle-leaf cushion.','red'),('mersea-yellow','Mersea Yellow cultivar interpretation with upward narrow yellow tubular flowers.','yellow')]):
        seed=721+n; rng=random.Random(seed); col=collection('pineleaf-penstemon__'+vid)
        stem=MeshBuilder('Fine woody branching stems',bark_material('Penstemon stem',(.20,.13,.075)))
        leafm=[material('Needle foliage'+str(i),(.07+i*.018,.17+i*.018,.055+i*.013),.67,.05) for i in range(3)]
        leaves=[FineLeaf('Needle leaves'+str(i),m) for i,m in enumerate(leafm)]
        flowers=([],[]); calyx=MeshBuilder('Flower calyx and pedicels',leafm[0])
        for i in range(160):
            a=rng.random()*TAU; reach=rng.uniform(.06,.24); h=rng.uniform(.11,.23)
            root=point(a,rng.random()*.045); end=point(a,reach,h); mid=root.lerp(end,.48)+Vector((0,0,.025))
            stem.tube([root,mid,end],[.0015,.0009,.00035],5)
            for j in range(13):
                t=.1+j*.068; p=root.lerp(mid,t/.48) if t <= .48 else mid.lerp(end,(t-.48)/.52)
                for k in range(2):
                    axis=point(a+j*.85+k*math.pi,.72,.6).normalized(); length=rng.uniform(.009,.017)
                    leaves[(i+j)%3].leaf(p+axis*length/2,axis,length,.0014,'needle')
            # Dense opposite needle-bearing side shoots make the evergreen cushion.
            for shoot in range(4):
                t=.20+shoot*.20
                attach=root.lerp(mid,t/.48) if t <= .48 else mid.lerp(end,(t-.48)/.52)
                sa=a+(-1 if shoot%2 else 1)*rng.uniform(.45,1.30)
                shootend=attach+point(sa,rng.uniform(.025,.045),rng.uniform(.025,.060))
                stem.tube([attach,shootend],[.00065,.00012],4)
                for node in range(20):
                    p=attach.lerp(shootend,.02+node*.048)
                    for sign in [-1,1]:
                        axis=point(sa+sign*1.05+node*.08,.80,.42).normalized()
                        length=rng.uniform(.011,.021)
                        leaves[(i+node)%3].leaf(p+axis*length/2,axis,length,.0016,'needle')
            if bloom and i%4==0:
                top=end+Vector((0,0,rng.uniform(.09,.17))); stem.tube([end,top],[.00085,.00025],5)
                for j in range(4):
                    p=end.lerp(top,.3+.19*j); axis=point(a+j*1.9,.8,.65).normalized(); base=p+axis*.008
                    calyx.tube([p,base],[.00055,.0004],5)
                    flower_tube(flowers,base,axis,.025 if bloom=='yellow' else .028,.0032)
                    for k in range(5):calyx.leaf(base+axis*.001,axis+point(k*TAU/5,.3),.004,.0013,'lance')
        finish_nonempty(stem, col)
        for b in leaves:finish_nonempty(b, col)
        finish_nonempty(calyx, col)
        if bloom:mesh_object('Open tubular five-lobed corollas',flowers,material('Yellow corolla' if bloom=='yellow' else 'Orange red corolla',(.75,.54,.035) if bloom=='yellow' else (.67,.06,.025),.48,.12),col)
        col['deterministic_seed']=seed; col['cultivar']='Mersea Yellow' if bloom=='yellow' else 'unspecified species form'; variants.append((vid,col,desc))
    meta=base_meta('Penstemon pinifolius',[{'url':'https://extension.colostate.edu/resource/herbaceous-perennials/','supports':'Dry garden perennial selection.'},{'url':'https://www.rhs.org.uk/plants/99125/penstemon-pinifolius-mersea-yellow/details','supports':'Named yellow selection, needle foliage, spreading subshrub and narrow 2.5 cm yellow tubes.'}], 'Floral tube and lobes modeled; reproductive organs simplified. Mersea Yellow form is a cultivar interpretation, not nursery provenance.', 'Sunny well-drained gravel and dry garden; winter moisture and frost tolerance require locality review.')
    meta['cultivar']='Mersea Yellow only for mersea-yellow collection; other forms unspecified species.'
    save_family('pineleaf-penstemon','Pineleaf penstemon',variants,meta)


class FineLeaf(MeshBuilder):
    """Four-quad folded pinnules; compound architecture carries visible detail."""
    def leaf(self, center, direction, length, width, style='lance', roll=0):
        axis=Vector(direction).normalized(); side=axis.cross(Vector((0,0,1)))
        if side.length<.01: side=Vector((1,0,0))
        side.normalize(); normal=side.cross(axis).normalized()
        c=Vector(center); start=len(self.vertices)
        for t,w in [(0,.00002),(.5,width/2),(1,.00001)]:
            p=c+axis*((t-.5)*length)+normal*(.035*length*math.sin(t*math.pi))
            self.vertices.extend([tuple(p-side*w),tuple(p+normal*w*.12),tuple(p+side*w)])
        for j in range(2):
            for k in range(2):
                q=start+j*3+k; self.faces.append((q,q+1,q+4,q+3))
        return self


def fern_leaf(leaves,stems,p,axis,length,rng):
    axis=Vector(axis).normalized(); side=axis.cross(Vector((0,0,1)))
    if side.length<.01:side=Vector((1,0,0))
    side.normalize(); end=p+axis*length
    stems.tube([p,end],[.0006,.00014],4)
    for j in range(5):
        t=.12+j*.17; center=p+axis*length*t; pairsize=length*.29*math.sin(math.pi*t)
        for sign in [-1,1]:
            direction=(side*sign*.85+axis*.55).normalized(); mid=center+direction*pairsize
            stems.tube([center,mid],[.00025,.0001],3)
            # Twice-divided foliage: each pinna bears tiny opposite lobed leaflets.
            for k in range(3):
                pos=center.lerp(mid,.20+k*.32)
                for sign2 in [-1,1]:
                    d=(direction*.45+axis*sign2*.8).normalized(); size=length*.135*(1-k*.19)
                    leaves.leaf(pos+d*size/2,d,size,size*.56,'lobed')
    leaves.leaf(end-axis*.004,axis,.012,.004,'lance')


def build_fernbush():
    reset(); variants=[]
    specs=[('young-lacy','Young open lacy shrub with twice-divided fern-like foliage.',.70,False,False,731),('mature-white-bloom','Spreading mature shrub with many white terminal panicles and lacy foliage.',1.55,True,False,732),('winter-structure','Sparse winter branching shrub with reduced dry foliage and spent panicles.',1.34,False,True,733)]
    for vid,desc,size,bloom,winter,seed in specs:
        rng=random.Random(seed); col=collection('fernbush__'+vid)
        bark=bark_material('Fernbush reddish woody stems',(.20,.10,.055)); stems=MeshBuilder('Open branching skeleton',bark)
        leafmat=material('Dry fernbush foliage' if winter else 'Gray green fernbush foliage',(.24,.21,.13) if winter else (.14,.23,.10),.72,.05)
        leaf=FineLeaf('Twice divided fern-like foliage',leafmat); axes=MeshBuilder('Leaf rachises',leafmat)
        flowers=FineLeaf('Five petal white panicle flowers',material('Fernbush ivory',(.82,.78,.60),.65,.1)); centers=MeshBuilder('Flower centers',material('Fernbush pollen',(.43,.29,.07),.65))
        count=11 if winter else 17
        for i in range(count):
            a=TAU*i/count+rng.uniform(-.18,.18); tip=point(a,size*rng.uniform(.23,.50),size*rng.uniform(.47,.94)); root=point(a,.02)
            middle=root.lerp(tip,.5)+Vector((0,0,size*.06)); stems.tube([root,middle,tip],[size*.012,size*.006,.0015],7)
            for j in range(6 if winter else 8):
                t=.26+.088*j; p=root.lerp(middle,t/.5) if t <= .5 else middle.lerp(tip,(t-.5)/.5); branchend=p+point(a+(1 if j%2 else -1)*.8,size*.25*(1-t*.4),size*.11)
                stems.tube([p,branchend],[.003,.0007],5)
                for k in range(9 if not winter else 1):
                    q=p.lerp(branchend,.07+k*.11); direction=point(a+k*2.4,1,.26)
                    fern_leaf(leaf,axes,q,direction,rng.uniform(.10,.165)*(size/.9)**.28,rng)
                if bloom or winter:
                    panicle=branchend+Vector((0,0,.11)); stems.tube([branchend,panicle],[.0009,.0003],4)
                    for k in range(25 if bloom else 5):
                        t=k/(25 if bloom else 5); cp=branchend.lerp(panicle,t)+point(k*2.4,.041*(1-t)**.5,0)
                        stems.tube([branchend.lerp(panicle,t),cp],[.00035,.0001],3)
                        if bloom:
                            centers.ellipsoid(cp,(.0017,.0017,.0017),4,3)
                            for l in range(5):
                                d=point(l*TAU/5,1,.12); flowers.leaf(cp+d*.003,d,.006,.0042,'oval')
        finish_nonempty(stems, col); finish_nonempty(leaf, col); finish_nonempty(axes, col); finish_nonempty(flowers, col); finish_nonempty(centers, col); col['deterministic_seed']=seed; variants.append((vid,col,desc))
    save_family('fernbush','Fernbush',variants,base_meta('Chamaebatiaria millefolium',[{'url':'https://arapahoe.extension.colostate.edu/2025/09/03/from-the-hort-desk-23/','supports':'Intermountain shrub selection; fern-like foliage and white flowers.'}], 'Foliage twice divided, white five-petal flowers aggregated into panicles; tiny leaflet serrations simplified.', 'Intermountain western garden shrub; allow mature spreading habit and verify local hardiness.'))


def build_coneflower():
    reset(); variants=[]
    specs=[('yellow-rays','Yellow ray flowers with elongated brown-green centers and finely divided foliage.',False,False,741),('red-yellow-rays','Red-brown ray bases with yellow tips; distinctly drooping rays around tall cones.',True,False,742),('dry-cones','Dry elongated seed cones above sparse dormant tan stems and foliage.',False,True,743)]
    for vid,desc,red,dry,seed in specs:
        rng=random.Random(seed); col=collection('prairie-coneflower__'+vid)
        green=material('Ratibida dry' if dry else 'Ratibida foliage',(.31,.23,.12) if dry else (.12,.22,.065),.75,.03); stem=MeshBuilder('Slender branching stems',green); leaf=MeshBuilder('Divided narrow leaves',green)
        centers=MeshBuilder('Elongated central cones',material('Brown cone',(.105,.062,.023),.85)); dots=MeshBuilder('Individual disk florets',material('Olive golden floret tips',(.23,.18,.038) if not dry else (.17,.115,.055),.8))
        rays=Ribbons('Drooping ray petals',material('Rust red ray base' if red else 'Golden ray petals',(.36,.039,.015) if red else (.85,.53,.012),.56,.07)); tips=Ribbons('Yellow ray tips',material('Golden ray margin',(.94,.61,.016),.55,.07))
        for i in range(18):
            a=rng.random()*TAU; root=point(a,rng.uniform(0,.075)); top=point(a,rng.uniform(.05,.24),rng.uniform(.44,.81)); stem.tube([root,root.lerp(top,.52),top],[.002,.00135,.00075],6)
            for j in range(3 if dry else 6):
                p=root.lerp(top,.12+j*.09); d=point(a+j*2.4,1,.18); end=p+d*.08; stem.tube([p,end],[.0006,.00015],4)
                for k in range(3):
                    mid=p.lerp(end,.25+.22*k)
                    for sign in [-1,1]:
                        axis=point(a+j*2.4+sign*.8,1,.1); length=.04*(1-k*.17)
                        leaf.leaf(mid+axis*length/2,axis,length,.0035,'lance')
                leaf.leaf(end,d,.028,.003,'lance')
            length=rng.uniform(.027,.042); radius=rng.uniform(.006,.008); c=top+Vector((0,0,length/2))
            centers.ellipsoid(c,(radius,radius,length/2),12,8)
            for j in range(65):
                t=(j+.5)/65; phi=j*2.399; width=radius*math.sqrt(max(0,1-(2*t-1)**2)); q=top+point(phi,width,length*t)
                dots.ellipsoid(q,(.0011,.0011,.0012),5,3)
            if not dry:
                for j in range(6):
                    a2=j*TAU/6+rng.uniform(-.13,.13); direction=point(a2,1); L=rng.uniform(.029,.039)
                    path=[top+direction*(.004+.017*t)+Vector((0,0,-L*t*t)) for t in [0,.2,.4,.6,.8,1]]
                    rays.blade(path,.010,a2+math.pi/2,False)
                    if red:
                        tip_path=[top+direction*(.004+.017*t)+Vector((0,0,-L*t*t+.00012)) for t in [.8,.9,1]]
                        tips.blade(tip_path,.008,a2+math.pi/2,False)
        for ob in [stem,leaf,centers,dots]:finish_nonempty(ob, col)
        finish_nonempty(rays, col); finish_nonempty(tips, col); col['deterministic_seed']=seed; col['botanical_form']='forma pulcherrima interpretation' if red else 'species form'; variants.append((vid,col,desc))
    save_family('prairie-coneflower','Prairie coneflower',variants,base_meta('Ratibida columnifera',[{'url':'https://plantfinder.mobot.org/PlantFinderDetails.aspx?taxonid=277224','supports':'Clump-forming 1–3 foot habit, long central disk and drooping rays; brownish-purple form pulcherrima.'}], 'Species-informed architectural asset; ray color variation is a form interpretation, not a nursery cultivar guarantee. Individual disk florets simplified.', 'Sunny prairie and low-water garden with suitable drainage; verify local range and soil.'))


if __name__=='__main__':
    functions={'blue-grama':build_grama,'little-bluestem':build_bluestem,'pineleaf-penstemon':build_penstemon,'fernbush':build_fernbush,'prairie-coneflower':build_coneflower}
    chosen=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(functions)
    for slug in chosen:functions[slug]()
    print('XERIC_FAMILIES_COMPLETE',chosen)
