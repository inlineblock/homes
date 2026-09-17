"""Export architectural geometry and labeled design zones from the saved scene."""
import bpy,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
from design import *
import ifcopenshell,ifcopenshell.api,ifcopenshell.validate
api=ifcopenshell.api.run
f=api('project.create_file',version='IFC4')
project=api('root.create_entity',f,ifc_class='IfcProject',name='Atrium 01 | Concept')
units=[api('unit.add_si_unit',f,unit_type=t) for t in ['LENGTHUNIT','AREAUNIT','VOLUMEUNIT']]
api('unit.assign_unit',f,units=units)
site=api('root.create_entity',f,ifc_class='IfcSite',name='Unspecified conceptual site')
building=api('root.create_entity',f,ifc_class='IfcBuilding',name='Atrium 01')
storey=api('root.create_entity',f,ifc_class='IfcBuildingStorey',name='Ground floor')
for parent,child in [(project,site),(site,building),(building,storey)]:api('aggregate.assign_object',f,products=[child],relating_object=parent)
model=api('context.add_context',f,context_type='Model')
body=api('context.add_context',f,context_type='Model',context_identifier='Body',target_view='MODEL_VIEW',parent=model)
ps=api('pset.add_pset',f,product=building,name='Homes_DesignBrief')
api('pset.edit_pset',f,pset=ps,properties={'Stage':'Concept - not construction documentation','Bedrooms':3,'Bathrooms':3,'GrossEnclosedAreaSquareFeet':2400.0,'AreaBasis':'60 x 44 ft outer footprint minus 16 x 15 ft open atrium, includes walls','AuthoringSource':'tools/atrium01/design.py'})
styles={}
def style_for(mat):
    if mat.name in styles:return styles[mat.name]
    s=api('style.add_style',f,name=mat.name);r,g,b,_=mat.diffuse_color
    api('style.add_surface_style',f,style=s,attributes={'SurfaceColour':{'Name':None,'Red':float(r),'Green':float(g),'Blue':float(b)},'Transparency':.78 if 'glass' in mat.name.lower() else 0.0})
    styles[mat.name]=s;return s
counts={}
for obj in bpy.context.scene.objects:
    if obj.type!='MESH':continue
    names=[c.name for c in obj.users_collection];cls=None
    if any(n.startswith('01 Architecture') for n in names):
        cls='IfcWindow' if 'pane' in obj.name else 'IfcDoor' if 'door' in obj.name else 'IfcMember' if any(k in obj.name for k in ['mullion','frame','pull']) else 'IfcWall'
    elif any(n.startswith('02 Architecture') for n in names):cls='IfcSlab'
    elif any(n.startswith('08 Structure') for n in names):cls='IfcColumn' if 'post' in obj.name else 'IfcBeam'
    elif obj.name.startswith('Flat insulated roof'):cls='IfcRoof'
    elif any(k in obj.name for k in ['Island walnut core','Island limestone top','Island stone waterfall','South limestone worktop']):cls='IfcFurnishingElement'
    if not cls:continue
    e=api('root.create_entity',f,ifc_class=cls,name=obj.name)
    verts=[tuple(obj.matrix_world@v.co) for v in obj.data.vertices];faces=[tuple(p.vertices) for p in obj.data.polygons]
    rep=api('geometry.add_mesh_representation',f,context=body,vertices=[verts],faces=[faces])
    api('geometry.assign_representation',f,product=e,representation=rep)
    api('spatial.assign_container',f,products=[e],relating_structure=storey)
    if obj.data.materials:api('style.assign_representation_styles',f,shape_representation=rep,styles=[style_for(obj.data.materials[0])])
    counts[cls]=counts.get(cls,0)+1
for slug,(x1,y1,x2,y2),label in ROOMS:
    e=api('root.create_entity',f,ifc_class='IfcSpace',name=label);e.LongName=slug
    api('aggregate.assign_object',f,products=[e],relating_object=storey)
    p=api('pset.add_pset',f,product=e,name='Homes_DesignZone')
    api('pset.edit_pset',f,pset=p,properties={'Purpose':'Labeled planning zone, not a measured net-area schedule','XMinFeet':float(x1),'YMinFeet':float(y1),'XMaxFeet':float(x2),'YMaxFeet':float(y2)})
path=ROOT/'homes/atrium-01/model/atrium-01.ifc';f.write(str(path))
reopened=ifcopenshell.open(str(path));logger=ifcopenshell.validate.json_logger();ifcopenshell.validate.validate(reopened,logger)
errors=[x for x in logger.statements if x.get('level')=='error']
report={'schema':f.schema,'counts':counts,'spaces':len(reopened.by_type('IfcSpace')),'schema_errors':len(errors),'details':errors[:10]}
(path.parent/'ifc-validation.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print('IFC_EXPORT',report)
if errors:raise RuntimeError('IFC schema validation failed')
