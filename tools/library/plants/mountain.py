"""Original montane plant geometry, in meters. Run with Blender --background --python.

This authors new, unadopted v001 assets. Species references inform architecture;
all meshes and procedural materials are original, with no downloaded textures.
"""
import sys
import math
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MeshBuilder, material, bark_material, collection, reset, save_family
from mathutils import Vector

TAU = 2 * math.pi
CSU = 'https://extension.colostate.edu/resource/native-shrubs-for-colorado-landscapes/'
USU = 'https://extension.usu.edu/forestry/tree-identification/poplar-aspen/quaking-aspen'
GENERATOR = 'tools/library/plants/mountain.py'


def v(x=0, y=0, z=0):
    return Vector((x, y, z))


def polar(a, r, z=0):
    return v(math.cos(a)*r, math.sin(a)*r, z)


def stem(mesh, a, b, radius, bend=.07):
    a, b = Vector(a), Vector(b)
    mid = a.lerp(b, .48)
    mesh.tube([a, mid, b], [radius, radius*.65, max(radius*.12, .0007)], sides=7)


def maple_blade(mesh, base, direction, length, width, roll):
    """Three pointed palmate lobes with small marginal teeth, not an oval card."""
    axis=Vector(direction).normalized()
    side=axis.cross(v(0,0,1)).normalized()
    normal=side.cross(axis).normalized()
    side,normal=side*math.cos(roll)+normal*math.sin(roll),normal*math.cos(roll)-side*math.sin(roll)
    outline=[(0,0),(-.18,.12),(-.29,.19),(-.24,.24),(-.44,.35),(-.37,.39),(-.50,.55),(-.24,.51),(-.19,.63),(-.13,.61),(-.12,.77),(-.065,.73),(0,1)]
    outline+= [(-x,y) for x,y in reversed(outline[1:-1])]
    start=len(mesh.vertices)
    mesh.vertices.append(tuple(Vector(base)+axis*length*.43+normal*length*.06))
    for x,y in outline:
        mesh.vertices.append(tuple(Vector(base)+side*(x*width)+axis*(y*length)+normal*(length*.025*math.sin(y*math.pi))))
    for i in range(len(outline)):
        mesh.faces.append((start,start+1+i,start+1+(i+1)%len(outline)))


def bearberry_blade(mesh, base, direction, length, width, roll):
    """Rounded obovate leathery blade with narrowed base and shallow fold."""
    axis=Vector(direction).normalized()
    side=axis.cross(v(0,0,1)).normalized()
    normal=side.cross(axis).normalized()
    side,normal=side*math.cos(roll)+normal*math.sin(roll),normal*math.cos(roll)-side*math.sin(roll)
    outline=[(0,0),(-.16,.10),(-.34,.28),(-.46,.49),(-.50,.68),(-.46,.84),(-.30,.96),(0,1)]
    outline += [(-x,y) for x,y in reversed(outline[1:-1])]
    start=len(mesh.vertices)
    mesh.vertices.append(tuple(Vector(base)+axis*length*.52+normal*length*.036))
    for x,y in outline:
        mesh.vertices.append(tuple(Vector(base)+side*x*width+axis*y*length+normal*length*.015*math.sin(y*math.pi)))
    for i in range(len(outline)):
        mesh.faces.append((start,start+1+i,start+1+(i+1)%len(outline)))


