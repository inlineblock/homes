"""Original orchard plant geometry; run with Blender --background --python this-file.
Species silhouettes and attached foliage are illustrations, not cultivar specimens.
"""
from pathlib import Path
import sys, math, random
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

TAU=math.tau

def v(x,y,z): return Vector((x,y,z))
def polar(a,r,z): return v(math.cos(a)*r, math.sin(a)*r,z)
def mix(a,b,t): return a.lerp(b,t)
def onpath(points,t):
    f=t*(len(points)-1); i=min(int(f),len(points)-2)
    return mix(points[i],points[i+1],f-i)

def pear_mesh(name, centers, mat, col, seed=1):
    """Continuous pear profile, pointed attachment above broad basal fruit."""
    vs=[]; fs=[]; rng=random.Random(seed)
    profile=[(-.095,.014),(-.082,.043),(-.046,.057),(0,.052),(.038,.035),(.075,.016),(.095,.007)]
    for c,size in centers:
        off=len(vs); n=12
        for z,r in profile:
            for j in range(n):
                a=TAU*j/n; vs.append(tuple(c+v(r*size*math.cos(a),r*size*math.sin(a),z*size)))
        for k in range(len(profile)-1):
            for j in range(n):
                fs.append((off+k*n+j,off+k*n+(j+1)%n,off+(k+1)*n+(j+1)%n,off+(k+1)*n+j))
        fs.append(tuple(off+j for j in reversed(range(n))))
        fs.append(tuple(off+(len(profile)-1)*n+j for j in range(n)))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(vs,[],fs); mesh.materials.append(mat)
    ob=bpy.data.objects.new(name,mesh); col.objects.link(ob)
    for p in mesh.polygons: p.use_smooth=True

