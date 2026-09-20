"""Meter-based host assembly and actual shared-asset placement records."""
import json, math
from pathlib import Path
import bpy
from common import geometry as g
from common.metric import box, rod, cyl, area, camera, mesh, prism
from common.library import linked_collection
ROOT=Path(__file__).resolve().parents[2]
PLAN=[]
HOST=[]
CACHE={}

def host_footprint(name,corners,kind='host'):
    HOST.append({'name':name,'kind':kind,'corners_m':corners})

def asset(category,slug,name,loc,rotation=0,version='v001'):
    key=(category,slug,version)
    if key not in CACHE:CACHE[key]=linked_collection(ROOT,*key)
    coll=CACHE[key]
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=coll
    g.ACTIVE.objects.link(o);o.location=loc;o.rotation_euler.z=rotation
    o['asset_id']=f'{category}/{slug}';o['asset_version']=version
    if category=='furniture' and slug in ('oak-linen-king-bed','oak-linen-queen-bed'):o['bed_count']=1
    meta=json.loads((ROOT/'library'/category/slug/version/'asset.json').read_text())
    if category in ('furniture','cabinetry','appliances','fixtures') and not any(word in slug for word in ('lighting','pendant','outlet')):
        bounds=meta.get('bounds_m')
        if bounds:x0,y0,_=bounds['min'];x1,y1,_=bounds['max']
        else:
            w,d,_=meta['dimensions_m'];x0,y0,x1,y1=-w/2,-d/2,w/2,d/2
        cs,sn=math.cos(rotation),math.sin(rotation)
        corners=[[round(loc[0]+x*cs-y*sn,6),round(loc[1]+x*sn+y*cs,6)] for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]]
        PLAN.append({'name':name,'kind':category,'asset_id':f'{category}/{slug}','version':version,'rotation_rad':rotation,'corners_m':corners,'x':loc[0],'y':loc[1],'z':loc[2]})
    return o

def linked_material(slug,version='v001'):
    folder=ROOT/'library/materials'/slug/version
    meta=json.loads((folder/'asset.json').read_text());path=folder/meta['files']['blender']
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.materials=[src.materials[0]]
    return dst.materials[0]

def write_layout():
    (ROOT/'tools/atrium01/interiors-layout.json').write_text(json.dumps({'units':'meters','placements':PLAN,'host_footprints':HOST},indent=2)+'\n')

def dependencies():
    rows=[]
    for lib in bpy.data.libraries:
        path=Path(bpy.path.abspath(lib.filepath)).resolve()
        if not path.is_relative_to(ROOT/'library'):continue
        meta=json.loads((path.parent/'asset.json').read_text())
        rows.append({'id':meta['id'],'version':meta['version'],'path':'../../'+str(path.relative_to(ROOT))})
    return sorted(rows,key=lambda x:(x['id'],x['version']))
