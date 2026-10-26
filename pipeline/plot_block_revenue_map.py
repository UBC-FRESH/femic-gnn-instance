#!/usr/bin/env python3
"""Map the block revenue screen and the positive replacement schedule."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from plot_gnn_aoi_map import _basemap

POSITIVE = "#8fbf7f"
NEGATIVE = "#c43c39"
REPLACEMENT = "#2b6cb0"
GREY = "#b8b8b8"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--aoi",
        type=Path,
        default=Path("data/source/aoi/gnn_full.gpkg"),
    )
    parser.add_argument(
        "--fragments",
        type=Path,
        default=Path("output/patchworks_gnn/fragments_merged/fragments.shp"),
    )
    parser.add_argument(
        "--screen",
        type=Path,
        default=Path("runtime/gnn/block_revenue_screen.csv"),
    )
    parser.add_argument(
        "--base-schedule",
        type=Path,
        default=Path("runtime/gnn/schedules/opening_first.csv"),
    )
    parser.add_argument(
        "--positive-schedule",
        type=Path,
        default=Path("runtime/gnn/schedules/opening_first_positive.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/_static/block_revenue_map.png"),
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("runtime/gnn/aoi_basemap_osm"),
    )
    parser.add_argument("--zoom", type=int, default=10)
    return parser.parse_args()


def _blocks(path: Path) -> gpd.GeoDataFrame:
    support = gpd.read_file(path)
    support = (
        support.set_crs(3005, allow_override=True) if support.crs is None else support.to_crs(3005)
    )
    blocks = support[["BLOCK", "TSA", "AU", "geometry"]].dissolve(
        by=["BLOCK", "TSA", "AU"], as_index=False
    )
    return blocks.rename(columns={"BLOCK": "block_id", "TSA": "tsa", "AU": "au"})


def _scale_bar(ax: plt.Axes, *, bounds: tuple[float, float, float, float], lat: float) -> None:
    minx, miny, maxx, maxy = bounds
    pad_x = (maxx - minx) * 0.08
    pad_y = (maxy - miny) * 0.08
    bar_map_units = 50_000.0 / math.cos(math.radians(lat))
    x0 = minx - pad_x * 0.45
    y0 = miny - pad_y * 0.45
    ax.plot([x0, x0 + bar_map_units], [y0, y0], color="black", linewidth=3, zorder=5)
    ax.text(
        x0 + bar_map_units / 2,
        y0 + pad_y * 0.15,
        "50 km",
        ha="center",
        va="bottom",
        fontsize=9,
        zorder=6,
    )


def main() -> None:
    """Render the two-panel block review map."""
    args = _parse_args()
    aoi = gpd.read_file(args.aoi).to_crs(3005)
    bounds_4326 = tuple(aoi.to_crs(4326).total_bounds)
    mosaic, extent = _basemap(
        bounds_4326=bounds_4326,
        zoom=args.zoom,
        cache_dir=args.cache_dir,
    )
    blocks = _blocks(args.fragments)
    screen = pd.read_csv(args.screen)[
        ["block_id", "positive", "operability_dominant", "thlb_ha", "net_base_cad"]
    ]
    blocks = blocks.merge(screen, on="block_id", how="left")
    blocks = blocks.to_crs(3857)
    aoi_3857 = aoi.to_crs(3857)
    minx, miny, maxx, maxy = aoi_3857.total_bounds
    pad_x = (maxx - minx) * 0.08
    pad_y = (maxy - miny) * 0.08
    base_ids = set(pd.read_csv(args.base_schedule)["block_id"].astype(int))
    positive_schedule_ids = set(pd.read_csv(args.positive_schedule)["block_id"].astype(int))
    screened = blocks[blocks["positive"].notna()].copy()
    unscreened = blocks[blocks["positive"].isna()].copy()
    positive = screened[screened["positive"].astype(bool)]
    negative = screened[~screened["positive"].astype(bool)]
    negative_ids = set(negative["block_id"])
    removed = blocks[blocks["block_id"].isin(base_ids & negative_ids)].to_crs(3857)
    replacement = blocks[blocks["block_id"].isin(positive_schedule_ids)].to_crs(3857)

    fig, axes = plt.subplots(1, 2, figsize=(19, 9.5), sharex=True, sharey=True)
    for ax in axes:
        ax.imshow(mosaic, extent=extent, origin="upper", alpha=0.55, zorder=0)
        aoi_3857.boundary.plot(ax=ax, color="#444444", linewidth=1.0, zorder=4)
        ax.set_xlim(minx - pad_x, maxx + pad_x)
        ax.set_ylim(miny - pad_y, maxy + pad_y)
        ax.set_aspect("equal")
        ax.set_axis_off()

    unscreened.plot(
        ax=axes[0],
        color=GREY,
        edgecolor="none",
        alpha=0.12,
        zorder=1,
    )
    positive.plot(
        ax=axes[0],
        color=POSITIVE,
        edgecolor="none",
        alpha=0.30,
        zorder=2,
    )
    negative.plot(
        ax=axes[0],
        color=NEGATIVE,
        edgecolor="none",
        alpha=0.88,
        zorder=3,
    )
    axes[0].set_title(
        f"Block screen: {len(positive):,} positive / {len(negative):,} negative / "
        f"{len(unscreened):,} not screened",
        fontsize=13,
        loc="left",
    )
    axes[0].legend(
        handles=[
            Patch(facecolor=POSITIVE, alpha=0.5, label="Direct-positive block"),
            Patch(facecolor=NEGATIVE, label="Direct-negative block"),
            Patch(facecolor=GREY, alpha=0.3, label="Not screened"),
        ],
        loc="lower right",
        fontsize=9,
        framealpha=0.9,
    )

    positive.plot(
        ax=axes[1],
        color=GREY,
        edgecolor="none",
        alpha=0.18,
        zorder=1,
    )
    replacement.plot(
        ax=axes[1],
        color=REPLACEMENT,
        edgecolor=REPLACEMENT,
        linewidth=0.25,
        alpha=0.45,
        zorder=2,
    )
    removed.plot(
        ax=axes[1],
        color=NEGATIVE,
        edgecolor="black",
        linewidth=0.55,
        alpha=0.9,
        zorder=3,
    )
    axes[1].set_title(
        f"Replacement: {len(removed):,} removed negative / {len(replacement):,} positive scheduled",
        fontsize=13,
        loc="left",
    )
    axes[1].legend(
        handles=[
            Patch(
                facecolor=NEGATIVE,
                edgecolor="black",
                label="Negative block removed from base schedule",
            ),
            Patch(facecolor=REPLACEMENT, alpha=0.55, label="Positive replacement schedule"),
            Line2D([0], [0], color="#444444", lw=1.0, label="GNN AOI"),
        ],
        loc="lower right",
        fontsize=9,
        framealpha=0.9,
    )
    lat = (bounds_4326[1] + bounds_4326[3]) / 2.0
    _scale_bar(axes[1], bounds=(minx, miny, maxx, maxy), lat=lat)
    fig.suptitle(
        "Block-level revenue screen and positive replacement schedule",
        fontsize=18,
        x=0.02,
        ha="left",
    )
    fig.text(
        0.01,
        0.015,
        "Direct cost only. Shared road/landing/terminal/overhead costs are unallocated. "
        "Not a sustainable result.",
        fontsize=8,
        color="#444444",
    )
    fig.text(
        0.99,
        0.015,
        "Basemap: © OpenStreetMap contributors",
        fontsize=8,
        color="#444444",
        ha="right",
    )
    fig.tight_layout(rect=(0, 0.035, 1, 0.96))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