class Plant:
    def __init__(self,col,species,seed):
        self.col=col; self.species=species; self.r=random.Random(seed)
        colors={'avocado':[(.035,.13,.035),(.08,.23,.052),(.19,.30,.066)],
                'fig':[(.06,.22,.047),(.12,.30,.065),(.21,.36,.10)],
                'pomegranate':[(.08,.21,.028),(.17,.31,.047),(.31,.37,.067)],
                'apple':[(.06,.21,.041),(.15,.31,.065),(.27,.36,.09)]}[species]
        self.wood=C.MeshBuilder(species+'-branches', C.bark_material(species+'-bark',(.19,.14,.09) if species!='fig' else (.32,.30,.23)))
        self.leaves=[C.MeshBuilder(species+'-leaf-'+str(i),C.material(species+'-leaf-'+str(i),c,roughness=.48,subsurface=.08)) for i,c in enumerate(colors)]
        self.fruit=C.MeshBuilder(species+'-fruit',C.material(species+'-fruit',{'avocado':(.035,.095,.022),'fig':(.19,.065,.12),'pomegranate':(.42,.024,.016),'apple':(.46,.043,.019)}[species],roughness=.4))
        self.calyx=C.MeshBuilder(species+'-calyx',C.material(species+'-calyx',(.22,.09,.025),roughness=.65))
        self.bloom=C.MeshBuilder(species+'-flowers',C.material(species+'-flowers',(.8,.04,.009),roughness=.45))
        self.pear=[]; self.woody_segments=[]; self.fruit_requests=[]; self.fruit_clearance=[]; self.dense=False
    def branch(self,points,r0,r1=.003):
        n=len(points); radii=[r0+(r1-r0)*i/(n-1) for i in range(n)]; self.wood.tube(points,radii,sides=(9 if r0>.025 else 6) if self.dense else 7)
        self.woody_segments.extend((Vector(a),Vector(b),max(radii[i],radii[i+1])) for i,(a,b) in enumerate(zip(points,points[1:])))
    def blade(self,attach,d,length,width,style):
        d=Vector(d).normalized(); pet=length*.15; center=attach+d*(pet+length*.5)
        self.branch([attach,attach+d*pet],max(.001,length*.012),.0007)
        builder=self.r.choices(self.leaves,weights=[.35,.5,.15])[0]
        if self.species=='fig':
            # Five pronounced palmate lobes joined at a broad petiole sinus.
            side=d.cross(v(0,0,1)).normalized(); normal=side.cross(d).normalized()
            outline=[(0,0),(-.24,.12),(-.50,.23),(-.40,.43),(-.21,.34),(-.39,.64),(-.24,.86),(-.09,.58),(0,1),(.09,.58),(.24,.86),(.39,.64),(.21,.34),(.40,.43),(.50,.23),(.24,.12)]
            off=len(builder.vertices); base=attach+d*pet
            builder.vertices.append(tuple(base+d*(length*.42)+normal*.012))
            for x,y in outline: builder.vertices.append(tuple(base+side*(x*width)+d*(y*length)+normal*(.016*math.sin(y*math.pi))))
            for i in range(len(outline)): builder.faces.append((off,off+1+i,off+1+(i+1)%len(outline)))
        else:
            builder.leaf(center,d,length,width,style=style,roll=self.r.uniform(-.7,.7))
    def fruit_at(self,attach,size=1):
        if self.dense:
            self.fruit_requests.append((Vector(attach),size)); return
        self.real_fruit(attach,size)
    def real_fruit(self,attach,size=1,drop=.07):
        s=self.species; loc=attach+v(0,0,-drop*size); self.branch([attach,loc],.002,.0015)
        if s=='avocado':
            self.pear.append((loc-v(0,0,.095*size),size)); return
        rad={'fig':(.025,.027,.035),'pomegranate':(.055,.055,.055),'apple':(.045,.048,.042)}[s]
        center=loc-v(0,0,rad[2]*size)
        self.fruit.ellipsoid(center,tuple(x*size for x in rad),segments=12,rings=8)
        if s=='pomegranate':
            tip=center-v(0,0,rad[2]*size)
            for j in range(6):
                a=j*TAU/6; self.calyx.leaf(tip+polar(a,.009*size,-.007*size),polar(a,.7,-1),.021*size,.007*size,style='lance')
        elif s=='apple':
            self.calyx.ellipsoid(center-v(0,0,.041*size),(.009,.009,.002),segments=7,rings=4)
    def twig(self,start,d,length,foliage=True,fruit=False,flower=False):
        d=Vector(d).normalized(); end=start+d*length; mid=mix(start,end,.5)+v(0,0,.035)
        path=[start,mid,end]; self.branch(path,.007,.0018)
        s=self.species
        settings={'avocado':(.20,.060,'lance',9),'fig':(.24,.20,'lobed',5),'pomegranate':(.080,.028,'lance',13),'apple':(.095,.049,'oval',8)}
        ll,ww,style,count=settings[s]
        if self.dense:
            count=14 if s!='pomegranate' else 12
            if s=='avocado': ll=.24; ww=.075
            if s=='apple': ll=.115; ww=.058
        if foliage:
            for k in range(count):
                t=(.07+.92*k/count) if self.dense else (.16+.81*k/count); p=onpath(path,t)
                ang=math.atan2(d.y,d.x)+(1 if k%2 else -1)*1.15
                direction=polar(ang,1,self.r.uniform(-.15,.5))
                sc=self.r.uniform(.7,1.15)
                self.blade(p,direction,ll*sc,ww*sc,style)
                if s=='pomegranate': self.blade(p,-direction+v(0,0,.3),ll*sc,ww*sc,style)
        if fruit and self.r.random()<{'avocado':.14,'fig':.33,'pomegranate':.20,'apple':.25}[s]:
            self.fruit_at(onpath(path,.92 if self.dense else .45),self.r.uniform(.8,1.1 if self.dense else 1.2))
        if flower and self.r.random()<.25:
            p=end
            self.bloom.tube([p,p+v(0,0,.025)], [.009,.018],sides=7)
            for j in range(5):
                a=j*TAU/5; self.bloom.leaf(p+polar(a,.017,.029),polar(a,.9,.35),.025,.018,style='oval')
    def spray(self,start,d,length,count=9,foliage=True,fruit=False,flower=False):
        d=Vector(d).normalized(); end=start+d*length
        path=[start,mix(start,end,.5)+v(0,0,.08),end]; self.branch(path,.016 if self.dense else .022,.0008 if self.dense else .004)
        angle=math.atan2(d.y,d.x)
        for j in range(count):
            t=.08+.9*j/max(1,count-1) if self.dense else .22+.73*j/max(1,count-1); p=onpath(path,t)
            side=1 if j%2 else -1
            td=polar(angle+side*self.r.uniform(.6,1.4),1,self.r.uniform(-.08,.6))
            self.twig(p,td,self.r.uniform(.20,.34) if self.dense else self.r.uniform(.35,.58)*(1-.3*t),foliage,fruit,flower)
    def crown(self,height,spread,stem_count=1,foliage=True,fruit=False,flower=False,branches=8):
        for si in range(stem_count):
            a=TAU*si/stem_count+.2
            base=polar(a,.025 if stem_count>1 else 0,0)
            bend=polar(a,spread*.12 if stem_count>1 else .035,height*.54)
            top=polar(a,spread*.23 if stem_count>1 else .08,height*.87)
            radius=.10*(height/4)/max(1,stem_count*.55)
            trunk=[base,base+v(0,0,height*.22),bend,top]; self.branch(trunk,radius,.018)
            for j in range(branches):
                t=.22+.73*j/(branches-1); start=onpath(trunk,t)
                ba=j*2.39996+si*1.9+self.r.uniform(-.2,.2)
                reach=spread*.48*math.sin(t*math.pi*.87)
                end=start+polar(ba,reach,height*(.13+.1*(1-t)))
                branchpath=[start,mix(start,end,.45)-v(0,0,.09),end]; self.branch(branchpath,radius*.55*(1-.45*t),.01)
                for k in range(5 if self.species=='avocado' else (3 if self.species=='pomegranate' else 4)):
                    tt=.3+.65*k/4; p=onpath(branchpath,tt)
                    da=ba+(-1 if k%2 else 1)*self.r.uniform(.4,1.1)
                    self.spray(p,polar(da,1,self.r.uniform(.25,.75)),.55+spread*.17,count=8 if self.species!='pomegranate' else 4,foliage=foliage,fruit=fruit,flower=flower)
            self.spray(top,v(.08,.08,1),height*.10,7,foliage,fruit,flower)
    def natural_crown(self,height,spread,stem_count=1,fruit=False,flower=False):
        self.dense=True
        # Low scaffold forks and irregular secondary branches fill an ellipsoid,
        # rather than one ascending ladder of bare horizontal limbs.
        pome=self.species=='pomegranate'
        stems=stem_count
        for si in range(stems):
            sa=si*TAU/stems+.31
            base=polar(sa,.025 if stems>1 else 0,0)
            stemtop=polar(sa,spread*.10 if stems>1 else .05,height*.56)
            trunk=[base,base+v(0,0,height*.18),mix(base,stemtop,.64),stemtop]
            radius=height*.026/max(1,stems*.60)
            self.branch(trunk,radius,.016)
            primaries=7 if stems==1 else 3
            for j in range(primaries):
                angle=sa+j*2.40+self.r.uniform(-.4,.4)
                anchor=onpath(trunk,self.r.uniform(.48,.94))
                end=polar(angle,spread*self.r.uniform(.20,.28),height*self.r.uniform(.57,.83))
                if stems>1: end+=polar(sa,spread*.07,0)
                path=[anchor,mix(anchor,end,.46)+v(0,0,.04),end]
                self.branch(path,radius*.57,.007)
                for k in range(4):
                    root=onpath(path,.24+.22*k)
                    a=angle+(-1 if k%2 else 1)*self.r.uniform(.35,1.2)
                    tip=root+polar(a,spread*self.r.uniform(.13,.22),height*self.r.uniform(-.04,.12))
                    sec=[root,mix(root,tip,.5)+v(0,0,.035),tip]
                    self.branch(sec,.019,.003)
                    for m in range(3):
                        r=onpath(sec,.18+.34*m)
                        a2=a+(-1 if m%2 else 1)*self.r.uniform(.6,1.6)
                        # Dense short leafy shoots grow from connected tertiary arms.
                        direction=polar(a2,1,self.r.uniform(-.4,.8))
                        self.spray(r,direction,self.r.uniform(.32,.52),count=6 if not pome else 5,fruit=fruit,flower=flower)
            self.spray(stemtop,v(.1,.2,1),.35,8,fruit=fruit,flower=flower)
    def espalier(self):
        self.dense=True
        self.branch([v(0,0,0),v(.015,0,1.1),v(0,0,2.3)],.052,.003)
        for tier,z in enumerate([.65,1.3,1.95]):
            for sign in [-1,1]:
                pts=[v(0,0,z-.08),v(sign*.28,0,z),v(sign*1.65,.015*sign,z+.04)]
                self.branch(pts,.025,.001)
                for i in range(10):
                    t=.52+.45*(i+self.r.uniform(-.2,.2))/9
                    p=onpath(pts,t)
                    # Pruned spurs vary in length, lean and lateral leaf rosettes.
                    d=v(sign*self.r.uniform(-.4,.45),self.r.uniform(-.48,.48),1)
                    length=self.r.uniform(.13,.34)
                    self.twig(p,d,length,True,True)
                    if i%2==0:
                        q=p+d.normalized()*length*.30
                        self.twig(q,v(sign*.35,self.r.uniform(-.8,.8),.6),self.r.uniform(.12,.22),True,False)
    def resolve_fruit(self):
        def segment_distance(p,a,b):
            d=b-a; t=max(0,min(1,(p-a).dot(d)/max(d.length_squared,1e-10)))
            return (p-(a+d*t)).length
        # Reject fruit intersecting woody geometry; hang clear below each tip.
        segments=list(self.woody_segments)
        height={'avocado':.095,'pomegranate':.055,'apple':.042}[self.species]
        radius={'avocado':.10,'pomegranate':.056,'apple':.049}[self.species]
        accepted=[]
        for attach,size in self.fruit_requests:
            for drop in (.09,.13,.18,.24,.30):
                center=attach-v(0,0,(drop+height)*size)
                near=[(a,b,r) for a,b,r in segments if (a-center).length < .65 or (b-center).length < .65]
                clearance=min((segment_distance(center,a,b)-r-radius*size for a,b,r in near),default=1)
                if clearance>.004 and all((center-q).length>radius*size+qr+.012 for q,qr in accepted):
                    self.real_fruit(attach,size,drop); accepted.append((center,radius*size)); self.fruit_clearance.append(clearance); break
    def finish(self):
        if self.dense: self.resolve_fruit()
        for b in [self.wood,*self.leaves,self.fruit,self.calyx,self.bloom]:
            if b.vertices: b.finish(self.col)
        if self.pear: pear_mesh('pear-shaped-attached-avocados',self.pear,self.fruit.material,self.col)

