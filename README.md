# sample-python-app

This repository exists to **validate and demonstrate** the reusable Python security pipeline **end-to-end** (not to ship production features).

Minimal **Flask** app used as a **reference consumer** of [`workflow-python`](https://github.com/thadiust/workflow-python): it shows how a small Python repo wires **Gitleaks** (secrets), **Bandit** (SAST issues), and **pip-audit** (dependency vulnerabilities) through one reusable workflow.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) (Flask’s default port) or set `FLASK_APP=app` and use `flask run` if you prefer.

### Lint / format (Ruff)

CI runs **Ruff** first (see **`workflow-python`**). If **ruff-lint** fails, open the workflow run → failed **ruff-lint** job → **Summary** tab for short fix steps, or the **log** for the full **diff** and commands — you don’t need this README for that.

Optional — match CI before you push:

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
ruff format --force-exclude .
ruff check --fix --force-exclude .
ruff check --force-exclude . && ruff format --check --force-exclude .
```

The **`ruff`** line in **`requirements.txt`** is pinned to match [workflow-python’s default `ruff_version`](https://github.com/thadiust/workflow-python/blob/main/README.md); bump both when you upgrade.

### Editor / type checker (“could not be resolved”)

**`typings/flask/`** ships a **minimal `.pyi` stub** so **Pyright/Basedpyright** can resolve `import flask` even when your selected interpreter is **plain system Python** (no Flask installed). **`reportMissingModuleSource`** is turned off so you do not get a warning for “stub only, no package source.” When **`.venv`** exists and contains Flask, the **real** package is still used for analysis.

For **running** the app you still need **`pip install -r requirements.txt`** (usually inside **`.venv`**). **`pyrightconfig.json`** points Pyright at **`.venv`** when present. **Do not commit `.venv/`** — it stays gitignored.

**Monorepo (parent folder is the Cursor/VS Code workspace root):** Pyright treats the **workspace root** as the project root. It does **not** apply a subfolder’s `stubPath` the same way, so **`import flask`** can break if the only config is here and your root is something like **`security-pipeline`**. Fix one of these: (1) keep a **`pyrightconfig.json` at the monorepo root** (with `stubPath` pointing at `sample-python-app/typings` — that file is for local layout only if you do not commit the monorepo), or (2) **open `sample-python-app` as the folder** (or add it as a workspace folder) so this file is the effective project root. Reload or **Basedpyright: Restart** after changes.

## CI

Workflow runs on **pull requests** to `main`, **pushes** to `main`, and **workflow_dispatch**. The caller sets **`permissions: contents: read`**; **`workflow-python`** applies **`concurrency`** with **`cancel-in-progress`** on the reusable jobs so rapid pushes do not pile up runs.

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) calls **`thadiust/workflow-python/.github/workflows/ci.yml@main`** with:

- **Ruff** (lint + format check) first
- **Gitleaks** (full git history)
- **Bandit** and **pip-audit** in parallel after Gitleaks (and after Ruff, when Ruff is enabled)

**Expected behavior:** the workflow run **fails** if any **enabled** job reports a problem (**lint/format**, **secrets**, **Bandit issues**, or **dependency vulnerabilities**, per settings). It **passes** only when **all enabled jobs** succeed.

To change toggles, Python version, or Bandit severity, add or adjust `with:` inputs on that job; see the [workflow-python README](https://github.com/thadiust/workflow-python/blob/main/README.md).

**Note:** Gitleaks scans **history**, not only the latest commit. If you ever commit something that looks like a secret, deleting the file in a later commit may **not** clear CI until you [rewrite history or use a baseline](https://github.com/thadiust/secrets-gitleaks/blob/main/README.md#removed-the-file-but-ci-still-fails).

## Contents

| Path | Role |
|------|------|
| `app.py` | Tiny Flask app with a single `/` route |
| `requirements.txt` | Runtime deps + **ruff** (test-repo convenience; pin matches CI) |
| `pyrightconfig.json` | Pyright/Basedpyright: `.venv` when present + `reportMissingModuleSource` off |
| `typings/flask/__init__.pyi` | Minimal stub so `import flask` resolves without a venv (types only) |
