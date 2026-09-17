"""Export classified concept geometry from an open home scene into IFC4."""
import bpy,json
from pathlib import Path
import ifcopenshell,ifcopenshell.api,ifcopenshell.validate
api=ifcopenshell.api.run
HOME=Path(bpy.data.filepath).parent.parent;manifest=json.loads((HOME/'project.json').read_text());slug=manifest['id']
f=api('project.create_file',version='IFC4');p=api('root.create_entity',f,ifc_class='IfcProject',name=manifest['name']+' | Concept')
api('unit.assign_unit',f,units=[api('unit.add_si_unit',f,unit_type=t) for t in ['LENGTHUNIT','AREAUNIT','VOLUMEUNIT']])
site=api('root.create_entity',f,ifc_class='IfcSite',name='Conceptual site - orientation unassigned');building=api('root.create_entity',f,ifc_class='IfcBuilding',name=manifest['name']);storey=api('root.create_entity',f,ifc_class='IfcBuildingStorey',name='Ground floor')
for a,b in [(p,site),(site,building),(building,storey)]:api('aggregate.assign_object',f,products=[b],relating_object=a)
context=api('context.add_context',f,context_type='Model');body=api('context.add_context',f,context_type='Model',context_identifier='Body',target_view='MODEL_VIEW',parent=context)
props=api('pset.add_pset',f,product=building,name='Homes_Concept')
api('pset.edit_pset',f,pset=props,properties={'Stage':manifest['status'],'GrossEnclosedAreaSquareFeet':float(manifest['gross_enclosed_area_sqft']),'AreaBasis':manifest['area_basis'],'Bedrooms':3,'Bathrooms':3})
styles={};counts={}
def getstyle(mat):
    if mat.name in styles:return styles[mat.name]
    s=api('style.add_style',f,name=mat.name);r,g,b,_=mat.diffuse_color
    api('style.add_surface_style',f,style=s,attributes={'SurfaceColour':{'Name':None,'Red':float(r),'Green':float(g),'Blue':float(b)},'Transparency':.8 if 'glass' in mat.name.lower() else 0.0});styles[mat.name]=s;return s
for obj in bpy.context.scene.objects:
    if obj.type!='MESH':continue
    groups=[c.name for c in obj.users_collection];cls=None;name=obj.name.lower()
    if any(c.startswith('01 Architecture') for c in groups):
        cls='IfcCovering' if 'cedar board' in name else 'IfcWindow' if 'glazing' in name or 'glass triangle' in name else 'IfcMember' if any(k in name for k in ['mullion','rail','truss','pull']) else 'IfcWall'
    elif any(c.startswith('02 Architecture') for c in groups):cls='IfcSlab'
    elif any(c.startswith('08 Structure') for c in groups):cls='IfcColumn' if 'post' in name else 'IfcBeam'
    elif any(c.startswith('09 Roof') for c in groups):cls='IfcMember' if any(k in name for k in ['seam','fascia','trim']) else 'IfcChimney' if 'chimney' in name else 'IfcRoof'
    if not cls:continue
    e=api('root.create_entity',f,ifc_class=cls,name=obj.name)
    verts=[tuple(obj.matrix_world@v.co) for v in obj.data.vertices];faces=[tuple(p.vertices) for p in obj.data.polygons]
    rep=api('geometry.add_mesh_representation',f,context=body,vertices=[verts],faces=[faces]);api('geometry.assign_representation',f,product=e,representation=rep);api('spatial.assign_container',f,products=[e],relating_structure=storey)
    if obj.data.materials:api('style.assign_representation_styles',f,shape_representation=rep,styles=[getstyle(obj.data.materials[0])])
    counts[cls]=counts.get(cls,0)+1
path=HOME/'model'/f'{slug}.ifc';f.write(str(path));reopened=ifcopenshell.open(str(path));logger=ifcopenshell.validate.json_logger();ifcopenshell.validate.validate(reopened,logger)
errors=[e for e in logger.statements if e.get('level')=='error'];report={'schema':f.schema,'counts':counts,'schema_errors':len(errors),'errors':errors[:10]};(HOME/'model/ifc-validation.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
if errors:raise RuntimeError('IFC schema errors')
print('IFC_EXPORTED',report,flush=True)
