"""Rigid bedroom roller-blind adoption with paired open/closed native states."""
import json,math
import bpy
from common import geometry as g
import design as d


def build(root,asset):
    coll=g.collection('04 Bedroom shading | alternate privacy states')
    result=[];closed_cache={}
    # Match the actual bays produced by architecture.glazing, not rough whole windows.
    targets={('south',0):('Bedroom 02','roller-blackout-54in-78in',math.pi),
             ('west',0):('Bedroom 02','roller-blackout-42in-78in',math.pi/2),
             ('west',1):('Bedroom 03','roller-blackout-42in-78in',math.pi/2),
             ('west',2):('Primary','roller-blackout-48in-107p4in',math.pi/2),
             ('north',0):('Primary','roller-blackout-60in-107p4in',0)}
    for name,a,b,thickness,openings in d.WALLS:
        length=math.dist(a,b);ux=(b[0]-a[0])/length;uy=(b[1]-a[1])/length
        for index,(off,width,sill,head,kind) in enumerate(sorted(openings)):
            if (name,index) not in targets:continue
            room,slug,rotation=targets[(name,index)]
            pitch=width/max(1,round(width/d.ft(4)));count=round(width/pitch)
            inward=(math.sin(rotation),-math.cos(rotation))
            folder=root/'library/openings'/slug/'v001';meta=json.loads((folder/'asset.json').read_text())
            if slug not in closed_cache:
                path=folder/meta['files']['blender']
                with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.collections=[meta['blender']['states']['closed']]
                closed_cache[slug]=dst.collections[0]
            for bay in range(count):
                x=a[0]+ux*(off+pitch*(bay+.5));y=a[1]+uy*(off+pitch*(bay+.5))
                loc=(x+inward[0]*.15,y+inward[1]*.15,head)
                label=f'{room} {name} bay {bay+1} privacy blind'
                obj=asset('openings',slug,label+' open',loc,rotation)
                obj['ifc_class']='IfcCovering';obj['shade_state']='open';obj['shade_pair']=label
                closed=bpy.data.objects.new(label+' closed',None);closed.instance_type='COLLECTION';closed.instance_collection=closed_cache[slug]
                coll.objects.link(closed);closed.location=loc;closed.rotation_euler.z=rotation
                closed.hide_render=True;closed.hide_viewport=True
                closed['asset_id']='openings/'+slug;closed['asset_version']='v001';closed['shade_state']='closed';closed['shade_pair']=label
                result.append({'id':label,'room':room,'asset':'openings/'+slug+'/v001','open_instance':obj.name,'closed_instance':closed.name,'origin_m':list(loc),'rotation_rad':rotation,'nominal_bay_pitch_m':pitch,'glass_clear_width_m':pitch-.084,'glass_sill_m':sill+.025+.042,'glass_head_m':head-.015-.042,'privacy_basis':'Opaque modeled fabric covers the visible glazing in closed state; actual product edge-light, mounting and blackout performance unverified.'})
    return result
