# Optimisation backlog (updated 2026-09-21, run 35582342578)

## Done
- [DONE 2026-09-14, PR #1 MERGED] merge_with_building_footprints.py: removed redundant second rasterio.mask.mask() pass over all building geometries (was computing "unknown" pct in a separate loop from the buffer=0 damage/built pct loop, calling mask() 4N times instead of 3N). ~19-25% wall-clock reduction measured on synthetic 200/1500-building datasets.
- [DONE 2026-09-14, PR #3 MERGED] bda/samplers.py RandomGeoSampler.__iter__: vectorized 3 per-sample RNG calls (np.random.choice with p= weights + 2x np.random.randint, each in a Python loop run length=train_batches_per_epoch*batch_size times/epoch, default 32,768) into a handful of batched numpy calls. ~31x wall-clock reduction measured (0.4605s -> 0.0148s for one epoch's worth of sampling, 50 synthetic tiles). Correctness verified (valid i/y/x ranges).
- [DONE 2026-09-21, run 35582342578, draft PR created] bda/datasets.py TileDataset.__getitem__: added per-instance `_handle_cache` dict caching open rasterio dataset handles keyed by filename, instead of `with rasterio.open(fn) as f` reopening on every sample read. ~5.4x wall-clock reduction measured (11.29s -> 2.09s for 5,000 random 256x256 window reads across 20 synthetic 1024x1024x4 tiles). Correctness verified via matching checksums between baseline and cached implementations. Branch: efficiency/cache-rasterio-handles. Safe with DataLoader num_workers>0 since each worker gets its own Dataset copy/cache; handles closed in __del__.

## Backlog (not yet started)
- MEDIUM: dpm_intersection.py has a similar tqdm loop over fiona features calling rasterio.mask.mask() once each (already single-pass, no obvious redundancy) — low priority, already efficient.
- MEDIUM: bda/footprints.py `record_batch_reader` — pyarrow streaming approach already avoids loading full dataset into memory (good practice, uses generator for non-empty batches). No action needed currently.
- LOW: environment.yml pins `torch<2.11` twice (duplicate line) - cosmetic, not energy-related, skip.
- [REVIEWED 2026-09-14, no action] download_building_footprints.py: already uses server-side bbox filter (Overture only supports bbox server-side) + column projection (`footprints[["id","geometry","subtype","class"]]`) before clipping to exact AOI shape. Already efficient, no over-fetching found.
- TODO: Investigate create_masks.py, fine_tune.py, inference.py, project_setup.py for algorithmic inefficiencies (not yet reviewed in depth — large files, need explore pass next run).
- TODO: Investigate scripts/merge_vector_files.py for network/data efficiency — not yet reviewed.
- TODO: bda/datasets.py TileDataset.__init__ sanity_check loop opens 2 rasterio files per tile pair sequentially at startup — one-time cost, likely low priority (startup-only, not per-epoch).
- TODO: Task 6 (measurement infrastructure) still deferred every run so far — consider prioritising next run: no benchmark suite, no CI perf regression tracking exists in this repo.

## Measurement strategy notes
- For raster/vector processing scripts (merge_with_building_footprints.py, dpm_intersection.py): benchmark with synthetic rasterio GeoTIFF (random classified array) + synthetic fiona/shapely footprints, time via `/usr/bin/time -f "elapsed=%e s"`, verify correctness via property-dict equality across fiona features between old/new outputs.
- Full deps (rasterio, shapely, fiona, numpy, tqdm, pyyaml, pytest) can be pip-installed into a venv without needing the full conda/torch/geopandas/gdal stack for scripts that don't import those.
