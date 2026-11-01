import os
from datetime import date

from github_api import fetch_total_commits, fetch_total_stars, get_start_year
from themes import resolve_colors

username = os.environ["INPUT_USERNAME"]
start_date_in = os.environ.get("INPUT_START_DATE", "").strip()
output_dir = os.environ.get("INPUT_OUTPUT_DIR", "assets").rstrip("/")
out_file = f"{output_dir}/stats/stats.svg"
mobile_out_file = f"{output_dir}/stats/stats-640px.svg"
c = resolve_colors()
primary, bg, text, muted = c["primary"], c["bg"], c["text"], c["muted"]

account_start_year = get_start_year(username)
total_commits = fetch_total_commits(username, account_start_year)
total_stars = fetch_total_stars(username)
commits_fmt = f"{total_commits:,}"
stars_fmt = f"{total_stars:,}"

font = "'Courier New', Courier, monospace"

# Build stat blocks - conditionally include years experience
blocks = []

if start_date_in:
    today = date.today()
    start = date.fromisoformat(start_date_in)
    years = (today - start).days // 365
    blocks.append(("years experience", f"{years}+"))

blocks.append(("commits", commits_fmt))
blocks.append(("stars", stars_fmt))

count = len(blocks)
width = 820
col_w = width // count
svg_h = 120

items_svg = ""
for i, (label, value) in enumerate(blocks):
    cx = col_w * i + col_w // 2
    items_svg += f'''
  <text font-family="{font}" x="{cx}" y="38" text-anchor="middle" fill="{muted}" font-size="20">{label}</text>
  <text font-family="{font}" x="{cx}" y="96" text-anchor="middle" fill="{primary}" font-size="46" font-weight="bold">{value}</text>'''

dividers_svg = ""
for i in range(1, count):
    x = col_w * i
    dividers_svg += (
        f'\n  <line x1="{x}" y1="15" x2="{x}" y2="105" stroke="{c["divider"]}" stroke-width="1"/>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {svg_h}" width="640" height="{svg_h * 640 // width}">
  <rect width="{width}" height="{svg_h}" fill="{bg}"/>{dividers_svg}{items_svg}
</svg>'''

os.makedirs(f"{output_dir}/stats", exist_ok=True)
open(out_file, "w").write(svg)
print(f"written {out_file} ({count} stats)")


def _stats_mobile_svg(m_w, label_size, value_size, inner_gap, group_gap):
    pad = 20
    label_cap = int(label_size * 0.72)
    value_cap = int(value_size * 0.72)
    group_h = label_cap + inner_gap + value_cap
    m_h = pad + count * group_h + (count - 1) * group_gap + pad
    items = ""
    for i, (lbl, val) in enumerate(blocks):
        gy = pad + i * (group_h + group_gap)
        items += f'''
  <text font-family="{font}" x="{m_w // 2}" y="{gy + label_cap}" text-anchor="middle" fill="{muted}" font-size="{label_size}">{lbl}</text>
  <text font-family="{font}" x="{m_w // 2}" y="{gy + label_cap + inner_gap + value_cap}" text-anchor="middle" fill="{primary}" font-size="{value_size}" font-weight="bold">{val}</text>'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {m_w} {m_h}" width="{m_w}" height="{m_h}">\n  <rect width="{m_w}" height="{m_h}" fill="{bg}"/>{items}\n</svg>'


svg_640 = _stats_mobile_svg(m_w=420, label_size=16, value_size=40, inner_gap=12, group_gap=44)
svg_420 = _stats_mobile_svg(m_w=360, label_size=16, value_size=48, inner_gap=16, group_gap=50)

sm_out = f"{output_dir}/stats/stats-420px.svg"
open(mobile_out_file, "w").write(svg_640)
open(sm_out, "w").write(svg_420)
print(f"written {mobile_out_file}")
print(f"written {sm_out}")
