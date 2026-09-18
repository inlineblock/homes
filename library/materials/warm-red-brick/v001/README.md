# Warm red clay brick

![Neutral native sample](preview.png)

Original fired-clay appearance with red, rust and brown variation, fine grain, and light warm-gray mortar. The running-bond pitch is 225 × 75 mm: 215 × 65 mm clay face plus 10 mm joints. The shader has 4 mm bump relief; the optional individual module includes beveled geometry and mortar recessed 4 mm.

Link `warm-red-brick.blend`, material **Warm red brick | running bond | meters**. The optional geometry collection is **Warm red brick | 225 x 75 mm module**, at floor/bottom center with front −Y. Its footprint is 225 × 102.5 × 75 mm. Keep module scale 1 and stagger alternate courses 112.5 mm.

## Required facade mapping

With `tools` on the Python import path:

```python
from library.build_lindon_assets import link_assets, apply_brick_uv
assets = link_assets(ROOT)
wall.data.materials.append(assets['brick'])
# Call after final world transforms, on each local facade mesh.
apply_brick_uv(wall)
```

The shader requires the named **Brick meters** UV layer. The helper derives a horizontal tangent for each face, so angled wings retain physical brick scale. Reapply after changing mesh geometry, scale or rotation. Do not use normalized Generated coordinates. Corner UV seams are intentional; actual corner bond/quoins remain a host detailing decision.

![Same material on a 45-degree wall](preview-45-degrees.png)

Fresh-process checks include meter mapping on a wall rotated 45° and scaled nonuniformly; edge-length error is below 0.000001 m. Both actual native previews were inspected. Preview lighting: Cycles CPU, 48 samples, AgX Medium High Contrast, exposure 0, neutral world strength 0.45 and large area lights. Sunny/shaded host review remains the adopting home's responsibility.

Original by Homes project contributors, CC BY 4.0. Generator `tools/library/build_lindon_assets.py` uses MIT. No external textures or proprietary photo content. This is appearance geometry, not a structural masonry assembly or weather approval.
