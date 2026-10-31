import os

THEMES = {
    "dark": {
        "primary": "#0969da",
        "bg": "#0d1117",
        "text": "#8b949e",
        "muted": "#484f58",
        "divider": "#21262d",
    },
    "light": {
        "primary": "#0969da",
        "bg": "#ffffff",
        "text": "#57606a",
        "muted": "#6e7781",
        "divider": "#d0d7de",
    },
}


def resolve_colors() -> dict[str, str]:
    """Returns colors merged from theme + any individual overrides."""
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
