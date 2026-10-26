#!/usr/bin/env python3
"""Build GNN LiDAR terrain/canopy products from materialized LidarBC tiles.

The GNN AOI is too large for a native 1 m single-file mosaic. This builder
creates an explicit 10 m strategic grid, averages the 1 m LidarBC DEM/DSM onto
it, derives Horn slope and CHM, and packages the reviewed products as a FEMIC
LiDAR bundle.

The 10 m grid is a documented GNN modelling choice, not a native LidarBC
product. It must not be described as a field-level or 1 m validation dataset.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.features
import rasterio.merge
from femic.lidar.canopy import build_canopy_products
from femic.lidar.products import (
    build_lidar_product_bundle,
    validate_lidar_product_bundle,
)
from femic.lidar.terrain import build_terrain_products
from rasterio.enums import Resampling
from rasterio.transform import Affine, from_origin
from rasterio.vrt import WarpedVRT
from shapely.geometry.base import BaseGeometry

DEFAULT_RESOLUTION_M = 10.0
DEFAULT_VERTICAL_DATUM = "Canadian Geodetic Vertical Datum of 2013"
PRODUCTS = ("dem", "dsm")


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _load_materialization(path: Path) -> Mapping[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"materialization manifest is not an object: {path}")
    tiles = payload.get("tiles")
    if not isinstance(tiles, list) or not tiles:
        raise ValueError(f"materialization manifest has no tiles: {path}")
    return payload


def _verified_tiles(
    manifest: Mapping[str, Any],
    *,
    root: Path,
    products: Sequence[str],
) -> dict[str, list[Mapping[str, Any]]]:
    selected: dict[str, list[Mapping[str, Any]]] = {product: [] for product in products}
    for tile in manifest["tiles"]:
        if not isinstance(tile, dict):
            continue
        product = str(tile.get("product", ""))
        if product not in selected:
            continue
        if tile.get("status") != "verified":
            continue
        relative = tile.get("relative_path")
        if not isinstance(relative, str) or not relative:
            raise ValueError(f"verified tile has no relative_path: {tile!r}")
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"verified tile is missing: {path}")
        record = dict(tile)
        record["_path"] = path
        selected[product].append(record)
    for product, records in selected.items():
        if not records:
            raise ValueError(f"no verified tiles for product {product!r}")
    return selected


def _target_grid(
    aoi_path: Path,
    resolution_m: float,
) -> tuple[tuple[float, float, float, float], int, int, Affine, BaseGeometry]:
    aoi = gpd.read_file(aoi_path)
    if aoi.crs is None:
        raise ValueError(f"AOI has no CRS: {aoi_path}")
    aoi = aoi.to_crs(3005)
    geometry = aoi.geometry.union_all()
    minx, miny, maxx, maxy = geometry.bounds
    left = math.floor(minx / resolution_m) * resolution_m
    bottom = math.floor(miny / resolution_m) * resolution_m
    right = math.ceil(maxx / resolution_m) * resolution_m
    top = math.ceil(maxy / resolution_m) * resolution_m
    width = int((right - left) / resolution_m)
    height = int((top - bottom) / resolution_m)
    transform = from_origin(left, top, resolution_m, resolution_m)
    return (left, bottom, right, top), width, height, transform, geometry


def _mosaic_product(
    tiles: Sequence[Mapping[str, Any]],
    *,
    bounds: tuple[float, float, float, float],
    resolution_m: float,
    aoi_geometry: BaseGeometry,
    output_path: Path,
    vertical_datum: str,
) -> dict[str, object]:
    sources: list[Any] = []
    vrt_sources: list[Any] = []
    source_crs: set[str] = set()
    try:
        for tile in tiles:
            dataset = rasterio.open(tile["_path"])
            if dataset.crs is None:
                dataset.close()
                raise ValueError(f"tile has no CRS: {dataset.name}")
            source_crs.add(dataset.crs.to_string())
            if abs(dataset.res[0] - 1.0) > 1e-6:
                dataset.close()
                raise ValueError(
                    f"expected 1 m native tile resolution: {dataset.name} ({dataset.res})"
                )
            sources.append(dataset)
            vrt_sources.append(
                WarpedVRT(
                    dataset,
                    crs="EPSG:3005",
                    resampling=Resampling.average,
                    src_nodata=dataset.nodata,
                    nodata=np.nan,
                )
            )
        merged, transform = rasterio.merge.merge(
            vrt_sources,
            bounds=bounds,
            res=resolution_m,
            nodata=np.nan,
            dtype="float32",
            resampling=Resampling.average,
            method="first",
            mem_limit=2048,
        )
    finally:
        for vrt in reversed(vrt_sources):
            vrt.close()
        for dataset in reversed(sources):
            dataset.close()

    values = np.asarray(merged[0], dtype="float32")
    if values.ndim != 2:
        raise ValueError(f"merged raster has unexpected shape: {values.shape}")
    height, width = values.shape
    outside = rasterio.features.geometry_mask(
        [aoi_geometry],
        out_shape=(height, width),
        transform=transform,
        invert=False,
    )
    values[outside] = np.nan
    output_path.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:3005",
        "transform": transform,
        "nodata": np.nan,
        "compress": "deflate",
        "predictor": 3,
        "tiled": True,
        "blockxsize": 512,
        "blockysize": 512,
        "BIGTIFF": "IF_SAFER",
    }
    with rasterio.open(output_path, "w", **profile) as destination:
        destination.write(values, 1)
        destination.update_tags(
            source="LidarBC 1 m DEM/DSM",
            aggregation=f"mean to {resolution_m:g} m strategic grid",
            vertical_datum=vertical_datum,
            aoi="GNN proposed SOI clipped to TSA 46/47",
        )
    valid = np.isfinite(values)
    return {
        "path": str(output_path),
        "width": width,
        "height": height,
        "resolution_m": resolution_m,
        "source_crs": sorted(source_crs),
        "output_crs": "EPSG:3005",
        "valid_pixels": int(valid.sum()),
        "nodata_pixels": int((~valid).sum()),
        "min": float(np.nanmin(values)) if valid.any() else None,
        "max": float(np.nanmax(values)) if valid.any() else None,
        "mean": float(np.nanmean(values)) if valid.any() else None,
    }


def _product_spec(
    *,
    product: str,
    path: Path,
    media_type: str,
    resolution_m: float,
    vertical_datum: str,
    retrieved_utc: str,
    tiles: Sequence[Mapping[str, Any]],
    derived: bool,
    lineage: Sequence[str],
) -> dict[str, object]:
    tile_ids = [str(tile["tile_id"]) for tile in tiles]
    layer_ids = sorted({int(tile["layer_id"]) for tile in tiles})
    return {
        "product": product,
        "path": str(path),
        "media_type": media_type,
        "crs": "EPSG:3005",
        "resolution_m": resolution_m,
        "vertical_datum": vertical_datum,
        "retrieved_utc": retrieved_utc,
        "source_tile_ids": tile_ids,
        "source_layer_ids": layer_ids,
        "derived": derived,
        "lineage": list(lineage),
    }


def _write_product_plan(
    *,
    plan_path: Path,
    output_dir: Path,
    bundle_version: str,
    processing_version: str,
    resolution_m: float,
    vertical_datum: str,
    retrieved_utc: str,
    tiles: Mapping[str, Sequence[Mapping[str, Any]]],
    dem_qa: Mapping[str, object],
    canopy_qa: Mapping[str, object],
) -> dict[str, object]:
    slope_path = output_dir / "terrain" / "slope_percent.tif"
    chm_path = output_dir / "canopy" / "chm.tif"
    canopy_path = output_dir / "canopy" / "canopy_structure.json"
    dem_tiles = list(tiles["dem"])
    dsm_tiles = list(tiles["dsm"])
    both_tiles = [*dem_tiles, *dsm_tiles]

    products = [
        _product_spec(
            product="slope",
            path=slope_path,
            media_type="image/tiff",
            resolution_m=resolution_m,
            vertical_datum=vertical_datum,
            retrieved_utc=retrieved_utc,
            tiles=dem_tiles,
            derived=True,
            lineage=[
                f"Horn percent slope from {resolution_m:g} m DEM",
                "edge replication",
            ],
        ),
        _product_spec(
            product="chm",
            path=chm_path,
            media_type="image/tiff",
            resolution_m=resolution_m,
            vertical_datum=vertical_datum,
            retrieved_utc=retrieved_utc,
            tiles=both_tiles,
            derived=True,
            lineage=[
                f"DSM minus DEM on the {resolution_m:g} m GNN strategic grid",
                "negative heights clamped to zero",
            ],
        ),
        _product_spec(
            product="canopy",
            path=canopy_path,
            media_type="application/json",
            resolution_m=resolution_m,
            vertical_datum=vertical_datum,
            retrieved_utc=retrieved_utc,
            tiles=both_tiles,
            derived=True,
            lineage=[
                "canopy structure from CHM",
                "thresholds 2, 5, 10, 20 m",
            ],
        ),
    ]
    plan = {
        "schema_version": "femic.lidar.product_plan.v1",
        "bundle_version": bundle_version,
        "processing_version": processing_version,
        "processing_lineage": [
            "femic.lidar.selection.v1",
            "femic.lidar.materialization.v1",
            "gnn-10m-strategic-mosaic",
            "femic.lidar.terrain.v1",
            "femic.lidar.canopy.v1",
        ],
        "parameters": {
            "resolution_m": resolution_m,
            "resampling": "average",
            "reprojection": "explicit source tile CRS to EPSG:3005",
            "aoi_mask": "GNN AOI (gnn_full.gpkg)",
            "slope_method": "horn_3x3",
            "chm": "dsm_minus_dem",
            "negative_chm": "clamped_to_zero",
            "vertical_datum": vertical_datum,
            "dem_qa": dem_qa,
            "canopy_qa": canopy_qa,
        },
        "products": products,
    }
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return plan


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--materialization",
        type=Path,
        default=Path("data/lidar/materialization.json"),
    )
    parser.add_argument(
        "--aoi",
        type=Path,
        default=Path("data/source/aoi/gnn_full.gpkg"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/lidar/gnn_10m"),
    )
    parser.add_argument(
        "--resolution",
        type=float,
        default=DEFAULT_RESOLUTION_M,
        help="Strategic grid resolution in metres.",
    )
    parser.add_argument(
        "--bundle-version",
        default="2026.10.0-gnn-10m",
    )
    parser.add_argument(
        "--processing-version",
        default="femic-p79.8-gnn-10m-v1",
    )
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=None,
        help="Bundle destination; defaults to data/lidar/products/<bundle-version>.",
    )
    parser.add_argument(
        "--max-tiles",
        type=int,
        default=None,
        help="Bounded test run; omit for the full selection.",
    )
    return parser.parse_args()


def main() -> None:
    """Build and validate the GNN strategic-grid LiDAR bundle."""
    args = _parse_args()
    if args.resolution <= 0:
        raise ValueError("--resolution must be positive")
    materialization_path = args.materialization.expanduser().resolve()
    manifest = _load_materialization(materialization_path)
    root = materialization_path.parent
    tiles = _verified_tiles(manifest, root=root, products=PRODUCTS)
    if args.max_tiles is not None:
        for product in PRODUCTS:
            tiles[product] = tiles[product][: args.max_tiles]
    bounds, width, height, _transform, aoi_geometry = _target_grid(
        args.aoi.expanduser().resolve(),
        args.resolution,
    )
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    vertical_datum = DEFAULT_VERTICAL_DATUM
    retrieved_utc = str(manifest.get("generated_utc") or _utc_now())

    dem_path = output_dir / f"dem_{args.resolution:g}m.tif"
    dsm_path = output_dir / f"dsm_{args.resolution:g}m.tif"
    dem_summary = _mosaic_product(
        tiles["dem"],
        bounds=bounds,
        resolution_m=args.resolution,
        aoi_geometry=aoi_geometry,
        output_path=dem_path,
        vertical_datum=vertical_datum,
    )
    dsm_summary = _mosaic_product(
        tiles["dsm"],
        bounds=bounds,
        resolution_m=args.resolution,
        aoi_geometry=aoi_geometry,
        output_path=dsm_path,
        vertical_datum=vertical_datum,
    )

    generated_utc = _utc_now()
    terrain = build_terrain_products(
        dem_path,
        output_dir / "terrain",
        generated_utc=generated_utc,
    )
    canopy = build_canopy_products(
        dsm_path,
        dem_path,
        output_dir / "canopy",
        vertical_datum=vertical_datum,
        generated_utc=generated_utc,
    )

    plan_path = output_dir / "product_plan.json"
    _write_product_plan(
        plan_path=plan_path,
        output_dir=output_dir,
        bundle_version=args.bundle_version,
        processing_version=args.processing_version,
        resolution_m=args.resolution,
        vertical_datum=vertical_datum,
        retrieved_utc=retrieved_utc,
        tiles=tiles,
        dem_qa=terrain.to_dict(),
        canopy_qa=canopy.to_dict(),
    )
    bundle_dir = (
        args.bundle_dir.expanduser().resolve()
        if args.bundle_dir is not None
        else Path("data/lidar/products") / args.bundle_version
    )
    selection_manifest = Path("metadata/lidar/lidarbc_selection_dem_dsm.json")
    bundle = build_lidar_product_bundle(
        selection_manifest_path=selection_manifest,
        product_plan_path=plan_path,
        output_dir=bundle_dir,
        overwrite=True,
    )
    validation = validate_lidar_product_bundle(bundle.bundle_dir)
    summary = {
        "generated_utc": generated_utc,
        "resolution_m": args.resolution,
        "target": {
            "bounds": list(bounds),
            "width": width,
            "height": height,
            "pixels": width * height,
        },
        "tile_counts": {product: len(records) for product, records in tiles.items()},
        "dem": dem_summary,
        "dsm": dsm_summary,
        "terrain": terrain.to_dict(),
        "canopy": canopy.to_dict(),
        "bundle": {
            "bundle_dir": str(bundle.bundle_dir),
            "bundle_id": bundle.manifest.bundle_id,
            "bundle_version": bundle.manifest.bundle_version,
            "manifest_path": str(bundle.manifest_path),
            "products": [product.product for product in bundle.manifest.products],
            "validation": validation.to_dict(),
        },
    }
    summary_path = output_dir / "build_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
