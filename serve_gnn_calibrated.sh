#!/usr/bin/env bash
# Serve the GNN prototype on loopback.
set -euo pipefail

INSTANCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8019}"
MODEL_DIR="${MODEL_DIR:-$INSTANCE_ROOT/runtime/gnn}"
DATASET="${DATASET:-$MODEL_DIR/matrix}"
RUNS="${RUNS:-$MODEL_DIR/runs}"
GEOMETRY="${GEOMETRY:-$MODEL_DIR/fragments_full.geojson}"
GEOMETRY_OVERVIEW="${GEOMETRY_OVERVIEW:-$MODEL_DIR/fragments.geojson}"
LAND_BASE="${LAND_BASE:-$MODEL_DIR/land_base.geojson}"
TARGETS="${TARGETS:-$INSTANCE_ROOT/config/targets.gnn_opening.yaml}"
TILE_CACHE="${TILE_CACHE:-$MODEL_DIR/tile-cache}"

cd "$INSTANCE_ROOT"
exec python3 -m ws4.cli serve \
  --dataset "$DATASET" \
  --runs "$RUNS" \
  --geometry "$GEOMETRY" \
  --geometry-overview "$GEOMETRY_OVERVIEW" \
  --land-base "$LAND_BASE" \
  --targets "$TARGETS" \
  --tile-cache "$TILE_CACHE" \
  --crs EPSG:3005 \
  --allow-runs \
  --allow-agent \
  --agent-cwd "$INSTANCE_ROOT" \
  --host 127.0.0.1 \
  --port "$PORT"
