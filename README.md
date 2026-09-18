# Homes

Editable homes, measured drawings, beautiful renders, and a shared asset library.

## Browse the projects

### Mountain House

A timber-clad home on a wooded downhill site: road-level garage and living, a walkout below, and a broad rear deck with a side return. Two levels total · 3 bedrooms · 2.5 baths · 3,528 sq ft conditioned gross.

[![Mountain House forest elevation](homes/mountain-house/outputs/images/01-forest-rear.png)](homes/mountain-house/outputs/README.md)

[All images and plans](homes/mountain-house/outputs/README.md) · [Project and editable models](homes/mountain-house/README.md)


### Coastal House

Bright modern coastal living with a 30-foot pocketing glass wall and a separate 12-foot kitchen serving window. Counters and cabinetry face both indoors and outdoors. A low pitched roof, two-car carport, generous foyer, bedroom storage and a full primary bathing suite complete the revision. 2,720 sq ft gross enclosed · 3 bedrooms · 2 baths.

[![Coastal House terrace](homes/coastal-house/outputs/images/01-terrace-open.png)](homes/coastal-house/outputs/README.md)

[![Coastal House front arrival and parking](homes/coastal-house/outputs/images/06-front-arrival.png)](homes/coastal-house/outputs/README.md)

[All images and plans](homes/coastal-house/outputs/README.md) · [Project and editable models](homes/coastal-house/README.md)

### Garage Loft 03

Two garage bays, four-car KLAUS-style pit parking, and a heated/cooled game room above. 36 x 34 ft footprint · 8 ft pool table · internal stair access and fixed-floor operator bay.

[![Garage Loft exterior](homes/garage-loft-03/outputs/images/01-exterior.png)](homes/garage-loft-03/outputs/README.md)

[All images and plans](homes/garage-loft-03/outputs/README.md) · [Concept book PDF](homes/garage-loft-03/outputs/plans/garage-loft.pdf) · [Project and editable models](homes/garage-loft-03/README.md)

### Timber Courtyard 02

Cedar wings, dark pitched roofs, a glazed gable, and a planted courtyard. Exterior-led concept; flexible interior. 2,400 sq ft gross enclosed · 3 bedrooms · 3 baths.

[![Timber Courtyard exterior](homes/timber-courtyard-02/outputs/images/01-exterior.png)](homes/timber-courtyard-02/outputs/README.md)

[All images and plans](homes/timber-courtyard-02/outputs/README.md) · [Project and editable models](homes/timber-courtyard-02/README.md)

### Atrium 01

Modern Eichler-inspired home with a walnut-and-sage kitchen and central atrium. 2,400 sq ft gross enclosed · 3 bedrooms · 3 baths.

[![Atrium kitchen](homes/atrium-01/outputs/images/01-kitchen.png)](homes/atrium-01/outputs/README.md)

[All images and plans](homes/atrium-01/outputs/README.md) · [Project and editable models](homes/atrium-01/README.md)

### Plan previews

[![Mountain House main floor](homes/mountain-house/outputs/plans/main-floor.png)](homes/mountain-house/outputs/plans/design-board.pdf)

[Mountain House main and walkout plans, sections and views](homes/mountain-house/outputs/plans/design-board.pdf)


[![Coastal House concept floor plan](homes/coastal-house/outputs/plans/floor-plan.png)](homes/coastal-house/outputs/plans/design-board.pdf)

[Coastal House design booklet](homes/coastal-house/outputs/plans/design-board.pdf)

| Timber Courtyard 02 | Atrium 01 |
| --- | --- |
| [![Timber Courtyard schematic floor plan](homes/timber-courtyard-02/outputs/plans/floor-plan.png)](homes/timber-courtyard-02/outputs/plans/design-board.pdf) | [![Atrium concept floor plan](homes/atrium-01/outputs/plans/floor-plan.png)](homes/atrium-01/outputs/plans/floor-plan.pdf) |
| [Exterior and plan PDF](homes/timber-courtyard-02/outputs/plans/design-board.pdf) | [Dimensioned concept plan PDF](homes/atrium-01/outputs/plans/floor-plan.pdf) |

