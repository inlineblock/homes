# Homes

Editable homes, measured drawings, beautiful renders, and a shared asset library.

## Open the first home

[Atrium 01 — a modern Eichler-inspired home](homes/atrium-01/README.md)

Each home lives in `homes/<home-name>/`. Shared materials and objects live in `library/`, independent of any one house. Project-specific experiments stay with their home until they are useful elsewhere.

```text
homes/<home-name>/
  project.json       Brief, dimensions, software, asset versions
  model/             Editable Blender and IFC building models
  drawings/          Floor plans and dimensioned drawings
  renders/           Selected finished views
  exports/           Interchange and presentation deliverables
  references/        Source notes and design references
  assets/            Assets unique to this home
library/
  materials/         Tile, wood, stone, plaster, fabric, metal
  components/        Windows, doors, cabinetry, handles
  furniture/         Chairs, sofas, tables, stools
  fixtures/          Sinks, faucets, appliances, lighting
  landscape/         Plants, planters, paving
  environments/      Lighting rigs, skies, backdrops
  assemblies/        Reusable combinations such as a kitchen island
templates/           Starting point for another home or asset
tools/               Reproducible model and drawing generation
docs/                Collaboration and asset conventions
```

## Get a complete copy

Install Git LFS before cloning. Models, textures, images, and selected exports are stored using Git LFS. A host with LFS support is needed when this repository is published.

```sh
git lfs install
git clone <repository-url>
cd homes
git lfs pull
```

Keep the folder structure intact: Blender links use relative paths. Open the home's `.blend` file for the furnished presentation model or its `.ifc` file in Bonsai for the architectural model. Software versions and the distinction between these deliverables are recorded in each project.

No remote hosting destination is configured yet. This is a local repository; other people cannot clone it until it is pushed to a shared Git host.

## Start another home

Copy `templates/home` to `homes/<new-name>`, update `project.json` and its README, then add your models. Use lowercase hyphenated names. See [collaboration](docs/collaboration.md) and [shared assets](docs/assets.md).

No blanket redistribution license has been assigned to the designs. Third-party assets must retain their own licensing and attribution information.