class Parts:
    def __init__(self, name, leaf_color, bark_color, seed, red=False):
        self.r = random.Random(seed)
        self.wood = MeshBuilder(name+'_attached_branches', bark_material(name+'_bark', bark_color))
        self.leaves = [MeshBuilder(name+'_leaves_'+str(i), material(name+'_leaf_'+str(i), tuple(c*f for c in leaf_color), roughness=.43)) for i,f in enumerate((.82,1,1.13))]
        self.petioles = MeshBuilder(name+'_petioles', material(name+'_petiole', (.22,.13,.052) if not red else (.24,.023,.025)))
        self.flowers = MeshBuilder(name+'_flower_petals', material(name+'_petal', (.88,.88,.75), roughness=.54))
        self.fruit = MeshBuilder(name+'_fruit', material(name+'_fruit_skin', (.055,.032,.105), roughness=.38))

    def foliage(self, base, axis, length, width, style='oval', count=9, opposite=False):
        """Twigs are physically joined to wood; each leaf has an attached petiole."""
        axis=Vector(axis)
        end=Vector(base)+axis
        stem(self.wood, base, end, .004 if length>.04 else .002)
        direction=axis.normalized()
        side=direction.cross(v(0,0,1)).normalized()
        if side.length<.01: side=v(1,0,0)
        for i in range(count):
            t=.15+.8*i/max(1,count-1)
            p=Vector(base)+axis*t
            for sign in ((-1,1) if opposite else ((-1 if i%2 else 1),)):
                d=(side*sign + direction*.30 + v(0,0,self.r.uniform(-.3,.65))).normalized()
                pet=length*(.70 if style=='heart' else .23)
                q=p+d*pet
                self.petioles.tube([p,q],[.0011,.0005],sides=4)
                # Shared leaf helper is centered on its blade; blade base meets petiole.
                size=length*self.r.uniform(.82,1.12)
                blade=self.leaves[self.r.randrange(3)]
                width_here=width*self.r.uniform(.85,1.1);roll=self.r.uniform(-.45,.45)
                if style=='lobed':
                    maple_blade(blade,q,d,size,width_here,roll)
                elif style=='obovate':
                    bearberry_blade(blade,q,d,size,width_here,roll)
                else:
                    blade.leaf(q+d*size*.5,d,size,width_here,style=style,roll=roll)
        return end

    def flower(self, center, scale=1, petals=5):
        center=Vector(center)
        for k in range(petals):
            d=polar(k*TAU/petals,1,.18).normalized()
            self.flowers.leaf(center+d*.005*scale,d,.014*scale,.0065*scale,style='oval')
        self.flowers.ellipsoid(center,(.0025*scale,)*3,segments=6,rings=3)

    def finish(self,col):
        for mesh in [self.wood,self.petioles,*self.leaves,self.flowers,self.fruit]:
            if mesh.vertices:
                mesh.finish(col)


def meta(botanical, notes, variants, source=CSU):
    profiles={
        'Populus tremuloides':('Quaking aspen',110,'Cool moist mountain setting; avoid hot dry valleys. Full sun; moist soil.'),
        'Acer glabrum':('Rocky Mountain maple',220,'Foothill to montane understory; low to moderate moisture; tolerates shade.'),
        'Amelanchier alnifolia':('Saskatoon serviceberry',330,'Foothill through subalpine candidate; low to moderate moisture. Verify local soil and sun.'),
        'Cornus sericea':('Red-osier dogwood',440,'Moist streamside understory; moderate to high moisture; shade tolerant.'),
        'Arctostaphylos uva-ursi':('Kinnikinnick',550,'Well-drained gravelly ground; select local light and moisture conditions.')}
    common,seed,site=profiles[botanical]
    return {'botanical_name':botanical,'common_name':common,'source_generator':GENERATOR,'generator':GENERATOR,'browse_tags':['mountain'],
        'deterministic_seeds':[seed,seed+1,seed+2],
        'sources':[{'url':source,'purpose':'Plant habit, foliage and seasonal selection; no copied geometry or photographs.'}],
        'cultivar':'species habit; no named cultivar claimed','rootstock':'not applicable / seedling species concept',
        'modeling_notes':notes,'variant_intents':variants,
        'site_selection':{'region':'Suitable mountain/foothill sites; browse tag is not blanket approval','salt_spray':'unknown','saline_inundation':'unknown','water':'Match species and regional source; provide establishment water','sun_soil':site},
        'visual_accuracy_limitations':'Original architectural botanical interpretation; branch placement is seeded, leaves are simplified folded blades. Not a nursery product or plant performance specification.',
        'host_adoption':{'status':'not adopted','host_placement_reviewed':False}}


