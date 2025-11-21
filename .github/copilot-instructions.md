# Copilot / AI Agent Instructions for this repository

Purpose: Help AI coding agents become productive quickly in this repo by documenting the
project layout, important workflows, conventions, and integration points discovered in the code.

- **Quick context:** This project analyzes historical electric generation in the U.S.; docs and
  data definitions live under `data/` and `docs/`. The repository mixes Jupyter-style scripts
  (under `scripts/`) and a small Python package under `src/nombre_paquete`.

- **Quick start (recommended for agents before code edits):**
  - Create a Python 3.8+ virtualenv and install the package in editable mode:
    `python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -e .`
  - The `pyproject.toml` currently lists only `numpy`; many scripts import `pandas`,
    `seaborn`, `matplotlib`, `sqlalchemy`, and `kaggle` / `kagglehub`. If you add code
    that requires new packages, update `pyproject.toml` dependencies.

- **Project layout & important files to reference:**
  - `README.md` — high-level Spanish project description and goals.
  - `pyproject.toml` — packaging metadata; package name `nombre_paquete` and `src/` layout.
  - `scripts/` — pipeline-style folders: `data_acquisition/`, `eda/`, `preprocessing/`,
    `training/`, `evaluation/`. Each contains a `main.py` that acts as the entrypoint.
  - `src/nombre_paquete/` — library code (currently minimal).
  - `data/` and `docs/` — data dictionaries, summaries, and modeling reports.

- **Key patterns & conventions (codebase-specific):**
  - Scripts under `scripts/` are often exported from notebooks and retain cell magics
    (e.g., `%%time`, `%matplotlib inline`) and Kaggle-specific paths (`/kaggle/input`).
    Do not blindly remove or change magics — if converting a notebook to a runnable
    script, convert magics intentionally and verify environment assumptions.
  - Data acquisition code (example: `scripts/data_acquisition/main.py`) calls
    `kagglehub.dataset_download('catalystcooperative/pudl-project')` and expects a
    Kaggle/KaggleHub environment. External datasets (PUDL) are required to run
    end-to-end flows.
  - SQL interaction is performed via `sqlalchemy` — look for `sqlalchemy` imports
    and preserve connection semantics when refactoring.
  - Code comments and docs are in Spanish; preserve language/context when editing
    so domain reviewers can validate intent easily.

- **When making changes, follow these rules for agents:**
  - If adding runtime dependencies, update `pyproject.toml` dependencies.
  - When converting notebook-style scripts to pure Python entrypoints, remove
    cell magics and convert Kaggle-specific paths (`/kaggle/input`) to configurable
    paths (use environment variables or CLI args) and document the change.
  - Avoid changing data dictionaries or `data/` markdowns unless requested — they
    represent domain knowledge and must be preserved.
  - There are no tests or CI configs detected; run changed scripts locally where
    possible and report environment differences (Kaggle vs local) in PR descriptions.

- **Integration & external dependencies to note:**
  - Kaggle datasets (PUDL) via `kagglehub` — may require credentials or Docker image.
  - SQL databases accessed via `sqlalchemy` — preserve connection strings and secrets
    handling (do not hardcode credentials).

- **Quick examples to reference:**
  - Notebook-style Kaggle download: `scripts/data_acquisition/main.py` (uses `kagglehub`).
  - Packaging location: `pyproject.toml` and `src/nombre_paquete/`.

If anything in this summary is unclear or you want the instructions to emphasize other
areas (for example: adding a `requirements.txt`, adding CI, or converting notebooks to
scripts), tell me which areas to expand and I will iterate.
