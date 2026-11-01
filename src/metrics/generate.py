import os
import sys
from datetime import date, timedelta

from github_api import fetch_contributions, get_start_year
from themes import resolve_colors

username = os.environ["INPUT_USERNAME"]
output_dir = os.environ.get("INPUT_OUTPUT_DIR", "assets").rstrip("/")
out_file = f"{output_dir}/metrics/metrics.svg"
mobile_out_file = f"{output_dir}/metrics/metrics-640px.svg"
c = resolve_colors()
primary, bg, text, muted, divider = c["primary"], c["bg"], c["text"], c["muted"], c["divider"]

today = date.today()
start_year = get_start_year(username)
all_days = fetch_contributions(username, start_year)

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
active = [v for v in counts if v > 0]
highest_day = max(counts) if counts else 0
avg_per_day = round(sum(active) / len(active), 1) if active else 0.0

print(f"streak={current_streak}, best={best_streak}, highest={highest_day}, avg={avg_per_day}")

font = "'Courier New', Courier, monospace"

blocks = [
    ("current streak", str(current_streak), "days"),
    ("best streak", str(best_streak), "days"),
    ("highest / day", str(highest_day), "commits"),
    ("avg / day", str(avg_per_day), "commits"),
]

count = len(blocks)
width = 820
col_w = width // count
svg_h = 145

dividers_svg = ""
for i in range(1, count):
    x = col_w * i
    dividers_svg += (
        f'\n  <line x1="{x}" y1="15" x2="{x}" y2="132" stroke="{divider}" stroke-width="1"/>'
    )

items_svg = ""
for i, (label, value, unit) in enumerate(blocks):
    cx = col_w * i + col_w // 2
    items_svg += f'''
  <text font-family="{font}" x="{cx}" y="40" text-anchor="middle" fill="{muted}" font-size="19">{label}</text>
  <text font-family="{font}" x="{cx}" y="98" text-anchor="middle" fill="{primary}" font-size="46" font-weight="bold">{value}</text>
  <text font-family="{font}" x="{cx}" y="134" text-anchor="middle" fill="{text}" font-size="19">{unit}</text>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {svg_h}" width="640" height="{svg_h * 640 // width}">
  <rect width="{width}" height="{svg_h}" fill="{bg}"/>{dividers_svg}{items_svg}
</svg>'''

os.makedirs(f"{output_dir}/metrics", exist_ok=True)
open(out_file, "w").write(svg)
print(f"written {out_file}")


def _metrics_mobile_svg(m_w, label_size, value_size, unit_size, inner_gap, unit_gap, group_gap):
    pad = 20
    label_cap = int(label_size * 0.72)
    value_cap = int(value_size * 0.72)
    unit_cap = int(unit_size * 0.72)
    group_h = label_cap + inner_gap + value_cap + unit_gap + unit_cap
    m_h = pad + count * group_h + (count - 1) * group_gap + pad
    items = ""
    for i, (lbl, val, unit_lbl) in enumerate(blocks):
        gy = pad + i * (group_h + group_gap)
        ly = gy + label_cap
        vy = ly + inner_gap + value_cap
        uy = vy + unit_gap + unit_cap
        items += f'''
  <text font-family="{font}" x="{m_w // 2}" y="{ly}" text-anchor="middle" fill="{muted}" font-size="{label_size}">{lbl}</text>
  <text font-family="{font}" x="{m_w // 2}" y="{vy}" text-anchor="middle" fill="{primary}" font-size="{value_size}" font-weight="bold">{val}</text>
  <text font-family="{font}" x="{m_w // 2}" y="{uy}" text-anchor="middle" fill="{text}" font-size="{unit_size}">{unit_lbl}</text>'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {m_w} {m_h}" width="{m_w}" height="{m_h}">\n  <rect width="{m_w}" height="{m_h}" fill="{bg}"/>{items}\n</svg>'


svg_640 = _metrics_mobile_svg(
    m_w=420, label_size=16, value_size=40, unit_size=15, inner_gap=12, unit_gap=12, group_gap=44
)
svg_420 = _metrics_mobile_svg(
    m_w=360, label_size=16, value_size=48, unit_size=14, inner_gap=16, unit_gap=16, group_gap=50
)

sm_out = f"{output_dir}/metrics/metrics-420px.svg"
open(mobile_out_file, "w").write(svg_640)
open(sm_out, "w").write(svg_420)
print(f"written {mobile_out_file}")
print(f"written {sm_out}")
