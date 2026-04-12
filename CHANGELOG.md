# Changelog

Notable changes to this **sample / reference app** are listed here (this repo does not ship library semver on a fixed schedule).

## [Unreleased]

- **README:** **CI** section matches **`workflow-python`** DAG (**Ruff ∥ Gitleaks** → **pytest** → scanners).
- **Dockerfile:** **DEMO ONLY** banner lines (copy-paste hazard) at top of file.
- **README:** **Dockerfile (demo only)** warning — root **`pip install`** before **`USER`**; not a production template.
- **PRs:** [`.github/workflows/pull-request.yml`](.github/workflows/pull-request.yml) uses **`python-pr-suite.yml@main`** with the **same `with:`** as push [**`ci.yml`**](.github/workflows/ci.yml) (explicit parity). **Push / dispatch:** [**`ci.yml`**](.github/workflows/ci.yml) → **`ci.yml@main`**. Removed standalone **`dependency-review.yml`**. **`workflow-python`** refs **`@main`** unless you pin **`@v…`**.

## 2026-04-09 — workflow-python v1.0.8

- Bumped **`workflow-python`** to **`@v1.0.8`** (**`ci.yml`**, **`reusable-actionlint`**, **`dependency-review`**): actionlint tarball **SHA256** verification, pinned **PyYAML**, reusable **dependency-review**, nested action pins (**Gitleaks** / **Bandit** / **pip-audit**).

## 2026-04-06 — pip-tools lockfile

- **`requirements.in`** and **pip-compile**-locked **`requirements.txt`** (same graph for **`pip install`**, **pytest**, and **pip-audit**).
- **`workflow-python`** **`@v1.0.7`**: **pip-tools** lock enforcement + shared **reusable-actionlint** (see [workflow-python **CHANGELOG**](https://github.com/thadiust/workflow-python/blob/main/CHANGELOG.md)).
- Explicit **`pytest_requirements_file`** matching the lock (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## 2026-04-06 — Code Scanning (SARIF)

- Caller **`permissions: security-events: write`**, **`upload_code_scanning: true`**, **`workflow-python`** **`@v1.0.4`+**.
