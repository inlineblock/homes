"""Original species-specific Southwest plant collections, meters/Z-up.
Run: Blender --background --factory-startup --threads 2 --python tools/library/plants/desert.py
Optional after --: one or more family slugs. Does not change an adopted version.
"""
from pathlib import Path
import math, random, sys
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import material, bark_material, MeshBuilder, collection, reset, save_family

TAU=math.tau

def raw_mesh(name, verts, faces, mat, col):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); col.objects.link(ob); me.materials.append(mat)
    for p in me.polygons: p.use_smooth=True
    return ob

def flower(builder, center, radius=.032, count=5, axis=(0,0,1)):
    c=Vector(center); n=Vector(axis).normalized()
    u=n.cross(Vector((0,1,0))).normalized()
    if u.length<.1:u=Vector((1,0,0))
    v=n.cross(u)
    for j in range(count):
        d=u*math.cos(j*TAU/count)+v*math.sin(j*TAU/count)
        builder.leaf(c+d*radius*.56,d,radius*1.5,radius*.8,style='oval',roll=.12)

def finish(builders,col):
    for b in builders:
        if b.vertices and b.faces: b.finish(col)

def lens(builder,base,axis,L,W,roll=0):
    """A folded six-face small leaflet/petal, attached at its base."""
    axis=Vector(axis).normalized(); ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0))
    side=axis.cross(ref).normalized(); n=side.cross(axis).normalized()
    side,n=side*math.cos(roll)+n*math.sin(roll),n*math.cos(roll)-side*math.sin(roll)
    b=Vector(base); i=len(builder.vertices)
    builder.vertices.extend([tuple(b),tuple(b+axis*L*.43-side*W*.5),tuple(b+axis*L*.48+n*W*.15),tuple(b+axis*L*.43+side*W*.5),tuple(b+axis*L),tuple(b+axis*L*.73+n*W*.08)])
    builder.faces.extend([(i,i+1,i+2),(i,i+2,i+3),(i+1,i+4,i+5,i+2),(i+2,i+5,i+4,i+3)])

