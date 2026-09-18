"""Original physical-scale shaders; publish reusable immutable material assets."""
import bpy,json
from common.geometry import material

def textured(name,c1,c2,scale,rough=.5,bump=.0002,stretch=(1,1,1)):
    m=material(name,c1,rough);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    tc=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=stretch;l.new(tc.outputs['Object'],v.inputs[0])
    t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=scale;t.inputs['Detail'].default_value=3;l.new(v.outputs[0],t.inputs['Vector'])
    r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*c1,1);r.color_ramp.elements[1].color=(*c2,1);l.new(t.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
    b=n.new('ShaderNodeBump');b.inputs['Distance'].default_value=bump;b.inputs['Strength'].default_value=.16;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
    return m

def publish(root,slug,m,description):
    folder=root/'library/materials'/slug/'v001';path=folder/(slug+'.blend');folder.mkdir(parents=True,exist_ok=True)
    if not path.exists():
        bpy.data.libraries.write(str(path),{m},fake_user=True)
        meta={'schema_version':1,'id':'materials/'+slug,'version':'v001','name':m.name,'units':'meters','license':'CC-BY-4.0','rights':'Original; attribution Homes project contributors','source':{'kind':'original','generator':'tools/coastal04/materials.py'},'files':{'blender':path.name},'dependencies':[],'description':description,'texture_scale':'Object coordinates in meters; no external images.'}
        (folder/'asset.json').write_text(json.dumps(meta,indent=2)+'\n')
    with bpy.data.libraries.load(str(path),link=True) as (src,dst):dst.materials=[src.materials[0]]
    return dst.materials[0]

def palette(root):
    M={}
    M['oak']=publish(root,'coastal-white-oak',textured('Natural white oak | fine longitudinal grain',(.30,.20,.105),(.47,.34,.20),5,.42,.00015,(32,32,.55)),'Fine vertically oriented original white oak. Rotate geometry as required for grain direction.')
    M['stone']=publish(root,'coastal-honed-limestone',textured('Warm pale honed limestone',(.53,.50,.435),(.66,.635,.565),110,.48,.00018),'Subtle physical-scale limestone grain, suitable for interior and terrace pavers.')
    M['plaster']=textured('Chalk mineral plaster',(.73,.72,.685),(.79,.78,.745),180,.82,.00012)
    M['ceiling']=material('Warm white ceiling',(.80,.795,.76),.85)
    M['linen']=textured('Ivory linen weave',(.58,.56,.505),(.72,.70,.65),420,.9,.00012)
    M['blue']=textured('Muted sea blue linen',(.095,.16,.18),(.14,.235,.26),420,.92,.00015)
    M['sand']=textured('Fine dune sand',(.47,.405,.29),(.65,.59,.45),75,.96,.0008)
    M['bronze']=material('Satin champagne aluminum',(.21,.185,.135),.28,.75)
    M['dark']=material('Graphite hardware',(.025,.029,.028),.3,.55)
    M['steel']=material('Brushed stainless',(.52,.53,.51),.23,.9)
    M['porcelain']=material('Warm glazed porcelain',(.80,.80,.76),.21)
    M['leaf']=textured('Coastal sage foliage',(.085,.12,.055),(.21,.255,.145),12,.75,.0001)
    M['grass']=material('Dune grass',(.255,.285,.13),.85)
    M['bark']=textured('Olive bark',(.055,.042,.027),(.15,.12,.08),35,.92,.002)
    M['glass']=material('Low tint clear architectural glass',(.97,.99,1),.025);p=M['glass'].node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
    M['counter']=textured('Ivory quartzite quiet mineral field',(.67,.655,.59),(.78,.76,.69),2.5,.25,.00005,(1,1,4))
    M['glow']=material('Warm LED diffuser',(1,.88,.66),.4);p=M['glow'].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.82,.57,1);p.inputs['Emission Strength'].default_value=2
    return M
