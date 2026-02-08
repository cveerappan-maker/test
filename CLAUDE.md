# CLAUDE.md

## Project Overview

This is a minimal Python project. It currently contains a single script (`hello_world.py`) that prints "Hello, World!" to standard output.

## Repository Structure

```
.
└── hello_world.py    # Main script entry point
```

## Language & Runtime

- **Language**: Python 3
- **No external dependencies** — uses only the Python standard library

## Running the Project

```bash
python hello_world.py
```

## Development Workflows

### Build

No build step is required. Python scripts are executed directly.

### Tests

No test framework is configured yet. When tests are added, prefer `pytest` as the test runner:

```bash
pytest
```

### Linting & Formatting

No linter or formatter is configured yet. When added, prefer:

- **Formatter**: `black` (or `ruff format`)
- **Linter**: `ruff` (or `flake8`)

### CI/CD

No CI/CD pipeline is configured.

## Conventions

- Keep scripts simple and readable.
- Use Python 3 syntax.
- Follow PEP 8 style guidelines.

## Git Workflow

- The default branch is `main`.
- Feature branches use the `claude/` prefix.
