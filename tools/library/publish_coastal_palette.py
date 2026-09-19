"""Warm driftwood and quiet bronze-gray metal: original shared appearance assets.

Assets CC BY 4.0, authoring code MIT. Meter UVs and local-longest-axis grain.
Commands: publish, previews, verify. All previews deliberately use CPU only.
"""
from pathlib import Path
import json
import math
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from common.timber_materials import timber, grain_uv, UV_NAME
from library.build_lindon_palette import mineral
from library.build_lindon_assets import cube, material

WOOD = 'Coastal driftwood | warm weathered oak | v001'
METAL = 'Bronze-gray standing seam | matte coastal | v001'
SPECS = {
    'coastal-driftwood': WOOD,
    'bronze-gray-standing-seam': METAL,
}
WOOD_COLORS = [(0.060,0.049,0.039), (0.145,0.123,0.098), (0.255,0.226,0.188)]
METAL_COLORS = [(0.085,0.077,0.065), (0.135,0.122,0.103)]

def folder(slug):
    return ROOT / 'library/materials' / slug / 'v001'

def native(slug):
    return folder(slug) / (slug + '.blend')

def publish():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for slug,name in SPECS.items():
        destination = native(slug)
        if destination.exists():
            print('PRESERVED_EXISTING_IMMUTABLE_ASSET', destination, flush=True)
            continue
        parent_id,parent_version = ('materials/smoked-oak','v001') if slug=='coastal-driftwood' else ('materials/charcoal-standing-seam','v002')
        assert (ROOT/'library'/parent_id/parent_version/'asset.json').exists()
        if slug=='coastal-driftwood':
            mat = timber(name, *WOOD_COLORS)
            p = mat.node_tree.nodes.get('Principled BSDF')
            p.inputs['Specular IOR Level'].default_value=.24
            p.inputs['Coat Weight'].default_value=.01
            p.inputs['Coat Roughness'].default_value=.8
            for n in mat.node_tree.nodes:
                if n.bl_idname=='ShaderNodeMapRange':
                    if abs(n.inputs['To Min'].default_value-.72)<1e-4:
                        n.inputs['To Min'].default_value=.84;n.inputs['To Max'].default_value=1.16
                    elif abs(n.inputs['To Min'].default_value-.48)<1e-4:
                        n.inputs['To Min'].default_value=.58;n.inputs['To Max'].default_value=.82
        else:
            mat = mineral(name, *METAL_COLORS, 120, .62, .16, .00006)
        destination.parent.mkdir(parents=True,exist_ok=True)
        bpy.data.libraries.write(str(destination),{mat},fake_user=True,compress=True)
        meta={
            'schema_version':1,'id':'materials/'+slug,'version':'v001','name':name,'units':'meters',
            'license':'CC-BY-4.0','rights':'Original procedural asset; attribution Homes project contributors',
            'derived_from':{'id':parent_id,'version':parent_version,'basis':'Existing original physical-scale shader recipe; revised color and surface response. Parent asset is preserved unchanged.'},
            'source':{'kind':'original','generator':'tools/library/publish_coastal_palette.py','shader_helper':'tools/common/timber_materials.py' if slug=='coastal-driftwood' else 'tools/library/build_lindon_palette.py:mineral','command':'Blender --factory-startup --background --python tools/library/publish_coastal_palette.py -- publish'},
            'files':{'blender':destination.name,'preview':'preview.png'},'blender':{'material':name},
            'dependencies':[],'software':{'blender':bpy.app.version_string},
            'placement':'Material-only asset. Host owns actual member/roof geometry, connections, supports, joints and assembly build-up.',
            'host_integration':{'checked':False,'required':'Review actual sunny/shaded host views and use the same pinned timber on exposed interior members and exterior pergola where intended.'},
            'preview_settings':{'renderer':'Cycles CPU','samples':64,'resolution_px':[1100,1100],'color_management':'AgX Medium High Contrast','exposure':0,'lighting':'Neutral environment strength 0.32, neutral large key and grazing area light'},
            'limitations':'Original finish appearance, not a commercial product, actual weathering process or structural/durability/corrosion certification.',
        }
        if slug=='coastal-driftwood':
            meta.update({
                'linear_rgb':{'dark':WOOD_COLORS[0],'mid':WOOD_COLORS[1],'light':WOOD_COLORS[2]},
                'texture_scale':{'uv_map':UV_NAME,'U':'meters across grain','V':'meters along member longest local mesh axis','growth_width_m':.025,'fiber_width_m':.003,'bump_distance_m':.00065,'application':'common.timber_materials.grain_uv(obj) on local applied mesh; apply_grain([material]) can process a material family'},
                'variation':'Independent per-object phase and restrained .84–1.16 tone multiplier. Physical UV meters remain unchanged across different member lengths. Inspect horizontal, vertical and rotated sloping members.',
                'roughness_range':[.58,.82],
                'changes_from_parent':'Warm weathered medium oak/taupe rather than deep smoked chocolate, with low-chroma brown grain, restrained board variation and matte finish. No whitewash or gray bleaching.',
                'grain_limitations':'End faces use transverse grain, not species-specific growth-ring scans. Longest-local-axis mapping requires intentionally modeled/applied member geometry. It does not define a structural timber species or grade.',
            })
        else:
            meta.update({
                'linear_rgb':{'dark':METAL_COLORS[0],'light':METAL_COLORS[1]},
                'texture_scale':{'coordinates':'World position in meters','noise_scale_per_m':120,'bump_distance_m':.00006,'bump_strength':.15},
                'roughness':.62,'metallic':.16,'specular_ior_level':.28,
                'variation':'Quiet physical microtexture; host supplies standing seams, fold geometry, flashings and joints. Preview seam spacing is illustrative and not a product requirement.',
                'changes_from_parent':'Lighter muted bronze-gray body color than the near-black parent; low-metallic coated appearance and matte specular response to reduce silver glare.',
            })
        (destination.parent/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
        (destination.parent/'README.md').write_text('# '+name+'\n\n![Native material review](preview.png)\n\n'+meta['changes_from_parent']+'\n\n'
            +'Link material `'+name+'` from `'+destination.name+'`. '+meta['variation']+'\n\n'
            +('Timber uses `Timber meters`: U across grain, V along the member. Run `common.timber_materials.grain_uv` after applying member scale, or `apply_grain` over this material. The neutral preview includes vertical boards and horizontal members.\n\n' if slug=='coastal-driftwood' else 'This material does not create seams. The neutral preview uses actual standing-seam geometry and a grazing light.\n\n')
            +'Derived from `'+parent_id+'/'+parent_version+'`; original version remains unchanged. Original Homes project contributors asset, CC BY 4.0. Generator `tools/library/publish_coastal_palette.py` uses MIT code and supports `publish`, `previews`, and `verify`.\n\n'
            +meta['limitations']+' Host sun/shade review is a separate step.\n')
        (destination.parent/'AGENTS.md').write_text('# '+name+'\n\n'
            +'- Preserve this adopted version; publish a new version or distinct sibling for a different finish.\n'
            +'- Link the exact named material; record the pinned asset and adoption. Read asset.json for physical mapping and limitations.\n'
            +'- Review the actual neutral preview plus sunny/shaded host views. Correct inappropriate albedo rather than disguising it with exposure.\n'
            +('- Keep warm weathered brown/taupe grain, not whitewash, blue-gray bleaching or deep chocolate. Apply physical member-aligned UVs to horizontal, vertical and sloping timber.\n' if slug=='coastal-driftwood' else '- Keep a restrained warm bronze-gray matte surface; actual seams, folded edges, roof slope and drainage belong to the host.\n'))
        print('COASTAL_PALETTE_PUBLISHED',slug,name,flush=True)

def load(slug):
    with bpy.data.libraries.load(str(native(slug)),link=True,relative=True) as (src,dst):
        assert SPECS[slug] in src.materials,src.materials
        dst.materials=[SPECS[slug]]
    return dst.materials[0]

def previews():
    for slug,name in SPECS.items():
        bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;c=s.collection;m=load(slug)
        ground=material('Neutral material review floor',(.30,.29,.275),.85)
        cube('Neutral ground',(0,0,-.07),(200,200,.12),ground,c)
        if slug=='coastal-driftwood':
            for i in range(11):
                o=cube('Vertical driftwood sample',((i-5)*.205,0,1.3),(.198,.15,2.6),m,c,.002);grain_uv(o)
            for z in [.40,2.18]:
                o=cube('Horizontal driftwood beam',(0,-.16,z),(2.6,.20,.24),m,c,.004);grain_uv(o)
        else:
            roof=cube('Folded roof panel',(0,.10,1.2),(2.8,.085,2.4),m,c,.001)
            for i in range(7):cube('Actual standing seam',((i-3)*.42,.041,1.2),(.014,.030,2.4),m,c,.001)
            cube('Folded side return',(-1.398,.035,1.2),(.018,.06,2.4),m,c,.001)
        target=Vector((0,0,1.25))
        for label,loc,energy,size in [('Large neutral key',(-3,-4,5),400,4),('Neutral grazing light',(3,-1,3.5),190,2)]:
            d=bpy.data.lights.new(label,'AREA');d.energy=energy;d.shape='DISK';d.size=size
            o=bpy.data.objects.new(label,d);c.objects.link(o);o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
        d=bpy.data.cameras.new('Native material portrait');o=bpy.data.objects.new(d.name,d);c.objects.link(o);o.location=(3.4,-6.6,3.15);o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler();d.lens=57;s.camera=o
        s.world=bpy.data.worlds.new('Neutral material daylight');s.world.use_nodes=True
        s.world.node_tree.nodes['Background'].inputs[0].default_value=(.6,.6,.6,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.32
        s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=64;s.cycles.use_denoising=True
        s.render.resolution_x=s.render.resolution_y=1100;s.render.resolution_percentage=100
        s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
        s.render.image_settings.file_format='PNG';s.render.filepath=str(folder(slug)/'preview.png')
        bpy.ops.render.render(write_still=True);print('COASTAL_PALETTE_CPU_PREVIEW',slug,flush=True)

def verify():
    for slug,name in SPECS.items():
        bpy.ops.wm.read_factory_settings(use_empty=True);mat=load(slug)
        assert mat.library and Path(bpy.path.abspath(mat.library.filepath)).resolve()==native(slug)
        assert len(bpy.data.images)==0
        texture_checks={}
        if slug=='coastal-driftwood':
            c=bpy.context.scene.collection
            cases=[('vertical',(0,0,0),(.2,.15,2.4),0,2),('horizontal',(0,0,0),(2.4,.2,.15),0,0),('sloping',(0,0,0),(.2,.15,2.4),math.radians(24),2)]
            for label,loc,dims,rot,axis in cases:
                o=cube(label,loc,dims,mat,c);o.rotation_euler.y=rot;grain_uv(o)
                assert o['timber_grain_local_axis']=='XYZ'[axis]
                uv=o.data.uv_layers.get(UV_NAME);assert uv
                physical_errors=[]
                for poly in o.data.polygons:
                    ids=list(poly.loop_indices)
                    for a,b in zip(ids,ids[1:]+ids[:1]):
                        va=o.matrix_world@o.data.vertices[o.data.loops[a].vertex_index].co
                        vb=o.matrix_world@o.data.vertices[o.data.loops[b].vertex_index].co
                        physical_errors.append(abs((va-vb).length-(uv.data[a].uv-uv.data[b].uv).length))
                assert max(physical_errors)<1e-5
                texture_checks[label]={'grain_local_axis':'XYZ'[axis],'max_uv_meter_edge_error':max(physical_errors)}
        else:
            p=mat.node_tree.nodes.get('Principled BSDF')
            assert abs(p.inputs['Roughness'].default_value-.62)<1e-5
            assert abs(p.inputs['Metallic'].default_value-.16)<1e-5
            assert any(n.bl_idname=='ShaderNodeNewGeometry' for n in mat.node_tree.nodes)
            texture_checks={'roughness':.62,'metallic':.16,'coordinates':'World position in meters'}
        bpy.ops.wm.open_mainfile(filepath=str(native(slug)))
        assert name in bpy.data.materials and not bpy.data.libraries
        dest=folder(slug)/'verification.json'
        review=json.loads(dest.read_text()).get('visual_preview_review') if dest.exists() else None
        receipt={'native_linked_in_fresh_process':True,'native_reopened':True,'blender':bpy.app.version_string,'material':name,'external_dependencies':[],'texture_checks':texture_checks,'host_integration_checked':False,'visual_preview_review':review or 'Pending actual CPU preview inspection'}
        dest.write_text(json.dumps(receipt,indent=2)+'\n');print('COASTAL_PALETTE_VERIFIED',slug,json.dumps(receipt),flush=True)

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['publish']
    {'publish':publish,'previews':previews,'verify':verify}[args[0]]()
