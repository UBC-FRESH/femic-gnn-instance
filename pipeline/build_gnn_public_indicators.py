#!/usr/bin/env python3
"""Build model-wide GNN terrain and VRI proxy indicators from public data.

Terrain comes from the public AWS Open Data Terrarium tiles at zoom 12,
reprojected explicitly to EPSG:3005 and summarized over block polygons. Canopy
and stand indicators come from the existing public VRI-derived checkpoint.

The LidarBC fields are not used to fill missing public values. They are read
only to validate the public proxies on the bounded LiDAR pilot.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterio.mask
import rasterio.warp
import requests
from femic.lidar.terrain import build_terrain_products
from PIL import Image
from pyproj import Transformer
from rasterio.transform import from_origin
from shapely.geometry.base import BaseGeometry
from ws4.model.schema import validate_dataset

TILE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
WEB_MERCATOR_HALF = 20037508.342789244
WEB_MERCATOR_RES = 156543.03392
DEFAULT_ZOOM = 12
DEFAULT_RESOLUTION_M = 30.0
TERRAIN_SOURCE = "aws-terrarium-z12-30m"
VRI_SOURCE = "gnn-vri-checkpoint"
VRI_FIELDS = {
    "LABEL_HEIGHT": "vri_height_m",
    "CROWN_CLOSURE": "vri_crown_closure_pct",
    "LIVE_STAND_VOLUME_125": "vri_live_volume_125_m3_ha",
    "WHOLE_STEM_BIOMASS_PER_HA": "vri_whole_stem_biomass_ha",
}
PUBLIC_TERRAIN_FIELDS = (
    "terrain_source",
    "terrain_resolution_m",
    "terrain_method",
    "terrain_valid_fraction",
    "terrain_elev_mean_m",
    "terrain_slope_mean_pct",
    "terrain_slope_p90_pct",
    "terrain_slope_max_pct",
    "terrain_available",
)
PUBLIC_VRI_FIELDS = (
    "vri_source",
    "vri_join_method",
    *VRI_FIELDS.values(),
    "vri_available",
)


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _tile_xy(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    count = 2**zoom
    x = math.floor((lon + 180.0) / 360.0 * count)
    lat_rad = math.radians(lat)
    y = math.floor((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * count)
    return x, y


def _tile_range(
    bbox: tuple[float, float, float, float],
    zoom: int,
) -> tuple[int, int, int, int]:
    min_lon, min_lat, max_lon, max_lat = bbox
    x0, y0 = _tile_xy(min_lon, max_lat, zoom)
    x1, y1 = _tile_xy(max_lon, min_lat, zoom)
    return x0, y0, max(x0, x1), max(y0, y1)


def _decode_tile(data: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(data)).convert("RGB")
    rgb = np.asarray(image, dtype=np.float64)
    return rgb[:, :, 0] * 256.0 + rgb[:, :, 1] + rgb[:, :, 2] / 256.0 - 32768.0


def _download_tile(
    cache_dir: Path,
    *,
    zoom: int,
    x: int,
    y: int,
) -> tuple[tuple[int, int, int], str]:
    path = cache_dir / str(zoom) / str(x) / f"{y}.png"
    if path.is_file():
        data = path.read_bytes()
    else:
        last_error: Exception | None = None
        data = b""
        for _ in range(3):
            try:
                response = requests.get(
                    TILE_URL.format(z=zoom, x=x, y=y),
                    timeout=60,
                )
                response.raise_for_status()
                data = response.content
                break
            except Exception as exc:  # pragma: no cover - network boundary
                last_error = exc
        if not data:
            raise RuntimeError(f"unable to download Terrarium tile {zoom}/{x}/{y}: {last_error}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return (zoom, x, y), hashlib.sha256(data).hexdigest()


def _load_elevation_mosaic(
    *,
    aoi_path: Path,
    cache_dir: Path,
    zoom: int,
    workers: int,
) -> tuple[np.ndarray, rasterio.Affine, tuple[int, int, int, int], dict[str, object]]:
    aoi = gpd.read_file(aoi_path)
    aoi = aoi.to_crs(3005)
    geometry = aoi.geometry.union_all()
    to_wgs = Transformer.from_crs(3005, 4326, always_xy=True)
    b = geometry.bounds
    corners = [
        to_wgs.transform(b[0], b[1]),
        to_wgs.transform(b[2], b[1]),
        to_wgs.transform(b[0], b[3]),
        to_wgs.transform(b[2], b[3]),
    ]
    lons = [p[0] for p in corners]
    lats = [p[1] for p in corners]
    bbox = (min(lons), min(lats), max(lons), max(lats))
    x0, y0, x1, y1 = _tile_range(bbox, zoom)
    requests_to_make = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    tile_hashes: dict[str, str] = {}
    arrays: dict[tuple[int, int], np.ndarray] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_download_tile, cache_dir, zoom=zoom, x=x, y=y): (x, y)
            for x, y in requests_to_make
        }
        for future in as_completed(futures):
            (_, x, y), digest = future.result()
            arrays[(x, y)] = _decode_tile(
                (cache_dir / str(zoom) / str(x) / f"{y}.png").read_bytes()
            )
            tile_hashes[f"{zoom}/{x}/{y}"] = digest
    columns: list[np.ndarray] = []
    for x in range(x0, x1 + 1):
        columns.append(np.concatenate([arrays[(x, y)] for y in range(y0, y1 + 1)], axis=0))
    mosaic = np.concatenate(columns, axis=1)
    resolution = WEB_MERCATOR_RES / (2**zoom)
    transform = from_origin(
        x0 * 256 * resolution - WEB_MERCATOR_HALF,
        WEB_MERCATOR_HALF - y0 * 256 * resolution,
        resolution,
        resolution,
    )
    manifest = {
        "source": "AWS Open Data Terrarium terrain tiles",
        "url_template": TILE_URL,
        "zoom": zoom,
        "tile_range": [x0, y0, x1, y1],
        "tile_count": len(requests_to_make),
        "tile_sha256": tile_hashes,
        "crs": "EPSG:3857",
        "resolution_m_web_mercator": resolution,
    }
    return mosaic, transform, (x0, y0, x1, y1), manifest


def _write_dem_3005(
    *,
    elevation: np.ndarray,
    source_transform: rasterio.Affine,
    aoi_path: Path,
    output_path: Path,
    resolution_m: float,
) -> tuple[Path, dict[str, object]]:
    aoi = gpd.read_file(aoi_path).to_crs(3005)
    b = aoi.geometry.union_all().bounds
    left = math.floor(b[0] / resolution_m) * resolution_m
    bottom = math.floor(b[1] / resolution_m) * resolution_m
    right = math.ceil(b[2] / resolution_m) * resolution_m
    top = math.ceil(b[3] / resolution_m) * resolution_m
    width = int((right - left) / resolution_m)
    height = int((top - bottom) / resolution_m)
    target_transform = from_origin(left, top, resolution_m, resolution_m)
    target = np.full((height, width), np.nan, dtype=np.float32)
    rasterio.warp.reproject(
        source=elevation.astype(np.float32),
        destination=target,
        src_transform=source_transform,
        src_crs="EPSG:3857",
        dst_transform=target_transform,
        dst_crs="EPSG:3005",
        resampling=rasterio.warp.Resampling.bilinear,
        src_nodata=None,
        dst_nodata=np.nan,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(
        output_path,
        "w",
        driver="GTiff",
        height=height,
        width=width,
        count=1,
        dtype="float32",
        crs="EPSG:3005",
        transform=target_transform,
        nodata=np.nan,
        compress="deflate",
        predictor=3,
        tiled=True,
        blockxsize=512,
        blockysize=512,
        BIGTIFF="IF_SAFER",
    ) as destination:
        destination.write(target, 1)
        destination.update_tags(
            source="AWS Open Data Terrarium terrain tiles",
            source_zoom=12,
            aggregation="bilinear reprojection to EPSG:3005",
        )
    valid = np.isfinite(target)
    return output_path, {
        "path": str(output_path),
        "bounds": [left, bottom, right, top],
        "width": width,
        "height": height,
        "resolution_m": resolution_m,
        "valid_pixels": int(valid.sum()),
        "min_m": float(np.nanmin(target)),
        "max_m": float(np.nanmax(target)),
        "mean_m": float(np.nanmean(target)),
    }


def _masked_values(
    source: rasterio.DatasetReader,
    geometry: BaseGeometry,
) -> np.ndarray:
    try:
        masked, _ = rasterio.mask.mask(source, [geometry], crop=True, filled=False)
    except ValueError:
        return np.array([], dtype=float)
    values = np.asarray(masked[0].compressed(), dtype=float)
    return values[np.isfinite(values)]


def _sample_terrain_blocks(
    *,
    blocks: gpd.GeoDataFrame,
    dem_path: Path,
    slope_path: Path,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    with rasterio.open(dem_path) as dem, rasterio.open(slope_path) as slope:
        for _, record in blocks.iterrows():
            geometry = record.geometry
            block_id = record["BLOCK"]
            area_ha = float(geometry.area / 10_000.0)
            dem_values = _masked_values(dem, geometry)
            slope_values = _masked_values(slope, geometry)
            valid_pixels = int(min(dem_values.size, slope_values.size))
            valid_area_ha = valid_pixels * (dem.res[0] * dem.res[1]) / 10_000.0
            rows.append(
                {
                    "block_id": block_id,
                    "area_ha": area_ha,
                    "terrain_valid_pixels": valid_pixels,
                    "terrain_valid_area_ha": valid_area_ha,
                    "terrain_valid_fraction": min(
                        1.0,
                        valid_area_ha / area_ha if area_ha else 0.0,
                    ),
                    "terrain_elev_mean_m": (
                        float(np.mean(dem_values)) if dem_values.size else None
                    ),
                    "terrain_slope_mean_pct": (
                        float(np.mean(slope_values)) if slope_values.size else None
                    ),
                    "terrain_slope_p90_pct": (
                        float(np.percentile(slope_values, 90)) if slope_values.size else None
                    ),
                    "terrain_slope_max_pct": (
                        float(np.max(slope_values)) if slope_values.size else None
                    ),
                }
            )
    return pd.DataFrame(rows)


def _area_weighted_vri(
    geometry: BaseGeometry,
    checkpoint: gpd.GeoDataFrame,
) -> dict[str, object]:
    indices = checkpoint.sindex.query(geometry, predicate="intersects")
    if len(indices) == 0:
        return {
            **dict.fromkeys(VRI_FIELDS.values()),
            "vri_valid_area_ha": 0.0,
        }
    subset = checkpoint.iloc[indices]
    clipped = subset.geometry.intersection(geometry)
    valid = ~clipped.is_empty
    subset = subset.loc[valid].copy()
    clipped = clipped.loc[valid]
    if subset.empty:
        return {
            **dict.fromkeys(VRI_FIELDS.values()),
            "vri_valid_area_ha": 0.0,
        }
    areas = clipped.area / 10_000.0
    result: dict[str, object] = {"vri_valid_area_ha": float(areas.sum())}
    for source_field, output_field in VRI_FIELDS.items():
        values = pd.to_numeric(subset[source_field], errors="coerce")
        mask = values.notna()
        if not mask.any():
            result[output_field] = None
            continue
        value = float((values[mask] * areas[mask]).sum() / areas[mask].sum())
        if output_field == "vri_height_m":
            # The VRI label height is carried in decimetres in the checkpoint.
            value *= 0.1
        result[output_field] = value
    return result


def _sample_vri_blocks(
    *,
    blocks: gpd.GeoDataFrame,
    checkpoint: gpd.GeoDataFrame,
) -> pd.DataFrame:
    checkpoint = checkpoint.to_crs(3005)
    rows: list[dict[str, object]] = []
    for _, record in blocks.iterrows():
        values = _area_weighted_vri(record.geometry, checkpoint)
        rows.append({"block_id": record["BLOCK"], **values})
    return pd.DataFrame(rows)


def _read_checkpoint(path: Path) -> gpd.GeoDataFrame:
    if path.suffix == ".feather":
        frame = pd.read_feather(path)
        if "geometry" not in frame.columns:
            raise ValueError(f"checkpoint has no geometry: {path}")
        from shapely import wkb

        frame["geometry"] = frame["geometry"].map(
            lambda value: (
                wkb.loads(bytes(value)) if isinstance(value, (bytes, bytearray)) else value
            )
        )
        return gpd.GeoDataFrame(frame, geometry="geometry", crs="EPSG:3005")
    return gpd.read_file(path).to_crs(3005)


def _merge_public_blocks(
    *,
    terrain: pd.DataFrame,
    vri: pd.DataFrame,
) -> pd.DataFrame:
    merged = terrain.merge(vri, on="block_id", how="outer", validate="one_to_one")
    merged["terrain_source"] = TERRAIN_SOURCE
    merged["terrain_resolution_m"] = DEFAULT_RESOLUTION_M
    merged["terrain_method"] = "block_zonal_terrarium_horn"
    merged["terrain_available"] = merged["terrain_slope_mean_pct"].notna()
    merged["vri_source"] = VRI_SOURCE
    merged["vri_join_method"] = "block_area_weighted_vri"
    merged["vri_available"] = merged["vri_height_m"].notna()
    return merged


def _validate_against_lidar(
    *,
    dataset: Path,
    public_blocks: pd.DataFrame,
) -> dict[str, object]:
    blocks = pd.read_parquet(dataset / "blocks.parquet")
    existing_public = [column for column in public_blocks.columns if column != "block_id"]
    blocks = blocks.drop(
        columns=[column for column in existing_public if column in blocks.columns],
        errors="ignore",
    )
    joined = blocks.merge(public_blocks, on="block_id", how="left", validate="many_to_one")
    joined = joined[joined["lidar_available"].fillna(False)]
    comparisons = {
        "terrain_slope_mean_vs_lidar_slope_mean": (
            "terrain_slope_mean_pct",
            "lidar_slope_mean",
        ),
        "terrain_slope_p90_vs_lidar_slope_p95": (
            "terrain_slope_p90_pct",
            "lidar_slope_p95",
        ),
        "vri_height_vs_lidar_chm_mean": ("vri_height_m", "lidar_chm_mean"),
        "vri_height_vs_lidar_chm_p95": ("vri_height_m", "lidar_chm_p95"),
    }
    result: dict[str, object] = {"n_blocks": len(joined), "comparisons": {}}
    for name, (proxy_field, lidar_field) in comparisons.items():
        frame = joined[[proxy_field, lidar_field]].apply(pd.to_numeric, errors="coerce").dropna()
        if frame.empty:
            result["comparisons"][name] = {"n": 0}
            continue
        proxy = frame[proxy_field].to_numpy()
        lidar = frame[lidar_field].to_numpy()
        delta = proxy - lidar
        result["comparisons"][name] = {
            "n": len(frame),
            "bias_proxy_minus_lidar": float(np.mean(delta)),
            "mae": float(np.mean(np.abs(delta))),
            "rmse": float(np.sqrt(np.mean(delta**2))),
            "pearson_r": float(np.corrcoef(proxy, lidar)[0, 1]) if len(frame) > 1 else None,
            "proxy_mean": float(np.mean(proxy)),
            "lidar_mean": float(np.mean(lidar)),
        }
    return result


def _integrate_public_fields(
    *,
    dataset: Path,
    public_blocks: pd.DataFrame,
    backup: Path,
) -> dict[str, object]:
    if not backup.exists():
        shutil.copytree(dataset, backup)
    fragments = pd.read_parquet(dataset / "fragments.parquet")
    blocks = pd.read_parquet(dataset / "blocks.parquet")
    public_fields = [
        *PUBLIC_TERRAIN_FIELDS,
        *PUBLIC_VRI_FIELDS,
        "terrain_valid_pixels",
        "terrain_valid_area_ha",
        "vri_valid_area_ha",
    ]
    blocks = blocks.drop(columns=[c for c in public_fields if c in blocks.columns], errors="ignore")
    fragments = fragments.drop(
        columns=[c for c in public_fields if c in fragments.columns],
        errors="ignore",
    )
    block_values = public_blocks[["block_id", *public_fields]].drop_duplicates("block_id")
    blocks = blocks.merge(block_values, on="block_id", how="left", validate="many_to_one")
    fragments = fragments.merge(block_values, on="block_id", how="left", validate="many_to_one")
    blocks.to_parquet(dataset / "blocks.parquet", index=False)
    fragments.to_parquet(dataset / "fragments.parquet", index=False)
    manifest_path = dataset / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    metadata = dict(manifest.get("metadata") or {})
    metadata["public_indicators"] = {
        "terrain_source": TERRAIN_SOURCE,
        "terrain_resolution_m": DEFAULT_RESOLUTION_M,
        "terrain_method": "block_zonal_terrarium_horn",
        "vri_source": VRI_SOURCE,
        "vri_join_method": "block_area_weighted_vri",
        "fragment_fields": [c for c in public_fields if c in fragments.columns],
        "block_fields": [c for c in public_fields if c in blocks.columns],
        "generated_utc": _now(),
    }
    manifest["metadata"] = metadata
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    errors = validate_dataset(dataset)
    if errors:
        raise ValueError("dataset validation failed: " + "; ".join(errors))
    return {
        "fragments": len(fragments),
        "blocks": len(blocks),
        "fragment_fields": [c for c in public_fields if c in fragments.columns],
        "block_fields": [c for c in public_fields if c in blocks.columns],
        "validation_errors": errors,
        "fragment_terrain_available": int(fragments["terrain_available"].fillna(False).sum()),
        "fragment_vri_available": int(fragments["vri_available"].fillna(False).sum()),
        "block_terrain_available": int(blocks["terrain_available"].fillna(False).sum()),
        "block_vri_available": int(blocks["vri_available"].fillna(False).sum()),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aoi", type=Path, default=Path("data/source/aoi/gnn_full.gpkg"))
    parser.add_argument(
        "--fragments",
        type=Path,
        default=Path("output/patchworks_gnn/fragments_merged/fragments.shp"),
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("data/gnn_combined_checkpoint.feather"),
    )
    parser.add_argument("--dataset", type=Path, default=Path("runtime/gnn/matrix"))
    parser.add_argument(
        "--backup",
        type=Path,
        default=Path("runtime/gnn/matrix_pre_public"),
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("runtime/gnn/public_terrain/terrarium_z12"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runtime/gnn/public_terrain"),
    )
    parser.add_argument("--zoom", type=int, default=DEFAULT_ZOOM)
    parser.add_argument("--resolution", type=float, default=DEFAULT_RESOLUTION_M)
    parser.add_argument("--workers", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    """Build, validate, and integrate the public terrain/VRI proxies."""
    args = _parse_args()
    if args.zoom < 0 or args.resolution <= 0:
        raise ValueError("zoom must be >= 0 and resolution must be positive")
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = args.cache_dir.expanduser().resolve()
    elevation, source_transform, tile_range, tile_manifest = _load_elevation_mosaic(
        aoi_path=args.aoi,
        cache_dir=cache_dir,
        zoom=args.zoom,
        workers=args.workers,
    )
    dem_path, dem_summary = _write_dem_3005(
        elevation=elevation,
        source_transform=source_transform,
        aoi_path=args.aoi,
        output_path=output_dir / f"terrarium_z{args.zoom}_{args.resolution:g}m_dem.tif",
        resolution_m=args.resolution,
    )
    terrain_report = build_terrain_products(
        dem_path,
        output_dir / "terrain",
        generated_utc=_now(),
    )
    slope_path = terrain_report.products[0].path
    support = gpd.read_file(args.fragments)
    support = (
        support.set_crs(3005, allow_override=True) if support.crs is None else support.to_crs(3005)
    )
    blocks = support[["BLOCK", "geometry"]].dissolve(by="BLOCK", as_index=False)
    blocks = blocks.rename(columns={"BLOCK": "BLOCK"})
    terrain_blocks = _sample_terrain_blocks(
        blocks=blocks,
        dem_path=dem_path,
        slope_path=slope_path,
    )
    checkpoint = _read_checkpoint(args.checkpoint)
    vri_blocks = _sample_vri_blocks(blocks=blocks, checkpoint=checkpoint)
    public_blocks = _merge_public_blocks(terrain=terrain_blocks, vri=vri_blocks)
    public_path = output_dir / "public_block_indicators.csv"
    public_blocks.to_csv(public_path, index=False)
    validation = _validate_against_lidar(
        dataset=args.dataset,
        public_blocks=public_blocks,
    )
    integration = _integrate_public_fields(
        dataset=args.dataset,
        public_blocks=public_blocks,
        backup=args.backup,
    )
    summary = {
        "generated_utc": _now(),
        "tile_manifest": tile_manifest,
        "tile_range": list(tile_range),
        "dem": dem_summary,
        "terrain": terrain_report.to_dict(),
        "public_blocks": {
            "path": str(public_path),
            "rows": len(public_blocks),
            "terrain_available": int(public_blocks["terrain_available"].sum()),
            "vri_available": int(public_blocks["vri_available"].sum()),
        },
        "validation": validation,
        "integration": integration,
    }
    summary_path = output_dir / "public_indicator_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