def aspen():
    reset()
    variants=[]
    for idx,(key,desc,offsets,autumn) in enumerate([
        ('young','Slender young tree, cool-season green foliage',[(0,0,3.8)],False),
        ('grove','Three mature pale-trunk trees with staggered crowns',[(-.8,-.35,6.5),(.65,-.3,5.7),(0,.65,6.0)],False),
        ('autumn-grove','Three differently arranged gold-leaf autumn stems',[(-.75,0,5.7),(.65,.35,6.25),(.15,-.7,5.1)],True)]):
        col=collection('QuakingAspen_'+key.replace('-','_'))
        p=Parts('Aspen_'+key,(.55,.30,.027) if autumn else (.17,.31,.046),(.64,.68,.53),110+idx)
        scars=MeshBuilder('Aspen_'+key+'_horizontal_lenticels',material('Aspen_lenticels_'+key,(.065,.071,.055)))
        for tree,(x,y,h) in enumerate(offsets):
            base=v(x,y,0); rad=h*.022
            points=[base+v(.065*math.sin(j*.8+tree)*j/8,.045*math.sin(j*1.3)*j/8,h*j/8) for j in range(9)]
            points[0]=base
            p.wood.tube(points,[max(.012,rad*(1-j/8)**.8) for j in range(9)],sides=12)
            for j in range(38):
                t=p.r.uniform(.02,.86); z=h*t
                a=p.r.uniform(0,TAU); w=p.r.uniform(.16,.5)
                center=points[min(7,int(t*8))].lerp(points[min(8,int(t*8)+1)],t*8-int(t*8))
                rr=rad*(1-t)**.8+.001
                path=[center+polar(a+(k/4-.5)*w,rr) for k in range(5)]
                scars.tube(path,[.003,.004,.004,.004,.002],sides=4)
            # Open lower trunk, fine ascending and spreading branches above.
            for b in range(25):
                t=.28+b*.026
                start=points[int(t*8)].lerp(points[int(t*8)+1],t*8-int(t*8))
                a=b*2.399+tree*.7
                reach=h*(.13+.13*math.sin((t-.25)/.7*math.pi))
                tip=start+polar(a,reach,h*p.r.uniform(.055,.13))
                stem(p.wood,start,tip,rad*.33*(1-t),.05)
                for q in range(9):
                    f=.22+q*.087
                    origin=start.lerp(tip,f)
                    aa=a+(-1 if q%2 else 1)*p.r.uniform(.35,1.3)
                    branch=polar(aa,.30+.22*(1-f),p.r.uniform(.13,.32))
                    twig_end=p.foliage(origin,branch,.061,.061,'heart',count=10)
                    if q%2==0:
                        p.foliage(origin.lerp(twig_end,.55),polar(aa+.9,.20,.17),.055,.054,'heart',count=6)
        p.finish(col);scars.finish(col)
        variants.append((key,col,desc))
    save_family('quaking-aspen','Quaking aspen',variants,meta('Populus tremuloides','Round/ovate blades on long petioles; pale trunks with horizontal dark lenticels; three-stem groves have individual ground-contact origins.',[x[2] for x in variants],USU))


def maple():
    reset(); variants=[]
    for idx,(key,desc,n,h,spread,fall) in enumerate([
        ('small-tree','Small branching understory tree',3,3.8,1.45,False),
        ('multi-stem','Broad multi-stem montane shrub',7,2.6,1.5,False),
        ('autumn','Yellow autumn shrub with staggered scaffold limbs',5,3.0,1.4,True)]):
        col=collection('RockyMountainMaple_'+key.replace('-','_'))
        p=Parts('Maple_'+key,(.49,.34,.035) if fall else (.12,.25,.037),(.20,.19,.14),220+idx)
        for s in range(n):
            a=s*TAU/n+.27
            base=polar(a,.07,0)
            tip=polar(a,spread*.42,h*p.r.uniform(.77,1))
            stem(p.wood,base,tip,.065 if h>3 else .044)
            for b in range(9):
                t=.25+b*.075
                origin=base.lerp(tip,t)
                aa=a+b*2.37
                end=origin+polar(aa,spread*(.35+.18*math.sin(t*math.pi)),.25+.16*h*(1-t))
                stem(p.wood,origin,end,.018*(1-t)+.004)
                for q in range(7):
                    z=.22+q*.1
                    start=origin.lerp(end,z)
                    direction=polar(aa+(-.8 if q%2 else .8),.23+.15*(1-z),.20)
                    p.foliage(start,direction,.085,.082,'lobed',count=6,opposite=True)
        p.finish(col);variants.append((key,col,desc))
    save_family('rocky-mountain-maple','Rocky Mountain maple',variants,meta('Acer glabrum','Multi-stem smooth gray branching and paired lobed blades. Lobes are simplified; preserve natural broad shrub versus taller small-tree habit.',[x[2] for x in variants]))