def palo_verde(col,seed,form):
    rng=random.Random(seed); young=form==0; bloom=form==2
    H=3.4 if young else 5.4; R=1.55 if young else 2.4
    bark=MeshBuilder('Sinuous green trunk limbs and attached twig network',material('Photosynthetic blue green palo verde bark',(.145,.24,.10),.77))
    leaves=[MeshBuilder('Palo verde fine compound foliage '+str(k),material('Palo leaflet green '+str(k),(.12+.035*k,.25+.035*k,.06+.025*k),.67,.035)) for k in range(3)]
    petals=MeshBuilder('Thousands of attached five-petalled golden flowers',material('Palo golden yellow petals',(.95,.63,.018),.53))
    stamens=MeshBuilder('Palo flower rusty hearts',material('Palo flower centers',(.55,.24,.014),.6))
    trunk=[Vector((0,0,0)),Vector((-.04,.02,H*.14)),Vector((.12,-.015,H*.3)),Vector((.02,.08,H*.43))]
    bark.tube(trunk,[.13 if young else .22,.12 if young else .19,.08 if young else .14,.047],sides=11)
    nmajor=9 if young else 14
    for j in range(nmajor):
        a=j*2.399+rng.uniform(-.2,.2); dr=Vector((math.cos(a),math.sin(a),0)); tang=Vector((-dr.y,dr.x,0))
        origin=trunk[1].lerp(trunk[3],.3+.65*rng.random())
        reach=R*rng.uniform(.67,1.03)
        tip=origin+dr*reach+Vector((0,0,H*rng.uniform(.39,.58)))
        pts=[origin, origin.lerp(tip,.25)+tang*.16,origin.lerp(tip,.51)-tang*.06+Vector((0,0,.18)),origin.lerp(tip,.77)+tang*.05+Vector((0,0,.16)),tip]
        bark.tube(pts,[.065 if not young else .04,.041,.023,.011,.002],sides=8)
        for k in range(9):
            tt=.24+k*.09; ix=min(3,int(tt*4)); base=pts[ix].lerp(pts[ix+1],tt*4-ix)
            aa=a+(-1 if k%2 else 1)*rng.uniform(.53,1.0)
            end=base+Vector((math.cos(aa)*rng.uniform(.45,.86),math.sin(aa)*rng.uniform(.45,.86),rng.uniform(.12,.44)))
            mid=base.lerp(end,.48)+Vector((0,0,.09))
            bark.tube([base,mid,end],[.012,.0065,.0011],sides=6)
            for m in range(10):
                t=.14+m*.09; o=base.lerp(mid,t*2) if t<.5 else mid.lerp(end,(t-.5)*2)
                az=aa+(-1 if m%2 else 1)*rng.uniform(.55,1.55)
                ee=o+Vector((math.cos(az)*rng.uniform(.25,.55),math.sin(az)*rng.uniform(.25,.55),rng.uniform(-.15,.35)))
                bend=o.lerp(ee,.5)+Vector((0,0,.028))
                bark.tube([o,bend,ee],[.003,.0015,.00035],sides=5)
                for q in range(7 if not bloom else 2):
                    at=o.lerp(ee,.22+q*(.115 if not bloom else .6))
                    # The compound foliage is borne on fine terminal twigs, never on canopy blobs.
                    for sign in (-1,1):
                        axis=Vector((math.cos(az+sign*1.1),math.sin(az+sign*1.1),rng.uniform(-.3,.45))).normalized()
                        rr=at+axis*.075
                        bark.tube([at,rr],[.00065,.00025],sides=4)
                        side=Vector((-axis.y,axis.x,.14)).normalized()
                        for z in range(3):
                            lc=at.lerp(rr,.28+z*.28)
                            for si in (-1,1):
                                d=(side*si+axis*.22).normalized()
                                lens(leaves[(j+k)%3],lc,d,.028,.012,rng.uniform(-.4,.4))
                if bloom:
                    for q in range(4):
                        anchor=o.lerp(ee,.16+q*.27)
                        for cc in range(2):
                            angle=cc*2.399+q; c=anchor+Vector((math.cos(angle)*.022,math.sin(angle)*.022,.018+cc*.008))
                            bark.tube([anchor,c],[.0007,.0003],sides=4)
                            for pp in range(5):
                                aa2=pp*TAU/5+angle
                                d=Vector((math.cos(aa2),math.sin(aa2),rng.uniform(.0,.4)))
                                lens(petals,c,d,.018,.014,.12)
                            stamens.ellipsoid(c,(.0025,.0025,.0025),segments=5,rings=3)
    finish([bark,*leaves,petals,stamens],col)

def willow_trumpet(builder,c,axis,L):
    """Open corrugated trumpet surface: five-lobed mouth, no solid cap."""
    axis=Vector(axis).normalized(); side=axis.cross(Vector((0,0,1))).normalized(); normal=axis.cross(side)
    base=len(builder.vertices); rings=7; seg=30
    for k in range(rings):
        t=k/(rings-1); radius=.002+(.020-.002)*(t**2.1)
        for j in range(seg):
            a=j*TAU/seg; lobe=.5+.5*math.cos(5*a)
            r=radius*(1+.20*lobe*t**4)
            pt=Vector(c)+axis*(L*t+L*.09*lobe*t**6)+side*(r*math.cos(a))+normal*(r*math.sin(a))
            builder.vertices.append(tuple(pt))
    for k in range(rings-1):
        for j in range(seg):
            a=base+k*seg+j;b=base+k*seg+(j+1)%seg
            builder.faces.append((a,b,b+seg,a+seg))

