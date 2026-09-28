# Run state

Last run: 2026-09-28 (run id 36407871218)
Tasks done this run: 1 (skip - commands already validated), 2 (identify opportunities - reviewed create_masks.py, scripts/merge_vector_files.py), 3 (implement improvement - fixed O(cells*features) redundant CRS transform + linear scan in create_masks.py cluster_labels via STRtree spatial index), 4 (checked - PR #4 still open/draft, clean/mergeable, no CI failures, no comments to address, no action needed), 7 (monthly summary)
Tasks skipped this run: 5 (searched for efficiency/performance/energy issues, none found besides own monthly summary), 6 (measurement infra - deferred again, 4th run in a row; strongly consider prioritising next run)

Backlog cursor: next run should investigate fine_tune.py, inference.py, project_setup.py for algorithmic inefficiencies (not yet reviewed in depth). Also strongly consider Task 6 (measurement infrastructure) since it's been deferred 4 runs running - no benchmark suite or perf regression CI exists.

Monthly activity issue: #2 "[efficiency-improver] Monthly Activity 2026-09" (label: efficiency) - existing issue for this month, updated in this run (not created new).

## Completed this run (2026-09-28, run 36407871218)
- Verified via `github list_pull_requests` that PR #4 (cache-rasterio-handles) is still open, draft, mergeable_state=clean, no CI checks configured (pending/0 statuses), no PR comments to address. No maintenance action needed.
- Reviewed create_masks.py (previously unreviewed, ~480 lines) and found `cluster_labels()` re-transforming every feature's geometry to dst_crs on EVERY grid-cell iteration (O(cells*features) redundant `fiona.transform.transform_geom` calls + linear scan), only triggered when `--labels.cluster_size_in_meters` is configured.
- Created draft PR (branch efficiency/spatial-index-cluster-labels): transform each feature geometry once up front + build a shapely STRtree spatial index for O(log n) per-cell candidate lookup instead of O(features) linear scan per cell.
- Measured ~228x speedup (173.20s -> 0.76s) on synthetic 2000-feature/401-cluster dataset (cluster_size=100m in EPSG:32633), via direct git-stash before/after comparison of the real `cluster_labels()` function imported from create_masks.py. Correctness verified: identical cluster count (401), total feature count (2143), and per-cluster size distribution.
- Ran `pytest tests/test_config.py -q` — 8 passed, no regressions.
- Reviewed scripts/merge_vector_files.py — thin ogr2ogr subprocess wrapper, already efficient (LOW priority, no Python-level optimization opportunity).
- Searched for efficiency/performance/energy issues via search_issues — none found (besides own monthly summary issue).
- Updated Monthly Activity issue #2 with new run history entry and refreshed backlog table.

## Completed previous run (2026-09-21, run 35582342578)
- Verified via `github list_pull_requests --state open` that no open efficiency-improver PRs exist (both prior PRs merged).
- Created draft PR (branch efficiency/cache-rasterio-handles): cached open rasterio file handles in bda/datasets.py TileDataset.__getitem__ instead of reopening per sample. ~5.4x measured speedup (11.29s -> 2.09s, 5,000 samples, 20 synthetic 1024x1024x4 tiles). Correctness verified via matching checksums.
- Updated Monthly Activity issue #2 with new run history entry and refreshed backlog table (marked TileDataset item DONE).
- Searched for efficiency/performance/energy issues via search_issues — none found (besides own monthly summary issue).

## Completed previous run (2026-09-14, run 34888275547)
- Verified PR #1 (merge-footprints-single-pass) was merged by maintainer via PR #1 merge commit on main.
- Created draft PR (branch efficiency/vectorize-random-geo-sampler, became PR #3, merged): vectorized bda/samplers.py RandomGeoSampler.__iter__ random draws, ~31x measured speedup on the sampling logic itself (0.4605s -> 0.0148s for one epoch, 32,768 samples).
- Updated Monthly Activity issue #2 with new run history entry and refreshed backlog table.
