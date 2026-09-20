"""Original suburban plant families. Blender background publisher; meters, fixed seeds.

Run from repository root with Blender --background --python this/file.py.
Only overwrites the five unadopted v001 families owned by this publisher.
"""
from pathlib import Path
import sys
import math
import random
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import material, bark_material, MeshBuilder, collection, reset, save_family

TAU = math.tau


class Blades:
    """Batch folded, serrated and palmately dissected leaf geometry."""
    def __init__(self, name, mat):
        self.name, self.mat = name, mat
        self.v, self.f = [], []

    def polygon(self, center, xaxis, yaxis, outline, fold=0.0):
        center, xaxis, yaxis = Vector(center), Vector(xaxis), Vector(yaxis)
        normal = xaxis.cross(yaxis).normalized()
        start = len(self.v)
        self.v.append(tuple(center + normal * fold))
        self.v.extend(tuple(center + xaxis*x + yaxis*y) for x, y in outline)
        n = len(outline)
        self.f.extend((start, start+1+i, start+1+(i+1)%n) for i in range(n))

    def leaf(self, base, direction, length, width, kind, roll=0):
        axis = Vector(direction).normalized()
        side = axis.cross(Vector((0, 0, 1)))
        if side.length < .01:
            side = axis.cross(Vector((0, 1, 0)))
        side.normalize()
        normal = axis.cross(side)
        side = side*math.cos(roll) + normal*math.sin(roll)
        center = Vector(base) + axis*length*({'heart':1/6,'dissected':.25}.get(kind,.5))
        if kind == 'dissected':
            # Seven long slender palmately arranged fingers, deep sinuses,
            # coarse secondary incisions along each side: no generic star cards.
            outline = [(0,-length*.25)]
            for k in range(7):
                a = -.99*math.pi + k*1.98*math.pi/6
                reach = length * (.53 + .47*math.cos(a/2))
                root = .105*length
                for u, offset in ((root,-.12),(.40*reach,-.11),(.48*reach,-.05),
                                  (.70*reach,-.08),(reach,0),(.70*reach,.08),
                                  (.48*reach,.05),(.40*reach,.11),(root,.12)):
                    outline.append((math.sin(a+offset)*u, math.cos(a+offset)*u-length*.25))
            self.polygon(center, side, axis, outline, length*.045)
        else:
            outline = []
            steps = 12 if length < .03 else 32
            for k in range(steps):
                a = TAU*k/steps
                if kind == 'heart':
                    # Broad cordate blade with two basal shoulders and a cleft.
                    x = math.sin(a)**3 * width*.5
                    y = (13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a))/30*length
                    outline.append((x, -y))
                else:
                    wave = (1 if k%2 else .92)
                    lobes = 1 + (.18*math.cos(3*a) if kind == 'ninebark' else 0)
                    outline.append((math.sin(a)*width*.5*wave*lobes, math.cos(a)*length*.5*wave))
            self.polygon(center, side, axis, outline, length*.045)

    def finish(self, col):
        if not self.v:
            return
        mesh = bpy.data.meshes.new(self.name)
        mesh.from_pydata(self.v, [], self.f)
        mesh.materials.append(self.mat)
        mesh.update()
        obj = bpy.data.objects.new(self.name, mesh)
        col.objects.link(obj)


def palette(prefix, rgb, season='summer'):
    return [material(prefix+str(i), tuple(min(1,c*f) for c in rgb), .48, .04)
            for i,f in enumerate((.70,1,1.24))]


def curved(builder, pts, r):
    pts=[Vector(p) for p in pts]
    smooth=[]
    for j in range(len(pts)-1):
        p0,p1,p2,p3=pts[max(0,j-1)],pts[j],pts[j+1],pts[min(len(pts)-1,j+2)]
        for step in range(4):
            t=step/4
            smooth.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
    smooth.append(pts[-1])
    builder.tube(smooth, [r*(1-.92*i/(len(smooth)-1)) for i in range(len(smooth))], sides=7)
    return smooth


def on_path(points, fraction):
    """Exact centerline interpolation along the authored tube's segment path."""
    scaled=min(1,max(0,fraction))*(len(points)-1)
    idx=min(len(points)-2,int(scaled))
    return points[idx].lerp(points[idx+1],scaled-idx)