def desert_willow(col,seed,form):
    rng=random.Random(seed); dormant=form==2; bloom=form==0
    bark=MeshBuilder('Curved willow trunk limbs and branching shoots',bark_material('Willow fissured gray brown bark',(.20,.135,.085)))
    leaves=[MeshBuilder('Fine willow leaf sprays '+str(k),material('Willow olive foliage '+str(k),(.12+k*.033,.235+k*.036,.074+k*.020),.62,.04)) for k in range(3)]
    pink=MeshBuilder('Open five lobed pink trumpet corollas',material('Willow mauve corolla',(.51,.13,.30),.57))
    inner=MeshBuilder('Willow small throat stamens',material('Willow golden stamens',(.65,.39,.055),.6))
    pods=MeshBuilder('Curved hanging dry seed capsules',material('Willow capsule dark brown',(.15,.065,.022),.85))
    H=3.8 if form==0 else 4.8; R=1.65 if form==0 else 2.0
    nstems=1 if form==0 else 3
    for s in range(nstems):
        aa=s*2.399; off=Vector((.08*math.cos(aa),.08*math.sin(aa),0)) if s else Vector((0,0,0))
        tr=[off,off+Vector((.09*math.cos(aa),.09*math.sin(aa),H*.2)),off+Vector((.33*math.cos(aa+.4),.33*math.sin(aa+.4),H*.42)),off+Vector((.45*math.cos(aa+.2),.45*math.sin(aa+.2),H*.6))]
        bark.tube(tr,[.12 if nstems==1 else .085,.095,.055,.019],sides=10)
        for j in range(12 if nstems==1 else 5):
            a=j*2.399+s*1.9+rng.uniform(-.35,.35); tt=rng.uniform(.45,.90)
            o=tr[1].lerp(tr[3],tt); dr=Vector((math.cos(a),math.sin(a),0)); tan=Vector((-dr.y,dr.x,0))
            end=o+dr*(R*rng.uniform(.72,1.18))+Vector((0,0,H*rng.uniform(.15,.36)))
            pts=[o,o.lerp(end,.25)+tan*.14,o.lerp(end,.50)+tan*.2+Vector((0,0,.17)),o.lerp(end,.75)+tan*.1+Vector((0,0,.12)),end]
            bark.tube(pts,[.038,.029,.019,.008,.0015],sides=8)
            for k in range(8):
                t=.22+k*.105; ix=min(3,int(t*4)); start=pts[ix].lerp(pts[ix+1],t*4-ix)
                a2=a+(-1 if k%2 else 1)*rng.uniform(.6,1.5)
                end2=start+Vector((math.cos(a2)*rng.uniform(.35,.7),math.sin(a2)*rng.uniform(.35,.7),rng.uniform(-.09,.3)))
                mid=start.lerp(end2,.5)+Vector((0,0,.08))
                bark.tube([start,mid,end2],[.008,.004,.0008],sides=6)
                for m in range(8 if not dormant else 3):
                    t2=.18+m*(.11 if not dormant else .36); anchor=start.lerp(mid,t2*2) if t2<.5 else mid.lerp(end2,(t2-.5)*2)
                    az=a2+(-1 if m%2 else 1)*rng.uniform(.6,1.8)
                    tip=anchor+Vector((math.cos(az)*rng.uniform(.2,.5),math.sin(az)*rng.uniform(.2,.5),rng.uniform(-.12,.18)))
                    bend=anchor.lerp(tip,.50)+Vector((0,0,.028))
                    bark.tube([anchor,bend,tip],[.0024,.0014,.0004],sides=5)
                    if dormant:
                        if rng.random()<.5:
                            pend=tip+Vector((rng.uniform(-.04,.04),rng.uniform(-.04,.04),-.24))
                            pods.tube([tip,tip.lerp(pend,.4)+Vector((.025,0,0)),tip.lerp(pend,.75),pend],[.002,.004,.003,.0007],sides=7)
                        continue
                    for q in range(10):
                        lc=anchor.lerp(tip,.10+q*.092)
                        for sign in (-1,1):
                            angle=az+sign*rng.uniform(.8,1.8)
                            axis=Vector((math.cos(angle),math.sin(angle),rng.uniform(-.65,.35))).normalized()
                            length=rng.uniform(.15,.23)
                            leaves[(j+k+q)%3].leaf(lc+axis*length*.5,axis,length,rng.uniform(.022,.032),style='lance',roll=rng.uniform(-.8,.8))
                    if bloom and rng.random()<.38:
                        for q in range(2):
                            base=tip+Vector(((q+.3)*.02,0,(q+.3)*.026));axis=Vector((math.cos(az+q*.6),math.sin(az+q*.6),rng.uniform(-.25,.4))).normalized()
                            bark.tube([tip,base],[.0012,.0006],sides=4)
                            willow_trumpet(pink,base,axis,rng.uniform(.038,.052))
                            inner.tube([base+axis*.01,base+axis*.03],[.0005,.00035],sides=4)
    finish([bark,*leaves,pink,inner,pods],col)

