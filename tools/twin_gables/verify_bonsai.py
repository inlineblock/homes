"""Fresh Bonsai import; no native or saved-preferences mutation."""
import bpy,sys,runpy,tempfile,json,hashlib,addon_utils,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/eichler-twin-gables'
parser=argparse.ArgumentParser();parser.add_argument('--runtime-path',type=Path)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
if args.runtime_path:sys.path.insert(0,str(args.runtime_path))
module='bl_ext.user_default.bonsai'
try:bpy.ops.bim.load_project.get_rna_type()
except Exception:
 addon_utils.enable(module,default_set=True,persistent=False)
prefs=bpy.context.preferences.addons[module].preferences;prefs.save_metadata_blend_file=False
with tempfile.TemporaryDirectory(prefix='twin-bonsai-') as cache:
 prefs.cache_dir=cache;sys.argv=['verify_bonsai.py','--','eichler-twin-gables'];runpy.run_path(str(ROOT/'tools/common/verify_bonsai.py'),run_name='__main__')
rpath=HOME/'model/bonsai-validation.json';r=json.loads(rpath.read_text());r['source_blend_sha256']=hashlib.sha256((HOME/'model/eichler-twin-gables.blend').read_bytes()).hexdigest();r['ifc_sha256']=hashlib.sha256((HOME/'model/eichler-twin-gables.ifc').read_bytes()).hexdigest();r['limits']='Fresh import of classified concept meshes, not engineering or complete semantic BIM';rpath.write_text(json.dumps(r,indent=2)+'\n')
