#!/usr/bin/env python3
"""Register, map, and integrate a FEMIC LiDAR bundle into the GNN dataset.

The compiled GNN dataset can contain the same block on multiple track rows.
WS4 keeps fragment mapping one-to-one and block mapping many-to-one; this
driver then propagates each block-level value to fragments that only have the
block support. No model, curve, THLB, or AAC value is changed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from ws4.io.lidar import (
    integrate_lidar_mapping_into_dataset,
    load_registered_femic_lidar_bundle,
    map_femic_lidar_to_fragments,
    read_registered_femic_lidar,
    register_femic_lidar_bundle,
    write_lidar_mapping,
)
from ws4.model.schema import validate_dataset

KEEP_FRAGMENT_STATS = (
    "slope_valid_pixels",
    "slope_mean",
    "slope_p95",
    "chm_valid_pixels",
    "chm_mean",
    "chm_p95",
    "chm_cover_ge_2",
    "chm_cover_ge_5",
    "chm_cover_ge_10",
    "chm_cover_ge_20",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_support_keys(
    path: Path,
    *,
    id_field: str,
    target_id: str,
    block_field: str,
    area_field: str,
) -> None:
    """Normalize custom support field names to the WS4 integration keys."""
    frame = pd.read_csv(path)
    rename = {id_field: target_id}
    if block_field in frame.columns and block_field != target_id:
        rename[block_field] = "block_id"
    if area_field in frame.columns:
        rename[area_field] = "area_ha"
    frame = frame.rename(columns=rename)
    if target_id not in frame.columns:
        raise ValueError(f"mapping is missing normalized key {target_id!r}: {path}")
    frame.to_csv(path, index=False)


def _filter_mapping(
    source: Path,
    destination: Path,
    *,
    key: str,
    pixel_ha: float,
) -> pd.DataFrame:
    frame = pd.read_csv(source)
    keep = [key]
    if "block_id" in frame.columns and key != "block_id":
        keep.append("block_id")
    if "area_ha" in frame.columns:
        keep.append("area_ha")
    keep.extend(column for column in frame.columns if column in KEEP_FRAGMENT_STATS)
    missing = [column for column in KEEP_FRAGMENT_STATS if column not in keep]
    if missing:
        raise ValueError(f"mapping is missing expected fields: {', '.join(missing)}")
    filtered = frame[keep].copy()
    valid_pixels = filtered[["slope_valid_pixels", "chm_valid_pixels"]].fillna(0).max(axis=1)
    filtered["available"] = valid_pixels > 0
    filtered["supported_ha"] = valid_pixels * pixel_ha
    filtered.to_csv(destination, index=False)
    return filtered


def _propagate_blocks_to_fragments(dataset: Path) -> dict[str, int]:
    fragments_path = dataset / "fragments.parquet"
    blocks_path = dataset / "blocks.parquet"
    fragments = pd.read_parquet(fragments_path)
    blocks = pd.read_parquet(blocks_path)
    lidar_columns = sorted(column for column in fragments.columns if column.startswith("lidar_"))
    if not lidar_columns:
        raise ValueError("fragments table has no lidar_* fields")
    missing = [column for column in lidar_columns if column not in blocks.columns]
    if missing:
        raise ValueError(f"blocks table is missing: {', '.join(missing)}")

    block_values = blocks[["block_id", *lidar_columns]].drop_duplicates()
    if "lidar_available" in block_values.columns:
        block_values = block_values[
            block_values["lidar_available"].fillna(False).astype(bool)
        ].copy()
    duplicate_conflicts = (
        block_values.groupby("block_id", dropna=False)[lidar_columns].nunique(dropna=False).gt(1)
    )
    if duplicate_conflicts.any().any():
        conflicts = duplicate_conflicts.any(axis=1)
        raise ValueError(
            "block-level LiDAR values differ across track rows for block_id(s): "
            + ", ".join(str(value) for value in conflicts[conflicts].index[:10])
        )
    block_values = block_values.drop_duplicates("block_id")

    original = fragments.copy()
    available_before = (
        fragments.get("lidar_available", pd.Series(False, index=fragments.index))
        .fillna(False)
        .astype(bool)
    )
    merged = fragments.merge(
        block_values.rename(columns={column: f"__{column}" for column in lidar_columns}),
        on="block_id",
        how="left",
        validate="many_to_one",
    )
    for column in lidar_columns:
        block_column = f"__{column}"
        if column == "lidar_available":
            merged[column] = merged[column].fillna(False).astype(bool) | merged[
                block_column
            ].fillna(False).astype(bool)
        elif column == "lidar_supported_ha":
            merged[column] = np.maximum(
                merged[column].fillna(0.0).astype(float),
                merged[block_column].fillna(0.0).astype(float),
            )
        else:
            merged[column] = merged[column].combine_first(merged[block_column])
        merged = merged.drop(columns=[block_column])
    if len(merged) != len(original):
        raise ValueError("fragment propagation changed the row count")
    available_after = merged["lidar_available"].fillna(False).astype(bool)
    filled_fragments = int((~available_before & available_after).sum())
    merged.to_parquet(fragments_path, index=False)
    return {
        "fragments": len(merged),
        "fragments_filled_from_blocks": filled_fragments,
        "fields": len(lidar_columns),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("runtime/gnn/matrix"),
    )
    parser.add_argument(
        "--bundle",
        type=Path,
        default=Path("data/lidar/products/lidarbc-gnn-10m"),
    )
    parser.add_argument(
        "--fragments",
        type=Path,
        default=Path("output/patchworks_gnn/fragments_merged/fragments.shp"),
    )
    parser.add_argument(
        "--mapping-dir",
        type=Path,
        default=Path("data/lidar/gnn_mapping"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("data/lidar/gnn_10m/integration_summary.json"),
    )
    parser.add_argument(
        "--fragment-id-field",
        default="FRAGMENT_I",
    )
    parser.add_argument("--block-id-field", default="BLOCK")
    parser.add_argument("--area-field", default="AREA_HA")
    parser.add_argument(
        "--backup",
        type=Path,
        default=Path("runtime/gnn/matrix_pre_lidar"),
        help="One-time dataset backup; skipped if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    """Register, map, integrate, and validate the GNN LiDAR fields."""
    args = _parse_args()
    dataset = args.dataset.expanduser().resolve()
    bundle_dir = args.bundle.expanduser().resolve()
    fragments = args.fragments.expanduser().resolve()
    mapping_dir = args.mapping_dir.expanduser().resolve()
    mapping_dir.mkdir(parents=True, exist_ok=True)
    if not dataset.is_dir():
        raise FileNotFoundError(f"dataset not found: {dataset}")
    if not bundle_dir.is_dir():
        raise FileNotFoundError(f"bundle not found: {bundle_dir}")
    if not fragments.is_file():
        raise FileNotFoundError(f"fragment support not found: {fragments}")
    if args.backup is not None and not args.backup.exists():
        shutil.copytree(dataset, args.backup)
        backup_note = f"created {args.backup}"
    else:
        backup_note = f"kept existing {args.backup}"

    registration = read_registered_femic_lidar(dataset)
    if registration is None:
        register_femic_lidar_bundle(dataset, bundle_dir)
    else:
        registered_bundle = Path(str(registration.get("bundle_dir", "")))
        if not registered_bundle.is_absolute():
            registered_bundle = dataset / registered_bundle
        if registered_bundle.resolve() != bundle_dir:
            raise ValueError(
                f"dataset is already pinned to a different LiDAR bundle: {registered_bundle}"
            )
    bundle = load_registered_femic_lidar_bundle(dataset)
    mapping = map_femic_lidar_to_fragments(
        bundle,
        fragments,
        products=("slope", "chm"),
        statistics=(
            "mean",
            "p95",
            "cover_ge_2",
            "cover_ge_5",
            "cover_ge_10",
            "cover_ge_20",
        ),
        id_field=args.fragment_id_field,
        block_field=args.block_id_field,
        area_field=args.area_field,
    )
    paths = write_lidar_mapping(mapping, mapping_dir)
    _normalize_support_keys(
        paths["fragments"],
        id_field=args.fragment_id_field,
        target_id="fragment_id",
        block_field=args.block_id_field,
        area_field=args.area_field,
    )
    _normalize_support_keys(
        paths["blocks"],
        id_field=args.block_id_field,
        target_id="block_id",
        block_field=args.block_id_field,
        area_field=args.area_field,
    )
    filtered_fragments = mapping_dir / "lidar_fragments_filtered.csv"
    filtered_blocks = mapping_dir / "lidar_blocks_filtered.csv"
    resolution = bundle.products["chm"].resolution_m or 10.0
    pixel_ha = resolution * resolution / 10_000.0
    _filter_mapping(
        paths["fragments"],
        filtered_fragments,
        key="fragment_id",
        pixel_ha=pixel_ha,
    )
    _filter_mapping(
        paths["blocks"],
        filtered_blocks,
        key="block_id",
        pixel_ha=pixel_ha,
    )

    integration = integrate_lidar_mapping_into_dataset(
        dataset,
        filtered_fragments,
        block_mapping_path=filtered_blocks,
        overwrite=True,
    )
    integrated_fragments = pd.read_parquet(dataset / "fragments.parquet")
    direct_fragments_available = int(
        integrated_fragments.get("lidar_available", pd.Series(dtype=bool)).fillna(False).sum()
    )
    direct_fragment_supported_ha = float(
        integrated_fragments.get("lidar_supported_ha", pd.Series(dtype=float)).fillna(0.0).sum()
    )
    propagation = _propagate_blocks_to_fragments(dataset)
    errors = validate_dataset(dataset)
    if errors:
        raise ValueError("dataset validation failed: " + "; ".join(errors))

    fragments_table = pd.read_parquet(dataset / "fragments.parquet")
    blocks_table = pd.read_parquet(dataset / "blocks.parquet")
    coverage = {
        column: {
            "fragments": int(fragments_table[column].notna().sum()),
            "blocks": int(blocks_table[column].notna().sum()),
        }
        for column in sorted(
            column for column in fragments_table.columns if column.startswith("lidar_")
        )
    }
    coverage_summary = {
        "fragments_with_direct_support": direct_fragments_available,
        "fragments_available": int(
            fragments_table.get("lidar_available", pd.Series(dtype=bool)).fillna(False).sum()
        ),
        "direct_fragment_supported_ha": direct_fragment_supported_ha,
        "blocks_available": int(
            blocks_table.get("lidar_available", pd.Series(dtype=bool)).fillna(False).sum()
        ),
        "block_supported_ha": float(
            blocks_table.get("lidar_supported_ha", pd.Series(dtype=float)).fillna(0.0).sum()
        ),
    }
    summary = {
        "generated_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "dataset": str(dataset),
        "backup": backup_note,
        "bundle": {
            "bundle_dir": str(bundle.bundle_dir),
            "bundle_id": bundle.bundle_id,
            "bundle_version": bundle.bundle_version,
            "manifest_sha256": bundle.manifest_sha256,
        },
        "fragment_support": {
            "path": str(fragments),
            "sha256": _sha256(fragments),
            "fragment_id_field": args.fragment_id_field,
            "block_id_field": args.block_id_field,
            "area_field": args.area_field,
        },
        "mapping": {
            "directory": str(mapping_dir),
            "fragment_rows": len(mapping.fragments),
            "block_rows": len(mapping.blocks),
            "products": list(mapping.products),
            "statistics": list(mapping.statistics),
            "warnings": list(mapping.warnings),
        },
        "integration": integration.to_dict(),
        "propagation": propagation,
        "validation_errors": errors,
        "coverage_summary": coverage_summary,
        "coverage": coverage,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
