"""The Cocktail Menu / Vesper: Phil in a tux, the Martini page's Bond scene, with a lemon peel for the garnish (Philip, Nov 24 2026).
Written by menu_pages.write_drink."""
from martini_scenes import bond


def write(folder):
    svg, css = bond('lemon-peel', 'Vesper')
    (folder / 'scenes' / 'bond.svg').write_text(svg + '\n')
    return '\n'.join(css) + '\n'