def shoot(leaves, wood, rng, start, end, kind, length, width, pairs=7):
    start, end = Vector(start), Vector(end)
    wood.tube([start, end], [.0035, .0008], sides=5)
    delta = end-start
    outward = Vector((delta.x, delta.y, .15)).normalized()
    side = Vector((-outward.y, outward.x, .13))
    for j in range(pairs):
        t = .18+.80*j/max(1,pairs-1)
        point = start + delta*t
        for sign in (-1,1):
            direction = (outward*.40+side*sign + Vector((0,0,rng.uniform(-.55,.5)))).normalized()
            petiole = point + direction * length*.17
            wood.tube([point,petiole], [.0012,.0007], sides=4)
            leaves[rng.randrange(len(leaves))].leaf(petiole,direction,length*rng.uniform(.82,1.12),width,kind,rng.uniform(-.55,.55))


def tree_skeleton(wood,rng,height,spread,multi=False,weeping=False,muscle=False,full_crown=False):
    """Connected trunk scaffolds return woody terminal branches for foliage."""
    endpoints=[]
    stems = 3 if multi else 1
    for s in range(stems):
        angle=TAU*s/stems + .4
        base=Vector((.07*math.cos(angle),.07*math.sin(angle),0))
        fork=Vector((math.cos(angle)*spread*.12 if multi else .06,
                     math.sin(angle)*spread*.12 if multi else -.04,height*.50))
        pts=[base,base.lerp(fork,.3)+Vector((.07,-.02,0)),base.lerp(fork,.7),fork]
        trunk_path=curved(wood,pts,height*.034/(1 if not multi else 1.5))
        if muscle:
            # Long, merging low relief flutes over the trunk rather than a smooth pole.
            for k in range(7):
                a=TAU*k/7
                rib=[]
                for t in (0,.2,.45,.7,1):
                    p=base.lerp(fork,t)
                    radius=height*.024*(1-.75*t)
                    rib.append(p+Vector((math.cos(a+t*.4)*radius,math.sin(a+t*.4)*radius,0)))
                curved(wood,rib,height*.010)
        branches=(10 if not multi else 6) if full_crown else (7 if not multi else 5)
        for j in range(branches):
            a=TAU*j/branches+s*.65+rng.uniform(-.3,.3)
            attachment=on_path(trunk_path,.50+.49*j/max(1,branches-1)) if full_crown else base.lerp(fork,.65+.35*j/max(1,branches-1))
            z=height*(.64+.27*rng.random())
            end=Vector((math.cos(a)*spread*.45,math.sin(a)*spread*.45,z))
            elbow=attachment.lerp(end,.52)+Vector((0,0,height*.11))
            primary_path=curved(wood,[attachment,elbow,end],height*.013)
            secondary_count=13 if full_crown else 9
            for k in range(secondary_count):
                t=.08+.90*k/(secondary_count-1)
                attach=on_path(primary_path,.24+.74*k/(secondary_count-1)) if full_crown else elbow.lerp(end,t)
                az=a+((-1 if k%2 else 1)*rng.uniform(.4,1.10))
                extension=spread*rng.uniform(.14,.25)
                terminal=attach+Vector((math.cos(az)*extension,math.sin(az)*extension,
                                       -height*rng.uniform(.15,.29) if weeping else height*rng.uniform(-.025,.20) if full_crown else height*rng.uniform(.08,.16)))
                midpoint=attach.lerp(terminal,.5)+Vector((0,0,height*.07 if weeping else .02))
                secondary_path=curved(wood,[attach,midpoint,terminal],height*.0038)
                endpoints.append(secondary_path if full_crown else [attach,terminal])
    return endpoints


