# Shared asset publishing and verification

- Shared asset generation must be independent of a single home's layout. Reuse `common` geometry and material utilities; do not import a home's generator as the library API.
- `publish_shared.py` only creates missing immutable versions. Never delete an adopted asset to force this command to regenerate it. Publish a new version and explicitly migrate dependents.
- Before completing a new asset, run `verify_shared.py -- --render` in Blender and inspect the actual previews. It verifies native reopening, relative dependencies and measured dimensions; rendered appearance still requires human/agent visual inspection.
- `shared-validation.json` is the current verification receipt. Do not create a dated history of receipts or previews.
