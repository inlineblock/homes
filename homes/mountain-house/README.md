# Mountain House

![Mountain House — Imagegen photographic study](outputs/images/photo-hero.png)

*Photorealistic AI study of the design. [Source and prompt](outputs/photo-study.md).*

A wood-clad hillside home with two levels total: road-level living and an integrated two-car garage above a downhill walkout level. A 14-foot-deep rear deck wraps around one side, with a partial timber pergola and a shaded patio below.

The timber finish uses neutral brown cedar and deeper thermo-ash, with physical-scale grain following each board and beam, individual grain/tone variation and a matte surface. These shared material revisions replace the earlier pale peach appearance without changing the house geometry or lighting.

**Rear overview — two levels facing the forest**

![Mountain House forest elevation](outputs/images/01-forest-rear.png)

[Current images and plans](outputs/README.md) · [Concept booklet](outputs/plans/design-board.pdf) · [Editable Blender model](model/mountain-house.blend) · [Classified IFC concept](model/mountain-house.ifc)

## Exterior gallery

### Front arrival and integrated garage

The front road meets the main living level. A separate pedestrian path leads to the sheltered entry beside the two-car garage.

![Road-level arrival and integrated two-car garage](outputs/images/02-road-arrival.png)

### The defining feature: a deck among the trees

The 14-foot-deep rear deck provides outdoor dining beneath a partial pergola, an open lounge and an eight-foot side return. The deck extends usable outdoor space over the slope.

![Rear deck, outdoor dining and timber pergola](outputs/images/03-deck-living.png)

### Walkout living and shaded patio

The lower lounge opens onto a locally graded patio beneath the deck. Timber posts and knee braces remain visible; the spaced deck above is not a waterproof roof.

![Walkout lounge and lower patio beneath the deck](outputs/images/04-walkout-patio.png)

### Side view and hillside relationship

This elevated side view shows the descending terrain, deck return, exposed lower level and timber supports together.

![Elevated side view showing deck, walkout and descending site](outputs/images/05-hillside-section.png)

## Interior gallery

### Living room and fireplace

Living room with closed-glass fireplace, stone hearth and forest-facing glazing. The insert is shown unlit; product selection and installation requirements remain unresolved.

![Living room with closed-glass fireplace, stone hearth and forest-facing glazing](outputs/images/09-living-fireplace.png)

### Kitchen facing the forest

The island cooktop and separate hood face the sink wall and broad glazing, with direct access to the deck.

![Kitchen island, extraction hood and forest-facing sink](outputs/images/06-kitchen.png)

### Kitchen equipment and storage

The reverse view shows the oven, drawer storage and wide cabinet-matched refrigerator.

![Kitchen oven and integrated refrigeration](outputs/images/08-kitchen-appliances.png)

### Primary vanity and soaking tub

This detail shows the double vanity and freestanding tub. The plan below locates the separate shower, enclosed toilet room and walk-in clothes storage.

![Primary bathroom vanity and soaking tub](outputs/images/07-primary-bath.png)

## Plans for both levels

### Main floor — road level

Living, dining, kitchen, primary suite and garage share the main level. [Open the full-size plan](outputs/plans/main-floor.png) or [vector drawing](outputs/plans/main-floor.svg) to inspect labels and dimensions.

![Dimensioned main-floor concept plan](outputs/plans/main-floor.png)

### Walkout floor — 11 feet below

Two bedrooms, a lounge, shared bath, laundry and service spaces occupy the exposed lower level. [Open the full-size plan](outputs/plans/walkout-floor.png) or [vector drawing](outputs/plans/walkout-floor.svg).

![Dimensioned walkout-floor concept plan](outputs/plans/walkout-floor.png)

### Site section

The diagram explains the road, main floor, lower walkout and deck relationship. It is an illustrative section, not a surveyed terrain or structural drawing.

![Concept section through the descending hillside](outputs/plans/hillside-section.png)

[Section vector drawing](outputs/plans/hillside-section.svg) · [Complete concept booklet](outputs/plans/design-board.pdf)

## Brief and program

The user requested two levels total, a built-in garage at the front road, a wooded downhill site, predominantly wood exterior, a walkout basement and a large deck to compensate for limited usable yard. The concept assumes three bedrooms and 2.5 baths; no actual parcel, survey or jurisdiction was supplied.

Main floor: open living/dining/kitchen facing the trees, primary suite with walk-in clothes storage, double vanity, separate shower/tub and enclosed toilet room, powder room, mudroom/coat storage, U stair and 24 x 24 ft integrated garage. Lower level: two bedrooms with dedicated wardrobes, shared bath, lounge opening to the patio, laundry/linen and mechanical/workshop allowance. Bedrooms are placed along the exposed rear, not the buried front.

## Area and dimensions

- Exterior main footprint: 60 x 40 ft. Main enclosed floor: 2,280 sq ft after excluding the 120 sq ft stair opening.
- Lower L-shaped footprint: 1,824 sq ft. No occupied lower room beneath the front garage.
- Total gross enclosed floor: 4,104 sq ft including walls and the 576 sq ft garage. Conditioned gross: 3,528 sq ft; this is not measured net living area.
- Rear deck: 60 x 14 ft; side return: 8 x 36 ft. Total deck: 1,128 sq ft, excluded from enclosed area.
- Main datum 0 ft; lower datum -11 ft. Lower patio -11.14 ft with a local grading bench; surrounding slope continues downhill.

The kitchen includes shared cooktop, oven, hood, dishwasher and 48-inch panel-ready refrigeration. A fireplace is selected for Mountain. [Program and explicit choices](program.md) records modeled provisions and unresolved product/engineering decisions.

## Files and reproducibility

Blender 4.5.14 LTS / Bonsai 0.8.5. Meters internally; feet/inches in drawings. Authoring modules are in `tools/mountain05/`; pinned assets are listed in `project.json` and [asset-use schedule](assets/README.md). Review scope is recorded in [design review](design-review.md).

The dedicated fireplace view has a [gallery camera review receipt](model/gallery-validation.json), recording the reopened native model, preserved existing scene and inspected final image. This camera-only addition leaves the home geometry, IFC and drawings unchanged.

From the repository root, run Blender with `--background --python-exit-code 1 --python tools/mountain05/build.py`. This replaces the generated native model; preserve manual edits first. Open the saved model and run `tools/mountain05/render.py` to create review drafts, with optional view slugs after `--`. Images are 3200 x 2000 with Cycles adaptive sampling and denoising; the final view receipt records 256 or 512 maximum samples by view. Inspect drafts before copying current selected images into `outputs/images/`. Run `tools/mountain05/draw_plans.py` with the documented PDF dependencies. Run the common IFC exporter from the saved scene and Bonsai verifier with `-- mountain-house`.

This is an editable architectural visualization and dimensioned concept, not construction documentation. A real project needs a survey, geotechnical/retaining design, structural and snow-load engineering, local egress/fire review, roof system/drainage design, energy and mechanical design, and site-specific approvals. Terrain, trees and road are original illustrations.
