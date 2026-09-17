"""Import a saved IFC with Bonsai itself, in a separate Blender process."""
import bpy,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
slug=sys.argv[sys.argv.index('--')+1]
path=ROOT/'homes'/slug/'model'/f'{slug}.ifc'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
result=bpy.ops.bim.load_project(filepath=str(path),should_start_fresh_session=False)
assert result=={'FINISHED'},result
import bonsai.tool as tool
model=tool.Ifc.get();assert model is not None
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
assert len(objects)>20,len(objects)
receipt={'bonsai_import':'passed','schema':model.schema,'imported_mesh_objects':len(objects),'project':model.by_type('IfcProject')[0].Name}
(path.parent/'bonsai-validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('BONSAI_IMPORT_VERIFIED',receipt,flush=True)
