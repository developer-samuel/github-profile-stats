# GitHub Profile Stats - task runner
# Requires: just (https://github.com/casey/just) + uv

# List available commands
default:
    just --list

# Install dev dependencies
sync:
    uv sync --group dev

# Lint with Ruff
lint:
    uv run ruff check src/

# Format source code
format:
    uv run ruff format src/

# Check formatting without writing changes
format-check:
    uv run ruff format --check src/

# Static type checking with Mypy
type-check:
    uv run mypy src/

# Dead code detection with Vulture
dead-code:
    uv run vulture src/

# Run all checks (same as CI)
check: lint format-check type-check dead-code

# Auto-fix lint issues + format
fix:
    uv run ruff check --fix src/
    uv run ruff format src/
