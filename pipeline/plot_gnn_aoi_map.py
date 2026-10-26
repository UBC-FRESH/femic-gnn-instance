#!/usr/bin/env python3
"""Render the GNN AOI map with a pale public basemap for context."""

from __future__ import annotations

import argparse
import io
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from PIL import Image

TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
WEB_MERCATOR_HALF = 20037508.342789244
WEB_MERCATOR_RES = 156543.03392


def _tile_xy(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    count = 2**zoom
    x = math.floor((lon + 180.0) / 360.0 * count)
    y = math.floor((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * count)
    return x, y


def _download_tile(cache_dir: Path, zoom: int, x: int, y: int) -> None:
    path = cache_dir / str(zoom) / str(x) / f"{y}.png"
    if path.is_file():
        return
    response = requests.get(
        TILE_URL.format(z=zoom, x=x, y=y),
        timeout=60,
        headers={
            "User-Agent": (
                "femic-gnn-docs-map/1.0 (https://github.com/UBC-FRESH/femic-gnn-instance)"
            )
        },
    )
    response.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)


def _basemap(
    *,
    bounds_4326: tuple[float, float, float, float],
    zoom: int,
    cache_dir: Path,
) -> tuple[np.ndarray, tuple[float, float, float, float]]:
    min_lon, min_lat, max_lon, max_lat = bounds_4326
    x0, y0 = _tile_xy(min_lon, max_lat, zoom)
    x1, y1 = _tile_xy(max_lon, min_lat, zoom)
    count = 2**zoom
    tile_range = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_download_tile, cache_dir, zoom, x, y) for x, y in tile_range]
        for future in as_completed(futures):
            future.result()
    rows: list[np.ndarray] = []
    for x in range(x0, x1 + 1):
        columns: list[np.ndarray] = []
        for y in range(y0, y1 + 1):
            path = cache_dir / str(zoom) / str(x) / f"{y}.png"
            image = Image.open(io.BytesIO(path.read_bytes())).convert("RGB")
            # Lighten the public OSM tile so the AOI remains the visual focus.
            values = np.asarray(image, dtype=np.float32)
            values = 255.0 - (255.0 - values) * 0.45
            columns.append(np.asarray(values, dtype=np.uint8))
        rows.append(np.concatenate(columns, axis=0))
    mosaic = np.concatenate(rows, axis=1)
    resolution = WEB_MERCATOR_RES / count
    left = x0 * 256 * resolution - WEB_MERCATOR_HALF
    top = WEB_MERCATOR_HALF - y0 * 256 * resolution
    right = (x1 + 1) * 256 * resolution - WEB_MERCATOR_HALF
    bottom = WEB_MERCATOR_HALF - (y1 + 1) * 256 * resolution
    return mosaic, (left, right, bottom, top)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--soi",
        type=Path,
        default=Path("data/source/aoi/gnn_soi.gpkg"),
    )
    parser.add_argument(
        "--aoi",
        type=Path,
        default=Path("data/source/aoi/gnn_full.gpkg"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/_static/gnn_aoi_map.png"),
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("runtime/gnn/aoi_basemap_osm"),
    )
    parser.add_argument("--zoom", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    """Render the AOI map and write the PNG."""
    args = _parse_args()
    soi = gpd.read_file(args.soi).to_crs(3005)
    aoi = gpd.read_file(args.aoi).to_crs(3005)
    soi_4326 = soi.to_crs(4326)
    bounds_4326 = tuple(soi_4326.total_bounds)
    mosaic, extent = _basemap(
        bounds_4326=bounds_4326,
        zoom=args.zoom,
        cache_dir=args.cache_dir,
    )
    soi_3857 = soi.to_crs(3857)
    aoi_3857 = aoi.to_crs(3857)
    minx, miny, maxx, maxy = aoi_3857.total_bounds
    pad_x = (maxx - minx) * 0.08
    pad_y = (maxy - miny) * 0.08

    fig, ax = plt.subplots(figsize=(13.5, 10.0))
    ax.imshow(mosaic, extent=extent, origin="upper", alpha=0.78, zorder=0)
    aoi_3857.plot(
        ax=ax,
        facecolor="#2e8b57",
        edgecolor="#1f5f3a",
        linewidth=1.6,
        alpha=0.24,
        zorder=2,
    )
    soi_3857.boundary.plot(
        ax=ax,
        color="#333333",
        linewidth=1.3,
        linestyle=(0, (4, 3)),
        zorder=3,
    )
    ax.set_xlim(minx - pad_x, maxx + pad_x)
    ax.set_ylim(miny - pad_y, maxy + pad_y)
    ax.set_aspect("equal")
    ax.set_axis_off()

    area_aoi = aoi.geometry.area.sum() / 10_000_000.0
    area_soi = soi.geometry.area.sum() / 10_000_000.0
    ax.set_title(
        "GNN AOI — proposed SOI clipped to TSA 46/47",
        fontsize=18,
        loc="left",
        pad=12,
    )
    ax.text(
        0.01,
        0.965,
        "Northern Vancouver Island · boundary coordinates EPSG:3005",
        transform=ax.transAxes,
        fontsize=10,
        color="#444444",
        ha="left",
    )
    ax.annotate(
        f"{area_aoi:.1f} thousand ha",
        xy=((minx + maxx) / 2, (miny + maxy) / 2),
        xytext=((minx + maxx) / 2 + 6_000, (miny + maxy) / 2 + 10_000),
        fontsize=13,
        color="#1f5f3a",
        arrowprops={"arrowstyle": "-", "color": "#1f5f3a", "lw": 1.0},
        zorder=5,
    )

    # A 50 km ground distance is wider than 50 km in Web Mercator at this
    # latitude. This bar is approximate but sufficient for page context.
    lat = (bounds_4326[1] + bounds_4326[3]) / 2.0
    bar_map_units = 50_000.0 / math.cos(math.radians(lat))
    bar_x = minx - pad_x * 0.45
    bar_y = miny - pad_y * 0.45
    ax.plot(
        [bar_x, bar_x + bar_map_units],
        [bar_y, bar_y],
        color="black",
        linewidth=3,
        solid_capstyle="butt",
        zorder=3,
    )
    ax.text(
        bar_x + bar_map_units / 2,
        bar_y + pad_y * 0.15,
        "50 km",
        ha="center",
        va="bottom",
        fontsize=10,
    )

    ax.annotate(
        "N",
        xy=(maxx + pad_x * 0.72, maxy + pad_y * 0.22),
        xytext=(maxx + pad_x * 0.72, maxy - pad_y * 0.05),
        ha="center",
        va="bottom",
        fontsize=13,
        arrowprops={"arrowstyle": "-|>", "color": "black", "lw": 1.2},
        zorder=4,
    )

    legend_handles = [
        Patch(
            facecolor="#2e8b57",
            edgecolor="#1f5f3a",
            alpha=0.35,
            label=f"GNN AOI inside TSA 46/47 ({area_aoi:.1f} thousand ha)",
        ),
        Line2D(
            [0],
            [0],
            color="#333333",
            linestyle=(0, (4, 3)),
            lw=1.3,
            label=f"Proposed SOI boundary ({area_soi:.1f} thousand ha)",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower right",
        frameon=True,
        framealpha=0.9,
        fontsize=10,
    )

    fig.text(
        0.01,
        0.015,
        "Boundary: BCGW proposed First Nation Statement of Intent; clipped to TSA 46/47. "
        "Proposed boundary, not a legal title determination. Confirm with "
        "Gwa'sala-'Nakwaxda'xw Nation.",
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
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
