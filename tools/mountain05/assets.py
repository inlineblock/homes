"""New original conifer and deck material; reuse pinned library finishes."""
import bpy,math,random,json
from common import geometry as g
from common.geometry import F,material
from common.architecture import mesh
from common.landscape import foliage_mesh
from common.library import linked_collection
from common.finish_palette import palette as coastal_palette,textured

def mats(root):
    M=coastal_palette(root)
    for slug,version,key in [('warm-vertical-cedar','v003','cedar'),('charcoal-standing-seam','v001','roof')]:
        p=root/'library/materials'/slug/version/(slug+'.blend')
        with bpy.data.libraries.load(str(p),link=True) as (a,b):b.materials=[a.materials[0]]
        M[key]=b.materials[0]
    slug='mountain-thermo-ash';folder=root/'library/materials'/slug/'v002';p=folder/(slug+'.blend')
    with bpy.data.libraries.load(str(p),link=True) as (a,b):b.materials=[a.materials[0]]
    M['deck']=b.materials[0]
    M['bark']=textured('Rough conifer bark',(.025,.017,.010),(.09,.064,.034),22,.96,.003,(5,5,.4))
    M['firleaf']=textured('Deep mountain fir needles',(.012,.033,.014),(.052,.090,.032),9,.72,.0001)
    M['soil']=textured('Forest duff',(.027,.025,.014),(.075,.064,.035),45,.96,.002)
    M['moss']=textured('Forest moss',(.04,.065,.018),(.10,.13,.035),60,.98,.003)
    M['rock']=textured('Dark mountain granite',(.09,.10,.095),(.25,.26,.24),17,.86,.012)
    return M

def _conifer_v001(root,M):
    slug='mountain-conifer';folder=root/'library/landscape'/slug/'v001';path=folder/(slug+'.blend')
    if not path.exists():
        saved=g.ACTIVE;c=g.collection('Mountain fir | 46 foot original tree');rng=random.Random(505)
        verts=[];faces=[]
        def branch(a,b,r1,r2):
            from mathutils import Vector
            a,b=Vector(a),Vector(b);axis=(b-a).normalized();u=axis.cross(Vector((0,0,1)))
            if u.length<.01:u=axis.cross(Vector((0,1,0)))
            u.normalize();v=axis.cross(u);start=len(verts);N=10
            for p,r in [(a,r1),(b,r2)]:
                for i in range(N):q=p+r*(math.cos(i*math.tau/N)*u+math.sin(i*math.tau/N)*v);verts.append(tuple(q))
            for i in range(N):faces.append((start+i,start+(i+1)%N,start+N+(i+1)%N,start+N+i))
            faces.append(tuple(start+N+i for i in range(N)))
        for j in range(10):branch((.08*math.sin(j),0,j*4.6),(.08*math.sin(j+1),0,(j+1)*4.6),.52*(1-j/11),.52*(1-(j+1)/11))
        clusters=[]
        for tier in range(15):
            z=7+tier*2.45;rad=9.6*(1-z/49)**.72
            for i in range(6):
                a=i*math.tau/6+tier*1.91;dx,dy=math.cos(a),math.sin(a);r=rad*rng.uniform(.85,1.16)
                tip=(dx*r,dy*r,z-.65);branch((0,0,z),(dx*r*.50,dy*r*.50,z-.7),.10*(1-tier/20),.05);branch((dx*r*.50,dy*r*.50,z-.7),tip,.05,.015)
                for k in range(4):
                    t=(k+1)/4;px,py=dx*r*t,dy*r*t;zz=z-.6+.25*t
                    for side in [-1,1]:
                        aa=a+side*.65;sp=.4+.7*(1-t);end=(px+math.cos(aa)*sp,py+math.sin(aa)*sp,zz+.16)
                        branch((px,py,zz),end,.021,.007);clusters.append((end,.45+.3*(1-t)))
        o=mesh('Fir trunk and branching',verts,faces,M['bark'])
        for f in o.data.polygons:f.use_smooth=True
        foliage_mesh('Dense original fir needle sprays',clusters,M['firleaf'],505,65,.16)
        folder.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
        (folder/'asset.json').write_text(json.dumps({'schema_version':1,'id':'landscape/'+slug,'version':'v001','name':'Original mountain conifer','units':'meters','nominal_height_m':46*F,'origin':'base of trunk, Z up','license':'CC-BY-4.0','rights':'Original; attribution Homes project contributors','source':{'kind':'original','generator':'tools/mountain05/assets.py'},'files':{'blender':path.name},'dependencies':[],'description':'Branched trunk and individual procedural needle sprays; use instancing and varied rotation/scale for forest stands.'},indent=2)+'\n')
        for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c);g.ACTIVE=saved
    return linked_collection(root,'landscape',slug)


