FONT = "'Courier New', Courier, monospace"
WIDTH = 820
SVG_H = 80


def render_dividers(count: int, col_w: int, color: str) -> str:
    return "".join(
        f'\n  <line x1="{col_w * i}" y1="10" x2="{col_w * i}" y2="70" stroke="{color}" stroke-width="1"/>'
        for i in range(1, count)
    )


def render_svg(bg: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {SVG_H}" width="100%">\n'
        f'  <rect width="{WIDTH}" height="{SVG_H}" fill="{bg}"/>{body}\n'
        f"</svg>"
    )
