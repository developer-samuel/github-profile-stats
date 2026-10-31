import os, sys
from datetime import date
from github_api import get_start_year, fetch_total_commits, fetch_total_stars
from themes import resolve_colors

username      = os.environ["INPUT_USERNAME"]
start_date_in = os.environ.get("INPUT_START_DATE", "").strip()
out_file      = os.environ.get("INPUT_STATS_FILE", "assets/stats.svg")
c             = resolve_colors()
primary, bg, text, muted = c["primary"], c["bg"], c["text"], c["muted"]

account_start_year = get_start_year(username)
total_commits = fetch_total_commits(username, account_start_year)
total_stars   = fetch_total_stars(username)
commits_fmt   = f"{total_commits:,}"
stars_fmt     = f"{total_stars:,}"

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

count  = len(blocks)
width  = 820
col_w  = width // count
svg_h  = 80

items_svg = ""
for i, (label, value) in enumerate(blocks):
    cx = col_w * i + col_w // 2
    items_svg += f'''
  <text font-family="{font}" x="{cx}" y="22" text-anchor="middle" fill="{muted}" font-size="11">{label}</text>
  <text font-family="{font}" x="{cx}" y="52" text-anchor="middle" fill="{primary}" font-size="26" font-weight="bold">{value}</text>'''

dividers_svg = ""
for i in range(1, count):
    x = col_w * i
    dividers_svg += f'\n  <line x1="{x}" y1="10" x2="{x}" y2="70" stroke="{c["divider"]}" stroke-width="1"/>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {svg_h}" width="100%">
  <rect width="{width}" height="{svg_h}" fill="{bg}"/>{dividers_svg}{items_svg}
</svg>'''

os.makedirs(os.path.dirname(out_file) if os.path.dirname(out_file) else ".", exist_ok=True)
open(out_file, "w").write(svg)
print(f"stats.svg written to {out_file} ({count} stats)")
