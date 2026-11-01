import os
import re
import tomllib
from pathlib import Path

output_dir = os.environ.get("INPUT_OUTPUT_DIR", "assets").rstrip("/")
readme_path = os.environ.get("INPUT_README_PATH", "README.md")

if not os.path.exists(readme_path):
    print(f"README not found at {readme_path}, skipping")
    exit(0)

_cards_toml = Path(__file__).parent / "cards.toml"
cards = tomllib.loads(_cards_toml.read_text())

raw = open(readme_path).read()

# Split into code-fenced blocks (```...```) and normal content
# We only process normal content, leave code blocks untouched
_FENCE = re.compile(r"(```.*?```)", re.DOTALL)
parts = _FENCE.split(raw)  # odd indices are code blocks


def find_breakpoints(base_dir: str, name: str) -> list[int]:
    breakpoints: list[int] = []
    if not os.path.isdir(base_dir):
        return breakpoints
    for f in os.listdir(base_dir):
        m = re.match(rf"^{re.escape(name)}-(\d+)px\.svg$", f)
        if m:
            breakpoints.append(int(m.group(1)))
    return sorted(breakpoints)


def picture_block(alt: str, base_dir: str, name: str) -> str:
    sources = ""
    for px in find_breakpoints(base_dir, name):
        sources += f'  <source media="(max-width: {px}px)" srcset="{base_dir}/{name}-{px}px.svg">\n'
    return (
        f'<p align="center">\n'
        f"<picture>\n"
        f"{sources}"
        f'  <img src="{base_dir}/{name}.svg" alt="{alt}">\n'
        f"</picture>\n"
        f"</p>"
    )


def process(text: str, name: str, alt: str, base_dir: str, main_svg: str, block: str) -> str:
    # 1. Replace existing <picture> block (idempotent update)
    text, n = re.subn(
        rf'<p align="center">\s*<picture>[^<]*(?:<source[^>]*>\s*)*<img[^>]*src="{re.escape(main_svg)}"[^>]*>\s*</picture>\s*</p>',
        block,
        text,
        flags=re.DOTALL,
    )
    if n:
        return text

    # 2. Replace markdown image: ![Stats](assets/stats/stats.svg)
    text = re.sub(
        rf"!\[{re.escape(alt)}\]\({re.escape(main_svg)}\)",
        block,
        text,
    )

    # 3. Replace bare <img src="assets/stats/stats.svg">
    text = re.sub(
        rf'<img[^>]*src="{re.escape(main_svg)}"[^>]*>',
        block,
        text,
    )
    return text


for name, cfg in cards.items():
    alt = cfg["alt"]
    base_dir = f"{output_dir}/{name}"
    main_svg = f"{base_dir}/{name}.svg"
    block = picture_block(alt, base_dir, name)
    # Process only non-code parts (even indices)
    for i in range(0, len(parts), 2):
        parts[i] = process(parts[i], name, alt, base_dir, main_svg, block)

content = "".join(parts)
open(readme_path, "w").write(content)
print(f"README updated: {readme_path}")