def conifer(root,M):
    """Pinned original fir: irregular 3-D boughs and needles attached to twigs."""
    from mathutils import Vector
    slug='mountain-conifer';version='v002'
    folder=root/'library/landscape'/slug/version;path=folder/(slug+'.blend')
    if not path.exists():
        saved=g.ACTIVE;c=g.collection('Mountain fir | irregular connected 46 foot crown')
        c['asset_id']='landscape/'+slug;c['asset_version']=version
        rng=random.Random(55202);wood_v=[];wood_f=[];needle_v=[];needle_f=[]
        def branch(a,b,r1,r2):
            a,b=Vector(a),Vector(b);axis=(b-a).normalized();u=axis.cross(Vector((0,0,1)))
            if u.length<.01:u=axis.cross(Vector((0,1,0)))
            u.normalize();v=axis.cross(u);start=len(wood_v);N=6 if r1<.07 else 10
            for p,r in [(a,r1),(b,r2)]:
                for i in range(N):wood_v.append(tuple(p+r*(math.cos(i*math.tau/N)*u+math.sin(i*math.tau/N)*v)))
            for i in range(N):wood_f.append((start+i,start+(i+1)%N,start+N+(i+1)%N,start+N+i))
            wood_f.append(tuple(start+N+i for i in range(N)))
        def spray(a,b):
            a,b=Vector(a),Vector(b);axis=(b-a).normalized()
            branch(a,b,.012,.0025)
            u=axis.cross(Vector((0,0,1)))
            if u.length<.01:u=Vector((1,0,0))
            u.normalize();v=axis.cross(u).normalized()
            # Needle bases lie directly on the branchlet; no disconnected clouds.
            for k in range(11):
                t=(k+.25)/11;p=a.lerp(b,t)
                for j in range(5):
                    ang=j*math.tau/5+k*.67;radial=u*math.cos(ang)+v*math.sin(ang)
                    direction=(radial*.82+axis*.40).normalized()
                    length=rng.uniform(.19,.32)*(1-.25*t)
                    q=p+direction*length;side=axis.cross(direction).normalized()*.018
                    m=p.lerp(q,.40);first=len(needle_v)
                    needle_v.extend([tuple(p),tuple(m+side),tuple(q),tuple(m-side)])
                    needle_f.append((first,first+1,first+2,first+3))
        def trunk(z):return Vector((.17*math.sin(z*.11),.10*math.sin(z*.19),z))
        for j in range(23):branch(trunk(j*2),trunk((j+1)*2),.48*(1-j/24)**1.1,.48*(1-(j+1)/24)**1.1)
        # Golden-angle branch origins and jitter break horizontal wreaths.
        for i in range(192):
            z=5.5+39.7*(i/191)+rng.uniform(-.42,.42)
            a=i*2.39996+rng.uniform(-.25,.25);d=Vector((math.cos(a),math.sin(a),0));side=Vector((-d.y,d.x,0))
            radius=(8.6*(1-z/48)**.70+.20)*rng.uniform(.75,1.22)
            start=trunk(z);mid=start+d*radius*.53+side*rng.uniform(-.3,.3)+Vector((0,0,-.65-radius*.065))
            end=start+d*radius+side*rng.uniform(-.55,.55)+Vector((0,0,rng.uniform(-.10,.70)))
            branch(start,mid,.11*(1-z/53),.028);branch(mid,end,.028,.008)
            for k in range(7):
                t=.18+k*.115;base=start.lerp(mid,t/.53) if t<.53 else mid.lerp(end,(t-.53)/.47)
                for sign in [-1,1]:
                    length=(.35+radius*.31*(1-t))*rng.uniform(.7,1.25)
                    direction=(side*sign*.83+d*.36+Vector((0,0,rng.uniform(-.28,.42)))).normalized()
                    tip=base+direction*length
                    branch(base,tip,.021,.004)
                    for n in range(4):
                        t2=.20+n*.22;origin=base.lerp(tip,t2)
                        s2=(-1 if n%2 else 1)
                        spray(origin,origin+(d*.46+side*sign*.12+Vector((0,0,s2*.38+.12)))*rng.uniform(.75,1.3))
                    spray(tip,tip+direction*.52+Vector((0,0,.17)))
            spray(end,end+d*.55+Vector((0,0,.35)))
        # Taper the terminal six feet to a natural pointed leader, preserving
        # continuity because the same smooth deformation affects wood and needles.
        def crown_taper(p):
            x,y,z=p
            t=1 if z<=40 else max(.02,(46.10-z)/6.10)**.65
            return (x*t,y*t,z)
        wood_v=[crown_taper(p) for p in wood_v];needle_v=[crown_taper(p) for p in needle_v]
        wood=mesh('Continuous trunk boughs and attached branchlets',wood_v,wood_f,M['bark'])
        for f in wood.data.polygons:f.use_smooth=True
        needle_material=material('Deep evergreen diffuse fir needles',(.012,.042,.017),.95)
        needle_material.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.15
        needles=mesh('Individual attached radial fir needles',needle_v,needle_f,needle_material)
        # A small tonal spread at needle level avoids a uniform plastic crown.
        for tint in [(.019,.052,.020),(.028,.070,.026),(.040,.083,.031)]:
            needles.data.materials.append(material('Fir needle natural variation',tint,.80))
        for f in needles.data.polygons:f.material_index=rng.choices([0,1,2,3],[.55,.20,.18,.07])[0]
        bpy.context.view_layer.update()
        points=[o.matrix_world@Vector(v) for o in c.objects for v in o.bound_box]
        lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
        folder.mkdir(parents=True,exist_ok=True)
        bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap='RELATIVE_ALL')
        metadata={'schema_version':1,'id':'landscape/'+slug,'version':version,
            'name':'Irregular mountain conifer with attached needle sprays','units':'meters',
            'dimensions_m':[round(hi[i]-lo[i],6) for i in range(3)],'bounds_m':{'min':lo,'max':hi},
            'placement':{'origin':'Trunk ground-contact base at Z=0, centered XY','front':'Radial crown; Z up','allowed_variation':'Uniform scale 0.78 to 1.4 and arbitrary rotation about Z; no nonuniform scale'},
            'license':'CC-BY-4.0','rights':'Original geometry; attribution Homes project contributors',
            'source':{'kind':'original','generator':'tools/mountain05/assets.py:conifer','entry_point':'conifer(root, M), with M from mats(root)','seed':55202},
            'software':{'blender':bpy.app.version_string},
            'files':{'blender':path.name,'preview':'preview.png','preview_renderer':'render_preview.py','validation':'validation.json'},'dependencies':[],
            'preview_command':'Blender --background --python library/landscape/mountain-conifer/v002/render_preview.py',
            'description':'Original generic 46-foot mountain fir silhouette, with irregular three-dimensional boughs, modeled branchlets and individually attached radial needles. Local original bark and needle shaders are embedded. Illustrative vegetation, not a botanical or planting suitability specification.'}
        (folder/'asset.json').write_text(json.dumps(metadata,indent=2)+'\n')
        for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c);g.ACTIVE=saved
    return linked_collection(root,'landscape',slug,version)