def leaf_tree(slug,variant,rng,height,spread,multi,kind,color,leaflength,leafwidth,
              weeping=False,muscle=False,flowers=False,dormant=False):
    col=collection(slug+'__'+variant)
    bark=bark_material(slug+' bark',(.27,.22,.16) if not muscle else (.35,.37,.33))
    wood=MeshBuilder('Connected woody structure',bark)
    leaves=[Blades('Foliage '+str(i),m) for i,m in enumerate(palette(slug+' leaves',color))]
    full_crown=(kind=='heart' or muscle)
    ends=tree_skeleton(wood,rng,height,spread,multi,weeping,muscle,full_crown)
    blossom=MeshBuilder('Redbud pea flower clusters',material('Redbud rose-purple',(.70,.095,.28),.5,.04))
    for path in ends:
        start,end=path[0],path[-1]
        delta=end-start
        if flowers:
            for t in (.15,.3,.48,.65,.85):
                point=on_path(path,t)
                for j in range(6):
                    a=TAU*j/6
                    stem=point+Vector((math.cos(a)*.028,math.sin(a)*.028,.012))
                    wood.tube([point,stem],[.001,.0007],sides=4)
                    # Short pea-like standard and keel petals on naked wood.
                    blossom.ellipsoid(stem,(.009,.006,.014),segments=6,rings=4)
                    blossom.ellipsoid(stem+Vector((.006,0,-.007)),(.008,.005,.006),segments=6,rings=4)
        if not dormant and not flowers:
            count=4 if multi else 6
            for k in range(count):
                t=.12+k*.85/(count-1)
                point=on_path(path,t)
                a=math.atan2(delta.y,delta.x)+(-1 if k%2 else 1)*1.1
                shoot_length=rng.uniform(.36,.62) if full_crown else rng.uniform(.30,.48)
                if full_crown: a+=rng.uniform(-.7,.7)
                finish=point+Vector((math.cos(a)*shoot_length,math.sin(a)*shoot_length,-rng.uniform(.18,.36) if weeping else rng.uniform(-.16,.38) if full_crown else rng.uniform(.12,.30)))
                pairs=(5 if multi else 6) if kind=='dissected' else 7
                shoot(leaves,wood,rng,point,finish,kind,leaflength,leafwidth,pairs=pairs)
    wood.finish(col)
    for leaf in leaves: leaf.finish(col)
    if flowers: blossom.finish(col)
    return col


def hydrangea(variant,seed,tree=False,pink=False):
    rng=random.Random(seed)
    col=collection('panicle-hydrangea__'+variant)
    wood=MeshBuilder('Hydrangea connected stems',bark_material('Hydrangea tan bark',(.33,.25,.15)))
    leaves=[Blades('Opposite serrated hydrangea leaves '+str(i),m) for i,m in enumerate(palette('Hydrangea',(.13,.28,.055)))]
    florets=[Blades('Four-sepal sterile florets '+str(i),material('Hydrangea petals '+str(i),c,.6,.05)) for i,c in enumerate(
        ((.77,.76,.59),(.95,.94,.81),(.76,.48,.47)) if pink else ((.80,.86,.55),(.95,.94,.81),(.87,.89,.70)))]
    base=Vector((0,0,1.05 if tree else 0))
    if tree: wood.tube([(0,0,0),(.025,0,.55),base],[.055,.043,.027],sides=9)
    for b in range(19 if tree else 25):
        a=TAU*b/19+rng.uniform(-.25,.25)
        radius=rng.uniform(.45,.85) if tree else rng.uniform(.45,.98)
        tip=Vector((math.cos(a)*radius,math.sin(a)*radius,base.z+rng.uniform(.7,1.15)))
        mid=base.lerp(tip,.57)+Vector((0,0,.16))
        curved(wood,[base,mid,tip],.014 if tree else .021)
        shoot(leaves,wood,rng,mid,tip,'oval',.14,.076,pairs=5)
        for q in range(3):
            point=base.lerp(mid,.36+q*.23)
            la=a+(-1 if q%2 else 1)*.7
            lateral=point+Vector((math.cos(la)*.29,math.sin(la)*.29,.17))
            shoot(leaves,wood,rng,point,lateral,'oval',.14,.078,pairs=5)
        # Explicit tapering cone, dozens of four-sepal flowers rather than blobs.
        h=rng.uniform(.25,.36)
        wood.tube([tip,tip+Vector((0,0,h))],[.0025,.0008],sides=5)
        for level in range(8):
            frac=level/8
            r=.115*(1-frac)+.009
            n=max(3,round(16*(1-frac)))
            for k in range(n):
                a=TAU*k/n+level*.83
                center=tip+Vector((math.cos(a)*r,math.sin(a)*r,h*frac))
                wood.tube([tip+Vector((0,0,h*frac)),center],[.0007,.0003],sides=3)
                f=florets[2 if pink and rng.random()<.6 else rng.randrange(2)]
                for p in range(4):
                    pa=TAU*p/4+a
                    direction=Vector((math.cos(pa),math.sin(pa),rng.uniform(-.2,.3)))
                    f.leaf(center,direction,.025,.021,'oval',0)
    wood.finish(col)
    for obj in leaves+florets: obj.finish(col)
    return col


