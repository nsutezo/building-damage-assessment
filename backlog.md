# Optimisation backlog (updated 2026-09-14)

## Done
- [DONE 2026-09-14] merge_with_building_footprints.py: removed redundant second rasterio.mask.mask() pass over all building geometries (was computing "unknown" pct in a separate loop from the buffer=0 damage/built pct loop, calling mask() 4N times instead of 3N). ~19-25% wall-clock reduction measured on synthetic 200/1500-building datasets. PR branch: efficiency/merge-footprints-single-pass.

## Backlog (not yet started)
- MEDIUM: dpm_intersection.py has a similar tqdm loop over fiona features calling rasterio.mask.mask() once each (already single-pass, no obvious redundancy) — low priority, already efficient.
- MEDIUM: bda/footprints.py `record_batch_reader` — pyarrow streaming approach already avoids loading full dataset into memory (good practice, uses generator for non-empty batches). No action needed currently.
- LOW: environment.yml pins `torch<2.11` twice (duplicate line) - cosmetic, not energy-related, skip.
- TODO: Investigate create_masks.py, fine_tune.py, inference.py, project_setup.py for algorithmic inefficiencies (not yet reviewed in depth — large files, need explore pass next run).
- TODO: Investigate download_building_footprints.py and merge_vector_files.py in scripts/ for network/data efficiency (over-fetching, missing bbox filters) — not yet reviewed.
- TODO: Check bda/datasets.py, bda/datamodules.py, bda/samplers.py, bda/trainers.py for training-loop efficiency (data loading, augmentation, batching) — not yet reviewed, likely highest-impact area given GPU training is probably the most energy-intensive workload in this repo.

## Measurement strategy notes
- For raster/vector processing scripts (merge_with_building_footprints.py, dpm_intersection.py): benchmark with synthetic rasterio GeoTIFF (random classified array) + synthetic fiona/shapely footprints, time via `/usr/bin/time -f "elapsed=%e s"`, verify correctness via property-dict equality across fiona features between old/new outputs.
- Full deps (rasterio, shapely, fiona, numpy, tqdm, pyyaml, pytest) can be pip-installed into a venv without needing the full conda/torch/geopandas/gdal stack for scripts that don't import those.
