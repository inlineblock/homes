"""Original, meter-scale citrus collections; run inside Blender from repository root.

Each crown is built from connected, tapered wood and alternate petiolate leaves.
Fruit surfaces are species-specific revolutions, with separate calyces and stalks.
No botanical photographs or downloaded meshes are redistributed.
"""
from pathlib import Path
import math
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MeshBuilder, material, reset, save_family

TAU = math.tau


def rind_material(name, color, pore_scale=1500, roughness=.43):
    mat = material(name, color, roughness=roughness)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    coord = nodes.new('ShaderNodeTexCoord')
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = pore_scale
    noise.inputs['Detail'].default_value = 2
    links.new(coord.outputs['Object'], noise.inputs['Vector'])
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .24
    bump.inputs['Distance'].default_value = .00023
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*[x * .77 for x in color[:3]], 1)
    ramp.color_ramp.elements[1].color = (*color[:3], 1)
    links.new(noise.outputs['Fac'], ramp.inputs[0])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    return mat


def citrus_bark():
    mat = material('Citrus / gray umber bark / fine original grain', (.19, .145, .092), roughness=.83)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    tex = nodes.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = 48
    tex.inputs['Detail'].default_value = 3
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = .32
    bump.inputs['Distance'].default_value = .0012
    links.new(tex.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


class FruitMesh:
    def __init__(self, name, mat):
        self.name, self.mat, self.verts, self.faces = name, mat, [], []

    def fruit(self, center, diameter, length, kind, angle=0):
        center = Vector(center)
        base = len(self.verts)
        seg, rings = 18, 13
        for j in range(rings + 1):
            theta = math.pi * j / rings
            s, c = math.sin(theta), math.cos(theta)
            radius = .5 * diameter * s
            z = .5 * length * c
            if kind == 'eureka':
                # Modest tapered nipple and shoulder, not a prolate yellow ball.
                radius *= 1 + .055 * math.cos(3 * theta)
                z += .008 * (abs(c) ** 18) * (1 if c >= 0 else -1)
            elif kind == 'meyer':
                z += .0028 * (abs(c) ** 14) * (1 if c >= 0 else -1)
            elif kind in ('satsuma', 'navel'):
                z -= .0035 * (abs(c) ** 12) * (1 if c >= 0 else -1)
            for i in range(seg):
                phi = TAU * i / seg + angle
                # Subtle real longitudinal irregularity, never noisy spikes.
                r = radius * (1 + (.014 if kind == 'eureka' else .006) * math.cos(7 * phi))
                self.verts.append(tuple(center + Vector((r * math.cos(phi), r * math.sin(phi), z))))
        for j in range(rings):
            for i in range(seg):
                a = base + j * seg + i
                b = base + j * seg + (i + 1) % seg
                self.faces.append((a, b, b + seg, a + seg))

    def finish(self, col):
        if not self.verts:
            return
        mesh = bpy.data.meshes.new(self.name)
        mesh.from_pydata(self.verts, [], self.faces)
        mesh.materials.append(self.mat)
        mesh.update()
        obj = bpy.data.objects.new(self.name, mesh)
        col.objects.link(obj)
        for face in mesh.polygons:
            face.use_smooth = True
        return obj


FAMILIES = {
    'lemon-tree': dict(name='Lemon trees — Improved Meyer and Eureka', botanical='Citrus × meyeri; Citrus × limon',
        source=['https://citrusvariety.ucr.edu/crc3737', 'https://citrusvariety.ucr.edu/crc3837'],
        leaf=(.105, .044), color=(.042, .145, .023), fruit=(.059, .078), fruit_color=(.74, .53, .016),
        selections=['Improved Meyer', 'Eureka (Cook reference form)', 'Improved Meyer'],
        variants=[('meyer-patio', 1.85, 1.28, .70, .10, 'meyer', 'Winter fruit; patio-trained small standard, no container supplied'),
                  ('eureka-garden', 3.05, 2.75, .61, .22, 'eureka', 'Winter fruit; open spreading Eureka with longer outer shoots'),
                  ('meyer-blossom-fruit', 2.22, 1.86, .38, .11, 'meyer', 'Spring bloom with retained winter fruit; irregular low-branched Meyer')]),
    'lime-tree': dict(name='Bearss lime trees', botanical='Citrus × latifolia',
        source=['https://citrusvariety.ucr.edu/crc3772'], leaf=(.095, .043), color=(.030, .105, .022),
        fruit=(.054, .064), fruit_color=(.21, .36, .022), selections=['Bearss'] * 3,
        variants=[('bearss-trained', 2.05, 1.52, .76, .05, 'lime', 'Late summer; compact trained standard with harvest-green fruit'),
                  ('bearss-natural', 2.75, 2.86, .31, .10, 'lime', 'Late summer; low-branched spreading natural shrub with green fruit'),
                  ('bearss-ripe', 2.45, 2.37, .51, .15, 'lime-ripe', 'Late autumn; full-ripening yellow-green fruit, open garden crown')]),
    'sweet-orange-tree': dict(name='Washington navel sweet orange trees', botanical='Citrus sinensis',
        source=['https://citrusvariety.ucr.edu/crc1241A'], leaf=(.112, .049), color=(.032, .121, .025),
        fruit=(.084, .088), fruit_color=(.88, .205, .009), selections=['Washington navel'] * 3,
        variants=[('washington-young', 2.45, 1.64, .80, .04, 'navel-young', 'Summer; young open rounded crown, sparse small immature fruit'),
                  ('washington-mature', 3.65, 3.40, .91, .23, 'navel', 'Winter fruit; rounded mature garden crown with drooping branch tips'),
                  ('washington-blossom', 2.75, 2.28, .70, .12, 'navel-blossom', 'Spring bloom with a few retained mature fruits; maintained garden tree')]),
    'satsuma-mandarin-tree': dict(name='Owari satsuma mandarin trees', botanical='Citrus unshiu',
        source=['https://citrusvariety.ucr.edu/crc3178'], leaf=(.103, .035), color=(.038, .133, .026),
        fruit=(.068, .047), fruit_color=(.82, .205, .014), selections=['Owari satsuma (Frost reference form)'] * 3,
        variants=[('owari-spreading', 2.12, 2.79, .36, .28, 'satsuma', 'Early winter; low spreading tree carrying oblate orange fruit'),
                  ('owari-loaded', 2.44, 3.28, .47, .43, 'satsuma-loaded', 'Early winter harvest; fruit-loaded pendant terminal branches'),
                  ('owari-patio', 1.62, 1.44, .63, .11, 'satsuma', 'Early winter; patio-trained standard, compact by training, rootstock unspecified')]),
    'grapefruit-tree': dict(name='Marsh grapefruit trees', botanical='Citrus × paradisi',
        source=['https://citrusvariety.ucr.edu/crc3184'], leaf=(.146, .071), color=(.034, .131, .031),
        fruit=(.114, .103), fruit_color=(.81, .65, .09), selections=['Marsh (Frost reference form)'] * 3,
        variants=[('marsh-young', 3.03, 2.01, 1.03, .03, 'grapefruit-young', 'Summer; upright young tree, foliage only before modeled fruit-bearing stage'),
                  ('marsh-spreading', 4.45, 4.54, 1.08, .15, 'grapefruit', 'Late winter; large spreading garden crown, not maximum mature size'),
                  ('marsh-clusters', 3.49, 3.67, .71, .29, 'grapefruit-clusters', 'Late winter; lower trained fruiting crown with hanging fruit clusters')]),
    'kumquat-tree': dict(name='Nagami kumquat trees', botanical='Fortunella margarita / Citrus japonica',
        source=['https://citrusvariety.ucr.edu/crc3877'], leaf=(.058, .023), color=(.033, .119, .027),
        fruit=(.019, .032), fruit_color=(.90, .25, .014), selections=['Nagami'] * 3,
        variants=[('nagami-shrub', 1.50, 1.55, .18, .02, 'kumquat', 'Late winter; dense fine-leaved multistem shrub with sparse fruit'),
                  ('nagami-standard', 1.90, 1.24, .90, .05, 'kumquat', 'Late winter; patio standard trained above a clear stem'),
                  ('nagami-fruiting', 2.25, 1.98, .40, .07, 'kumquat-loaded', 'Late winter; upright fine twigging and abundant small oval fruits')]),
}


def build_variant(slug, cfg, index):
    vid, height, width, clear, droop, kind, description = cfg['variants'][index]
    seed = 713 + list(FAMILIES).index(slug) * 100 + index * 19
    rng = random.Random(seed)
    col = bpy.data.collections.new(f'{slug.replace("-", "_")}__{vid.replace("-", "_")}')
    bpy.context.scene.collection.children.link(col)
    col['variant_id'] = vid
    col['deterministic_seed'] = seed
    col['season_and_training'] = description
    col['selection'] = cfg['selections'][index]
    col['rootstock'] = 'unspecified; geometry size reflects age and pruning, not dwarf-rootstock performance'
    wood = MeshBuilder(f'{vid} / connected woody scaffold', citrus_bark())
    greenmat = material(f'{vid} / living petioles and fruit calyces', (.080, .16, .027), roughness=.61)
    stems = MeshBuilder(f'{vid} / attached petioles pedicels and calyces', greenmat)
    leaves = []
    for j, value in enumerate((.78, .92, 1.04, 1.17)):
        leaves.append(MeshBuilder(f'{vid} / curved evergreen foliage {j+1}', material(
            f'{vid} / leaf tone {j+1}', tuple(c*value for c in cfg['color']), roughness=.38, subsurface=.07)))
    fruitcolor = cfg['fruit_color']
    if kind == 'lime-ripe': fruitcolor = (.53, .58, .066)
    if kind == 'navel-young': fruitcolor = (.12, .28, .027)
    fruit = FruitMesh(f'{vid} / shaped attached fruit', rind_material(f'{vid} / fine rind pores', fruitcolor))
    flower = MeshBuilder(f'{vid} / five petal citrus blossoms', material(f'{vid} / ivory petals', (.86, .84, .75), roughness=.55, subsurface=.08))
    pollen = MeshBuilder(f'{vid} / blossom centers', material(f'{vid} / cream stamens', (.66, .48, .10), roughness=.7))
    trunk_r = .020 + height * .012
    def path_point(points, t):
        t = max(0.0, min(1.0, t)) * (len(points)-1)
        segment = min(len(points)-2, int(t))
        return points[segment].lerp(points[segment+1], t-segment)
    # The leader and all subsequent wood are continuous sampled paths. Every
    # child begins on its parent's actual centerline, never a nearby chord.
    crown_depth = height-clear
    trunk = [Vector((0,0,0)), Vector((.010,-.006,.11)), Vector((-.014,.015,clear)),
             Vector((.022,.013,clear+crown_depth*.38)),
             Vector((-.018,.006,clear+crown_depth*.73)),
             Vector((.012,-.010,height*.95))]
    wood.tube(trunk,[trunk_r*1.38,trunk_r,trunk_r*.83,trunk_r*.49,trunk_r*.18,.0006],sides=10)
    for q in range(5):
        a=q*TAU/5+.2
        wood.tube([(0,0,.10),(.065*math.cos(a),.065*math.sin(a),.022),(.115*math.cos(a),.115*math.sin(a),0)],
                  [trunk_r*.40,trunk_r*.25,.004],sides=7)
    leaflen,leafwidth=cfg['leaf']
    branches=13 if height>2.5 else 11
    secondary_count=8 if height>2.5 else 7
    shoot_count=7
    leaf_count=12
    if slug=='kumquat-tree':
        branches=12; secondary_count=8; leaf_count=14
    fruit_count=0
    grapefruit_spheres=[]
    grapefruit_cluster_counts=[]
    leaf_total=0
    for b in range(branches):
        az=b*2.399963+rng.uniform(-.24,.24)
        tier=(b+.5)/branches
        start=path_point(trunk,.40+.55*tier)
        dome=math.sqrt(max(.05,1-((tier-.43)/.70)**2))
        reach=width*.40*dome*rng.uniform(.88,1.06)
        endpoint=Vector((math.cos(az)*reach,math.sin(az)*reach,
                         clear+crown_depth*(.26+.67*tier)-droop*.27))
        direction=endpoint-start
        scaffold=[start,start+direction*.30+Vector((0,0,.08)),
                  start+direction*.63+Vector((0,0,.11+droop*.25)),endpoint]
        wood.tube(scaffold,[trunk_r*.52,trunk_r*.31,trunk_r*.14,.0008],sides=8)
        for si in range(secondary_count):
            sf=.18+.82*si/(secondary_count-1)
            st=path_point(scaffold,sf)
            # Short lower, lateral and rising shoots fill the whole crown
            # rather than making a leaf shelf only at each scaffold end.
            a=az+(1 if si%2 else -1)*rng.uniform(.58,1.38)
            length=(.24+width*.08)*rng.uniform(.7,1.25)
            dz=rng.uniform(-.16,.32)*(1.1 if height>3 else .85)-droop*rng.uniform(.1,.5)
            tip=st+Vector((math.cos(a)*length,math.sin(a)*length,dz))
            secondary=[st,st.lerp(tip,.38)+Vector((0,0,.065)),st.lerp(tip,.75)+Vector((0,0,.04)),tip]
            wood.tube(secondary,[.007,.0048,.0022,.00045],sides=6)
            for t in range(shoot_count):
                tf=.16+.84*t/(shoot_count-1)
                base=path_point(secondary,tf)
                phi=a+t*2.39996+rng.uniform(-.38,.38)
                twiglen=(.20 if slug=='kumquat-tree' else .28)*rng.uniform(.75,1.38)
                dz=rng.uniform(-.18,.31)-droop*rng.uniform(.18,.57)
                direction=Vector((math.cos(phi)*twiglen,math.sin(phi)*twiglen,dz))
                end=base+direction
                shoot=[base,base+direction*.40+Vector((0,0,.035)),base+direction*.77+Vector((0,0,.025)),end]
                stems.tube(shoot,[.0024,.0017,.0010,.00025],sides=5)
                tangent=Vector((-math.sin(phi),math.cos(phi),0))
                for l in range(leaf_count):
                    f = .15 + .81*l/max(1,leaf_count-1)
                    node = path_point(shoot,f)
                    sign = 1 if l%2 else -1
                    d = (tangent*sign*.77 + direction.normalized()*.5 + Vector((0,0,rng.uniform(-.65,.70)))).normalized()
                    ll=leaflen*rng.uniform(.80,1.14)
                    ww=leafwidth*rng.uniform(.85,1.09)
                    petiole=.012 if slug!='grapefruit-tree' else .021
                    leafbase=node+d*petiole
                    stems.tube([node,leafbase],[.0011,.00065],sides=4)
                    if slug=='grapefruit-tree':
                        # Broad winged petiole, individually modeled at correct scale.
                        leaves[l%4].leaf(node+d*petiole*.53,d,petiole*.90,.010,style='oval',roll=.2)
                    leaves[rng.randrange(4)].leaf(leafbase+d*ll*.50,d,ll,ww,style='lance' if slug in ('kumquat-tree','satsuma-mandarin-tree') else 'oval',roll=rng.uniform(-.95,.95))
                    leaf_total += 1
                probability = .11
                if 'loaded' in kind or 'clusters' in kind: probability=.12
                if 'young' in kind: probability=.024 if slug=='sweet-orange-tree' else 0
                if 'blossom' in kind or 'blossom' in vid: probability=.045
                if kind=='eureka': probability=.09
                if rng.random()<probability:
                    cluster = rng.choice([1,1,2,2,3,4,5]) if kind=='grapefruit-clusters' else (2 if kind=='satsuma-loaded' and rng.random()<.42 else 1)
                    fruit_node=path_point(shoot,rng.uniform(.62,.90))
                    bunch_az=rng.uniform(0,TAU)
                    realized_cluster=0
                    for k in range(cluster):
                        fd, fl=cfg['fruit']
                        scale=(rng.uniform(.85,1.15) if slug=='grapefruit-tree' else rng.uniform(.87,1.08))*(.64 if 'young' in kind else 1)
                        fd*=scale; fl*=scale
                        bunch_angle=bunch_az+k*TAU/max(cluster,1)+rng.uniform(-.24,.24)
                        bunch_radius=(fd*.60 if cluster>1 else .012)*rng.uniform(.84,1.17)
                        offset=Vector((math.cos(bunch_angle)*bunch_radius,math.sin(bunch_angle)*bunch_radius,-rng.uniform(.035,.10)-(.025 if k%2 else 0)))
                        attach=fruit_node
                        top=attach+offset
                        center=top-Vector((0,0,fl*.5))
                        if slug=='grapefruit-tree':
                            # A loose bunch develops along different nearby nodes,
                            # not a repeated radial three-ball ornament. Spherical
                            # envelopes conservatively prevent fruit intersections.
                            radius=max(fd,fl)*.5
                            valid=False
                            for attempt in range(100):
                                branch=shoot if (k==0 or rng.random()<.42) else secondary
                                attach=path_point(branch,rng.uniform(.15,1.0))
                                offset=Vector((rng.uniform(-.034,.034),rng.uniform(-.034,.034),-rng.uniform(.023,.112)))
                                top=attach+offset
                                center=top-Vector((0,0,fl*.5))
                                if all((center-c).length>radius+r+.004 for c,r in grapefruit_spheres):
                                    valid=True;break
                            if not valid:
                                continue
                            grapefruit_spheres.append((center.copy(),radius))
                        stems.tube([attach,attach+offset*.6,top],[.0018,.0015,.0012],sides=5)
                        fruit.fruit(center,fd,fl,kind.split('-')[0],rng.random()*TAU)
                        for sepal in range(5):
                            angle=sepal*TAU/5
                            d=Vector((math.cos(angle),math.sin(angle),-.16))
                            stems.leaf(top+d*.0025,d,.007 if slug!='kumquat-tree' else .0038,.0025,style='lance')
                        if kind.startswith('navel'):
                            # A visibly inset blossom-end navel ring, not another fruit sphere.
                            ring=[center+Vector((.0035*math.cos(q*TAU/10),.0035*math.sin(q*TAU/10),-fl*.5+.003)) for q in range(11)]
                            stems.tube(ring,[.0008]*11,sides=4)
                        fruit_count += 1
                        realized_cluster += 1
                    if slug=='grapefruit-tree':
                        grapefruit_cluster_counts.append(realized_cluster)
                if ('blossom' in kind or 'blossom' in vid) and rng.random()<.25:
                    fc=end+Vector((0,0,.013))
                    stems.tube([end,fc],[.0013,.0008],sides=5)
                    for pet in range(5):
                        ang=pet*TAU/5
                        d=Vector((math.cos(ang),math.sin(ang),.17))
                        flower.leaf(fc+d*.008,d,.019,.007,style='oval')
                    pollen.ellipsoid(fc+Vector((0,0,.003)),(.003,.003,.004),segments=8,rings=4)
    for builder in [wood,stems,*leaves,flower,pollen]:
        if builder.vertices:
            obj=builder.finish(col)
            for vertex in obj.data.vertices:
                if vertex.co.z<0:
                    vertex.co.z=0
    fruit.finish(col)
    col['modeled_leaf_count']=leaf_total
    col['modeled_fruit_count']=fruit_count
    if slug=='grapefruit-tree':
        col['realized_cluster_sizes']=grapefruit_cluster_counts
        col['fruit_sphere_clearance_m']=.004
        for i,(c,r) in enumerate(grapefruit_spheres):
            assert all((c-d).length>=r+s+.00399 for d,s in grapefruit_spheres[i+1:]), 'Fruit collision'
        print('GRAPEFRUIT_CLUSTER_HISTOGRAM',vid,{size:grapefruit_cluster_counts.count(size) for size in range(6)},flush=True)
    col['fruit_diameter_length_m']=list(cfg['fruit'])
    faces=sum(len(o.data.polygons) for o in col.objects if o.type=='MESH')
    assert faces<500000, (vid,faces)
    print('CITRUS_VARIANT',slug,vid,'leaves',leaf_total,'fruit',fruit_count,'faces',faces,flush=True)
    return vid,col,description


def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    slugs=args or list(FAMILIES)
    for slug in slugs:
        reset()
        cfg=FAMILIES[slug]
        variants=[build_variant(slug,cfg,i) for i in range(3)]
        metadata={
            'botanical_name':cfg['botanical'], 'cultivars':cfg['selections'],
            'rootstock':'Unspecified; compact forms represent age and training, not a guaranteed dwarf rootstock.',
            'generator':'tools/library/plants/citrus.py',
            'command':f'blender -b --factory-startup -t 2 --python tools/library/plants/citrus.py -- {slug}',
            'browse_tags':['fruit tree', 'citrus', 'sheltered garden', 'patio-trained option'],
            'preferred_detail_variant':cfg['variants'][2][0],
            'variant_metadata':{v[0]:{'cultivar':cfg['selections'][i], 'seed':713+list(FAMILIES).index(slug)*100+i*19,
                'training_and_season':v[6], 'nominal_fruit_diameter_length_m':list(cfg['fruit']),
                'fruit_profile':v[5], 'rootstock':'unspecified'} for i,v in enumerate(cfg['variants'])},
            'source_urls':cfg['source'], 'botanical_sources':cfg['source'],
            'reference_checked':'2026-09-19',
            'visual_accuracy':'Original architectural botanical interpretation. Named citrus selections differentiated in crown habit, leaf dimensions, fruit profile and fruit clusters. Not a taxonomic specimen or horticultural performance model.',
            'modeled_size_basis':'Actual measured asset bounds describe pruned/young/garden specimens, not published maximum mature dimensions.',
            'climate_notes':'Sheltered citrus-suitable garden; verify local winter cold and cultivar/rootstock. This library is not an outdoor mountain planting specification.',
            'site_selection':{'region':'Frost exposure and cultivar-specific heat requirements require local verification; UCR reference forms are California accessions.',
                'sun':'Concept assumes a sunny, sheltered garden; verify local conditions.',
                'soil':'Free drainage assumed; soil suitability requires local verification.',
                'water_establishment':'Regular establishment care required; no irrigation rate specified.',
                'water_ongoing':'Site, rootstock and season dependent; not classified as unirrigated xeriscape.',
                'salt_spray':'Unknown; no direct ocean-front exposure claim.', 'saline_inundation':'Unknown; not specified.'},
            'dependencies':[],
            'materials':'Embedded original procedural bark, four subtly varied waxy foliage tones, rind pores, petals and calyx materials; no external textures.',
            'allowed_variation':'Rotate freely about Z; uniform scale 0.9–1.1 only. Choose actual collection for growth habit; do not squash into another species.',
            'adoption_status':'Modeled library candidate; no home adoption claimed. Preview/reopen/host reviews are recorded separately.',
            'review_notes':'Fruit stalks connect to twig nodes; attached petioles, ground-root flare, real calyces, and species-specific fruit dimensions. Blossoming variants explicitly permit retained earlier-season citrus fruit.'
        }
        save_family(slug,cfg['name'],variants,metadata)


if __name__=='__main__':
    main()
