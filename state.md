# Run state

Last run: 2026-09-21 (run id 35582342578)
Tasks done this run: 1 (skip - commands already validated), 2 (identify opportunities - confirmed TileDataset.__getitem__ file-open overhead from backlog cursor), 3 (implement improvement - cached rasterio handles in TileDataset), 7 (monthly summary)
Tasks skipped this run: 4 (checked - no open efficiency-improver PRs found to maintain; both prior PRs already merged), 5 (searched for efficiency/performance/energy/green-software issues, none found besides own monthly summary), 6 (measurement infra - deferred again, 3rd run in a row; consider prioritising next run)

Backlog cursor: next run should investigate create_masks.py, fine_tune.py, inference.py, project_setup.py for algorithmic inefficiencies (not yet reviewed in depth), then scripts/merge_vector_files.py for network/data efficiency. Also consider Task 6 (measurement infrastructure) since it's been deferred 3 runs running.

Monthly activity issue: #2 "[efficiency-improver] Monthly Activity 2026-09" (label: efficiency) - existing issue for this month, updated in this run (not created new).

## Completed this run (2026-09-21, run 35582342578)
- Verified via `github list_pull_requests --state open` that no open efficiency-improver PRs exist (both prior PRs merged).
- Created draft PR (branch efficiency/cache-rasterio-handles): cached open rasterio file handles in bda/datasets.py TileDataset.__getitem__ instead of reopening per sample. ~5.4x measured speedup (11.29s -> 2.09s, 5,000 samples, 20 synthetic 1024x1024x4 tiles). Correctness verified via matching checksums.
- Updated Monthly Activity issue #2 with new run history entry and refreshed backlog table (marked TileDataset item DONE).
- Searched for efficiency/performance/energy issues via search_issues — none found (besides own monthly summary issue).

## Completed previous run (2026-09-14, run 34888275547)
- Verified PR #1 (merge-footprints-single-pass) was merged by maintainer via PR #1 merge commit on main.
- Created draft PR (branch efficiency/vectorize-random-geo-sampler, became PR #3, merged): vectorized bda/samplers.py RandomGeoSampler.__iter__ random draws, ~31x measured speedup on the sampling logic itself (0.4605s -> 0.0148s for one epoch, 32,768 samples).
- Updated Monthly Activity issue #2 with new run history entry and refreshed backlog table.
