# GitHub Stats Generator

Generates SVG stats and metrics cards for your GitHub profile README.

---

## Setup

### 1. Create a Personal Access Token

Go to **GitHub → Settings → Developer Settings → Personal access tokens → Tokens (classic)** and create a token with:

- `public_repo`
- `read:user`

### 2. Add the token as a repository secret

In your profile repository go to **Settings → Secrets and variables → Actions** and add:

| Name          | Value                  |
|---------------|------------------------|
| `STATS_TOKEN` | your token from step 1 |

### 3. Add the workflow

Create `.github/workflows/stats.yml` in your profile repository:

```yaml
name: Update Stats

on:
  schedule:
    - cron: '0 2 * * *'  # Every day at 02:00 UTC
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v7

      - uses: developer-samuel/github-stats-generator@v1  # https://github.com/developer-samuel/github-stats-generator/releases
        with:
          token: ${{ secrets.STATS_TOKEN }}
          username: your-username
          start_date: '2020-01-01'  # Optional: YYYY-MM-DD, your local time zone
          stats_file: assets/stats.svg
          metrics_file: assets/metrics.svg

      - name: Commit changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add assets/
          git diff --staged --quiet || git commit -m "chore: update stats"
          git push
```

### 4. Add the cards to your README

```markdown
![Stats](assets/stats.svg)
![Metrics](assets/metrics.svg)
```

---

## Inputs

| Input           | Required | Default | Description                                                         |
|-----------------|----------|---------|---------------------------------------------------------------------|
| `token`         | ✅       | -       | PAT with `public_repo` + `read:user`                                |
| `username`      | ✅       | -       | Your GitHub username                                                |
| `stats_file`    | -        | -       | Output path for stats SVG (omit to skip)                            |
| `metrics_file`  | -        | -       | Output path for metrics SVG (omit to skip)                          |
| `start_date`    | -        | -       | Programming start date `YYYY-MM-DD` - shows *years experience* stat |
| `theme`         | -        | `dark`  | `dark` or `light`                                                   |
| `primary_color` | -        | -       | Accent color (hex) - overrides theme                                |
| `bg_color`      | -        | -       | Background color (hex) - overrides theme                            |
| `text_color`    | -        | -       | Secondary text color (hex) - overrides theme                        |
| `muted_color`   | -        | -       | Label color (hex) - overrides theme                                 |
| `divider_color` | -        | -       | Divider line color (hex) - overrides theme                          |

> At least one of `stats_file` or `metrics_file` must be set.

---

## Themes

### Dark (default)

| Key       | Color     |
|-----------|-----------|
| `primary` | `#0969da` |
| `bg`      | `#0d1117` |
| `text`    | `#8b949e` |
| `muted`   | `#484f58` |
| `divider` | `#21262d` |

### Light

| Key       | Color     |
|-----------|-----------|
| `primary` | `#0969da` |
| `bg`      | `#ffffff` |
| `text`    | `#57606a` |
| `muted`   | `#6e7781` |
| `divider` | `#d0d7de` |

Individual color inputs override the theme - you can mix and match. For example to use the dark theme with a custom accent color:

```yaml
theme: dark
primary_color: '#f78166'
```

---

## Related

- [DEVELOPMENT.md](DEVELOPMENT.md) - local dev setup, tooling and task runner
