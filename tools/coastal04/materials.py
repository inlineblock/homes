"""Pinned driftwood, warm mineral and muted metal coastal finishes."""
import bpy
from common.finish_palette import textured, publish, palette as base_palette

def palette(root):
    materials = base_palette(root)
    for key, slug in [('plaster', 'warm-limestone-plaster'), ('exterior_plaster', 'mushroom-mineral-plaster'),
                      ('accent_oak', 'coastal-driftwood'), ('roof_metal', 'bronze-gray-standing-seam')]:
        path = root / 'library/materials' / slug / 'v001' / (slug + '.blend')
        with bpy.data.libraries.load(str(path), link=True) as (source, target):
            target.materials = [source.materials[0]]
        materials[key] = target.materials[0]
    return materials
