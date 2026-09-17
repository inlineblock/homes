"""Promote useful existing Atrium 01 assets; run with its .blend already open."""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];F=.3048
def publish(category,slug,name,objects,origin,dimensions):
    folder=ROOT/'library'/category/slug/'v001';folder.mkdir(parents=True,exist_ok=True);path=folder/f'{slug}.blend'
    if path.exists():return
    c=bpy.data.collections.new(name)
    for obj in objects:
        copy=obj.copy()
        if obj.data:copy.data=obj.data.copy()
        copy.location-=Vector(origin)*F;c.objects.link(copy)
    bpy.data.libraries.write(str(path),{c},fake_user=True)
    data={'schema_version':1,'id':f'{category}/{slug}','version':'v001','name':name,'units':'meters','dimensions_m':[d*F for d in dimensions],'origin':'Ceiling mount' if category=='fixtures' else 'Floor beneath seat center','source':{'kind':'original','home':'atrium-01','generator':'tools/library/publish_from_atrium.py'},'license':'CC-BY-4.0','rights':'Original project asset; CC BY 4.0; attribution: Homes project contributors','files':{'blender':path.name}}
    (folder/'asset.json').write_text(json.dumps(data,indent=2)+'\n')
publish('fixtures','opal-globe-pendant','Opal globe pendant', [bpy.data.objects[n] for n in ['Pendant cable','Pendant cap','Opal globe pendant','Pendant pool']],(50,7.6,8.9),(1,1,3.5))
objects=[o for o in bpy.context.scene.objects if (any(o.name.startswith(s) for s in ['Walnut stool seat','Stool leg','Stool footrest']) and abs(o.location.y/F-7.3)<.7) or o.name=='Stool bentwood back']
# Curves store their shape in absolute coordinates; translate their control points instead.
for obj in objects:
    if obj.type=='CURVE':
        obj.data=obj.data.copy()
        for sp in obj.data.splines:
            for p in sp.bezier_points:p.co-=Vector((46.8,7.3,0))*F;p.handle_left-=Vector((46.8,7.3,0))*F;p.handle_right-=Vector((46.8,7.3,0))*F
        obj.location=Vector((46.8,7.3,0))*F
publish('furniture','walnut-counter-stool','Walnut counter stool',objects,(46.8,7.3,0),(1.5,1.5,3))
print('PUBLISHED_ATRIUM_ASSETS')
