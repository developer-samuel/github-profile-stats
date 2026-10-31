import os
import tomllib
from pathlib import Path

with open(Path(__file__).parent / "themes.toml", "rb") as f:
    THEMES: dict[str, dict[str, str]] = tomllib.load(f)


def resolve_colors() -> dict[str, str]:
    theme_name = os.environ.get("INPUT_THEME", "dark").strip().lower()
    base = THEMES.get(theme_name, THEMES["dark"]).copy()

    overrides = {
        "primary": os.environ.get("INPUT_PRIMARY_COLOR", "").strip(),
        "bg": os.environ.get("INPUT_BG_COLOR", "").strip(),
        "text": os.environ.get("INPUT_TEXT_COLOR", "").strip(),
        "muted": os.environ.get("INPUT_MUTED_COLOR", "").strip(),
        "divider": os.environ.get("INPUT_DIVIDER_COLOR", "").strip(),
    }

    for key, val in overrides.items():
        if val:
            base[key] = val

    return base
