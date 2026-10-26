#!/usr/bin/env python3
"""Build public road/stream/coast access exposure for candidate blocks.

The result is exposure, not a cost estimate. No road construction, crossing,
terminal, haul, or barge rate is invented.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from plot_gnn_aoi_map import _basemap

DRA_URL = (
    "https://openmaps.gov.bc.ca/geo/pub/"
    "WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP/ows?service=WFS&version=2.0.0"
    "&request=GetFeature&typeName=WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP"
    "&outputFormat=application/json&srsName=EPSG:3005"
    "&bbox=833086,637521,967460,727601,EPSG:3005&count=10000"
)
FWA_URL = (
    "https://openmaps.gov.bc.ca/geo/pub/"
    "WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP/ows?service=WFS&version=2.0.0"
    "&request=GetFeature&typeName=WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP"
    "&outputFormat=application/json&srsName=EPSG:3005"
    "&bbox=833086,637521,967460,727601,EPSG:3005&count=50000"
)
COAST_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_coastline.zip"
ROAD_BINS = [
    (-1.0, 0.01, "touching"),
    (0.01, 100.0, "≤100 m"),
    (100.0, 500.0, "100-500 m"),
    (500.0, float("inf"), ">500 m"),
]
ROAD_COLORS = {
    "touching": "#2f7d32",
    "≤100 m": "#86b96b",
    "100-500 m": "#e6b84a",
    ">500 m": "#c43c39",
}


def _download(url: str, path: Path, *, timeout: int = 180) -> Path:
    if path.is_file():
        return path
    import requests

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)
    return path


def _load_gis(path: Path) -> gpd.GeoDataFrame:
    frame = gpd.read_file(path)
    if frame.crs is None:
        frame = frame.set_crs(3005, allow_override=True)
    return frame.to_crs(3005)


def _coastline(cache: Path) -> gpd.GeoDataFrame:
    archive = _download(COAST_URL, cache / "ne_10m_coastline.zip")
    extract = cache / "ne_10m_coastline"
    if not extract.is_dir():
        with zipfile.ZipFile(archive) as zipped:
            zipped.extractall(extract)
    return _load_gis(extract / "ne_10m_coastline.shp")


def _nearest_distance(
    blocks: gpd.GeoDataFrame,
    other: gpd.GeoDataFrame,
    *,
    column: str,
) -> gpd.Series:
    nearest = gpd.sjoin_nearest(
        blocks[["block_id", "geometry"]],
        other[["geometry"]],
        how="left",
        distance_col=column,
    )
    nearest = nearest[["block_id", column]].drop_duplicates("block_id")
    return nearest.set_index("block_id")[column]


def _stream_crossings(
    blocks: gpd.GeoDataFrame,
    streams: gpd.GeoDataFrame,
) -> pd.DataFrame:
    joined = gpd.sjoin(
        blocks[["block_id", "geometry"]],
        streams[["LINEAR_FEATURE_ID", "GNIS_NAME", "geometry"]],
        how="inner",
        predicate="intersects",
    )
    if joined.empty:
        return pd.DataFrame(columns=["block_id", "stream_crossings", "named_streams"])
    return joined.groupby("block_id", as_index=False).agg(
        stream_crossings=("LINEAR_FEATURE_ID", "nunique"),
        named_streams=("GNIS_NAME", lambda values: values.notna().sum()),
    )


def _road_bin(distance: float) -> str:
    if distance <= 0.01:
        return "touching"
    if distance <= 100.0:
        return "≤100 m"
    if distance <= 500.0:
        return "100-500 m"
    return ">500 m"


def _summary(frame: pd.DataFrame) -> dict[str, object]:
    total = {
        "blocks": len(frame),
        "thlb_ha": float(frame["thlb_ha"].sum()),
        "road_touching_blocks": int((frame["road_distance_m"] <= 0.01).sum()),
        "road_touching_thlb_ha": float(
            frame.loc[frame["road_distance_m"] <= 0.01, "thlb_ha"].sum()
        ),
        "road_100m_blocks": int((frame["road_distance_m"] <= 100.0).sum()),
        "road_100m_thlb_ha": float(frame.loc[frame["road_distance_m"] <= 100.0, "thlb_ha"].sum()),
        "road_500m_blocks": int((frame["road_distance_m"] <= 500.0).sum()),
        "road_500m_thlb_ha": float(frame.loc[frame["road_distance_m"] <= 500.0, "thlb_ha"].sum()),
        "stream_crossing_blocks": int((frame["stream_crossings"] > 0).sum()),
        "stream_crossings": int(frame["stream_crossings"].sum()),
        "median_road_distance_m": float(frame["road_distance_m"].median()),
        "median_coast_distance_m": float(frame["coast_distance_m"].median()),
        "median_slope_pct": float(frame["terrain_slope_mean_pct"].median()),
    }
    by_tsa = frame.groupby("block_tsa", as_index=False).agg(
        blocks=("block_id", "size"),
        thlb_ha=("thlb_ha", "sum"),
        road_touching=("road_touching", "sum"),
        stream_crossing_blocks=("stream_crossings", lambda values: int((values > 0).sum())),
        median_road_distance_m=("road_distance_m", "median"),
    )
    by_operability = frame.groupby("operability_dominant", as_index=False).agg(
        blocks=("block_id", "size"),
        thlb_ha=("thlb_ha", "sum"),
        road_touching=("road_touching", "sum"),
        stream_crossing_blocks=("stream_crossings", lambda values: int((values > 0).sum())),
        median_road_distance_m=("road_distance_m", "median"),
    )
    return {
        "total": total,
        "by_tsa": by_tsa.to_dict(orient="records"),
        "by_operability": by_operability.to_dict(orient="records"),
    }


def _report(frame: pd.DataFrame, summary: dict[str, object], path: Path) -> None:
    total = summary["total"]
    lines = [
        "# Candidate schedule: public access exposure",
        "",
        "Status: exposure only. This is not a road, crossing, terminal, haul, or",
        "barge cost estimate.",
        "",
        "## Summary",
        "",
        f"- Candidate blocks: **{total['blocks']:,}**",
        f"- Candidate THLB: **{total['thlb_ha'] / 1000:.1f} thousand ha**",
        f"- Blocks touching a DRA road: **{total['road_touching_blocks']:,}** "
        f"({100.0 * total['road_touching_blocks'] / total['blocks']:.1f}%)",
        f"- Blocks within 100 m of a road: **{total['road_100m_blocks']:,}** "
        f"({100.0 * total['road_100m_blocks'] / total['blocks']:.1f}%)",
        f"- Blocks within 500 m of a road: **{total['road_500m_blocks']:,}** "
        f"({100.0 * total['road_500m_blocks'] / total['blocks']:.1f}%)",
        f"- Blocks with mapped stream crossings: **{total['stream_crossing_blocks']:,}**",
        f"- Total mapped stream crossings: **{total['stream_crossings']:,}**",
        f"- Median distance to DRA road: **{total['median_road_distance_m']:.0f} m**",
        f"- Median distance to Natural Earth coastline: "
        f"**{total['median_coast_distance_m']:.0f} m**",
        f"- Median descriptive slope: **{total['median_slope_pct']:.1f}%**",
        "",
        "## By TSA",
        "",
        "| TSA | Blocks | THLB (kha) | Road-touching | "
        "Stream-crossing blocks | Median road distance (m) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["by_tsa"]:
        lines.append(
            f"| {row['block_tsa']} | {row['blocks']:,} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['road_touching']:,} | {row['stream_crossing_blocks']:,} | "
            f"{row['median_road_distance_m']:.0f} |"
        )
    lines += [
        "",
        "## By dominant operability",
        "",
        "| System | Blocks | THLB (kha) | Road-touching | "
        "Stream-crossing blocks | Median road distance (m) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["by_operability"]:
        lines.append(
            f"| {row['operability_dominant']} | {row['blocks']:,} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['road_touching']:,} | {row['stream_crossing_blocks']:,} | "
            f"{row['median_road_distance_m']:.0f} |"
        )
    lines += [
        "",
        "## Definitions and limits",
        "",
        "- Road distance is the straight-line distance from a block polygon to the",
        "  nearest DRA road line in EPSG:3005, not a route or haul distance.",
        "- A stream crossing means a mapped FWA stream intersects the block polygon.",
        "  It is not a confirmed culvert, bridge, or fish-passage requirement.",
        "- Coast distance is straight-line distance to the Natural Earth 10m",
        "  coastline. It is not a barge route, terminal, or loading point.",
        "- Slope is the descriptive 30 m public terrain field, not LiDAR.",
        "- No road, crossing, terminal, haul, or barge rate is assigned.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _map(frame: gpd.GeoDataFrame, aoi: gpd.GeoDataFrame, path: Path) -> None:
    bounds_4326 = tuple(aoi.to_crs(4326).total_bounds)
    mosaic, extent = _basemap(
        bounds_4326=bounds_4326,
        zoom=10,
        cache_dir=Path("runtime/gnn/aoi_basemap_osm"),
    )
    frame = frame.to_crs(3857)
    aoi = aoi.to_crs(3857)
    minx, miny, maxx, maxy = aoi.total_bounds
    pad_x = (maxx - minx) * 0.06
    pad_y = (maxy - miny) * 0.06
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.imshow(mosaic, extent=extent, origin="upper", alpha=0.55, zorder=0)
    for label in ("touching", "≤100 m", "100-500 m", ">500 m"):
        subset = frame[frame["road_bin"] == label]
        if subset.empty:
            continue
        subset.plot(
            ax=ax,
            color=ROAD_COLORS[label],
            edgecolor="none",
            alpha=0.55 if label == "touching" else 0.85,
            zorder=2,
        )
    aoi.boundary.plot(ax=ax, color="#333333", linewidth=1.0, zorder=3)
    ax.set_xlim(minx - pad_x, maxx + pad_x)
    ax.set_ylim(miny - pad_y, maxy + pad_y)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(
        "Candidate schedule: distance to existing DRA roads",
        fontsize=16,
        loc="left",
    )
    ax.legend(
        handles=[
            Patch(facecolor=ROAD_COLORS[label], label=label)
            for label in ("touching", "≤100 m", "100-500 m", ">500 m")
        ],
        loc="lower right",
        fontsize=9,
        framealpha=0.9,
    )
    fig.text(
        0.01,
        0.015,
        "Exposure only. No road, crossing, terminal, haul, or barge cost is assigned. "
        "Basemap: © OpenStreetMap contributors.",
        fontsize=8,
        color="#444444",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("runtime/gnn/matrix"),
    )
    parser.add_argument(
        "--schedule",
        type=Path,
        default=Path("runtime/gnn/schedules/opening_first_positive.csv"),
    )
    parser.add_argument(
        "--fragments",
        type=Path,
        default=Path("output/patchworks_gnn/fragments_merged/fragments.shp"),
    )
    parser.add_argument("--aoi", type=Path, default=Path("data/source/aoi/gnn_full.gpkg"))
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("runtime/gnn/access"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runtime/gnn/access_exposure.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("runtime/gnn/access_exposure_summary.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("notes/reports/access-exposure.md"),
    )
    parser.add_argument(
        "--map",
        type=Path,
        default=Path("docs/_static/access_exposure_map.png"),
    )
    return parser.parse_args()


def main() -> None:
    """Build the access exposure layer and report."""
    args = _parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    roads = _load_gis(_download(DRA_URL, args.cache_dir / "dra_gnn.geojson"))
    streams = _load_gis(_download(FWA_URL, args.cache_dir / "fwa_gnn.geojson"))
    coast = _coastline(args.cache_dir)
    aoi = gpd.read_file(args.aoi).to_crs(3005)
    coast = gpd.clip(coast, aoi)

    support = gpd.read_file(args.fragments)
    support = (
        support.set_crs(3005, allow_override=True) if support.crs is None else support.to_crs(3005)
    )
    blocks = (
        support[["BLOCK", "TSA", "AU", "geometry"]]
        .dissolve(by=["BLOCK", "TSA", "AU"], as_index=False)
        .rename(columns={"BLOCK": "block_id", "TSA": "block_tsa", "AU": "block_au"})
    )
    scheduled = pd.read_csv(args.schedule)["block_id"].astype(int)
    blocks = blocks[blocks["block_id"].isin(set(scheduled))].copy().reset_index(drop=True)
    screen = pd.read_csv("runtime/gnn/block_revenue_screen.csv")[
        ["block_id", "thlb_ha", "operability_dominant"]
    ].drop_duplicates("block_id")
    blocks = blocks.merge(screen, on="block_id", how="left", validate="one_to_one")
    flat_blocks = pd.read_parquet(args.dataset / "blocks.parquet")[
        ["block_id", "terrain_slope_mean_pct"]
    ].drop_duplicates("block_id")
    blocks = blocks.merge(flat_blocks, on="block_id", how="left", validate="one_to_one")
    blocks["road_distance_m"] = blocks["block_id"].map(
        _nearest_distance(blocks, roads, column="road_distance_m")
    )
    blocks["coast_distance_m"] = blocks["block_id"].map(
        _nearest_distance(blocks, coast, column="coast_distance_m")
    )
    crossings = _stream_crossings(blocks, streams)
    blocks = blocks.merge(crossings, on="block_id", how="left")
    blocks["stream_crossings"] = blocks["stream_crossings"].fillna(0).astype(int)
    blocks["named_streams"] = blocks["named_streams"].fillna(0).astype(int)
    blocks["road_touching"] = blocks["road_distance_m"] <= 0.01
    blocks["road_bin"] = blocks["road_distance_m"].map(_road_bin)
    blocks = gpd.GeoDataFrame(blocks, geometry="geometry", crs="EPSG:3005")
    blocks.to_csv(args.out, index=False)
    summary = _summary(blocks)
    summary["inputs"] = {
        "schedule": str(args.schedule),
        "road_source": DRA_URL,
        "stream_source": FWA_URL,
        "coast_source": COAST_URL,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _report(blocks, summary, args.report)
    _map(blocks, aoi, args.map)
    print(
        f"blocks={len(blocks):,} road_touching={summary['total']['road_touching_blocks']:,} "
        f"stream_crossing_blocks={summary['total']['stream_crossing_blocks']:,}"
    )


if __name__ == "__main__":
    main()
