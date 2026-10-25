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
| `build_opening_schedule.py` | Build the opening-first schedule |
| `filter_gnn_validation.py` | Filter ground plots to the GNN AOI |
| `inventory_gnn_plots.py` | Count public ground-plot sites inside the AOI |
| `extract_coast_log_prices.py` | Draft local extraction of BC coast species/grade prices |
| `analyze_gnn_aus.py` | AU area/THLB and curve comparison |

## Guardrails

- Do not tune curves or targets to the derived AAC.
- Keep TSA-prefixed AUs; do not merge model AUs by nominal stratum.
- Label the boundary, THLB, and AAC as proposed and derived.
- Do not commit large artifacts or raw data.
