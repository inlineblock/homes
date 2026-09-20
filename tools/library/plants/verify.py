"""Fresh-process native and linked-instance verification of botanical collections."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3]

def measured(coll):
    points=[];faces=0
    for o in coll.all_objects:
        assert o.type=='MESH',(o.name,o.type)
        assert len(o.data.vertices)>0 and len(o.data.polygons)>0,o.name
        faces+=len(o.data.polygons)
        points.extend(o.matrix_world@v.co for v in o.data.vertices)
        assert all(math.isfinite(x) for p in points[-len(o.data.vertices):] for x in p),o.name
        assert o.data.materials,o.name
    assert points,'empty collection'
    lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
    return {'min':lo,'max':hi,'dimensions':[b-a for a,b in zip(lo,hi)]},faces,len(points)

def run(slug):
    folder=ROOT/'library/landscape'/slug/'v001';m=json.loads((folder/'asset.json').read_text());native=folder/m['files']['blender']
    bpy.ops.wm.open_mainfile(filepath=str(native),use_scripts=False)
    assert not bpy.data.libraries,(slug,'unexpected external dependency')
    for im in bpy.data.images:
        assert not im.filepath or im.packed_file,(slug,im.filepath)
    rows=[];variants=m['blender']['variants'];assert len(variants)==3,slug
    assert len({v['collection'] for v in variants})==3,slug
    for v in variants:
        coll=bpy.data.collections.get(v['collection']);assert coll is not None,v['collection']
        b,faces,verts=measured(coll)
        assert all(abs(a-c)<.001 for a,c in zip(b['dimensions'],v['dimensions_m'])),(slug,v['id'],'dimensions')
        assert -.08<=b['min'][2]<=.015,(slug,v['id'],'ground contact',b['min'][2])
        assert all(x>.01 for x in b['dimensions']),(slug,v['id'],'degenerate bounds')
        rows.append({'id':v['id'],'collection':v['collection'],'bounds_m':b,'vertices':verts,'faces':faces,'ground_min_z_m':b['min'][2]})
    bpy.ops.wm.read_factory_settings(use_empty=True)
    names=[v['collection'] for v in variants]
    with bpy.data.libraries.load(str(native),link=True,relative=True) as (src,dst):dst.collections=list(names)
    for i,coll in enumerate(dst.collections):
        obj=bpy.data.objects.new('Host instance '+str(i),None);obj.instance_type='COLLECTION';obj.instance_collection=coll
        bpy.context.scene.collection.objects.link(obj);obj.location=(i*20,5,0);obj.rotation_euler.z=.35
    bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
    linked=[it for it in deps.object_instances if it.is_instance and it.object.type=='MESH']
    assert linked,(slug,'no actual linked evaluated geometry')
    report={'asset':m['id'],'version':m['version'],'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'native_reopened':True,'variant_count':3,'portable_dependencies':True,'fresh_linked_host_instances':3,'evaluated_mesh_instances':len(linked),'variants':rows,'visual_review':'pending separate inspection of preview.png and detail.png','home_adoption':'not adopted; linked nursery test only','software':{'blender':bpy.app.version_string}}
    (folder/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PLANT_VERIFIED',slug,3,sum(r['faces'] for r in rows),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--assets',nargs='+',required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    for slug in args.assets:run(slug)
