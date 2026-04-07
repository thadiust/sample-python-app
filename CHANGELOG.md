# Changelog

Notable changes to this **sample / reference app** are listed here (this repo does not ship library semver on a fixed schedule).

## [Unreleased]

## 2026-04-06 — pip-tools lockfile

- **`requirements.in`** and **pip-compile**-locked **`requirements.txt`** (same graph for **`pip install`**, **pytest**, and **pip-audit**).
- **`workflow-python`** **`@v1.0.7`**: **pip-tools** lock enforcement + shared **reusable-actionlint** (see [workflow-python **CHANGELOG**](https://github.com/thadiust/workflow-python/blob/main/CHANGELOG.md)).
- Explicit **`pytest_requirements_file`** matching the lock (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## 2026-04-06 — Code Scanning (SARIF)

- Caller **`permissions: security-events: write`**, **`upload_code_scanning: true`**, **`workflow-python`** **`@v1.0.4`+**.
