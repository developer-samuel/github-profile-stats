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
just sync
```

## Tasks

| Command             | Description                      |
|---------------------|----------------------------------|
| `just sync`         | Install dev dependencies         |
| `just lint`         | Lint with Ruff                   |
| `just format`       | Format source code               |
| `just format-check` | Check formatting without writing |
| `just type-check`   | Static type checking with Mypy   |
| `just dead-code`    | Dead code detection with Vulture |
| `just check`        | Run all checks (same as CI)      |
| `just fix`          | Auto-fix lint issues + format    |
