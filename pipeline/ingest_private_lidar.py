#!/usr/bin/env python3
"""Verify and inventory a private LAS/LAZ drop without modifying it.

The raw point files are private. This script reads LAS/LAZ headers only, checks an
optional SHA-256 manifest, builds a tile index, and reports coverage against the
GNN AOI and the P13 request table. It writes:

- a private summary and tile table under ``--output-dir`` (do not publish);
- an optional public summary and tile index under ``--public-dir`` with no source
  filenames or paths.

It never copies, moves, deletes, or publishes a raw point file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import geopandas as gpd
import laspy
import pandas as pd
from pyproj import CRS, Transformer
from shapely.geometry import GeometryCollection, Point, box

HASH_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+)$")


def parse_args() -> argparse.Namespace:
    """Return command-line options.

    Returns
    -------
    argparse.Namespace
        Parsed options.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--aoi", type=Path, required=True)
    parser.add_argument("--request-csv", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--public-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--verify-hashes", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    return parser.parse_args()


def find_lidar_files(root: Path) -> list[Path]:
    """Return the LAS/LAZ files under ``root``.

    Parameters
    ----------
    root : pathlib.Path
        Uploaded dataset root.

    Returns
    -------
    list[pathlib.Path]
        Sorted point files.
    """
    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".las", ".laz"}
    ]
    return sorted(files)