def ocotillo(col,seed,form):
    rng=random.Random(seed)
    canes=MeshBuilder('Tapered jointed woody canes',bark_material('Ocotillo ridged gray green bark',(.28,.26,.19)))
    thorns=MeshBuilder('Paired woody thorns',material('Ocotillo woody spines',(.38,.27,.14),.9))
    leaves=MeshBuilder('Rain responsive oval leaves',material('Ocotillo fresh leaf',(.24,.38,.095),.64,.03))
    flowers=MeshBuilder('Ocotillo terminal scarlet tubular flowers',material('Ocotillo scarlet',(.78,.065,.018),.56))
    for j in range(14 if form==0 else 21):
        a=j*2.399+rng.uniform(-.3,.3); h=rng.uniform(2.2,3.4)*(1.2 if form==2 else 1)
        spread=rng.uniform(.7,1.45)
        pts=[]
        for k in range(15):
            t=k/14; rr=spread*t**1.45
            pts.append(Vector((math.cos(a)*rr+.035*math.sin(k*.7),math.sin(a)*rr,h*t)))
        canes.tube(pts,[.032*(1-k/16)**1.3 for k in range(15)],sides=7)
        for k in range(1,60):
            t=k/60; ix=min(13,int(t*14)); p=pts[ix].lerp(pts[ix+1],t*14-ix)
            aa=a+k*2.399; d=Vector((math.cos(aa),math.sin(aa),.17))
            thorns.tube([p,p+d*.055+Vector((0,0,.015))],[.0026,.0001],sides=4)
            if form==1:
                for n in range(2):
                    dd=Vector((math.cos(aa+n),math.sin(aa+n),.35)).normalized()
                    leaves.leaf(p+dd*.026,dd,.048,.026,style='oval',roll=.3)
        if form==2:
            tip=pts[-1]
            for k in range(25):
                aa=k*2.399; z=(k/25)*.22
                start=tip+Vector((0,0,z)); end=start+Vector((.045*math.cos(aa),.045*math.sin(aa),.035))
                flowers.tube([start,end],[.0045,.006],sides=6)
                flower(flowers,end,.009,count=5)
    finish([canes,thorns,leaves,flowers],col)