def serviceberry():
    reset();variants=[]
    for idx,(key,desc,n,h,state) in enumerate([
        ('flowering','Upright shrub, spring white racemes and emerging leaves',5,2.8,'flowers'),
        ('berry-thicket','Open multi-stem thicket bearing blue-purple fruit',8,2.4,'fruit'),
        ('autumn','Broad arching orange-red autumn shrub',6,2.7,'autumn')]):
        col=collection('SaskatoonServiceberry_'+key.replace('-','_'))
        p=Parts('Serviceberry_'+key,(.44,.11,.025) if state=='autumn' else (.14,.27,.06),(.18,.14,.105),330+idx)
        for s in range(n):
            a=s*2.399
            base=polar(a,.08,0);tip=polar(a,p.r.uniform(.45,.9),h*p.r.uniform(.82,1))
            stem(p.wood,base,tip,.027)
            for b in range(8 if state=='flowers' else 10):
                t=.23+b*(.09 if state=='flowers' else .073);origin=base.lerp(tip,t);aa=a+b*1.9
                end=origin+polar(aa,p.r.uniform(.32,.58),p.r.uniform(.1,.35))
                stem(p.wood,origin,end,.008)
                for q in range(4):
                    start=origin.lerp(end,.3+q*.19)
                    axis=polar(aa+(-.7 if q%2 else .7),.22,.17)
                    bud=p.foliage(start,axis,.048 if state!='flowers' else .034,.038 if state!='flowers' else .031,'oval',count=7 if state=='flowers' else 12)
                    if state!='flowers':
                        # Attached secondary shoots build a real leafy volume rather
                        # than leaving isolated leaf tufts on a bare scaffold.
                        for side in (-1,1):
                            sidebase=start+axis*(.32 if side<0 else .64)
                            p.foliage(sidebase,polar(aa+side*1.07,.18+p.r.random()*.08,p.r.uniform(-.03,.12)),.046,.036,'oval',count=11)
                    if state=='flowers':
                        top=bud+v(0,0,.08);stem(p.petioles,bud,top,.0016)
                        for f in range(6):
                            c=bud+polar(f*2.399,.025,.012*f)
                            stem(p.petioles,bud+v(0,0,.012*f),c,.001)
                            p.flower(c,scale=.75)
                    if state=='fruit':
                        for f in range(5):
                            c=bud+polar(f*2.399,.019,-.015-f*.006)
                            stem(p.petioles,bud,c,.001)
                            p.fruit.ellipsoid(c,(.0065,.0065,.007),segments=8,rings=4)
        p.finish(col);variants.append((key,col,desc))
    save_family('saskatoon-serviceberry','Saskatoon serviceberry',variants,meta('Amelanchier alnifolia','Upright/open thicket habit, small rounded leaves and terminal white racemes. Fruit represented as attached small blue-purple pomes; autumn uses independent branch arrangement.',[x[2] for x in variants]))


