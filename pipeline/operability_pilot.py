#!/usr/bin/env python3
"""Pilot: classify a small block sample into ground/cable/heli and screen costs.

This is not a representative GNN sample and not a net revenue run. It exercises
the terrain, stand, and FHOPS cable/heli paths on real blocks.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely import contains_xy, wkb

from sample_block_terrain import _mosaic, _slope_percent


def _load_checkpoint(path: Path) -> gpd.GeoDataFrame:
    frame = pd.read_feather(path)
    frame["geometry"] = frame["geometry"].map(
        lambda value: wkb.loads(bytes(value)) if isinstance(value, (bytes, bytearray)) else value
    )
    return gpd.GeoDataFrame(frame, geometry="geometry", crs="EPSG:3005")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--zoom", type=int, default=12)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    fhops_src = os.environ.get("FHOPS_SRC")
    if fhops_src:
        sys.path.insert(0, fhops_src)
    from fhops.costing.machine_rates import get_machine_rate
    from fhops.productivity.cable_logging import (
        HelicopterLonglineModel,
        estimate_cable_yarder_productivity_tr125_single_span,
        estimate_helicopter_longline_productivity,
    )

    blocks = gpd.read_file(args.blocks).set_crs(3005, allow_override=True)
    blocks["block_id"] = blocks["block_id"].astype(int)
    blocks["area_ha"] = blocks.area / 10000.0
    blocks = blocks[(blocks.area_ha >= 10) & (blocks.area_ha <= 40)].copy()
    checkpoint = _load_checkpoint(args.checkpoint)

    points = gpd.GeoDataFrame(blocks[["block_id", "area_ha"]], geometry=blocks.centroid, crs=3005)
    approx = gpd.sjoin(
        points,
        checkpoint[["LIVE_STAND_VOLUME_125", "geometry"]],
        predicate="within",
        how="inner",
    ).drop_duplicates("block_id")
    approx["volume_per_ha"] = pd.to_numeric(
        approx["LIVE_STAND_VOLUME_125"], errors="coerce"
    )
    candidates = approx[
        approx["volume_per_ha"].between(250, 750, inclusive="both")
    ].drop_duplicates("block_id")
    if len(candidates) < args.count:
        raise SystemExit(f"only {len(candidates)} candidates for count={args.count}")
    sample = candidates.sample(n=args.count, random_state=args.seed)

    cable_prod = estimate_cable_yarder_productivity_tr125_single_span(
        slope_distance_m=300.0, lateral_distance_m=25.0, payload_m3=1.6
    )
    cable_rates = {
        "cable_skyleadc40": get_machine_rate("grapple_yarder_skyleadc40"),
        "cable_cypress7280": get_machine_rate("grapple_yarder_cypress7280"),
    }
    heli_rates = {
        "heli_kmax": get_machine_rate("helicopter_kmax"),
        "heli_bell214b": get_machine_rate("helicopter_bell214b"),
    }
    heli_prod = {
        "heli_kmax": estimate_helicopter_longline_productivity(
            model=HelicopterLonglineModel.KMAX, flight_distance_m=1000.0
        ).productivity_m3_per_pmh0,
        "heli_bell214b": estimate_helicopter_longline_productivity(
            model=HelicopterLonglineModel.BELL_214B, flight_distance_m=1000.0
        ).productivity_m3_per_pmh0,
    }

    to_wgs = Transformer.from_crs(3005, 4326, always_xy=True)
    to_albers = Transformer.from_crs(4326, 3005, always_xy=True)
    cache: dict[tuple[int, int, int], np.ndarray] = {}
    records: list[dict[str, object]] = []
    for row in sample.itertuples(index=False):
        block_id = int(row.block_id)
        block = blocks.loc[blocks.block_id == block_id].geometry.union_all()
        area_ha = block.area / 10000.0
        sub = checkpoint[checkpoint.intersects(block)].copy()
        sub["clip_geom"] = sub.geometry.intersection(block)
        sub = sub[~sub.clip_geom.is_empty].copy()
        sub["clip_ha"] = sub.clip_geom.area / 10000.0
        volume = float(
            (
                pd.to_numeric(sub["LIVE_STAND_VOLUME_125"], errors="coerce").fillna(0)
                * sub["clip_ha"]
            ).sum()
        )
        stems = float(
            (
                pd.to_numeric(sub["VRI_LIVE_STEMS_PER_HA"], errors="coerce").fillna(0)
                * sub["clip_ha"]
            ).sum()
        )
        min_x, min_y, max_x, max_y = block.bounds
        corners = [to_wgs.transform(min_x, min_y), to_wgs.transform(max_x, max_y)]
        lons = [point[0] for point in corners]
        lats = [point[1] for point in corners]
        bbox = (min(lons), min(lats), max(lons), max(lats))
        elevation, x0, y0, _, _ = _mosaic(bbox, args.zoom, cache)
        slope = _slope_percent(elevation, zoom=args.zoom, origin_x=x0, origin_y=y0)
        height, width = elevation.shape
        col, row_idx = np.meshgrid(np.arange(width), np.arange(height))
        count = 2**args.zoom
        lon = (x0 + (col + 0.5) / 256.0) / count * 360.0 - 180.0
        lat = np.degrees(
            np.arctan(np.sinh(np.pi * (1.0 - 2.0 * (y0 + (row_idx + 0.5) / 256.0) / count)))
        )
        xs, ys = to_albers.transform(lon, lat)
        mask = contains_xy(block, xs, ys) & np.isfinite(slope)
        if not mask.any():
            continue
        slope_mean = float(np.nanmean(slope[mask]))
        slope_p90 = float(np.nanpercentile(slope[mask], 90))
        if slope_mean < 35 and slope_p90 < 45:
            operability = "ground"
        elif slope_mean < 50 and slope_p90 < 65:
            operability = "cable"
        else:
            operability = "heli_candidate"
        record: dict[str, object] = {
            "block_id": block_id,
            "area_ha": round(area_ha, 2),
            "volume_m3": round(volume, 1),
            "volume_per_ha": round(volume / area_ha, 1) if area_ha else None,
            "stems_per_ha": round(stems / area_ha, 1) if area_ha else None,
            "avg_stem_size_m3": round(volume / stems, 3) if stems else None,
            "slope_mean_pct": round(slope_mean, 2),
            "slope_p90_pct": round(slope_p90, 2),
            "elevation_mean_m": round(float(np.nanmean(elevation[mask])), 1),
            "operability": operability,
            "terrain_status": "coarse_dem_pilot",
        }
        species_groups = {
            "hembal": {"H", "BA", "HM"},
            "cedar": {"CW"},
            "cypress": {"YC"},
            "fir": {"FD"},
            "spruce": {"S", "SX", "SE"},
        }
        total_area = float(sub["clip_ha"].sum()) or 1.0
        shares: dict[str, float] = {}
        for group, codes in species_groups.items():
            share = 0.0
            for index in (1, 2, 3):
                species = sub[f"SPECIES_CD_{index}"].astype(str).str.upper()
                pct = pd.to_numeric(sub[f"SPECIES_PCT_{index}"], errors="coerce").fillna(0)
                share += float((pct / 100.0 * sub["clip_ha"] * species.isin(codes)).sum())
            shares[group] = round(100.0 * share / total_area, 1)
        record.update({f"{group}_share_pct": value for group, value in shares.items()})
        record["dominant_species_group"] = max(shares, key=shares.get)
        for name, rate in cable_rates.items():
            record[f"{name}_cad_per_m3"] = (
                round(rate.total_cost_per_smh / (rate.default_utilization * cable_prod), 2)
                if rate
                else None
            )
        for name, rate in heli_rates.items():
            record[f"{name}_cad_per_m3"] = (
                round(rate.total_cost_per_smh / (rate.default_utilization * heli_prod[name]), 2)
                if rate
                else None
            )
        records.append(record)

    frame = pd.DataFrame.from_records(records)
    for column in [
        column for column in frame.columns if column.endswith("_cad_per_m3")
    ]:
        frame[column.replace("_cad_per_m3", "_total_cad")] = (
            frame[column] * frame["volume_m3"]
        ).round(0)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    print(frame.to_string(index=False))
    if not frame.empty:
        print("\nvolume share by operability:")
        print(
            (frame.groupby("operability")["volume_m3"].sum() / frame.volume_m3.sum() * 100)
            .round(1)
            .to_string()
        )


if __name__ == "__main__":
    main()
