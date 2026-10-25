#!/usr/bin/env python3
"""Sample terrain slope for one GNN block from public Terrarium DEM tiles.

Terrarium tiles are elevation-encoded PNGs from the AWS Open Data terrain tiles.
The output is a local research sample; it is not a full-block operability survey.
"""

from __future__ import annotations

import argparse
import io
import math
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from PIL import Image
from pyproj import Transformer
from shapely import contains_xy

TILE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"


def _tile_xy(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    count = 2**zoom
    x = int((lon + 180.0) / 360.0 * count)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * count)
    return x, y


def _decode(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image.convert("RGB"), dtype=np.float64)
    return rgb[:, :, 0] * 256.0 + rgb[:, :, 1] + rgb[:, :, 2] / 256.0 - 32768.0


def _mosaic(bbox: tuple[float, float, float, float], zoom: int, cache: dict[tuple[int, int, int], np.ndarray] | None = None) -> tuple[np.ndarray, int, int, int, int]:
    min_lon, min_lat, max_lon, max_lat = bbox
    x0, y0 = _tile_xy(min_lon, max_lat, zoom)
    x1, y1 = _tile_xy(max_lon, min_lat, zoom)
    rows: list[np.ndarray] = []
    for x in range(x0, x1 + 1):
        tiles: list[np.ndarray] = []
        for y in range(y0, y1 + 1):
            key = (zoom, x, y)
            if cache is not None and key in cache:
                tiles.append(cache[key])
                continue
            response = requests.get(TILE_URL.format(z=zoom, x=x, y=y), timeout=30)
            response.raise_for_status()
            tile = _decode(Image.open(io.BytesIO(response.content)))
            if cache is not None:
                cache[key] = tile
            tiles.append(tile)
        rows.append(np.concatenate(tiles, axis=0))
    return np.concatenate(rows, axis=1), x0, y0, x1, y1


def _slope_percent(
    elevation: np.ndarray,
    *,
    zoom: int,
    origin_x: int,
    origin_y: int,
) -> np.ndarray:
    count = 2**zoom
    pixels = elevation.shape[0]
    # Approximate metres per pixel at the block latitude; the block is small.
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (origin_y + 0.5) / count))))
    x_m = 156543.03392 * math.cos(math.radians(lat)) / count
    y_m = 156543.03392 / count
    dz_dy, dz_dx = np.gradient(elevation, y_m, x_m)
    return np.sqrt(dz_dx**2 + dz_dy**2) * 100.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", type=Path, required=True)
    parser.add_argument("--block-id", type=int, required=True)
    parser.add_argument("--zoom", type=int, default=13)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    blocks = gpd.read_file(args.blocks)
    if blocks.crs is None or str(blocks.crs).upper() != "EPSG:3005":
        blocks = blocks.set_crs(3005, allow_override=True)
    row = blocks[blocks["block_id"].astype(int) == args.block_id]
    if row.empty:
        raise SystemExit(f"block {args.block_id} not found")
    block = row.geometry.union_all()
    area_ha = block.area / 10000.0

    to_wgs = Transformer.from_crs(3005, 4326, always_xy=True)
    to_albers = Transformer.from_crs(4326, 3005, always_xy=True)
    min_x, min_y, max_x, max_y = block.bounds
    corners = [to_wgs.transform(min_x, min_y), to_wgs.transform(max_x, max_y)]
    lons = [point[0] for point in corners]
    lats = [point[1] for point in corners]
    bbox = (min(lons), min(lats), max(lons), max(lats))

    elevation, x0, y0, x1, y1 = _mosaic(bbox, args.zoom)
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
        raise SystemExit("no terrain pixels inside the block")
    result = pd.DataFrame(
        [
            {
                "block_id": args.block_id,
                "area_ha": round(area_ha, 3),
                "slope_percent": round(float(np.nanmean(slope[mask])), 2),
                "slope_p90_percent": round(float(np.nanpercentile(slope[mask], 90)), 2),
                "elevation_mean_m": round(float(np.nanmean(elevation[mask])), 1),
                "pixels": int(mask.sum()),
                "zoom": args.zoom,
                "source": "AWS Open Data Terrarium terrain tiles",
                "data_status": "coarse_dem_sample",
            }
        ]
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.out, index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
