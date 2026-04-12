# sample-python-app

This repository exists to **validate and demonstrate** the reusable Python security pipeline **end-to-end** (not to ship production features).

Minimal **Flask** app used as a **reference consumer** of [`workflow-python`](https://github.com/thadiust/workflow-python): it exercises **composite actions → reusable workflow → app repo** by running **`pre-commit-check` ∥ `gitleaks-scan`** (prechecks: hooks include **Gitleaks**, **Black**, **Ruff**, etc.; job scans **full history**), then **pytest**, **Bandit**, **pip-audit**, and optional **Docker**/**Trivy** through one callable workflow.

## Dockerfile (demo only — copy-paste hazard)

The **[`Dockerfile`](Dockerfile)** is for **trying optional `docker-build` / Trivy image** flows in CI, **not** a production hardening template. It runs **`pip install`** as **root** before switching **`USER`** — fine for a sample; **do not** treat it as an org default without **multi-stage** builds, non-root install, and your own base-image policy.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # lockfile: regenerate from requirements.in when you change deps (see below)
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) (Flask’s default port) or set `FLASK_APP=app` and use `flask run` if you prefer.

### Lint / format (pre-commit)

CI runs **`pre-commit run --all-files`** first (**`pre-commit-check`** job; see **[`.pre-commit-config.yaml`](.pre-commit-config.yaml)**). Install hooks locally, then run the same command before every push:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

If **pre-commit-check** fails, open the workflow log for the failing hook. You can still run **Ruff** directly when debugging:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ruff format --force-exclude .
ruff check --fix --force-exclude .
ruff check --force-exclude . && ruff format --check --force-exclude .
```

**zsh:** Don’t put **`# comments` on the same line** as `ruff`/`python` commands when pasting — if `interactivecomments` is off, the shell can pass `#`, `apply`, etc. as extra arguments and Ruff will look for files with those names. Use comments on their own line or run commands one at a time.

The **`ruff`** line in **`requirements.txt`** is for local **`ruff`** CLI use; keep it aligned with the **`astral-sh/ruff-pre-commit`** **`rev:`** in **[`.pre-commit-config.yaml`](.pre-commit-config.yaml)** when you upgrade Ruff.

### Editor / type checker (“could not be resolved”)

**`typings/flask/`** ships a **minimal `.pyi` stub** so **Pyright/Basedpyright** can resolve `import flask` even when your selected interpreter is **plain system Python** (no Flask installed). **`reportMissingModuleSource`** is turned off so you do not get a warning for “stub only, no package source.” When **`.venv`** exists and contains Flask, the **real** package is still used for analysis.

For **running** the app you still need **`pip install -r requirements.txt`** (usually inside **`.venv`**). **`pyrightconfig.json`** points Pyright at **`.venv`** when present. **Do not commit `.venv/`** — it stays gitignored.

**Monorepo (parent folder is the Cursor/VS Code workspace root):** Pyright treats the **workspace root** as the project root. It does **not** apply a subfolder’s `stubPath` the same way, so **`import flask`** can break if the only config is here and your root is something like **`security-pipeline`**. Fix one of these: (1) keep a **`pyrightconfig.json` at the monorepo root** (with `stubPath` pointing at `sample-python-app/typings` — that file is for local layout only if you do not commit the monorepo), or (2) **open `sample-python-app` as the folder** (or add it as a workspace folder) so this file is the effective project root. Reload or **Basedpyright: Restart** after changes.

## CI

- **Pull requests:** [`.github/workflows/pull-request.yml`](.github/workflows/pull-request.yml) calls **`python-pr-suite.yml@main`** with the **same explicit `with:`** as push [**`ci.yml`**](.github/workflows/ci.yml) (PR/push **parity** on tool versions, lockfile, scanners, Docker, SARIF, image gate).
- **Push to `main` / `workflow_dispatch`:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml) calls **`ci.yml@main`** directly (no Dependency Review on push — same **`with:`** as before for lockfile, scanners, Docker, and image gate).

**Permissions:** PR workflow sets **`contents: read`**, **`pull-requests: read`**, **`security-events: write`**. Push workflow sets **`security-events: write`** for SARIF. **`workflow-python`** applies **`concurrency`** on reusable runs where configured.

**Lockfile:** **`enforce_pip_tools_lockfile: true`** so **`requirements.txt`** matches **`pip-compile`** from **`requirements.in`**. **`pytest_requirements_file`** matches **`requirements_file`** via **`ci.yml`** defaults.

**Authoritative DAG** (matches **`workflow-python`** `ci.yml`): **pre-commit-check ∥ gitleaks-scan** (parallel prechecks) → **pytest** → **Trivy repo ∥ Bandit ∥ pip-audit** (parallel trio). The **Gitleaks** hook runs inside **pre-commit**; the **Gitleaks** job scans **history** on a separate runner **in parallel** with pre-commit when both are enabled.

**Expected behavior:** the workflow run **fails** if any **enabled** job reports a problem (**lint/format**, **secrets**, **tests**, **Trivy**, **Bandit**, **pip-audit**, per settings). It **passes** only when **all enabled jobs** succeed.

To change toggles, Python version, or Bandit severity, add or adjust `with:` inputs on that job; see the [workflow-python README](https://github.com/thadiust/workflow-python/blob/main/README.md).

**Bandit:** The pipeline scans **the whole tree** by default, **including `tests/`**, so risky patterns in test code are visible too. **B101** on pytest **`assert`** lines is expected — add **`# nosec B101`** on those lines, or set **`bandit_exclude: tests`** in the workflow `with:` if you want Bandit to skip test directories. For anything else, read the job log (issue code, file, link) and fix or tune via **`bandit.yaml`** / **`bandit_minimum_severity`**.

**Note:** Gitleaks scans **history**, not only the latest commit. If you ever commit something that looks like a secret, deleting the file in a later commit may **not** clear CI until you [rewrite history or use a baseline](https://github.com/thadiust/secrets-gitleaks/blob/main/README.md#removed-the-file-but-ci-still-fails).

## Dependencies (`requirements.in` → `requirements.txt`)

**`requirements.in`** lists **direct** dependencies (you may use compatible ranges). **`requirements.txt`** is the **pip-compile lock** (fully pinned, including transitives). **pip-audit** scans that lock so SCA matches what **`pip install -r requirements.txt`** resolves.

Regenerate the lock after editing **`.in`** (use the same Python major/minor as CI, **3.11**, for fewer surprises):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install 'pip-tools>=7.4,<8'
pip-compile requirements.in -o requirements.txt --strip-extras
```

Commit **both** files. If you change **`.in`** but not the lock, CI fails on **`enforce_pip_tools_lockfile`**.

## Contents

| Path | Role |
|------|------|
| `app.py` | Tiny Flask app with a single `/` route |
| `requirements.in` | Direct deps (input to **pip-compile**) |
| `requirements.txt` | Pinned lock (**pytest**, **pip-audit**, local **`pip install`**) |
| `tests/test_app.py` | Minimal pytest for `/` |
| `pyrightconfig.json` | Pyright/Basedpyright: `.venv` when present + `reportMissingModuleSource` off |
| `typings/flask/__init__.pyi` | Minimal stub so `import flask` resolves without a venv (types only) |
