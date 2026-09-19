# Shared asset publishing and verification

- Shared asset generation must be independent of a single home's layout. Reuse `common` geometry and material utilities; do not import a home's generator as the library API.
- `publish_shared.py` only creates missing immutable versions. Never delete an adopted asset to force this command to regenerate it. Publish a new version and explicitly migrate dependents.
- For collections registered in `common.shared_assets.CATALOG`, run `verify_shared.py -- --render` in Blender and inspect the actual previews. It verifies native reopening, relative dependencies and measured dimensions; rendered appearance still requires human/agent visual inspection.
- That verifier does not discover standalone materials or assets outside its catalog. For those assets, run their publisher's fresh-process link/reopen verifier and native preview command; check texture scale/material parameters and dependencies, then inspect actual host views. Do not claim an unrelated catalog pass verifies a new material.
- `shared-validation.json` is the catalog's current receipt; standalone publishers keep their scoped receipt beside the asset. Do not create a dated history of receipts or previews.
