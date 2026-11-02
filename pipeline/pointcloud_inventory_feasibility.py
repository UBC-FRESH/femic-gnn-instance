#!/usr/bin/env python3
"""Audit GNN-area FAIB plots and LidarBC point-cloud coverage.

The audit reads a public FAIB plot header, an optional FAIB visit table, and a
LidarBC selection manifest. It reports plot composition, recent-plot counts,
point-cloud tile coverage inside the AOI, plot-to-tile overlap, and nearest-plot
distances. It does not download tiles, fit a model, or change the GNN dataset.

A no-go decision is a valid result. The report, not this script, owns the final
scientific decision; the script supplies the counts and distances behind it.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box

DEFAULT_RECENT_SINCE = 2018


def parse_args() -> argparse.Namespace:
    """Return command-line options.

    Returns
    -------
    argparse.Namespace
        Parsed options.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aoi", type=Path, required=True)
    parser.add_argument("--plots", type=Path, required=True)
    parser.add_argument("--visits", type=Path)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--recent-since", type=int, default=DEFAULT_RECENT_SINCE)
    return parser.parse_args()


def load_plots(path: Path, visits: Path | None) -> pd.DataFrame:
    """Load and optionally annotate the public FAIB plot header."""
    plots = pd.read_csv(path)
    if visits is not None:
        visit_table = pd.read_csv(visits)
        summary = (
            visit_table.groupby("SITE_IDENTIFIER")
            .agg(last_year=("MEAS_YR", "max"), visits=("VISIT_NUMBER", "count"))
            .reset_index()
        )
        plots = plots.merge(summary, on="SITE_IDENTIFIER", how="left")
    return plots


def load_point_cloud_tiles(path: Path) -> list[dict[str, Any]]:
    """Return the point-cloud tiles from a LidarBC selection manifest."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [tile for tile in payload.get("tiles", []) if tile.get("product") == "point_cloud"]


def summarize(args: argparse.Namespace) -> dict[str, Any]:
    """Return the audit summary."""
    aoi = gpd.read_file(args.aoi)
    aoi_geometry = aoi.geometry.union_all()
    plots = load_plots(args.plots, args.visits)
    plots = plots.dropna(subset=["BC_ALBERS_X", "BC_ALBERS_Y"]).copy()
    points = gpd.GeoDataFrame(
        plots,
        geometry=gpd.points_from_xy(plots["BC_ALBERS_X"], plots["BC_ALBERS_Y"]),
        crs=3005,
    )
    inside = gpd.sjoin(points, aoi[["geometry"]], how="inner", predicate="within").drop(
        columns="index_right", errors="ignore"
    )

    tiles = load_point_cloud_tiles(args.selection)
    boxes = [box(*tile["bbox_epsg3005"]) for tile in tiles]
    footprint = gpd.GeoSeries(boxes, crs=3005).union_all().intersection(aoi_geometry)

    def hit_years(point: Point) -> list[int]:
        years: set[int] = set()
        for tile, tile_box in zip(tiles, boxes, strict=True):
            if tile_box.contains(point):
                year = tile.get("acquisition_year")
                if year is not None:
                    years.add(int(year))
        return sorted(years)

    def nearest_m(point: Point) -> float:
        return min(tile_box.distance(point) for tile_box in boxes)

    inside = inside.copy()
    inside["pc_years"] = inside.geometry.apply(hit_years)
    inside["has_pointcloud"] = inside["pc_years"].apply(bool)
    inside["nearest_pc_m"] = inside.geometry.apply(nearest_m)
    inside["recent"] = inside["last_year"].fillna(0) >= args.recent_since
    recent = inside[inside["recent"]]

    def distance_stats(frame: pd.DataFrame) -> dict[str, float] | None:
        if frame.empty:
            return None
        return {
            "min": float(frame["nearest_pc_m"].min()),
            "median": float(frame["nearest_pc_m"].median()),
            "max": float(frame["nearest_pc_m"].max()),
        }

    return {
        "aoi_ha": float(aoi_geometry.area / 10000.0),
        "plot_count": int(len(inside)),
        "plots_by_bec": dict(Counter(inside["BEC_ZONE"].fillna("unknown"))),
        "plots_by_establishment": dict(
            Counter(inside["SAMPLE_ESTABLISHMENT_TYPE"].fillna("unknown"))
        ),
        "recent_since": args.recent_since,
        "recent_plot_count": int(len(recent)),
        "pointcloud_tile_count": int(len(tiles)),
        "pointcloud_years": dict(Counter(tile.get("acquisition_year") for tile in tiles)),
        "pointcloud_footprint_ha": float(footprint.area / 10000.0),
        "pointcloud_footprint_pct": float(footprint.area / aoi_geometry.area * 100.0),
        "plots_with_pointcloud": int(inside["has_pointcloud"].sum()),
        "recent_with_pointcloud": int(recent["has_pointcloud"].sum()),
        "nearest_distance_m": distance_stats(inside),
        "recent_nearest_distance_m": distance_stats(recent),
    }


def main() -> None:
    """Run the audit and write its JSON summary."""
    args = parse_args()
    summary = summarize(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
