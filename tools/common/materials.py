import bpy
from .geometry import material
def noise_material(name,c1,c2,scale,roughness=.5,bump=.03,mapping=(1,1,1)):
    m=material(name,c1,roughness);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale;tex.inputs['Detail'].default_value=3
    coord=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=mapping
    l.new(coord.outputs['Generated'],v.inputs[0]);l.new(v.outputs['Vector'],tex.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=(*c1,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(*c2,1)
    l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
    b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.2;b.inputs['Distance'].default_value=bump
    l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal']);return m
def palette():
    out={
      'plaster':noise_material('Warm chalk plaster',(.72,.68,.59),(.9,.86,.77),55,bump=.001),
      'concrete':noise_material('Honed warm concrete',(.39,.36,.30),(.62,.59,.52),22,.6,.002),
      'walnut':noise_material('Oiled walnut | vertical grain',(.035,.012,.006),(.17,.065,.025),3,.42,.0005,(7,7,.35)),
      'fir':noise_material('Douglas fir | exposed structure',(.23,.12,.055),(.51,.31,.14),4,.5,.001,(.25,5,5)),
      'stone':noise_material('Warm ivory limestone',(.7,.67,.58),(.92,.89,.8),7,.28,.001),
      'black':material('Blackened bronze',(.025,.03,.026),.3,.7),
      'steel':material('Brushed stainless',(.44,.48,.49),.24,.85),
      'white':material('Porcelain',(.88,.86,.79),.2),
      'fabric':noise_material('Oatmeal woven upholstery',(.56,.49,.39),(.79,.73,.63),125,.8,.001),
      'sage':material('Sage ceramic glaze',(.24,.34,.25),.22),
      'terracotta':material('Terracotta',(.43,.19,.10),.72),
      'soil':material('Dark earth',(.075,.065,.035),1),
      'leaves':material('Olive foliage',(.17,.25,.08),.65),
      'orange':material('Citrus',(.95,.3,.018),.37),
      'water':material('Still water',(.07,.12,.11),.14),
    }
    g=material('Clear architectural glass',(.95,.99,.97),.025)
    p=g.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
    out['glass']=g
    e=material('Opal glowing glass',(1,.88,.65),.25);p=e.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.69,.39,1);p.inputs['Emission Strength'].default_value=.6;out['glow']=e
    return out
