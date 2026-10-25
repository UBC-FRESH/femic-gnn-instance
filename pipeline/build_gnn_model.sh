#!/usr/bin/env bash
# Build the GNN prototype from the stabilized TSA 46/47 checkpoints and bundles.
set -euo pipefail

INSTANCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$INSTANCE_ROOT"
BASE46="${BASE46:-../femic-tsa46-instance}"
BASE47="${BASE47:-../femic-tsa47-instance}"
AOI="${AOI:-data/source/aoi/gnn_full.gpkg}"
CHECKPOINT="${CHECKPOINT:-$BASE46/runtime/tsa46_full_vdyp_20261023/thlb_calibrated_checkpoint.feather}"
CHECKPOINT47="${CHECKPOINT47:-$BASE47/runtime/tsa47_full_vdyp_20261023/thlb_calibrated_checkpoint.feather}"
OUT="${OUT:-output/patchworks_gnn}"
MODEL_DIR="${MODEL_DIR:-runtime/gnn}"
TARGET_PER_DECADE="${TARGET_PER_DECADE:-2527000}"

python3 pipeline/build_gnn_checkpoint.py \
  --tsa46-checkpoint "$CHECKPOINT" \
  --tsa47-checkpoint "$CHECKPOINT47" \
  --aoi "$AOI" \
  --out data/gnn_combined_checkpoint.feather \
  --stats data/gnn_checkpoint_stats.json

python3 pipeline/build_gnn_bundle.py \
  --tsa46-bundle "$BASE46/data/model_input_bundle" \
  --tsa47-bundle "$BASE47/data/model_input_bundle" \
  --out data/model_input_bundle_gnn

python3 -m femic export patchworks \
  --tsa 46 --tsa 47 \
  --bundle-dir data/model_input_bundle_gnn \
  --checkpoint data/gnn_combined_checkpoint.feather \
  --ifm-source-col thlb_raw_calibrated \
  --ifm-mode proportional \
  --output-dir "$OUT"

mkdir -p "$MODEL_DIR/evidence" "$MODEL_DIR/schedules" "$MODEL_DIR/runs"
python3 pipeline/merge_slivers.py \
  --fragments "$OUT/fragments/fragments.shp" \
  --out "$OUT/fragments_merged/fragments.shp" \
  --cutoff-ha 1.0 --age-tolerance 20 \
  > "$MODEL_DIR/evidence/sliver_merge.json"

python3 -m ws4.cli build \
  --xml "$OUT/forestmodel.xml" \
  --fragments "$OUT/fragments_merged/fragments.shp" \
  --out "$MODEL_DIR/matrix"
python3 -m ws4.cli validate --dataset "$MODEL_DIR/matrix"

python3 pipeline/prepare_ws4_ui.py \
  --fragments "$OUT/fragments_merged/fragments.shp" \
  --out "$MODEL_DIR/fragments.geojson" --simplify-m 100
python3 pipeline/build_topology.py \
  --fragments "$MODEL_DIR/fragments.geojson" \
  --out "$MODEL_DIR/topology.csv" --distance-m 0
python3 pipeline/build_opening_targets.py \
  --base config/targets.gnn.yaml \
  --out config/targets.gnn_opening.yaml
python3 pipeline/build_opening_schedule.py \
  --dataset "$MODEL_DIR/matrix" \
  --topology "$MODEL_DIR/topology.csv" \
  --out "$MODEL_DIR/schedules/opening_first.csv" \
  --years 100 --min-area 5 --max-area 40 \
  --target-per-decade "$TARGET_PER_DECADE" --intermediate-share 0
python3 -m ws4.cli simulate \
  --dataset "$MODEL_DIR/matrix" \
  --schedule "$MODEL_DIR/schedules/opening_first.csv" \
  --out "$MODEL_DIR/runs/opening_first" \
  --years 100 --topology "$MODEL_DIR/topology.csv" \
  --patch-accounts config/patch_accounts.gnn.yaml --patch-membership
python3 -m ws4.cli report \
  --run "$MODEL_DIR/runs/opening_first" \
  --targets config/targets.gnn_opening.yaml

echo "GNN prototype built under $MODEL_DIR"
