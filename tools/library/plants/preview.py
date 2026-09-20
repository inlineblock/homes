"""Render actual linked plant variants; writes current native previews, never AI studies."""
import argparse, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3]

def mat(name, color, roughness=.7):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=roughness
    return m

def cube(name,loc,scale,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);return o

def aim(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()

def text(label, pos, size, camera, material):
    c=bpy.data.curves.new('Caption','FONT');c.body=label;c.align_x='CENTER';c.align_y='CENTER';c.size=size
    o=bpy.data.objects.new(label,c);bpy.context.scene.collection.objects.link(o);o.location=pos;o.rotation_euler=camera.rotation_euler;o.data.materials.append(material)
    o.visible_shadow=False
    return o

def setup(samples, width,height,cpu):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=samples;sc.cycles.use_denoising=True;sc.cycles.adaptive_threshold=.025
    sc.cycles.max_bounces=7;sc.cycles.transparent_max_bounces=4
    sc.render.resolution_x=width;sc.render.resolution_y=height;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
    sc.render.threads_mode='FIXED';sc.render.threads=4
    sc.view_settings.view_transform='AgX'
    if not cpu:
        try:
            p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
            for d in p.devices:d.use=d.type=='METAL'
            if any(d.type=='METAL' for d in p.devices):sc.cycles.device='GPU'
        except Exception:pass
    sc.world=bpy.data.worlds.new('Studio world');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.82,.87,1,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.35
    return sc

def run(slug,args):
    directory=ROOT/'library/landscape'/slug/'v001';meta=json.loads((directory/'asset.json').read_text());native=directory/meta['files']['blender']
    bpy.ops.wm.read_factory_settings(use_empty=True)
    variants=meta['blender']['variants'];names=[v['collection'] for v in variants]
    with bpy.data.libraries.load(str(native),link=True,relative=True) as (src,dst):
        assert all(n in src.collections for n in names),slug
        dst.collections=list(names)
    loaded=dict(zip(names,dst.collections));instances=[];cursor=0;maxheight=0;depth=0
    for v in variants:
        dims=v['dimensions_m'];b=v['bounds_m'];w=max(dims[0],.15);h=max(dims[2],.15)
        gap=max(w*.18,.12);center=cursor+w/2
        o=bpy.data.objects.new(v['id'],None);o.instance_type='COLLECTION';o.instance_collection=loaded[v['collection']]
        o.location=(center-(b['min'][0]+b['max'][0])/2,-(b['min'][1]+b['max'][1])/2,0)
        bpy.context.scene.collection.objects.link(o);instances.append((o,v,center,w))
        cursor+=w+gap;maxheight=max(maxheight,h);depth=max(depth,dims[1])
    width=cursor;sc=setup(args.samples,1920,1080,args.cpu)
    soil=mat('Neutral soil',(0.15,.12,.085));floor=mat('Warm studio ground',(.63,.65,.60));ink=mat('Charcoal type',(.035,.045,.04))
    for o,v,center,w in instances:
        cube('Planting soil',(center,0,-.045*max(1,maxheight)),(w*1.07,max(v['dimensions_m'][1]*1.06,.18),.085*max(1,maxheight)),soil)
    cube('Studio floor',(width/2,0,-.1*max(1,maxheight)),(width*12,width*12,.03*max(1,maxheight)),floor)
    bpy.ops.object.camera_add(location=(width/2,-max(width,maxheight)*1.5,maxheight*.6+max(width,maxheight)*.58));cam=bpy.context.object
    target=Vector((width/2,0,maxheight*.45));aim(cam,target);cam.data.type='ORTHO';cam.data.ortho_scale=max(width*1.14,(maxheight+depth*.35)*1.9);sc.camera=cam
    scale=cam.data.ortho_scale
    for loc,energy,size in [((width*.1,-width*.5,maxheight+width*.6),width*width*12,width*.7),((width*.9,width*.3,maxheight+width*.5),width*width*8,width*.65)]:
        bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=energy;light.data.shape='DISK';light.data.size=max(size,1);aim(light,target)
    if not args.detail_only:
        plane=cam.rotation_euler.to_quaternion()
        screen_h=scale*sc.render.resolution_y/sc.render.resolution_x
        for o,v,center,w in instances:
            font=min(w/max(6,len(v['id'])*.54),scale/76)
            labelpos=cam.location+plane@Vector((center-width/2,-screen_h*.40,-1))
            sizepos=cam.location+plane@Vector((center-width/2,-screen_h*.445,-1))
            text(v['id'].replace('-',' '),labelpos,font,cam,ink)
            text('%.2f m tall | %.2f m wide'%(v['dimensions_m'][2],v['dimensions_m'][0]),sizepos,font*.72,cam,ink)
        sc.render.filepath=str(directory/'preview.png');bpy.ops.render.render(write_still=True)
        print('PLANT_PREVIEW',slug,flush=True)
    if args.preview_only:
        return
    # Detail is actual front canopy geometry, not an invented photographic embellishment.
    for o,v,c,w in instances:o.hide_render=True
    chosen=max(instances,key=lambda row:max([score for token,score in [('fruit',10),('berries',9),('bloom',8),('flower',8),('cluster',7),('mature',5),('summer',4)] if token in row[1]['id'].lower()] or [0]))
    preferred=meta.get('preferred_detail_variant')
    chosen=next((row for row in instances if row[1]['id']==preferred),chosen)
    o,v,c,w=chosen;o.hide_render=False
    for ob in bpy.data.objects:
        if ob.type=='FONT':ob.hide_render=True
    coll=o.instance_collection;points=[]
    for obj in coll.all_objects:
        if obj.type=='MESH':
            # Prefer visible foliage/flowers/fruit at the near canopy edge over bark.
            if any(k in obj.name.lower() for k in ('leaf','leav','foliage','flower','fruit','petal','needle','blade','seed')):
                step=max(1,len(obj.data.vertices)//2500)
                points.extend((obj.matrix_world@p.co)+o.location for p in list(obj.data.vertices)[::step])
    h=v['dimensions_m'][2]
    candidates=[p for p in points if p.z>h*.35 and p.z<h*.9]
    if candidates:
        ymin=min(p.y for p in candidates)
        near=[p for p in candidates if p.y<ymin+max(.2,v['dimensions_m'][1]*.15)]
        focal=min(near,key=lambda p:abs(p.z-h*.63)+abs(p.x-c)*.25)
    else:focal=Vector((c,-v['dimensions_m'][1]*.22,h*.65))
    span=max(.22,min(1.65,max(h*.33,w*.18)))
    cam.location=focal+Vector((span*.12,-span*2.5,span*.55));aim(cam,focal);cam.data.ortho_scale=span
    sc.render.resolution_x=1000;sc.render.resolution_y=1000;sc.cycles.samples=max(args.samples,48)
    sc.render.filepath=str(directory/'detail.png');bpy.ops.render.render(write_still=True)
    print('PLANT_DETAIL',slug,v['id'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--assets',nargs='+',required=True);p.add_argument('--samples',type=int,default=48);p.add_argument('--cpu',action='store_true');p.add_argument('--detail-only',action='store_true');p.add_argument('--preview-only',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    for slug in a.assets:run(slug,a)
