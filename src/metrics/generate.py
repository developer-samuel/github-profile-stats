import os
import sys
from datetime import date, timedelta

from github_api import fetch_contributions, get_start_year
from svg import FONT, WIDTH, render_dividers, render_svg
from themes import resolve_colors


def compute_current_streak(all_days: dict[str, int], today: date) -> int:
    streak = 0
    check = today
    if all_days.get(check.isoformat(), 0) == 0:
        check -= timedelta(days=1)
    while all_days.get(check.isoformat(), 0) > 0:
        streak += 1
        check -= timedelta(days=1)
    return streak


def compute_best_streak(all_days: dict[str, int]) -> int:
    best, streak = 0, 0
    prev: date | None = None
    for d in sorted(all_days.keys()):
        dt = date.fromisoformat(d)
        if all_days[d] > 0:
            streak = streak + 1 if prev and (dt - prev).days == 1 else 1
            best = max(best, streak)
        else:
            streak = 0
        prev = dt
    return best


def compute_metrics(
    all_days: dict[str, int],
    today: date,
) -> tuple[int, int, int, float]:
    current_streak = compute_current_streak(all_days, today)
    best_streak = compute_best_streak(all_days)
    counts = list(all_days.values())
    active = [n for n in counts if n > 0]
    highest_day = max(counts) if counts else 0
    avg_per_day = round(sum(active) / len(active), 1) if active else 0.0
    return current_streak, best_streak, highest_day, avg_per_day


def render_metrics_svg(
    blocks: list[tuple[str, str, str]],
    colors: dict[str, str],
) -> str:
    count = len(blocks)
    col_w = WIDTH // count

    items = ""
    for i, (label, value, unit) in enumerate(blocks):
        cx = col_w * i + col_w // 2
        items += (
            f'\n  <text font-family="{FONT}" x="{cx}" y="22" text-anchor="middle" fill="{colors["muted"]}" font-size="11">{label}</text>'
            f'\n  <text font-family="{FONT}" x="{cx}" y="52" text-anchor="middle" fill="{colors["primary"]}" font-size="26" font-weight="bold">{value}</text>'
            f'\n  <text font-family="{FONT}" x="{cx}" y="68" text-anchor="middle" fill="{colors["text"]}" font-size="11">{unit}</text>'
        )

    return render_svg(colors["bg"], render_dividers(count, col_w, colors["divider"]) + items)


if __name__ == "__main__":
    username = os.environ["INPUT_USERNAME"]
    out_file = os.environ.get("INPUT_METRICS_FILE", "assets/metrics.svg")

    today = date.today()
    start_year = get_start_year(username)
    all_days = fetch_contributions(username, start_year)

    if not all_days:
        print("No data fetched", file=sys.stderr)
        sys.exit(1)

    current_streak, best_streak, highest_day, avg_per_day = compute_metrics(all_days, today)
    print(f"streak={current_streak}, best={best_streak}, highest={highest_day}, avg={avg_per_day}")

    blocks: list[tuple[str, str, str]] = [
        ("current streak", str(current_streak), "days"),
        ("best streak", str(best_streak), "days"),
        ("highest / day", str(highest_day), "commits"),
        ("avg / day", str(avg_per_day), "commits"),
    ]

    svg = render_metrics_svg(blocks, resolve_colors())

    os.makedirs(os.path.dirname(out_file) if os.path.dirname(out_file) else ".", exist_ok=True)
    with open(out_file, "w") as f:
        f.write(svg)
    print(f"metrics.svg written to {out_file}")
