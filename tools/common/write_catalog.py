"""Write the compact root catalog; full galleries belong on home landing pages."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def home_entry(home):
    project = json.loads((home / 'project.json').read_text())
    gallery = json.loads((home / 'gallery.json').read_text())
    prefix = f'homes/{home.name}/'
    landing = prefix + 'README.md'
    photo = prefix + gallery['photographic_hero']['path']
    plan = gallery['plans'][0]  # Main/ground level first; all levels stay on the home page.
    plan_path = prefix + plan['path']
    level = plan['level'].replace('-', ' ')
    plan_label = level + (' plan' if 'floor' in level else ' floor plan')
    name = project['name']
    text = f'### {name}\n\n'
    text += '| AI photographic study | Floor plan |\n| --- | --- |\n'
    text += f'| [![{name} — AI photographic study]({photo})]({landing}) | '
    text += f'[![{name} — {plan_label}]({plan_path})]({landing}) |\n\n'
    text += f'[Full home: photo tour, all floor plans & 3D models]({landing})'
    pdf = Path(plan['path']).with_suffix('.pdf')
    if (home / pdf).is_file():
        text += f' · [Plan PDF]({prefix}{pdf.as_posix()})'
    return text + '\n\n'


def write_catalog(root=ROOT):
    readme = root / 'README.md'
    previous = readme.read_text() if readme.exists() else ''
    order = re.findall(r'^### (.+)$', previous, re.M)
    homes = [p.parent for p in (root / 'homes').glob('*/project.json')]
    names = {home: json.loads((home / 'project.json').read_text())['name'] for home in homes}
    homes.sort(key=lambda home: (order.index(names[home]) if names[home] in order else len(order), names[home]))
    text = '# Homes\n\nExplore the designs. Open a home for its full photographic tour, native 3D views, every floor plan and editable models.\n\n'
    text += 'Photos are AI architectural studies; plans and models are design concepts.\n\n'
    text += ''.join(home_entry(home) for home in homes)
    text += ('## Resources\n\n'
             '[Shared asset library](library/README.md) · [Design handbook](docs/design-guide/README.md) · '
             '[Create a home](.agents/skills/create-home/SKILL.md) · [Collaboration](docs/collaboration.md)\n\n'
             'Clone with Git LFS and run `git lfs pull` to retrieve full models and images. '
             'Keep the folder structure intact so linked assets resolve.\n\n'
             'Code: MIT. Original designs and assets: CC BY 4.0. [Licensing and attribution](LICENSE.md).\n')
    readme.write_text(text)
    print(f'CATALOG_WRITTEN {len(homes)} homes, two previews per home')


if __name__ == '__main__':
    write_catalog()
