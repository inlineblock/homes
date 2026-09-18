# Shared library

- Read `docs/assets.md`. Store assets under category/name/version, with an `asset.json` manifest.
- A published version is immutable once referenced by a home. Create the next version for changes; migrate homes explicitly.
- Every asset needs real-world scale, a clear origin, rights information, editable source or generator, and documented dependencies.
- Use local relative texture paths. Prefer reusable Blender collections or materials with meaningful names.
- Do not add fake previews or imply an original concept asset is an available commercial product.
- Before creating a reusable object, search the catalog. Prefer an existing asset; otherwise publish the missing component before filling the scene with local copies. Materials do not substitute for shared object geometry: plants, pavers, cabinet/wardrobe modules and repeated furnishings need reusable collections when repeated.
- Each new collection must specify dimensions, placement origin, front direction, allowed scaling/variation, pinned material dependencies and generator entry point. Verify it in a fresh Blender process, including relative dependency resolution. Plant origins belong at the ground-contact point.
- Link/instance published collections in adopting homes and list those versions in their manifests and asset-use schedules. A library file that no home uses is not evidence of reuse. Never modify an adopted version in place.
- Original shared assets use CC BY 4.0 with attribution to Homes project contributors; retain explicit third-party terms where applicable. See `LICENSE.md`.
