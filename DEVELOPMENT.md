# Development

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package manager
- [just](https://github.com/casey/just) - task runner
- Python 3.12+

### Install on Linux / WSL

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

Add `~/.local/bin` to PATH if not already there:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

## Setup

```bash
just setup
```

## Repository secrets

The following secrets must be configured in **Settings → Secrets and variables → Actions**:

| Secret        | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `PAT_TOKEN`   | Classic PAT with `repo` scope - used by release.yml to push CHANGELOG.md to main |

## Dependency updates

Dependencies are managed by [Renovate](https://github.com/apps/renovate). It runs every Monday before 6:00 AM and opens PRs for outdated GitHub Actions, Python dev dependencies and the Semgrep Docker image. Major updates require manual review.

To activate Renovate for this repository go to [github.com/apps/renovate](https://github.com/apps/renovate).

## Tasks

| Command             | Description                      |
|---------------------|----------------------------------|
| `just sync`         | Install dev dependencies         |
| `just setup`        | First-time setup (deps + hooks)  |
| `just lint`         | Lint with Ruff                   |
| `just format`       | Format source code               |
| `just format-check` | Check formatting without writing |
| `just type-check`   | Static type checking with Mypy   |
| `just dead-code`    | Dead code detection with Vulture |
| `just yaml-check`   | Lint YAML files                  |
| `just check`        | Run all checks (same as CI)      |
| `just fix`          | Auto-fix lint issues + format    |
