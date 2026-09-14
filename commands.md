# Validated commands

- Python: system python3 is 3.12.3, externally-managed (PEP 668). Use a venv: `python3 -m venv /tmp/venv && /tmp/venv/bin/pip install <pkgs>`.
- Tests: `tests/test_config.py` runs standalone with only `pytest` + `pyyaml` installed (does NOT require torch/geopandas/rasterio). Run: `python -m pytest tests/test_config.py -q` (8 tests pass).
- Other tests (test_trainers.py, test_download_building_footprints.sh) require heavy deps (torch, torchgeo, geopandas, gdal) via `environment.yml` (conda) — not validated yet in this sandbox (conda not available; would need full conda env or pip equivalents of gdal/geopandas/torchgeo).
- No lint/format config found in repo (no .flake8, pyproject.toml, pre-commit config) as of 2026-09-14.
- No CI workflow beyond the efficiency-improver workflow itself found in .github/workflows/.
- Network access to pypi.org confirmed available in sandbox.
- Core geo deps (rasterio, shapely, fiona, numpy, tqdm) install fine via pip into a venv for benchmarking scripts like merge_with_building_footprints.py and dpm_intersection.py.
