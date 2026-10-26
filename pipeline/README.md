# Pipeline entry points

This directory holds the GNN model build and analysis entry points. They are
runnable data-pipeline code, not the workflow tooling in `scripts/`.

The strict workflow gates (ruff, mypy, docstring checks, and the 95 percent
coverage gate) apply to `scripts/` and `tests/`. The pipeline is validated by
execution, `ws4 validate`, and the evidence recorded in `notes/reference/`.

## Build

```bash
pipeline/build_gnn_model.sh
```

The script expects the base instances at `../femic-tsa46-instance` and
`../femic-tsa47-instance`. It writes gitignored artifacts under `data/`,
`output/`, and `runtime/`.

## Entry points

| Script | Purpose |
| --- | --- |
| `build_gnn_model.sh` | Full build, schedule, simulation, and report sequence |
| `build_gnn_checkpoint.py` | Clip and combine the TSA 46/47 checkpoints |
| `build_gnn_bundle.py` | Combine the TSA 46/47 FEMIC bundles |
| `merge_slivers.py` | Merge safe slivers before the ws4 build |
| `prepare_ws4_ui.py` | Write the UI geometry |
| `prepare_land_base.py` | Write the land-base geometry |
| `build_topology.py` | Build the touching-block topology |
| `build_opening_targets.py` | Expand the derived benchmark targets |
| `build_opening_schedule.py` | Build the opening-first schedule; optional `--allowed-blocks` candidate pool |
| `filter_gnn_validation.py` | Filter ground plots to the GNN AOI |
| `inventory_gnn_plots.py` | Count public ground-plot sites inside the AOI |
| `extract_coast_log_prices.py` | Draft local extraction of BC coast species/grade prices |
| `analyze_gnn_aus.py` | AU area/THLB and curve comparison |
| `plot_gnn_aoi_map.py` | Render the AOI map with a pale OpenStreetMap basemap |
| `plot_gnn_au_figures.py` | Generate SI violin panels and AU curve plots |
| `screen_block_revenue.py` | Map the checkpoint revenue screen to blocks; direct-cost partial gate |
| `select_positive_blocks.py` | Write the direct-positive block candidate list from the block screen |
| `plot_block_revenue_map.py` | Map positive/negative blocks, removed blocks, and the replacement schedule |
| `screen_shared_cost_headroom.py` | Test shared-cost headroom for the positive-block candidate |
| `build_access_exposure.py` | Public road/stream/coast exposure for the candidate blocks |
| `screen_block_exclusion.py` | Filter negative-revenue blocks out of a candidate schedule for a diagnostic sensitivity |
| `build_gnn_lidar_products.py` | Optional: 10 m GNN strategic LiDAR bundle from LidarBC DEM/DSM |
| `integrate_gnn_lidar.py` | Optional: register/map/integrate LiDAR fields into the GNN dataset |
| `build_gnn_public_indicators.py` | Optional: model-wide Terrarium/VRI descriptive fields and LiDAR validation |

## Optional terrain and canopy indicators

These are not part of `build_gnn_model.sh` and do not change model semantics.
They require the FEMIC LiDAR producer and the WS4 consumer plus the multi-track
block fix.

```bash
python -m femic lidar materialize \
  --selection-manifest metadata/lidar/lidarbc_selection_dem_dsm.json \
  --output-root data/lidar

python pipeline/build_gnn_lidar_products.py \
  --aoi data/source/aoi/gnn_full.gpkg \
  --materialization data/lidar/materialization.json \
  --output-dir data/lidar/gnn_10m \
  --bundle-dir data/lidar/products/lidarbc-gnn-10m

python pipeline/integrate_gnn_lidar.py \
  --dataset runtime/gnn/matrix \
  --bundle data/lidar/products/lidarbc-gnn-10m \
  --fragments output/patchworks_gnn/fragments_merged/fragments.shp

python pipeline/build_gnn_public_indicators.py \
  --dataset runtime/gnn/matrix \
  --cache-dir runtime/gnn/public_terrain/terrarium_z12 \
  --output-dir runtime/gnn/public_terrain
```

The 549-tile LidarBC materialization is about **5.5 GiB**. `data/lidar/` and
`runtime/` are gitignored; the selection manifests under `metadata/lidar/` are
tracked. The LiDAR fields cover **181 direct fragments / 184 blocks** only. The
Terrarium/VRI fields are **descriptive proxies**; they are not operability
thresholds, CHM, or a model-wide LiDAR layer. See `docs/indicators.rst`.

## Guardrails

- Do not tune curves or targets to the derived AAC.
- Keep TSA-prefixed AUs; do not merge model AUs by nominal stratum.
- Label the boundary, THLB, and AAC as proposed and derived.
- Do not commit large artifacts or raw data.
- Do not treat the public terrain/VRI fields as operability thresholds or CHM;
  they are descriptive only.
- Do not present the 181-fragment / 184-block LiDAR pilot as GNN-wide.
