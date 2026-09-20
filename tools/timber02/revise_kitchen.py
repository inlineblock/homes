"""Create a reviewed candidate without overwriting the existing canonical scene."""
import sys,json,hashlib
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'tools'),str(Path(__file__).parent)]
from kitchen import build_kitchen
HOME=ROOT/'homes/timber-courtyard-02';WORK=HOME/'outputs/work/kitchen';WORK.mkdir(parents=True,exist_ok=True)
source=HOME/'model/timber-courtyard-02.blend'
bpy.ops.wm.open_mainfile(filepath=str(source))
pins=build_kitchen()
for lib in bpy.data.libraries:
    lib.filepath=bpy.path.abspath(lib.filepath)
bpy.context.scene.render.filepath='//06-kitchen.png'
bpy.ops.wm.save_as_mainfile(filepath=str(WORK/'kitchen-candidate.blend'))
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(WORK/'kitchen-candidate.blend'))
(WORK/'revision.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'status':'candidate_requires_review','asset_dependencies':pins,'canonical_unchanged':True},indent=2)+'\n')
print('TIMBER_KITCHEN_CANDIDATE_SAVED',flush=True)
