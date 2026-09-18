"""Verify a reopened home's exact native library pins and actual direct adoption."""
import bpy,json
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
home=Path(bpy.data.filepath).resolve().parent.parent
meta=json.loads((home/'project.json').read_text())
actual={};uses=defaultdict(list)
for lib in bpy.data.libraries:
    assert lib.filepath.startswith('//'),lib.filepath
    p=Path(bpy.path.abspath(lib.filepath)).resolve();assert p.is_relative_to(ROOT/'library'),p
    manifest=p.parent/'asset.json';assert manifest.exists(),manifest
    a=json.loads(manifest.read_text());actual[p]=(a['id'],a['version'])
for obj in bpy.context.scene.objects:
    coll=obj.instance_collection if obj.instance_type=='COLLECTION' else None
    if coll and coll.library:
        p=Path(bpy.path.abspath(coll.library.filepath)).resolve()
        if p in actual:uses[actual[p]].append(obj.name)
    for slot in obj.material_slots:
        if slot.material and slot.material.library:
            p=Path(bpy.path.abspath(slot.material.library.filepath)).resolve()
            if p in actual:uses[actual[p]].append(obj.name+' (material)')
pins={(d['id'],d['version']) for d in meta['asset_dependencies']}
assert pins==set(actual.values()),{'missing_pins':list(set(actual.values())-pins),'unused_manifest_pins':list(pins-set(actual.values()))}
rows=[]
for aid,ver in sorted(pins):
    names=uses[(aid,ver)]
    # Some linked materials are transitive dependencies of actual linked collections.
    parents=[]
    if not names:
        for p,(pid,pv) in actual.items():
            a=json.loads((p.parent/'asset.json').read_text())
            if any(d.get('id')==aid and d.get('version')==ver for d in a.get('dependencies',[]) if isinstance(d,dict)) and uses[(pid,pv)]:parents.append(pid)
    assert names or parents,(aid,ver,'loaded but no direct use or declared adopted parent')
    rows.append({'id':aid,'version':ver,'direct_placements_or_material_assignments':len(names),'examples':names[:8],'adopted_parent_dependencies':parents})
report={'home':meta['id'],'native_library_pins_match_manifest':True,'asset_versions':len(rows),'assets':rows}
(home/'model/asset-adoption.json').write_text(json.dumps(report,indent=2)+'\n')
print('ASSET_ADOPTION_VERIFIED',meta['id'],len(rows),flush=True)