def ninebark(variant,seed,compact=False,winter=False):
    rng=random.Random(seed)
    col=collection('ninebark__'+variant)
    wood=MeshBuilder('Arching ninebark canes',bark_material('Ninebark warm stems',(.29,.18,.09)))
    peels=Blades('Exfoliating bark ribbons',material('Ninebark exposed underbark',(.50,.31,.16),.9))
    leaves=[Blades('Three-lobed ninebark foliage '+str(i),m) for i,m in enumerate(palette('Ninebark',(.19,.045,.075) if compact else (.16,.30,.055)))]
    h=1.35 if compact else 2.1
    for b in range(22 if compact else 29):
        a=TAU*b/19
        base=Vector((rng.uniform(-.18,.18),rng.uniform(-.18,.18),0))
        mid=Vector((math.cos(a)*h*.30,math.sin(a)*h*.30,h*rng.uniform(.7,.94)))
        end=Vector((math.cos(a)*h*.62,math.sin(a)*h*.62,h*rng.uniform(.48,.72)))
        curved(wood,[base,base.lerp(mid,.48),mid,end],.022 if compact else .033)
        for j in range(5):
            p=base.lerp(mid,.1+j*.13)
            peels.polygon(p,Vector((.018,0,.001)),Vector((0,.01,.18)),[(-1,-.5),(.8,-.46),(1,.15),(.4,.6),(-.6,.47)],.007)
        for k in range(6):
            point=mid.lerp(end,k/6)
            sidea=a+(-1 if k%2 else 1)*.9
            tip=point+Vector((math.cos(sidea)*.30,math.sin(sidea)*.30,.12))
            wood.tube([point,tip],[.004,.0008],sides=5)
            if not winter: shoot(leaves,wood,rng,point,tip,'ninebark',.065,.058,pairs=6)
        if not winter:
            for k in range(5):
                point=base.lerp(mid,.23+k*.145)
                sidea=a+(-1 if k%2 else 1)*.5
                tip=point+Vector((math.cos(sidea)*.35,math.sin(sidea)*.35,.16))
                shoot(leaves,wood,rng,point,tip,'ninebark',.07,.06,pairs=6)
    wood.finish(col)
    peels.finish(col)
    for obj in leaves: obj.finish(col)
    return col


def publish(slug,name,variants,botanical,cultivars,notes,source):
    selected=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    if selected and slug not in selected:
        return
    metadata={
      'botanical_name':botanical,'cultivar_or_training':cultivars,
      'browse_tags':['suburban'], 'generator':'tools/library/plants/suburban.py',
      'deterministic_seeds':dict(zip([v[0] for v in variants], range({'eastern-redbud':301,'panicle-hydrangea':321,'ninebark':331,'american-hornbeam':341,'japanese-laceleaf-maple':351}[slug],{'eastern-redbud':301,'panicle-hydrangea':321,'ninebark':331,'american-hornbeam':341,'japanese-laceleaf-maple':351}[slug]+3))),
      'sources':[source], 'site_selection':notes,
      'visual_accuracy_limits':'Original architectural visualization geometry, not botanical scanning. Modeled dimensions are specimen sizes, not mature spacing or performance claims. Native preview and host adoption are separate review stages.',
      'phenology':'Each named collection is a separate coherent state; do not combine spring, autumn and dormant variants indiscriminately.',
      'license':'CC-BY-4.0','author':'Homes project contributors',
      'external_textures':False,'host_adoption':'not adopted; site placement unverified'}
    save_family(slug,name,variants,metadata)