FAMILIES={
'avocado-tree': dict(species='avocado',name='Avocado tree',scientific='Persea americana',source='https://ask.ifas.ufl.edu/publication/MG213',limits='Frost-sensitive orchard/garden concept. Drainage, cultivar and site govern suitability and pollination; not a two-tree guarantee.', forms=[('young-orchard','Young single-leader orchard tree, vegetative',2.4,1.7,1,False),('maintained-garden','Maintained garden crown with attached fruit',4.0,3.8,1,True),('mature-fruiting','Large spreading mature fruiting crown',6.0,6.0,1,True)]),
'fig-tree':dict(species='fig',name='Common fig',scientific='Ficus carica',source='https://extension.uga.edu/content/dam/extension-county-offices/madison-county/4h/fruit-tree-sale/Home%20Garden%20Figs.PDF',limits='Climate and cultivar dependent; deciduous summer and dormant states are separate. Maintained size is not a mature-size prediction.',forms=[('low-branching','Low branching summer tree with broad lobed leaves',3.0,3.6,2,False),('fruiting-bush','Multi-stem summer bush with figs at leaf axils',2.5,3.3,4,True),('bare-dormant','Bare winter branch structure',3.3,3.8,3,False)]),
'pomegranate-tree':dict(species='pomegranate',name='Pomegranate',scientific='Punica granatum',source='https://site.extension.uga.edu/fultonag/2020/12/pomegranates/',limits='Warm-site concept; check local cold exposure and fruit ripening. Flowering and ripe-fruit states intentionally separate.',forms=[('natural-shrub','Natural multi-stem leafy shrub',2.5,2.9,5,False),('flowering-standard','Single-trunk trained tree with red tubular flowers',3.1,2.7,1,False),('fruit-loaded','Maintained multi-stem ripe fruit crown',3.0,3.3,3,True)]),
'apple-tree':dict(species='apple',name='Apple tree',scientific='Malus domestica',source='https://yardandgarden.extension.iastate.edu/how-to/growing-apples-home-garden',limits='Illustrative training and fruiting forms. Match cultivar/rootstock, chill, support and pollenizer to site; no cultivar performance claim.',forms=[('gala-m9-dwarf','Gala on M.9 illustrative dwarf central-leader training; needs site-specific support',2.6,2.0,1,True),('orchard-open-crown','Freestanding maintained orchard tree, cultivar unspecified',4.0,4.5,1,True),('espalier-three-tier','Three-tier espalier with spur foliage and fruit, support wall excluded',2.5,3.5,1,True)])}

