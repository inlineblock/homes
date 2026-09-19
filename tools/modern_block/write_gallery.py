"""Refresh the reviewed gallery from selected photo prompts and stable native images."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];H=ROOT/'homes/modern-block'
rows=[
('01-front-arrival','Sheltered stone arrival, deep bedroom reveal and private cedar-screened bath','exterior','arrival'),
('13-east-arrival','East elevation: limestone fireplace pier, aligned stair glazing and sheltered entrance','exterior',None),
('02-courtyard-pool','Courtyard pool, sheltered seating and supported glass-guarded balcony','exterior','outdoor'),
('03-roof-and-site','Elevated roof and site view, skylights, guest pavilion and two-car garage','exterior','site'),
('04-lanai-open','Five pivoting timber screens open to the covered lanai','exterior',None),
('09-lanai-closed','The same five screens closed, from the identical camera','exterior',None),
('10-pool-and-balcony','Pool steps, covered upper balcony and continuous courtyard glazing','exterior',None),
('05-kitchen','Oak kitchen, wide refrigeration, island seating and slatted rooflight ceiling','interior',None),
('06-living','Living room with limestone hearth, charcoal chimney face and oak seating','interior',None),
('07-primary-bedroom','Primary bedroom with a king bed, oak nightstands and tree-level glazing','interior',None),
('08-primary-bath','Primary double vanity and separate dressing and enclosed toilet-room entries','interior',None),
('12-bath-tub-shower','Freestanding tub and separate glass shower in the primary bathroom','interior',None),
('11-stair-gallery','Upper landing with linen shelving, oak stair treads and glass guards','interior',None)]
lookup={r[0]:r for r in rows}
renders=[]
for n,c,v,role in rows:
 item={'path':f'outputs/images/{n}.png','caption':c,'view':v}
 if role:item['exterior_role']=role
 renders.append(item)
sha=lambda p:hashlib.sha256((H/p).read_bytes()).hexdigest()
specs=json.loads((H/'outputs/photo-prompts.json').read_text())
photos=[]
for spec in specs:
 n=Path(spec['source_render']).stem;c=lookup[n][1]
 photos.append({'path':spec['output'],'kind':'ai-photographic-study','tool':'Imagegen (built-in)','source_render':spec['source_render'],'source_sha256':sha(spec['source_render']),'image_sha256':sha(spec['output']),'provenance':'outputs/photo-study.md','caption':c+' — AI photographic study'})
plans=[{'path':f'outputs/plans/{n}.png','level':n,'caption':c} for n,c in [('ground-floor','Ground floor: furnished public rooms, guest retreat, service spaces, garage and courtyard'),('upper-floor','Upper floor: three bedrooms, primary suite, shared bath and stair gallery')]]
gallery={'schema_version':1,'renders':renders,'required_levels':['ground-floor','upper-floor'],'plans':plans,'signature_features':[{'id':'arrival-and-privacy','label':'Sheltered entry, screened bath and functional east stone pier','renders':['outputs/images/01-front-arrival.png','outputs/images/13-east-arrival.png']},{'id':'pivot-screens','label':'Operable timber-screen lanai','renders':['outputs/images/04-lanai-open.png','outputs/images/09-lanai-closed.png']},{'id':'courtyard-pool','label':'Courtyard pool and covered balcony','renders':['outputs/images/02-courtyard-pool.png','outputs/images/10-pool-and-balcony.png']},{'id':'hearth','label':'Limestone hearth with charcoal chimney face','renders':['outputs/images/06-living.png']},{'id':'slatted-rooflight','label':'Kitchen slatted ceiling and rooflight','renders':['outputs/images/05-kitchen.png']}],'photographic_hero':photos[0],'photographic_exteriors':[p for p in photos[1:] if lookup[Path(p['source_render']).stem][2]=='exterior'],'photographic_interiors':[p for p in photos if lookup[Path(p['source_render']).stem][2]=='interior']}
(H/'gallery.json').write_text(json.dumps(gallery,indent=2)+'\n')
prov='# AI photographic studies\n\nTen studies made with the built-in Imagegen editing tool from reviewed native renders. These are design illustrations, not photographs of a built property. The native model and native gallery govern dimensions and geometry. The selected studies were compared visually with their inputs; texture, sky, reflections and small material responses remain generative interpretations. Surrounding woodland, layered planting and landscape visible through glazing are intentionally enriched beyond the modeled planting to avoid an isolated setting; these additions are illustrative context, not surveyed conditions or modeled scope.\n\n'
for spec,p in zip(specs,photos):
 prov+=f"## {Path(p['path']).stem}\n\n- Source: `{p['source_render']}`\n- Source SHA-256: `{p['source_sha256']}`\n- Selected image: `{p['path']}`\n- Image SHA-256: `{p['image_sha256']}`\n- Tool: {p['tool']}\n\nActual prompt:\n\n> {spec['prompt']}\n\n"
for spec in specs:
 if spec.get('correction_prompt'):
  prov+=f"## Targeted correction — {Path(spec['output']).stem}\n\nThe initial photographic result was the edit target, with the current native render supplied again as the geometry/material reference. Actual correction prompt:\n\n> {spec['correction_prompt']}\n\n"
(H/'outputs/photo-study.md').write_text(prov.rstrip()+'\n')
intro='A sheltered limestone entrance, deep bedroom opening and screened bathing bay give the warm stone and cedar composition depth. A functional stone fireplace pier and aligned stair windows articulate the east side. The pavilions frame a private pool court within a wooded garden setting. Five pivoting timber screens open the covered lanai between the main house and a guest/office pavilion. The four-bedroom concept includes a complete kitchen, primary bathing suite, generous storage and a two-car garage.\n\n**Concept areas:** approximately 5,683 sq ft conditioned gross, plus 689 sq ft garage. Conditioned area includes wall footprints and excludes the upper stair void, lanai, pool, balcony and exterior terraces. Dimensions and unseen layout are creative design choices; this is not a measured as-built model or construction documentation.\n\n'
def img(item,prefix):return f"![{item['caption']}]({prefix}{item['path']})\n\n*{item['caption']}.*\n\n"
def page(prefix,homeprefix,title):
 text=f'# {title}\n\n'+img(photos[0],prefix)+intro
 text+=f"[Editable Blender model]({homeprefix}model/modern-block.blend) · [Classified concept IFC]({homeprefix}model/modern-block.ifc) · [Design intent]({homeprefix}design-intent.md) · [Program]({homeprefix}program.md) · [Review and limitations]({homeprefix}design-review.md) · [Assets]({homeprefix}assets/README.md)\n\n"
 text+='## Photographic tour\n\nAI photographic studies derived from the native views below. [Prompts and provenance]('+prefix+'outputs/photo-study.md).\n\n'
 for p in photos[1:]:
  text+=img(p,prefix)
  if p in gallery['photographic_interiors']:
   native=next(r for r in renders if r['path']==p['source_render']);text+=img(native,prefix)
 text+='## Native model tour\n\nThe following images are direct renders of the editable Blender model.\n\n'
 paired={p['source_render'] for p in gallery['photographic_interiors']}
 for r in renders:
  if r['path'] not in paired:text+=img(r,prefix)
 text+='## Furnished concept plans\n\n'
 for p in plans:
  text+=img(p,prefix);stem=p['path'][:-4];text+=f"[PDF]({prefix}{stem}.pdf) · [Editable SVG]({prefix}{stem}.svg)\n\n"
 text+=f"## Reproduce and inspect\n\n[Authoring instructions]({homeprefix}../../tools/modern_block/AGENTS.md) document generation, reopening and review. Blender 4.5.14 LTS; Bonsai and IfcOpenShell 0.8.5. Fifty-two exact library versions are pinned. Native file, IFC and plans reopened successfully; see the [verification record]({homeprefix}design-review.md).\n\nEngineering, surveyed site conditions, product selection, privacy/shading specifications, MEP sizing, pool safety and approvals remain unresolved. No permit or construction readiness is claimed.\n"
 return text
(H/'README.md').write_text(page('','','Modern Block'))
(H/'outputs/README.md').write_text(page('../','../','Modern Block — current outputs'))
# Root entry includes all native renders, every study and every occupied level.
entry='### Modern Block\n\n'+img(photos[0],'homes/modern-block/')+intro+'[Full project and editable models](homes/modern-block/README.md) · [Current outputs](homes/modern-block/outputs/README.md)\n\n'
entries=[]
for p in photos[1:]:
 entries.append(p)
 if p in gallery['photographic_interiors']:entries.append(next(r for r in renders if r['path']==p['source_render']))
paired={p['source_render'] for p in gallery['photographic_interiors']}
entries += [r for r in renders if r['path'] not in paired]
for i in range(0,len(entries),2):
 pair=entries[i:i+2]
 if len(pair)==1:entry+=img(pair[0],'homes/modern-block/');continue
 a,b=pair;entry+=f"| {a['caption']} | {b['caption']} |\n| --- | --- |\n| ![{a['caption']}](homes/modern-block/{a['path']}) | ![{b['caption']}](homes/modern-block/{b['path']}) |\n\n"
for p in plans:entry+=img(p,'homes/modern-block/')
root=ROOT/'README.md';s=root.read_text();start=s.find('### Modern Block\n');
if start>=0:
 end=s.find('\n### ',start+1);s=s[:start]+(s[end+1:] if end>=0 else '')
pos=s.index('### ');s=s[:pos]+entry+s[pos:];root.write_text(s)
print('GALLERY_WRITTEN',len(renders),len(photos),len(plans))
