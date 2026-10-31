import os
from datetime import date

from github_api import fetch_total_commits, fetch_total_stars, get_start_year
from svg import FONT, WIDTH, render_dividers, render_svg
from themes import resolve_colors


def build_stat_blocks(
    start_date: str,
    commits: int,
    stars: int,
) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    if start_date:
        today = date.today()
        start = date.fromisoformat(start_date)
        years = (today - start).days // 365
        blocks.append(("years experience", f"{years}+"))
    blocks.append(("commits", f"{commits:,}"))
    blocks.append(("stars", f"{stars:,}"))
    return blocks


def render_stats_svg(blocks: list[tuple[str, str]], colors: dict[str, str]) -> str:
    count = len(blocks)
    col_w = WIDTH // count

    items = ""
    for i, (label, value) in enumerate(blocks):
        cx = col_w * i + col_w // 2
        items += (
            f'\n  <text font-family="{FONT}" x="{cx}" y="22" text-anchor="middle" fill="{colors["muted"]}" font-size="11">{label}</text>'
            f'\n  <text font-family="{FONT}" x="{cx}" y="52" text-anchor="middle" fill="{colors["primary"]}" font-size="26" font-weight="bold">{value}</text>'
        )

    return render_svg(colors["bg"], render_dividers(count, col_w, colors["divider"]) + items)


if __name__ == "__main__":
    username = os.environ["INPUT_USERNAME"]
    start_date_in = os.environ.get("INPUT_START_DATE", "").strip()
    out_file = os.environ.get("INPUT_STATS_FILE", "assets/stats.svg")

    account_start_year = get_start_year(username)
    total_commits = fetch_total_commits(username, account_start_year)
    total_stars = fetch_total_stars(username)

    blocks = build_stat_blocks(start_date_in, total_commits, total_stars)
    svg = render_stats_svg(blocks, resolve_colors())

    os.makedirs(os.path.dirname(out_file) if os.path.dirname(out_file) else ".", exist_ok=True)
    with open(out_file, "w") as f:
        f.write(svg)
    print(f"stats.svg written to {out_file} ({len(blocks)} stats)")