def build(slug):
    C.reset(); info=FAMILIES[slug]; variants=[]
    for i,(vid,desc,h,w,n,fruit) in enumerate(info['forms']):
        col=C.collection(slug+'__'+vid)
        p=Plant(col,info['species'],1701+i*173+list(FAMILIES).index(slug)*31)
        if vid=='espalier-three-tier': p.espalier()
        elif info['species']!='fig': p.natural_crown(h,w,n,fruit=fruit,flower=vid=='flowering-standard')
        else: p.crown(h,w,n,foliage=vid!='bare-dormant',fruit=fruit,flower=vid=='flowering-standard',branches=9 if info['species']=='avocado' else (4 if info['species']=='pomegranate' else 7))
        p.finish()
        if p.dense:
            col['fruit_wood_clearance_checked']=True
            col['fruit_count']=len(p.fruit_clearance)
            col['minimum_fruit_wood_clearance_m']=min(p.fruit_clearance,default=0.0)
            print('ORCHARD_FRUIT_CLEARANCE',slug,vid,len(p.fruit_clearance),min(p.fruit_clearance,default=0.0),flush=True)
        variants.append((vid,col,desc))
    C.save_family(slug,info['name'],variants,dict(botanical_name=info['scientific'],botanical_sources=[info['source']],climate_notes=info['limits'],generator='tools/library/plants/orchard.py',geometry_notes='Original connected branch scaffolds, attached leaf petioles and species-specific foliage/fruit. Seasonal/trained forms use distinct deterministic geometry. Botanical visualization, not a verified cultivar specimen.',host_adoption='No home adoption claimed. Library-only geometry; site placement review required.'))

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    for slug in args or FAMILIES: build(slug)
