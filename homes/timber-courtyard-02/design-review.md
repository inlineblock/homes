# Timber Courtyard 02 design review

**Status: the revised kitchen, pantry and adjacent furniture pass the listed native geometry/planning checks; whole-home coordination remains unresolved.** This scoped result does not approve construction, selected products or the rest of the house.

The exterior direction remains paired timber wings, dark pitched roofs, glazed central gable, low entry canopy and planted courtyard. The user allowed the interior to change. The three-bedroom/three-bath concept retains **2,400 sq ft gross enclosed**: 62 × 48 ft less the 24 × 24 ft courtyard, including walls and excluding courtyard, landscape and overhangs. Actual slab measurement remains 2,400 sq ft.

## Reviewed kitchen revision

Complete shared concept equipment replaces the narrow blank fridge, flat sink/hob proxies and absent oven/extraction. Cooking moves to the solid east wall; garden-facing sink/cleanup remains at the rear. The 48 in integrated refrigerator, 36 in induction top, 30 in oven, 36 in hood and integrated dishwasher retain full scale. The dishwasher sits west of the island so its open door and operator use clear side space. The island has three seats and a waste/recycling module. The pantry contains six shelving modules, three lower bases, an appliance counter, usable access, high glazing and continuous fixing support.

Smoked oak, pale stone and a concentrated sage cooking-wall accent replace the coarse all-over walnut treatment. Shared, supported dining chairs, dining table, sofa and coffee table replace floating/unsupported local furniture. These corrections exist in native geometry; photographic interpretation is not their evidence. The [asset schedule](assets/README.md) identifies 25 direct pins and two transitive dependencies.

## Current measured evidence

The promoted [native model](model/timber-courtyard-02.blend) has fresh [kitchen validation](model/kitchen-validation.json), SHA256 `b8309bcfcf9475b40cdfb621abf22c6b5a37627c0dc0912864749ea369cd4574`. The [independent verifier](../../tools/timber02/verify_kitchen.py) completed **31 checks: zero geometry/planning failures and one explicit selected-product allowance note**. A subsequent native change requires rerunning the checks against its actual file hash. Native rendering, photographic review and video regeneration have separate evidence and are not implied by this measured review.

| Check | Measured result / scope |
| --- | --- |
| Shared adoption | Equipment linked at scale 1; relative dependencies resolve. All four outlets use their declared fixture collection with no preview cameras/lights. |
| Sink/cooktop/oven fit | Rays through evaluated counters clear actual bowl/cooktop underbody. Sink/cabinet and oven/housing mesh bounds have no intersections. Sink opening is 664 × 464 mm. |
| Dishwasher | Closed body and declared concept installation height fit below counter. Open-door allowance and a 600 × 600 mm operator footprint clear island/dining furniture. Opposing island drawers no longer intersect that allowance. |
| Working aisles | Rear 48.3 in; east 50.7 in; fridge pull to island 48.44 in. These are concept planning targets, not regulatory compliance claims. |
| Extraction | Lowest hood/filter is 30.114 in above highest cooktop geometry. Fitted riser continues toward roof; actual duct sizing, discharge and penetration remain unresolved. |
| Oven operation | Actual door/window/handle bounds posed 90° open plus 600 mm operator footprint clear island; pivot is a concept assumption. |
| Drawer operation | A single 500 mm extension leaves approximately733–847 mm operator depth. Opposing drawers are not assumed simultaneously extended. |
| Seating | Three full-scale seats at 30 in centers; approximately 557 mm knee overhang to finished cabinet back. Static placement and 450 mm pullback allowance measured separately. |
| Pantry access | Actual opening 36 in; shelf aisle approximately76.26 in; open-leaf bypass approximately42.72 in. Shelves clear rear counter/bases. |
| Pantry wall | East glass is above7 ft shelves. Full-run ledger bridges shelf backs to continuous solid backing. Fasteners/capacity remain concept requirements. |
| Walking route | A 700 mm walking cylinder sampled every 50 mm reaches pantry without fixed-object conflicts, with equipment closed and pantry leaf open. Not accessibility certification. |
| Electrical fixture fit | Actual rays clear declared 52 mm host recesses. Wiring, circuiting, protection, ratings and plug/cord space remain unselected. |
| Adjacent furniture | Shared sofa, six dining chairs, dining table and coffee table reach modeled floor within 3 mm. |

### Refrigerator allowance still unresolved

The generic refrigerator manifest's conservative rectangular sweep allowance overlaps the neighboring filler/counter. That rectangle is not proof of a physical clash: actual modeled panels **and pulls** clear neighbors in 5° samples from 0° to110°. Both findings remain in the receipt. Before specifying a real unit, verify its actual hinge mechanism, relief, ventilation, services and replacement access; sampled concept motion cannot establish compliance with an unselected manufacturer.

## Whole-home issues still open