def sha256(path: Path) -> str:
    """Return the SHA-256 of a file.

    Parameters
    ----------
    path : pathlib.Path
        File to hash.

    Returns
    -------
    str
        Hex digest.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest(path: Path) -> dict[str, str]:
    """Parse a ``SHA256SUMS`` file.

    Parameters
    ----------
    path : pathlib.Path
        Manifest path.

    Returns
    -------
    dict[str, str]
        Relative path to SHA-256.
    """
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HASH_LINE.match(line.strip())
        if not match:
            continue
        digest, relative = match.groups()
        entries[relative.lstrip("./")] = digest.lower()
    return entries


def vertical_datum(crs: CRS | None) -> str:
    """Return the vertical CRS name, or ``unknown``.

    Parameters
    ----------
    crs : pyproj.CRS or None
        Parsed file CRS.

    Returns
    -------
    str
        Vertical datum name.
    """
    if crs is None:
        return "unknown"
    for sub_crs in crs.sub_crs_list:
        if sub_crs.is_vertical:
            return sub_crs.name
    return "unknown"


def bounds_3005(mins: list[float], maxs: list[float], crs: CRS | None) -> tuple[list[float], bool]:
    """Transform native bounds to EPSG:3005.

    Parameters
    ----------
    mins : list[float]
        Native minimum x/y/z.
    maxs : list[float]
        Native maximum x/y/z.
    crs : pyproj.CRS or None
        Native CRS.

    Returns
    -------
    tuple[list[float], bool]
        Bounds ``[minx, miny, maxx, maxy]`` and a transform-success flag.
    """
    if crs is None:
        return [float(mins[0]), float(mins[1]), float(maxs[0]), float(maxs[1])], False
    target = CRS.from_epsg(3005)
    if crs.equals(target):
        return [float(mins[0]), float(mins[1]), float(maxs[0]), float(maxs[1])], True
    transformer = Transformer.from_crs(crs, target, always_xy=True)
    corners = [
        (mins[0], mins[1]),
        (mins[0], maxs[1]),
        (maxs[0], mins[1]),
        (maxs[0], maxs[1]),
    ]
    transformed = [transformer.transform(x, y) for x, y in corners]
    xs = [point[0] for point in transformed]
    ys = [point[1] for point in transformed]
    return [min(xs), min(ys), max(xs), max(ys)], True


def header_record(path: Path, tile_id: str) -> dict[str, Any]:
    """Read a LAS/LAZ header and return a tile record.

    Parameters
    ----------
    path : pathlib.Path
        Point file.
    tile_id : str
        Stable public tile identifier.

    Returns
    -------
    dict[str, Any]
        Header-derived tile record.
    """
    with laspy.open(path) as reader:
        header = reader.header
        try:
            crs = header.parse_crs()
        except Exception:  # malformed or missing CRS VLRs
            crs = None
        bounds, transformed = bounds_3005(header.mins, header.maxs, crs)
        point_count = int(header.point_count)
        area_m2 = max((bounds[2] - bounds[0]) * (bounds[3] - bounds[1]), 1.0)
        return {
            "tile_id": tile_id,
            "file_name": path.name,
            "relative_path": str(path),
            "size_bytes": path.stat().st_size,
            "point_count": point_count,
            "crs_epsg": crs.to_epsg() if crs is not None else None,
            "crs_name": crs.name if crs is not None else None,
            "vertical_datum": vertical_datum(crs),
            "bounds_epsg3005": bounds,
            "bounds_transformed": transformed,
            "area_ha": area_m2 / 10000.0,
            "density_ppm2": point_count / area_m2,
        }


def manifest_status(
    root: Path, files: list[Path], manifest: Path | None, verify_hashes: bool
) -> dict[str, Any]:
    """Compare the drop against its SHA-256 manifest.

    Parameters
    ----------
    root : pathlib.Path
        Uploaded dataset root.
    files : list[pathlib.Path]
        Point files.
    manifest : pathlib.Path or None
        Manifest path.
    verify_hashes : bool
        Whether to compute SHA-256 for every file.

    Returns
    -------
    dict[str, Any]
        Manifest status.
    """
    if manifest is None or not manifest.is_file():
        return {
            "manifest_present": False,
            "entries": 0,
            "missing_files": [],
            "extra_files": [path.relative_to(root).as_posix() for path in files],
            "hash_mismatches": [],
            "hashes_checked": 0,
        }
    entries = parse_manifest(manifest)
    relative_files = {path.relative_to(root).as_posix(): path for path in files}
    missing = sorted(set(entries) - set(relative_files))
    extra = sorted(set(relative_files) - set(entries))
    mismatches: list[str] = []
    checked = 0
    if verify_hashes:
        for relative, path in relative_files.items():
            if relative in entries:
                checked += 1
                if sha256(path) != entries[relative]:
                    mismatches.append(relative)
    return {
        "manifest_present": True,
        "entries": len(entries),
        "missing_files": missing,
        "extra_files": extra,
        "hash_mismatches": sorted(mismatches),
        "hashes_checked": checked,
    }


def coverage_summary(
    tiles: list[dict[str, Any]], aoi: gpd.GeoDataFrame, request: pd.DataFrame | None
) -> dict[str, Any]:
    """Return AOI and P13 plot coverage.

    Parameters
    ----------
    tiles : list[dict[str, Any]]
        Tile records with ``bounds_epsg3005``.
    aoi : geopandas.GeoDataFrame
        GNN AOI.
    request : pandas.DataFrame or None
        P13 request table.

    Returns
    -------
    dict[str, Any]
        Coverage summary.
    """
    aoi_geometry = aoi.geometry.union_all()
    valid_tiles = [tile for tile in tiles if tile["bounds_transformed"]]
    boxes = [box(*tile["bounds_epsg3005"]) for tile in valid_tiles]
    if boxes:
        footprint = gpd.GeoSeries(boxes, crs=3005).union_all().intersection(aoi_geometry)
    else:
        footprint = GeometryCollection()
    summary: dict[str, Any] = {
        "aoi_ha": float(aoi_geometry.area / 10000.0),
        "footprint_ha": float(footprint.area / 10000.0),
        "footprint_pct": float(footprint.area / aoi_geometry.area * 100.0),
        "untransformed_tiles": len(tiles) - len(valid_tiles),
        "p13_plots_covered": {},
        "p13_plot_count": 0,
        "p13_high_covered": 0,
    }
    if request is None or request.empty:
        return summary

    covered: dict[str, list[str]] = {}
    for row in request.itertuples(index=False):
        point = Point(float(row.x_epsg3005), float(row.y_epsg3005))
        if any(tile_box.contains(point) for tile_box in boxes):
            priority = str(row.request_priority)
            covered.setdefault(priority, []).append(str(row.site_identifier))
    summary["p13_plots_covered"] = {key: sorted(value) for key, value in covered.items()}
    summary["p13_plot_count"] = int(sum(len(value) for value in covered.values()))
    summary["p13_high_covered"] = len(covered.get("high", []))
    return summary


def main() -> None:
    """Run the ingest audit and write private and public outputs."""
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = find_lidar_files(args.root)
    if args.max_files > 0:
        files = files[: args.max_files]
    if not files:
        raise SystemExit(f"no .las/.laz files found under {args.root}")

    tiles = [header_record(path, f"tile_{index:06d}") for index, path in enumerate(files)]
    manifest = args.manifest or args.root / "SHA256SUMS.txt"
    manifest_result = manifest_status(args.root, files, manifest, args.verify_hashes)
    aoi = gpd.read_file(args.aoi)
    request = pd.read_csv(args.request_csv) if args.request_csv is not None else None
    coverage = coverage_summary(tiles, aoi, request)

    private_summary = {
        "privacy": "private-raw",
        "root": str(args.root),
        "file_count": len(tiles),
        "total_bytes": sum(tile["size_bytes"] for tile in tiles),
        "total_points": sum(tile["point_count"] for tile in tiles),
        "tiles": tiles,
        "manifest": manifest_result,
        "coverage": coverage,
    }
    args.output_dir.joinpath("summary_private.json").write_text(
        json.dumps(private_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    pd.DataFrame(tiles).to_csv(args.output_dir / "tiles_private.csv", index=False)

    if args.public_dir is not None:
        args.public_dir.mkdir(parents=True, exist_ok=True)
        public_tiles = [
            {
                "tile_id": tile["tile_id"],
                "point_count": tile["point_count"],
                "crs_epsg": tile["crs_epsg"],
                "vertical_datum": tile["vertical_datum"],
                "bounds_epsg3005": tile["bounds_epsg3005"],
                "area_ha": tile["area_ha"],
                "density_ppm2": tile["density_ppm2"],
            }
            for tile in tiles
        ]
        public_summary = {
            "privacy": "derived-public",
            "file_count": len(tiles),
            "total_bytes": sum(tile["size_bytes"] for tile in tiles),
            "total_points": sum(tile["point_count"] for tile in tiles),
            "crs_epsg": sorted({tile["crs_epsg"] for tile in tiles if tile["crs_epsg"]}),
            "vertical_datum": sorted({tile["vertical_datum"] for tile in tiles}),
            "manifest": {
                "manifest_present": manifest_result["manifest_present"],
                "entries": manifest_result["entries"],
                "missing_files": len(manifest_result["missing_files"]),
                "extra_files": len(manifest_result["extra_files"]),
                "hash_mismatches": len(manifest_result["hash_mismatches"]),
                "hashes_checked": manifest_result["hashes_checked"],
            },
            "coverage": coverage,
            "tiles": public_tiles,
        }
        args.public_dir.joinpath("summary_public.json").write_text(
            json.dumps(public_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        pd.DataFrame(public_tiles).to_csv(args.public_dir / "tile_index_public.csv", index=False)
        features = [
            {
                "type": "Feature",
                "properties": {
                    "tile_id": tile["tile_id"],
                    "point_count": tile["point_count"],
                    "crs_epsg": tile["crs_epsg"],
                    "area_ha": tile["area_ha"],
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [tile["bounds_epsg3005"][0], tile["bounds_epsg3005"][1]],
                            [tile["bounds_epsg3005"][2], tile["bounds_epsg3005"][1]],
                            [tile["bounds_epsg3005"][2], tile["bounds_epsg3005"][3]],
                            [tile["bounds_epsg3005"][0], tile["bounds_epsg3005"][3]],
                            [tile["bounds_epsg3005"][0], tile["bounds_epsg3005"][1]],
                        ]
                    ],
                },
            }
            for tile in public_tiles
        ]
        args.public_dir.joinpath("tile_index_public.geojson").write_text(
            json.dumps({"type": "FeatureCollection", "features": features}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(public_summary, indent=2, sort_keys=True))
    else:
        print(json.dumps(private_summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