def agave_rosette(col,seed,origin,size,leaf_mat,spine_builder):
    rng=random.Random(seed); verts=[]; faces=[]
    basal=MeshBuilder('Agave basal stem at planting grade',leaf_mat)
    basal.tube([origin,Vector(origin)+Vector((0,0,size*.11))],[size*.035,size*.060],sides=10)
    basal.finish(col)
    for j in range(40):
        a=j*2.399; age=j/39
        L=size*(.34+.62*age); wide=size*(.12+.03*math.sin(age*math.pi))
        base=Vector(origin)+Vector((0,0,size*.09))
        radial=Vector((math.cos(a),math.sin(a),0)); side=Vector((-math.sin(a),math.cos(a),0))
        start_index=len(verts)
        for k in range(11):
            t=k/10
            dist=L*t*(.22+.78*age)
            z=L*(t*(1.05-.73*age)+.18*math.sin(t*math.pi))
            mid=base+radial*dist+Vector((0,0,z))
            width=wide*math.sin(math.pi*t)**.62 if t not in (0,1) else (.018*size if t==0 else .001)
            for layer in (-1,1):
                for q in (-1,0,1):
                    thick=size*.020*math.sin(t*math.pi)
                    p=mid+side*(q*width*.5)+Vector((0,0,layer*thick+(1-abs(q))*size*.015))
                    verts.append(tuple(p))
            if 0<k<10 and j>9:
                for si in (-1,1):
                    tooth=mid+side*si*width*.5
                    spine_builder.tube([tooth,tooth+side*si*.013*size-radial*.009*size],[.002*size,.0001],sides=4)
        for k in range(10):
            s=start_index+k*6; n=s+6
            for layer in (0,3):
                for q in range(2):faces.append((s+layer+q,s+layer+q+1,n+layer+q+1,n+layer+q))
            faces.extend([(s,n,n+3,s+3),(s+2,s+5,n+5,n+2)])
        tip=Vector(verts[start_index+60+1]); spine_builder.tube([tip,tip+radial*.03*size+Vector((0,0,.035*size))],[.004*size,.0001],sides=5)
    return raw_mesh('Thick recurved blue gray agave blades',verts,faces,leaf_mat,col)

def agave(col,seed,form):
    mat=material('Parry agave powder blue leaf',(.29,.40,.39),.62)
    sp=MeshBuilder('Agave black terminal spines and marginal teeth',material('Agave dark terminal spine',(.09,.065,.042),.78))
    agave_rosette(col,seed,(0,0,0),.95 if form==0 else 1.15,mat,sp)
    if form==1:
        for k in range(4):
            a=k*2.399
            agave_rosette(col,seed+k+1,(.80*math.cos(a),.80*math.sin(a),0),.38+k*.05,mat,sp)
    if form==2:
        rng=random.Random(seed+501)
        stalk=MeshBuilder('Mature subtly arched branching agave inflorescence',material('Agave bloom stalk',(.29,.34,.12),.74))
        fl=MeshBuilder('Individual flared six lobed agave flowers',material('Agave yellow florets',(.76,.57,.06),.65))
        an=MeshBuilder('Agave projecting filaments and anthers',material('Agave golden anthers',(.55,.30,.045),.71))
        stem=[Vector((.07*math.sin(k*.37),.06*math.sin(k*.31),k*.4)) for k in range(11)]
        stalk.tube(stem,[.05*(1-k/13) for k in range(11)],sides=10)
        for k in range(13):
            a=k*2.399+rng.uniform(-.15,.15); z=2.08+k*.132
            reach=(.62*(1-(z-2.08)/2.35))*rng.uniform(.83,1.12)
            origin=Vector((.07*math.sin(z/.4*.37),.06*math.sin(z/.4*.31),z))
            end=origin+Vector((reach*math.cos(a),reach*math.sin(a),.19))
            mid=origin.lerp(end,.55)+Vector((0,0,-.045))
            stalk.tube([origin,mid,end],[.017,.011,.004],sides=7)
            for cluster in range(3):
                ca=a+cluster*2.399; cc=end+Vector((.10*math.cos(ca),.10*math.sin(ca),rng.uniform(0,.055)))
                stalk.tube([end,cc],[.004,.0015],sides=5)
                for m in range(11):
                    aa=m*2.399; rad=.026*math.sqrt(m)
                    pos=cc+Vector((rad*math.cos(aa),rad*math.sin(aa),rng.uniform(-.020,.022)))
                    stalk.tube([cc,pos],[.0012,.0008],sides=4)
                    ax=Vector((rng.uniform(-.17,.17),rng.uniform(-.17,.17),1)).normalized(); length=rng.uniform(.021,.043)
                    throat=pos+ax*length
                    fl.tube([pos,pos+ax*length*.6,throat],[.0028,.0040,.0060],sides=6)
                    for lobe in range(6):
                        la=lobe*TAU/6
                        d=Vector((math.cos(la),math.sin(la),.38)).normalized()
                        lens(fl,throat,d,.010,.005)
                        base=throat+d*.003
                        tip=base+ax*rng.uniform(.018,.030)+d*.004
                        an.tube([base,tip],[.00045,.00025],sides=3)
                        an.ellipsoid(tip,(.0010,.0010,.0022),segments=4,rings=3)
        finish([stalk,fl,an],col)
    sp.finish(col)

