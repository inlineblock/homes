"""Publish reviewed Twin Gables gallery metadata/pages, never generate images."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HOME=ROOT/'homes/eichler-twin-gables'
sys.path.insert(0,str(Path(__file__).parent))
from design import VIEWS

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review-note',required=True,help='Actual completed native/photo review, not a promised check')
    args=parser.parse_args()
    meta=json.loads((HOME/'project.json').read_text())
    image_dir=HOME/'outputs/images'
    captions={
      '01-front':'Private front arrival, twin gables and timber-covered framing',
      '02-rear':'Vaulted living and kitchen opening to the rear garden terrace',
      '03-side':'Coordinated side elevation, consistent eaves and window rhythm',
      '04-living':'Vaulted living room and garden connection',
      '05-kitchen':'Complete kitchen, preparation island and fitted storage',
      '06-courtyard':'Open-air courtyard and sheltered internal galleries',
      '07-primary':'Vaulted primary bedroom with screened street-facing glazing',
      '08-primary-bath':'Primary ensuite double vanity and bathing finishes',
      '09-rear-terrace':'Rear terrace for outdoor dining and sitting',
      '10-roof-site':'Two parallel roof ridges and the open courtyard',
      '11-east-primary':'Second equally complete primary bedroom',
      '12-east-bath':'Matching double vanity in the second primary ensuite',
      '13-dressing':'Walk-in clothes storage with a usable central aisle',
      '14-bath-detail':'Closed bathroom linen closet beside the separate shower',
    }
    exteriors={'01-front':'arrival','02-rear':'outdoor','03-side':'site','06-courtyard':'outdoor','09-rear-terrace':'outdoor','10-roof-site':'site'}
    renders=[]
    for key in VIEWS:
        p=image_dir/(key+'.png')
        if not p.exists():raise FileNotFoundError(p)
        row={'path':str(p.relative_to(HOME)),'caption':captions.get(key,key.replace('-',' ').title()),'view':'exterior' if key in exteriors else 'interior','sha256':digest(p)}
        if key in exteriors:row['exterior_role']=exteriors[key]
        renders.append(row)
    provenance_path=HOME/'outputs/photo-provenance.json'
    provenance=json.loads(provenance_path.read_text())
    photos=provenance['views']
    for v in photos:
        assert digest(HOME/v['source_render'])==v['source_sha256']
        assert digest(HOME/v['path'])==v['sha256']
    hero=next(v for v in photos if v['role']=='hero')
    def photo_record(v):return {k:v[k] for k in ['path','caption','source_render','source_sha256']}|{'image_sha256':v['sha256'],'kind':'ai-photographic-study','tool':'ImageGen (built-in)','provenance':'outputs/photo-provenance.json'}
    plan=HOME/'outputs/plans/floor-plan.png'
    assert plan.is_file()
    gallery={'schema_version':1,'home':meta['id'],'required_levels':['ground-floor'],'renders':renders,'plans':[{'level':'ground-floor','path':'outputs/plans/floor-plan.png','caption':'Dimensioned furnished ground-floor concept plan'}],'signature_features':[{'id':'courtyard','label':'Planted courtyard','renders':['outputs/images/06-courtyard.png']},{'id':'roof-framing','label':'Twin gables with wood-covered steel framing','renders':['outputs/images/01-front.png','outputs/images/04-living.png']},{'id':'dual-suites','label':'Two primary suites with ensuite and walk-in storage','renders':['outputs/images/07-primary.png','outputs/images/08-primary-bath.png','outputs/images/12-east-bath.png','outputs/images/13-dressing.png','outputs/images/14-bath-detail.png']}],'photographic_hero':photo_record(hero),'photographic_exteriors':[photo_record(v) for v in photos if v['role']=='exterior'],'photographic_interiors':[photo_record(v) for v in photos if v['role']=='interior'],'review_note':args.review_note}
    (HOME/'gallery.json').write_text(json.dumps(gallery,indent=2)+'\n')
    def page(output=False):
        prefix='' if not output else '../'
        def link(p):return p if not output else p.removeprefix('outputs/') if p.startswith('outputs/') else '../'+p
        s=f"# {meta['name']}"+(' — current outputs' if output else '')+'\n\n'
        s+=f"![{hero['caption']}]({link(hero['path'])})\n\n*AI photographic study of the reviewed native design; not a built-home photograph.*\n\n"
        s+='Two primary suites, each with its own walk-in closet, double vanity, separate tub and shower, enclosed toilet room and linen closet. A separate office/guest room, complete kitchen, fitted pantry and planted courtyard support everyday living.\n\n'
        s+='**3,360 sq ft gross planning area · two dedicated bedrooms + office/guest · three baths · one occupied level.** Includes wall allowances; excludes the 720 sq ft courtyard, parking, terraces and roof overhangs.\n\n'
        s+='The private street facade gives way to tall vaulted living spaces and a glazed rear garden elevation. Steel framing is a concept assumption; visible beams use nonstructural wood-look covers. Clear ceiling heights, equipment and door operation are recorded in the design review.\n\n'
        s+=f"[Brief]({link('brief.md')}) · [Design intent]({link('design-intent.md')}) · [Program]({link('program.md')}) · [Design review]({link('design-review.md')}) · [Shared asset schedule]({link('assets/README.md')})\n\n"
        s+='## Photographic tour\n\n'
        for v in photos:
            if v is hero:continue
            s+=f"### {v['caption']}\n\n![{v['caption']}]({link(v['path'])})\n\n"
            if v['role']=='interior':s+=f"*Matching native view:*\n\n![Native source for {v['caption']}]({link(v['source_render'])})\n\n"
        s+='## Native model views\n\n'
        for r in renders:s+=f"### {r['caption']}\n\n![{r['caption']}]({link(r['path'])})\n\n"
        s+=f"## Plans\n\n![Furnished ground floor]({link('outputs/plans/floor-plan.png')})\n\n[Plan PDF]({link('outputs/plans/floor-plan.pdf')}) · [Editable SVG]({link('outputs/plans/floor-plan.svg')})\n\n"
        roof=HOME/'outputs/plans/roof-and-section.png'
        if roof.exists():s+=f"![Roof and clear-height concept section]({link('outputs/plans/roof-and-section.png')})\n\n[Roof/section PDF]({link('outputs/plans/roof-and-section.pdf')})\n\n"
        s+='## Editable sources and evidence\n\n'
        for label,path in [('Blender visualization','model/eichler-twin-gables.blend'),('Classified IFC concept geometry','model/eichler-twin-gables.ifc'),('Photographic source hashes and prompts','outputs/photo-provenance.json'),('Original accepted concepts','references/README.md'),('Rebuild and review instructions','AUTHORING.md')]:
            if not (HOME/path).exists():raise FileNotFoundError(HOME/path)
            s+=f'- [{label}]({link(path)})\n'
        s+='\nThis is a coordinated architectural concept, not construction documentation. Site, climate, structure, fire/thermal enclosure, roof/glazing products, services sizing and local approvals remain unverified. AI studies interpret fine material, lighting and planting detail; the native model and drawings govern the modeled design.\n'
        return s
    (HOME/'README.md').write_text(page())
    (HOME/'outputs/README.md').write_text(page(True))
    print('TWIN_GALLERY_PAGES_WRITTEN',len(renders),'native',len(photos),'photographic')
if __name__=='__main__':main()
