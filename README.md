# mrb-shell-usage-check

Standalone shell usage checker for Python repositories.

## Usage

Run against the current repository:

```bash
mrb-shell-usage-check .
```

Run on specific files, as pre-commit would:

```bash
mrb-shell-usage-check path/to/file.py another.py
```

## Pre-commit

```yaml
repos:
  - repo: https://github.com/mrbeam/mrb-shell-usage-check
    rev: v0.1.0
    hooks:
      - id: mrb-shell-usage-check
```

## GitHub Actions

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
- run: pip install git+https://github.com/mrbeam/mrb-shell-usage-check@v0.1.0
- run: mrb-shell-usage-check .
```