- Complete bedroom clothes storage, premium bathroom fixtures/operation, laundry capacity and coordinated household provisions need a full review against the [home checklist](../../docs/home-program-checklist.md). Kitchen success does not resolve those rooms.
- Parking and actual road-to-entry/site arrangement remain unresolved. The courtyard approach image is not a survey or site plan.
- Roof drainage, weatherproofing, structure, assemblies, services, equipment selection, climate/site conditions and approvals remain unresolved. New wall/clerestory/duct details are visual concepts.
- Beds/bedside pieces, bathroom proxies, planting and paving still include repeated local geometry needing shared adoption. See the schedule rather than calling legacy repetition bespoke.
- Previously missing kitchen oven/hood, legless dining chairs and unsupported coffee/table/sofa elements are corrected in this revision. Do not retain them as current kitchen failures or treat their correction as whole-home approval.

## Output and photographic evidence

The refreshed [IFC receipt](model/ifc-validation.json) reports IFC4 with zero schema errors; [Bonsai receipt](model/bonsai-validation.json) reports a successful fresh import with 1,091 mesh objects. These validate export/import, not construction or room function. The fresh [native reopen](model/model-validation.json) verifies 27 relative dependencies and all ten source-matched cameras. The refreshed [camera receipt](model/gallery-camera-validation.json) records that current evidence and explicitly retires the earlier camera-only unchanged-scene claim. The refreshed [output receipt](model/gallery-output-validation.json) identifies all ten promoted native images, their actual resolutions and hashes, matching native-source hash, completed visual-review notes and regenerated plan/board hashes. These receipts describe the coordinated kitchen revision and complement the separate measured kitchen checks; they do not approve the unresolved whole-home program.

The production review has now visually reviewed and promoted **ten native views rendered at 256 samples** and **six Image Gen studies**: front hero, kitchen, cooking wall, pantry, living room and rear garden. The updated floor-plan SVG, PNG, PDF and preview were also reviewed. See the [gallery register](gallery.json), [home gallery](README.md) and [outputs index](outputs/README.md) for the current files and photographic provenance. The photographic studies retain the revised native layout while interpreting materials, lighting and landscaping; they are not photographs of an existing building. Prompts and source/output hashes identify their actual inputs.

The scoped repository audit also passes: the promoted model reopens, all **27 pinned dependencies** match actual native adoption and resolve relatively, enclosed floor area measures **2,400 sq ft**, and three modeled beds agree with the manifest. This adoption/export evidence complements the visual review; it does not resolve the whole-home issues above.

The revised [native walkthrough](outputs/videos/timber-courtyard-native.mp4) is promoted with fifteen current paired photographic checkpoints. Its 721 frames fully decode at 1280 × 720, 24 fps and 30.041667 seconds. Sixty-one half-second samples and eight high-sample keyframes were visually reviewed; no visible architecture or furniture crossing was found. A 700 mm body sweep across every camera pose and connecting segment clears 2,063 evaluated fixed meshes, with about 142 mm minimum additional bounds clearance. See the [video receipt](outputs/videos/video-verification.json) for exclusions and exact hashes. The native video also passed an in-app browser playback smoke test through the kitchen endpoint without a media error. The separately measured [walking-surface review](outputs/videos/route-support-review.json) found support at all 49,665 sampled rays, while documenting raised tracks and ground/paving transitions; this is not a step-free or accessibility-approved route.

The [AI-finished walkthrough](outputs/videos/timber-courtyard-ai.mp4) is a reviewed 626-frame, 26.083-second moving-camera concept film at 768 × 448 and 24 fps. One deliberate cut at 20.04 seconds joins the living-room pause to the kitchen approach, omitting the fast turn that produced visible AI distortion. The complete native route remains available separately. Review covered 54 ordered half-second/endpoint samples, denser source-clip and join samples, and 16 consecutive frames surrounding the edit. Full decoding passed, and browser playback reached the kitchen endpoint without a media error. The [AI receipt](outputs/videos/ai-review.json) and [edit map](outputs/videos/ai-edit-map.json) record the evidence and source frames. Fine material, lighting and foliage details remain interpretive; this is not footage of an existing building. The independent measured kitchen review, image/plan review and video review remain separate evidence.

For substantial future changes follow [create-home](../../.agents/skills/create-home/SKILL.md), program/asset workflows and native-output review. Keep whole-home status unresolved until remaining issues have their own evidence.

## Source rebuild check

An isolated full build from `tools/timber02/build.py` reopened and passed the same 31 kitchen checks with zero geometry/planning failures and the same explicitly unresolved selected-refrigerator allowance. It retained 1,945 scene objects and the 2,400 sq ft gross enclosed area. This confirms the kitchen assembly is present in the reproducible authoring source; the isolated build did not overwrite the reviewed current model or its media.

## Independent photographic comparison

A separate reviewer inspected all six selected photographic studies against their exact native sources and verified all 12 source/selected hashes. No blocking architectural, equipment, storage or furniture drift was found. Stove, oven, hood, refrigerator, sink, island seats and pantry layout remain recognizable in their modeled positions. Minor tile gloss, wood grain, textile and foliage changes are photographic interpretation; exterior woodland, distant hillside and groundcover are illustrative context, not site evidence. The corrected living-room image retains a pale concrete/mineral floor.
