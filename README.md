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

## CI

Workflow runs on **pull requests** to `main`, **pushes** to `main`, and **workflow_dispatch**. The caller sets **`permissions: contents: read`**; **`workflow-python`** applies **`concurrency`** with **`cancel-in-progress`** on the reusable jobs so rapid pushes do not pile up runs.

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) calls **`thadiust/workflow-python/.github/workflows/ci.yml@main`** with:

- **Gitleaks** (full git history)
- **Bandit** and **pip-audit** in parallel after Gitleaks

**Expected behavior:** the workflow run **fails** if any **enabled** scan reports a problem (**secrets**, **Bandit issues**, or **dependency vulnerabilities**, according to each job’s settings). It **passes** only when **all enabled jobs** succeed.

To change toggles, Python version, or Bandit severity, add or adjust `with:` inputs on that job; see the [workflow-python README](https://github.com/thadiust/workflow-python/blob/main/README.md).

**Note:** Gitleaks scans **history**, not only the latest commit. If you ever commit something that looks like a secret, deleting the file in a later commit may **not** clear CI until you [rewrite history or use a baseline](https://github.com/thadiust/secrets-gitleaks/blob/main/README.md#removed-the-file-but-ci-still-fails).

## Contents

| Path | Role |
|------|------|
| `app.py` | Tiny Flask app with a single `/` route |
| `requirements.txt` | Runtime dependencies (also what pip-audit reads) |