def main():
    reset()
    variants=[]
    for i,(ident,desc,h,w,multi,flowers,dormant) in enumerate([
      ('summer-multistem','Airy leafy multi-stem summer tree with broad cordate blades',4.0,4.4,True,False,False),
      ('spring-flowering','Single trunk early spring specimen; pea-like magenta flowers on leafless branch wood',4.2,4.2,False,True,False),
      ('winter-branching','Exposed dormant branch structure; no leaves or blossom',4.4,4.7,True,False,True)]):
        col=leaf_tree('eastern-redbud',ident,random.Random(301+i),h,w,multi,'heart',(.18,.34,.065),.11,.12,flowers=flowers,dormant=dormant)
        variants.append((ident,col,desc))
    publish('eastern-redbud','Eastern redbud',variants,'Cercis canadensis','Species concept; no cultivar asserted','Regional eastern North American garden candidate; verify local sun, moisture and form before selection. No coastal inundation or universal xeric suitability claim.','https://plants.ces.ncsu.edu/plants/cercis-canadensis/')
    reset()
    variants=[('white-shrub',hydrangea('white-shrub',321),'Rounded white cone-flowering shrub'),('late-pink-hedge',hydrangea('late-pink-hedge',322,pink=True),'Loose late-season pinking panicle shrub; untrimmed hedge building block'),('trained-tree',hydrangea('trained-tree',323,tree=True),'Young trained standard; explicit trunk below cone-flowering crown')]
    publish('panicle-hydrangea','Panicle hydrangea',variants,'Hydrangea paniculata','Unnamed garden selection; standard denotes training, not a dwarf cultivar','Sun/partial shade and adequate moisture; cultivar, pruning and locality affect ultimate size. Late pink tones represent aging panicles, not a named cultivar claim.','https://plants.ces.ncsu.edu/plants/hydrangea-paniculata/')
    reset()
    variants=[('arching-green',ninebark('arching-green',331),'Arching green-leaf shrub'),('compact-burgundy',ninebark('compact-burgundy',332,compact=True),'Little Devil cultivar habit study; compact burgundy foliage'),('winter-exfoliating',ninebark('winter-exfoliating',333,winter=True),'Dormant arching canes with actual curled exfoliating bark ribbons')]
    publish('ninebark','Ninebark',variants,'Physocarpus opulifolius',"Green species and compact Little Devil ('Donna May') visual habit study; cultivar performance not verified",'Select for actual summer heat, sun, soil and water. Foliage color is cultivar-specific; modeled compact size is not a species-wide mature size.','https://plants.ces.ncsu.edu/plants/physocarpus-opulifolius/')
    reset()
    variants=[]
    for i,(ident,desc,h,w,multi,color) in enumerate([
      ('young-slender','Slender young green tree',3.9,2.5,False,(.12,.25,.035)),
      ('mature-sculpted','Mature crown over fluted muscle-like trunk',6.1,5.6,False,(.13,.27,.045)),
      ('autumn-multistem','Multistem autumn orange canopy with sculpted trunks',4.8,4.7,True,(.65,.20,.035))]):
        variants.append((ident,leaf_tree('american-hornbeam',ident,random.Random(341+i),h,w,multi,'oval',color,.11,.052,muscle=True),desc))
    publish('american-hornbeam','American hornbeam',variants,'Carpinus caroliniana','Species habit studies; young/mature/multistem','Moist woodland/understory character; verify drought exposure and soil before placement. Autumn coloring varies by specimen and site.','https://plants.ces.ncsu.edu/plants/carpinus-caroliniana/')
    reset()
    variants=[]
    for i,(ident,desc,h,w,multi,weeping,color) in enumerate([
      ('green-cascade','Viridis habit study: broad green cascading dissected foliage',2.15,3.4,False,True,(.17,.32,.055)),
      ('burgundy-weeping','Crimson Queen habit study: low sweeping burgundy branch canopy',1.8,3.2,True,True,(.27,.038,.055)),
      ('upright-dissected','Seiryu habit study: upright airy branching with deeply dissected leaves',3.9,2.8,False,False,(.19,.34,.07))]):
        variants.append((ident,leaf_tree('japanese-laceleaf-maple',ident,random.Random(351+i),h,w,multi,'dissected',color,.087,.10,weeping=weeping),desc))
    publish('japanese-laceleaf-maple','Japanese laceleaf maple',variants,'Acer palmatum Dissectum Group',"Viridis, Crimson Queen and Seiryu habit studies; original geometry not exact cultivar clone",'Sheltered garden placement; assess afternoon sun, desiccating wind, drainage and climate. Fine dissected foliage and architectural habit are modeled; cultivar-specific cultivation remains a site selection decision.','https://plants.ces.ncsu.edu/plants/acer-palmatum-subsp-matsumurae/')
    selected=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    count=len(selected) if selected else 5
    print(f'SUBURBAN_PLANT_FAMILIES_BUILT {count} families / {count*3} distinct variants')


if __name__=='__main__':
    main()