def dogwood():
    reset();variants=[]
    for idx,(key,desc,n,h,state) in enumerate([
        ('leafy','Leafy arching red-stem shrub',12,1.85,'leaf'),
        ('flowering','Broad white flat-topped flowering mass',15,1.7,'flower'),
        ('winter','Dormant dense red cane structure with bare twigs',21,2.0,'winter')]):
        col=collection('RedOsierDogwood_'+key)
        p=Parts('Dogwood_'+key,(.10,.23,.055),(.28,.025,.034),440+idx,red=True)
        for s in range(n):
            a=s*2.399; hh=h*p.r.uniform(.67,1)
            base=polar(a,.08,0);tip=polar(a,p.r.uniform(.4,1),hh)
            path=[base,base.lerp(tip,.30)+v(0,0,.2),base.lerp(tip,.72)+v(0,0,.15),tip]
            p.wood.tube(path,[.020,.014,.009,.002],sides=7)
            for b in range(8):
                t=.3+b*.082;origin=path[min(2,int(t*3))].lerp(path[min(3,int(t*3)+1)],t*3-int(t*3))
                # Opposite branching at each red cane node.
                for sign in (-1,1):
                    aa=a+sign*(.7+b*.2)
                    end=origin+polar(aa,.25+.2*(1-t),.11)
                    stem(p.wood,origin,end,.005)
                    for q in range(2):
                        st=origin.lerp(end,.5+q*.4);axis=polar(aa+sign*.6,.15,.11)
                        if state=='winter':
                            stem(p.wood,st,st+axis,.0018)
                        else:
                            terminal=p.foliage(st,axis,.075,.037,'oval',count=4,opposite=True)
                            if state=='flower' and b>3 and q==1:
                                hub=terminal+v(0,0,.027);stem(p.petioles,terminal,hub,.0018)
                                for f in range(17):
                                    rr=.040*math.sqrt((f+.5)/17)
                                    c=hub+polar(f*2.399,rr,.007*(1-rr/.04))
                                    stem(p.petioles,hub,c,.0006)
                                    p.flower(c,scale=.38,petals=4)
        p.finish(col);variants.append((key,col,desc))
    save_family('red-osier-dogwood','Red-osier dogwood',variants,meta('Cornus sericea','Arching suckering canes with opposite elliptical blades; spring flat white corymbs and a genuinely leafless winter network. Moist understory/streamside concept, not dry-slope filler.',[x[2] for x in variants]))


def kinn():
    reset();variants=[]
    for idx,(key,desc,n,reach,fruit) in enumerate([
        ('small-mat','Small leathery evergreen mat',22,.44,False),
        ('broad-mat','Wide irregular prostrate branching groundcover',45,.85,False),
        ('berry-edge','Asymmetric berry-bearing rock-edge patch',35,.69,True)]):
        col=collection('Kinnikinnick_'+key.replace('-','_'))
        p=Parts('Kinnikinnick_'+key,(.064,.16,.036),(.20,.064,.031),550+idx)
        p.fruit=MeshBuilder('Kinnikinnick_'+key+'_red_berries',material('Kinnikinnick_'+key+'_berry_skin',(.40,.028,.012),roughness=.35))
        for s in range(n):
            a=s*2.399+.3;dist=reach*p.r.uniform(.65,1)
            if fruit: dist*=.75+.25*math.cos(a)
            base=v(0,0,0);end=polar(a,dist,.10+p.r.random()*.07)
            path=[base,polar(a-.16,dist*.30,.025),polar(a+.1,dist*.65,.065),end]
            p.wood.tube(path,[.008,.006,.003,.0013],sides=6)
            for q in range(10):
                t=.08+q*.095;origin=path[int(t*3)].lerp(path[int(t*3)+1],t*3-int(t*3))
                for side in (-1,1):
                    aa=a+side*p.r.uniform(.60,1.30)
                    axis=polar(aa,.10+p.r.random()*.045,.018+p.r.random()*.035)
                    terminal=p.foliage(origin,axis,.029,.019,'obovate',count=12)
                    if fruit and q>5 and side==1 and s%3==0:
                        for f in range(3):
                            c=terminal+polar(f*TAU/3,.008,-.011)
                            stem(p.petioles,terminal,c,.0008)
                            p.fruit.ellipsoid(c,(.005,.005,.0055),segments=8,rings=4)
        p.finish(col);variants.append((key,col,desc))
    save_family('kinnikinnick','Kinnikinnick / common bearberry',variants,meta('Arctostaphylos uva-ursi','Prostrate reddish woody runners with small leathery evergreen leaves and attached red fruit. Root-centered patch has all woody trails attached; rock-edge is asymmetric geometry, not a hidden rock prop.',[x[2] for x in variants]))


if __name__=='__main__':
    requested=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    funcs={'quaking-aspen':aspen,'rocky-mountain-maple':maple,'saskatoon-serviceberry':serviceberry,'red-osier-dogwood':dogwood,'kinnikinnick':kinn}
    for key,fn in funcs.items():
        if not requested or key in requested:
            fn()
            print('MOUNTAIN_FAMILY_COMPLETE',key,flush=True)
