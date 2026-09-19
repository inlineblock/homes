"""Pinned coastal finishes with a warm mineral shell and smoked-oak accents."""
import bpy
from common.finish_palette import textured, publish, palette as base_palette

def palette(root):
    materials = base_palette(root)
    for key, slug in [('plaster', 'warm-limestone-plaster'), ('accent_oak', 'smoked-oak')]:
        path = root / 'library/materials' / slug / 'v001' / (slug + '.blend')
        with bpy.data.libraries.load(str(path), link=True) as (source, target):
            target.materials = [source.materials[0]]
        materials[key] = target.materials[0]
    return materials