def cactus(col,seed,form):
    rng=random.Random(seed)
    H=[.52,1.35,.94][form]; R=[.29,.38,.36][form]; lean=.20 if form==1 else .01
    verts=[];faces=[]; ribs=23; segments=ribs*8; rings=36
    for k in range(rings+1):
        t=k/rings
        profile=(math.sin(math.pi*(.10+.90*t)))**.29
        for j in range(segments):
            a=j*TAU/segments
            rib=(.5+.5*math.cos(a*ribs))**1.7
            rad=R*profile*(.83+.17*rib)
            verts.append((math.cos(a)*rad+lean*t*t,math.sin(a)*rad,H*t))
    for k in range(rings):
        for j in range(segments):
            a=k*segments+j;b=k*segments+(j+1)%segments
            faces.append((a,b,b+segments,a+segments))
    faces.append(tuple(reversed(range(segments))))
    faces.append(tuple(rings*segments+j for j in range(segments)))
    raw_mesh('Fishhook barrel 23 sculpted longitudinal ribs',verts,faces,material('Barrel cactus blue green skin',(.16,.26,.14),.58),col)
    areoles=MeshBuilder('Woolly rib areoles',material('Cactus areole felt',(.64,.52,.31),.9))
    spines=MeshBuilder('Radial spines and curved central fishhooks',material('Amber red hooked spines',(.35,.14,.07),.83))
    bloom=MeshBuilder('Yellow orange cactus petals',material('Cactus golden flowers',(.98,.49,.025),.53))
    for j in range(ribs):
        a=j*TAU/ribs; normal=Vector((math.cos(a),math.sin(a),0)); tangent=Vector((-math.sin(a),math.cos(a),0))
        for k in range(1,16):
            t=k/17; profile=math.sin(math.pi*(.1+.90*t))**.29
            c=normal*(R*profile)+Vector((lean*t*t,0,H*t))
            areoles.ellipsoid(c,(.010,.010,.012),segments=16,rings=10)
            for m in range(5):
                aa=m*TAU/5
                d=normal*.022+tangent*.042*math.cos(aa)+Vector((0,0,.045*math.sin(aa)))
                spines.tube([c,c+d],[.0018,.0001],sides=4)
            # Smooth swept fishhook with variable length, turn and fine taper.
            length=rng.uniform(.72,1.18); hook=[]
            controls=[c,c+normal*.08*length+Vector((0,0,-.02*length)),c+normal*.09*length+Vector((0,0,-.085*length)),c+normal*.037*length+Vector((0,0,-.055*length))]
            for h in range(17):
                t=h/16; pt=controls[0]*(1-t)**3+controls[1]*3*(1-t)**2*t+controls[2]*3*(1-t)*t*t+controls[3]*t**3
                hook.append(pt+tangent*rng.uniform(-.0004,.0004))
            spines.tube(hook,[.0026*(1-h/17)**.8+.0001 for h in range(17)],sides=8)
            # Fine wool bristles soften the areole without borrowed textures.
            for w in range(8):
                wa=w*2.399; start=c+tangent*.005*math.cos(wa)+Vector((0,0,.006*math.sin(wa)))
                areoles.tube([start,start+normal*.013+tangent*.003*math.cos(wa)],[.0005,.0001],sides=3)
    if form==2:
        for j in range(12):
            a=j*TAU/12;c=Vector((.14*math.cos(a)+lean,.14*math.sin(a),H*.97))
            flower(bloom,c,.042,count=12)
            flower(bloom,c+Vector((0,0,.013)),.027,count=10)
    finish([areoles,spines,bloom],col)

