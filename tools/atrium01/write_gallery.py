"""Write Atrium's full landing pages from reviewed native/photo records."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];HOME=ROOT/'homes/atrium-01'
ROWS=[
('03-exterior','Sheltered arrival, continuous low timber roof and separate two-car carport','exterior','arrival'),
('05-rear-terrace','Garden elevation, supported canopy and outdoor living terrace','exterior','outdoor'),
('06-west-roof-atrium','Roof, open courtyard and parking relationship','exterior','site'),
('11-sheltered-arrival','Human-scale covered entrance and timber door','exterior',None),
('12-entry-gallery','Foyer with coat storage and direct indoor courtyard gallery','interior',None),
('01-kitchen','Walnut-and-sage kitchen with pale stone island and generous working aisle','interior',None),
('02-kitchen-courtyard','Kitchen looking into the open planted courtyard','interior',None),
('08-living','Garden-facing living room and dining connection','interior',None),
('07-open-air-atrium','Open-air planted atrium with actual sliding-door access','exterior',None),
('09-primary-bedroom','Primary bedroom with full-size bed and dedicated wardrobes','interior',None),
('10-primary-bath','Double vanity and freestanding tub in the primary bathing suite','interior',None),
('13-tub-and-shower','Separate tub and generous shower in the primary bathroom','interior',None),
('14-primary-privacy','Primary bedroom with the same opaque roller blinds fully lowered','interior',None),
('04-cutaway','Roof-off furnished layout and enclosed circulation around the atrium','cutaway',None)]
lookup={r[0]:r for r in ROWS}

def main():
    sha=lambda path:hashlib.sha256((HOME/path).read_bytes()).hexdigest()
    renders=[]
    for name,caption,kind,role in ROWS:
        item={'path':f'outputs/images/{name}.png','caption':caption,'view':kind}
        if role:item['exterior_role']=role
        assert (HOME/item['path']).is_file(),item['path']
        renders.append(item)
    specs=json.loads((HOME/'outputs/photo-prompts.json').read_text())
    photos=[]
    for spec in specs:
        name=Path(spec['source_render']).stem
        photos.append({'path':spec['output'],'kind':'ai-photographic-study','tool':'Imagegen (built-in)','source_render':spec['source_render'],'source_sha256':sha(spec['source_render']),'image_sha256':sha(spec['output']),'provenance':'outputs/photo-study.md','caption':lookup[name][1]+' — AI photographic study'})
    plans=[{'path':'outputs/plans/floor-plan.png','level':'main','caption':'Dimensioned furnished main-floor concept plan'}]
    gallery={'schema_version':1,'renders':renders,'required_levels':['main'],'plans':plans,'signature_features':[{'id':'kitchen','label':'Walnut-and-sage kitchen','renders':['outputs/images/01-kitchen.png','outputs/images/02-kitchen-courtyard.png']},{'id':'atrium','label':'Planted open-air courtyard','renders':['outputs/images/07-open-air-atrium.png']},{'id':'sheltered-arrival','label':'Covered arrival and indoor gallery','renders':['outputs/images/11-sheltered-arrival.png','outputs/images/12-entry-gallery.png']}],'photographic_hero':photos[0],'photographic_exteriors':[p for p in photos[1:] if lookup[Path(p['source_render']).stem][2]=='exterior'],'photographic_interiors':[p for p in photos[1:] if lookup[Path(p['source_render']).stem][2]=='interior']}
    (HOME/'gallery.json').write_text(json.dumps(gallery,indent=2)+'\n')
    provenance='# AI photographic studies\n\nThese built-in Imagegen edits follow reviewed native renders. They are illustrations of an original concept, not photographs of an existing building. Model geometry and dimensioned plans remain authoritative. Surrounding trees, distant context and small landscape textures are intentionally enriched to situate the house; these additions are illustrative, not surveyed or fully modeled landscape scope. Each selected study was compared to its actual source for architectural and furnishing consistency. Material texture, reflections and foliage remain generative interpretations.\n\n'
    for spec,photo in zip(specs,photos):
        provenance+=f"## {Path(photo['path']).stem}\n\n- Source: `{photo['source_render']}`\n- Source SHA-256: `{photo['source_sha256']}`\n- Output: `{photo['path']}`\n- Output SHA-256: `{photo['image_sha256']}`\n- Tool: Imagegen (built-in)\n\nActual prompt:\n\n> {spec['prompt']}\n\n"
        if spec.get('correction_prompt'):provenance+=f"Correction prompt:\n\n> {spec['correction_prompt']}\n\n"
    (HOME/'outputs/photo-study.md').write_text(provenance.rstrip()+'\n')
    def image(item,prefix):return f"![{item['caption']}]({prefix}{item['path']})\n\n*{item['caption']}.*\n\n"
    def page(prefix,title):
        t=f'# {title}\n\n'+image(photos[0],prefix)
        t+='A low post-and-beam home wrapped around a planted open-air courtyard. A sheltered entrance leads directly to both wings indoors. The walnut-and-sage kitchen has a generous working aisle, with separate pantry and laundry rooms. Three bedrooms have dedicated clothes storage; the primary suite includes a double vanity, separate tub and shower, and enclosed toilet room.\n\n'
        t+='**3 bedrooms · 3 full baths · 2,400 sq ft gross enclosed.** The 60 × 44 ft footprint excludes a 16 × 15 ft open court from enclosed area. Walls are included; the separate carport, canopies and terraces are excluded. The finished ceiling is 10 ft 6 in, with 9 ft 6 in beneath main beams and deliberate 9 ft service ceilings.\n\n'
        t+=f'[Blender model]({prefix}model/atrium-01.blend) · [Classified concept IFC]({prefix}model/atrium-01.ifc) · [Design intent]({prefix}design-intent.md) · [Program]({prefix}program.md) · [Review]({prefix}design-review.md) · [Shared assets]({prefix}assets/README.md)\n\n'
        t+='## Plans and spatial layout\n\n'+image(plans[0],prefix)
        t+=f'[Dimensioned PDF]({prefix}outputs/plans/floor-plan.pdf) · [Editable SVG]({prefix}outputs/plans/floor-plan.svg)\n\n'
        for stem,caption in [('site-plan','Illustrative site: parking, covered approach, terrace and drainage reservations'),('sections','Concept heights, roof support and service allowances')]:
            if (HOME/f'outputs/plans/{stem}.png').is_file():
                t+=image({'path':f'outputs/plans/{stem}.png','caption':caption},prefix)
                t+=f'[PDF]({prefix}outputs/plans/{stem}.pdf) · [SVG]({prefix}outputs/plans/{stem}.svg)\n\n'
        t+=image(next(r for r in renders if r['view']=='cutaway'),prefix)
        t+=f'## Photographic tour\n\nAI photographic studies derived from the native views. [Prompts and provenance]({prefix}outputs/photo-study.md).\n\n'
        for photo in photos[1:]:
            t+=image(photo,prefix)
            if photo in gallery['photographic_interiors']:t+=image(next(r for r in renders if r['path']==photo['source_render']),prefix)
        paired={p['source_render'] for p in gallery['photographic_interiors']}
        t+='## Native model views\n\nDirect renders of the editable model, including the sheltered arrival and courtyard.\n\n'
        for render in renders:
            if render['path'] not in paired and render['view']!='cutaway':t+=image(render,prefix)
        t+=f'## Reproduce and review\n\nSee the [authoring instructions]({prefix}../../tools/atrium01/AGENTS.md) and [review record]({prefix}design-review.md) for tested commands and evidence. Blender 4.5.14 LTS; IFC4 and Bonsai verification are recorded separately.\n\nThis is a coordinated architectural concept on illustrative terrain. Site conditions, structural sizing, waterproofing, drainage capacity, products, MEP performance and local approvals require professional development. It is not permit or construction documentation.\n'
        return t
    (HOME/'README.md').write_text(page('','Atrium 01'))
    (HOME/'outputs/README.md').write_text(page('../','Atrium 01 — current outputs'))
    print('ATRIUM_GALLERY_WRITTEN',len(renders),len(photos))

if __name__=='__main__':main()
