# Materials

- Tile, stone, timber, plaster, fabric, and metal are materials; a multi-part cabinet belongs in components or assemblies.
- Record texture or tile scale in meters. A repeating tile must have physical width, height, depth, and grout intent.
- Name texture maps by role and document color space. Procedural materials should have reproducible parameters and a preview.
- For fluted geometry, inspect grazing light and seams. Preserve efficient instancing so a kitchen backsplash is inexpensive to render.
- Review the same candidate material in a neutral-lit native sample and in sunlit and shaded host views, both close enough to judge texture and far enough to judge the facade. Record lighting, exposure and color-management settings so comparisons remain meaningful. Correct unsuitable base color/albedo in the material; do not hide it with arbitrary scene exposure changes.
- For timber, verify physical grain scale in meters, grain direction along each board or beam, and texture repeat phase across adjacent pieces. Check vertical boards and horizontal members separately; local Z is not necessarily the grain axis. Inspect applied transforms and mapping on the actual host geometry.
- Vary timber grain offsets and tone deliberately to avoid identical repeated samples while preserving the intended wood palette. Judge bump and matte/gloss response under grazing light; do not compensate for incorrect scale or direction with stronger noise. These timber checks apply to wood materials, not every material category.