FAMILIES={
'blue-palo-verde':('Blue palo verde','Parkinsonia florida',[("young-open","Young airy single-trunk leaf-on tree"),("mature-spreading","Mature multi-leader green bark canopy"),("yellow-bloom","Mature yellow-flowering spreading crown")],palo_verde,'https://extension.arizona.edu/publication/mesquite-and-palo-verde-trees-urban-landscape','Sonoran desert; thorns and pod litter require setback from paths.'),
'desert-willow':('Desert willow','Chilopsis linearis',[("single-trunk-bloom","Single-trunk flowering tree with lance leaves and pink trumpets"),("multi-stem","Leafy multi-stem canopy"),("dormant-capsules","Bare winter multi-stem tree with attached slender capsules")],desert_willow,'https://yavapaiplants.extension.arizona.edu/chilopsis-linearis','Dry-wash and Southwest foothill character; deciduous, not a true willow.'),
'ocotillo':('Ocotillo','Fouquieria splendens',[("leafless-canes","Sparse leafless jointed canes with woody spines"),("rain-leafed","Rain-responsive small oval foliage on canes"),("scarlet-tips","Dry canes with terminal scarlet tubular bloom clusters")],ocotillo,'https://extension.arizona.edu/publication/cactus-agave-yucca-and-ocotillo','Southwest dryland; foliage responds to moisture, never assume permanent lush foliage.'),
'parry-agave':("Parry’s agave",'Agave parryi',[("compact-rosette","Compact powder-blue fleshy rosette"),("offset-colony","Mature rosette with four smaller offsets"),("flowering-stalk","Mature terminal flowering rosette and branched stalk")],agave,'https://arboretum.arizona.edu/agave-parryi-parrys-agave','Upland Southwest; site suitability differs from low desert; sharp teeth require path setbacks.'),
'fishhook-barrel-cactus':('Fishhook barrel cactus','Ferocactus wislizeni',[("small-barrel","Small rounded barrel with ribbed skin and hooks"),("leaning-column","Mature gently leaning column with hooked central spines"),("flower-ring","Mature barrel with orange-yellow flower ring")],cactus,'https://www.nps.gov/tont/learn/nature/cacti.htm','Sonoran and Southwest hot-dry accent; substantial hook spines must stay outside circulation.')}

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(FAMILIES)
    for ix,slug in enumerate(FAMILIES):
        if slug not in args:continue
        reset(); title,botanical,forms,build,url,selection=FAMILIES[slug]; variants=[]
        for fi,(vid,desc) in enumerate(forms):
            col=collection(slug.replace('-','_')+'__'+vid.replace('-','_'))
            build(col,83000+ix*100+fi,fi)
            # Root cross-sections terminate at planting grade; prevent subterranean spine tips.
            for obj in col.all_objects:
                if obj.type == 'MESH':
                    for vertex in obj.data.vertices:
                        if vertex.co.z < 0: vertex.co.z = 0
            variants.append((vid,col,desc))
        save_family(slug,title,variants,{'botanical_name':botanical,'generator':'tools/library/plants/desert.py','seed':83000+ix*100,'browse_tags':['desert','southwest'],'sources':[url],'selection_notes':selection,'cultivar':'Species concept; no named cultivar or rootstock asserted','site_selection':{'region':selection,'sun':'Sunny landscape intent; confirm local exposure before planting','soil_drainage':'Well-drained concept setting; verify species/site requirements','establishment_water':'Local horticultural specification required','ongoing_water':'Dryland concept; irrigation needs not engineered','salt_spray':'unknown','saline_inundation':'unknown'},'visual_accuracy_limitations':'Original botanical visualization, not a taxonomic specimen or nursery specification; measured size is modeled size, not guaranteed mature spread. Species cues modeled as actual geometry.','adoption_status':'Not adopted in a home; host review pending.'})
        print('DESERT_FAMILY_BUILT',slug,flush=True)
if __name__=='__main__':main()
