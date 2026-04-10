# Changelog

Notable changes to this **sample / reference app** are listed here (this repo does not ship library semver on a fixed schedule).

## [Unreleased]

- **`workflow-python`** callable workflows use **`@main`** (**`ci.yml`**, **`reusable-actionlint`**, **`dependency-review`**) for solo development — flip back to **`@vX.Y.Z`** before onboarding others or when you need pinned, reproducible CI.

## 2026-04-09 — workflow-python v1.0.8

- Bumped **`workflow-python`** to **`@v1.0.8`** (**`ci.yml`**, **`reusable-actionlint`**, **`dependency-review`**): actionlint tarball **SHA256** verification, pinned **PyYAML**, reusable **dependency-review**, nested action pins (**Gitleaks** / **Bandit** / **pip-audit**).

## 2026-04-06 — pip-tools lockfile

- **`requirements.in`** and **pip-compile**-locked **`requirements.txt`** (same graph for **`pip install`**, **pytest**, and **pip-audit**).
- **`workflow-python`** **`@v1.0.7`**: **pip-tools** lock enforcement + shared **reusable-actionlint** (see [workflow-python **CHANGELOG**](https://github.com/thadiust/workflow-python/blob/main/CHANGELOG.md)).
- Explicit **`pytest_requirements_file`** matching the lock (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## 2026-04-06 — Code Scanning (SARIF)

- Caller **`permissions: security-events: write`**, **`upload_code_scanning: true`**, **`workflow-python`** **`@v1.0.4`+**.
