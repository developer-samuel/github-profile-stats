import os, sys
from datetime import date, timedelta
from github_api import get_start_year, fetch_contributions
from themes import resolve_colors

username = os.environ["INPUT_USERNAME"]
out_file = os.environ.get("INPUT_METRICS_FILE", "assets/metrics.svg")
c        = resolve_colors()
primary, bg, text, muted, divider = c["primary"], c["bg"], c["text"], c["muted"], c["divider"]

today      = date.today()
start_year = get_start_year(username)
all_days   = fetch_contributions(username, start_year)

if not all_days:
    print("No data fetched", file=sys.stderr)
    sys.exit(1)

sorted_dates = sorted(all_days.keys())

# Current streak
current_streak = 0
check = today
if all_days.get(check.isoformat(), 0) == 0:
    check -= timedelta(days=1)
while all_days.get(check.isoformat(), 0) > 0:
    current_streak += 1
    check -= timedelta(days=1)

# Best streak
best_streak, streak = 0, 0
prev = None
for d in sorted_dates:
    dt = date.fromisoformat(d)
    if all_days[d] > 0:
        streak = streak + 1 if prev and (dt - prev).days == 1 else 1
        best_streak = max(best_streak, streak)
    else:
        streak = 0
    prev = dt

# Highest day + avg per active day
counts = list(all_days.values())
active = [c for c in counts if c > 0]
highest_day = max(counts) if counts else 0
avg_per_day = round(sum(active) / len(active), 1) if active else 0

print(f"streak={current_streak}, best={best_streak}, highest={highest_day}, avg={avg_per_day}")

font = "'Courier New', Courier, monospace"

blocks = [
    ("current streak", str(current_streak), "days"),
    ("best streak",    str(best_streak),    "days"),
    ("highest / day",  str(highest_day),    "commits"),
    ("avg / day",      str(avg_per_day),    "commits"),
]

count = len(blocks)
width = 820
col_w = width // count
svg_h = 80

dividers_svg = ""
for i in range(1, count):
    x = col_w * i
    dividers_svg += f'\n  <line x1="{x}" y1="10" x2="{x}" y2="70" stroke="{divider}" stroke-width="1"/>'

items_svg = ""
for i, (label, value, unit) in enumerate(blocks):
    cx = col_w * i + col_w // 2
    items_svg += f'''
  <text font-family="{font}" x="{cx}" y="22" text-anchor="middle" fill="{muted}" font-size="11">{label}</text>
  <text font-family="{font}" x="{cx}" y="52" text-anchor="middle" fill="{primary}" font-size="26" font-weight="bold">{value}</text>
  <text font-family="{font}" x="{cx}" y="68" text-anchor="middle" fill="{text}" font-size="11">{unit}</text>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {svg_h}" width="100%">
  <rect width="{width}" height="{svg_h}" fill="{bg}"/>{dividers_svg}{items_svg}
</svg>'''

os.makedirs(os.path.dirname(out_file) if os.path.dirname(out_file) else ".", exist_ok=True)
open(out_file, "w").write(svg)
print(f"metrics.svg written to {out_file}")