These are editable architectural concepts and visualization models, not construction or permit documents.

## Organization

Each home lives in `homes/<home-name>/`. Shared materials and objects live in `library/`, independent of any one house. Project-specific experiments stay with their home until they are useful elsewhere.

```text
homes/<home-name>/
  project.json       Brief, dimensions, software, asset versions
  model/             Editable Blender and IFC building models
  outputs/
    README.md        Visual index of current results
    images/          Selected renders, one file per view
    plans/           PDFs, vector plans, and PNG previews
    work/            Ignored drafts and experiments
  exports/           Other interchange deliverables
  references/        Source notes and design references
  assets/            Assets unique to this home
library/
  materials/         Tile, wood, stone, plaster, fabric, metal
  components/        Window and door assemblies
  cabinetry/         Reusable cabinet and wardrobe modules
  hardware/          Cabinet pulls, knobs and door hardware
  furniture/         Chairs, sofas, tables, stools
  appliances/        Cooking, refrigeration and dishwashers
  fixtures/          Bath fixtures, fireplaces and lighting
  landscape/         Plants and trees
  surfaces/          Pavers and repeatable surface modules
  environments/      Lighting rigs, skies, backdrops
  assemblies/        Reusable combinations such as a kitchen island
templates/           Starting point for another home or asset
tools/               Reproducible model and drawing generation
docs/                Collaboration and asset conventions
```

Outputs use stable filenames and contain only the current reviewed results. Git keeps earlier revisions; do not create dated or versioned output folders. Shared library versions are independent asset dependencies. See [home guidance](homes/AGENTS.md).

## Get a complete copy

Install Git LFS before cloning. Models, textures, images, and selected exports are stored using Git LFS. A host with LFS support is needed when this repository is published.

```sh
git lfs install
git clone https://github.com/inlineblock/homes.git
cd homes
git lfs pull
```

Keep the folder structure intact: Blender links use relative paths. Open the home's `.blend` file for the furnished presentation model or its `.ifc` file in Bonsai for the architectural model. Software versions and the distinction between these deliverables are recorded in each project.

Repository: [inlineblock/homes](https://github.com/inlineblock/homes). Use Git LFS to retrieve the actual models and media.

## Design decisions and reusable assets

Start with the [home program checklist](docs/home-program-checklist.md), then use the [design and building handbook](docs/design-guide/README.md). The handbook covers feature tiers, kitchens and baths, climate/material choices, storage/access, enclosure, building systems, site/outdoor living and buildability. Each home records its actual selections and unresolved decisions in `program.md` and `design-review.md`.

The [visual asset catalog](library/README.md) includes materials, plants, paving, cabinetry, appliances, baths, lights and [15 hardware options](library/hardware/README.md). Choose an existing version, adapt it when necessary, and [contribute a reviewed reusable variation](docs/assets.md) without changing adopted versions underneath other homes.

| Shared integrated refrigeration | Shared cabinetry | Shared planting |
| --- | --- | --- |
| [![Cabinet-matched refrigerator](library/appliances/panel-ready-fridge-48in/v001/preview.png)](library/README.md) | [![Wardrobe bay](library/cabinetry/oak-wardrobe-2ft/v001/preview.png)](library/README.md) | [![Mountain conifer](library/landscape/mountain-conifer/v002/preview.png)](library/README.md) |

Repository-local skills capture the recurring workflows:

- [Home program and review](.agents/skills/home-program-review/SKILL.md)
- [Asset selection, adaptation and contribution](.agents/skills/home-asset-contribution/SKILL.md)
- [Model, IFC, render and plan QA](.agents/skills/home-model-output-qa/SKILL.md)

## Start another home

Copy `templates/home` to `homes/<new-name>`, fill its program, update `project.json` and README, select shared assets, then create the model and coordinated outputs. Use lowercase hyphenated names. See [collaboration](docs/collaboration.md) and [shared assets](docs/assets.md).

Code is licensed under MIT; original home designs, models, drawings, renders, and reusable assets are licensed under CC BY 4.0. See [licensing and attribution](LICENSE.md). Third-party reference images are excluded; third-party content retains its own terms.
