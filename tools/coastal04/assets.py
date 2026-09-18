"""Original reusable white-oak counter stool, published independently of the home."""
import bpy,json,math
from common import geometry as g
from common.geometry import box,rod,curve
from common.library import linked_collection
from furniture import soft

def counter_stool(root,M):
    slug='coastal-oak-counter-stool';folder=root/'library/furniture'/slug/'v001';path=folder/(slug+'.blend')
    if not path.exists():
        saved=g.ACTIVE;c=g.collection('Coastal oak counter stool | 25.3 inch seat')
        soft('Stool upholstered seat',(0,0,2.0),(1.60,1.65,.22),M['linen'],.12)
        curve('Stool curved oak back',[(-.80,.5,3.02),(0,.75,3.15),(.80,.5,3.02)],.07,M['oak'])
        for x in [-.64,.64]:
            rod('Stool rear leg',(x,.55,0),(x,.58,3.03),.055,M['oak'])
            rod('Stool front leg',(x,-.59,0),(x,-.57,1.95),.055,M['oak'])
        rod('Stool champagne footrest',(-.64,-.59,.70),(.64,-.59,.70),.03,M['bronze'])
        for x in [-.64,.64]:rod('Stool side brace',(x,-.59,.70),(x,.55,.70),.028,M['bronze'])
        for obj in c.objects:
            if obj.type=='CURVE':obj.data.use_fill_caps=True
        folder.mkdir(parents=True,exist_ok=True);bpy.data.libraries.write(str(path),{c},fake_user=True,path_remap="RELATIVE_ALL")
        data={'schema_version':1,'id':'furniture/'+slug,'version':'v001','name':'Coastal oak counter stool','units':'meters','dimensions_m':[.5304,.50292,.981456],'seat_height_m':.643128,'origin':'floor center, back toward +Y','license':'CC-BY-4.0','rights':'Original asset; attribution Homes project contributors','source':{'kind':'original','generator':'tools/coastal04/assets.py'},'files':{'blender':path.name},'dependencies':[{'id':'materials/coastal-white-oak','version':'v001','path':'../../../materials/coastal-white-oak/v001/coastal-white-oak.blend'}]}
        (folder/'asset.json').write_text(json.dumps(data,indent=2)+'\n')
        for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c);g.ACTIVE=saved
    return linked_collection(root,'furniture',slug)
