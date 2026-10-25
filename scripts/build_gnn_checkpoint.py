#!/usr/bin/env python3
"""Clip the TSA 46/47 checkpoints to the GNN AOI and combine them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely import wkb


def _load_checkpoint(path: Path) -> gpd.GeoDataFrame:
    frame = pd.read_feather(path)
    if "geometry" not in frame.columns:
        raise ValueError(f"checkpoint has no geometry column: {path}")
    frame["geometry"] = frame["geometry"].map(
        lambda value: wkb.loads(bytes(value)) if isinstance(value, (bytes, bytearray)) else value
    )
    return gpd.GeoDataFrame(frame, geometry="geometry", crs="EPSG:3005")


def _clip_checkpoint(
    *, frame: gpd.GeoDataFrame, aoi: gpd.GeoGeometry, tsa_code: int
) -> gpd.GeoDataFrame:
    clipped = gpd.clip(frame, aoi, keep_geom_type=True)
    if clipped.empty:
        raise ValueError(f"no checkpoint rows within the GNN AOI for TSA {tsa_code}")
    clipped = clipped.copy()
    clipped["tsa_code"] = tsa_code
    clipped["FEATURE_AREA_SQM"] = clipped.geometry.area
    clipped["POLYGON_AREA"] = clipped.geometry.area / 10000.0
    raw = pd.to_numeric(clipped["thlb_raw"], errors="coerce").fillna(0.0)
    clipped["thlb_area"] = clipped.geometry.area / 10000.0 * raw / 100.0
    clipped["gnn_clipped_area_ha"] = clipped.geometry.area / 10000.0
    calibrated = pd.to_numeric(
        clipped["thlb_raw_calibrated"], errors="coerce"
    ).fillna(0.0)
    clipped["gnn_clipped_thlb_ha"] = clipped["gnn_clipped_area_ha"] * calibrated / 100.0
    clipped["geometry"] = clipped.geometry.map(lambda geom: geom.wkb)
    return clipped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tsa46-checkpoint", type=Path, required=True)
    parser.add_argument("--tsa47-checkpoint", type=Path, required=True)
    parser.add_argument("--aoi", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--stats", type=Path, required=True)
    args = parser.parse_args()

    aoi_frame = gpd.read_file(args.aoi).to_crs(3005)
    aoi = aoi_frame.geometry.union_all()
    frames = []
    stats: dict[str, object] = {"aoi": str(args.aoi), "tsa": {}}
    for tsa, path in ((46, args.tsa46_checkpoint), (47, args.tsa47_checkpoint)):
        source = _load_checkpoint(path)
        clipped = _clip_checkpoint(frame=source, aoi=aoi, tsa_code=tsa)
        area_ha = float(clipped["gnn_clipped_area_ha"].sum())
        thlb_ha = float(clipped["gnn_clipped_thlb_ha"].sum())
        stats["tsa"][str(tsa)] = {
            "source_rows": int(len(source)),
            "clipped_rows": int(len(clipped)),
            "clipped_area_ha": round(area_ha, 2),
            "clipped_calibrated_thlb_ha": round(thlb_ha, 2),
        }
        frames.append(clipped)
    combined = pd.concat(frames, ignore_index=True, sort=False)
    combined.to_feather(args.out)
    stats["combined_rows"] = int(len(combined))
    stats["combined_calibrated_thlb_ha"] = round(
        sum(float(stats["tsa"][str(t)]["clipped_calibrated_thlb_ha"]) for t in (46, 47)),
        2,
    )
    args.stats.parent.mkdir(parents=True, exist_ok=True)
    args.stats.write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
