import bpy,json
from pathlib import Path
from . import geometry as g
from .geometry import F
def linked_collection(root,category,slug,version="v001"):
    path=Path(root)/'library'/category/slug/version/f'{slug}.blend'
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[src.collections[0]]
    return dst.collections[0]
def instance(name,coll,loc,rotation=0,scale=1):
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=coll;g.ACTIVE.objects.link(o)
    o.location=[x*F for x in loc];o.rotation_euler.z=rotation;o.scale=(scale,)*3;return o
def publish_material(root,slug,material,metadata):
    folder=Path(root)/'library/materials'/slug/'v001';folder.mkdir(parents=True,exist_ok=True);path=folder/f'{slug}.blend'
    if not path.exists():
        bpy.data.libraries.write(str(path),{material},fake_user=True)
        metadata.update({'schema_version':1,'id':f'materials/{slug}','version':'v001','units':'meters','source':{'kind':'original','generator':'tools/timber02/build.py'},'license':'CC-BY-4.0','rights':'Original project asset; CC BY 4.0; attribution: Homes project contributors','files':{'blender':path.name}})
        (folder/'asset.json').write_text(json.dumps(metadata,indent=2)+'\n')
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.materials=[src.materials[0]]
    return dst.materials[0]
