#!/usr/bin/env python3
"""Map the checkpoint-level revenue screen to GNN blocks.

The existing screen is per Vegetation Resources Inventory polygon. This script
allocates each screened polygon's volume, THLB area, and net revenue to the
blocks that overlap it. Shared road, landing, terminal, and overhead costs are
not allocated here; the result is a partial direct-cost gate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import wkb

EXPECTED_SCREEN_FIELDS = (
    "thlb_ha",
    "volume_m3",
    "net_base_per_m3",
    "operability",
)


def _load_checkpoint(path: Path) -> gpd.GeoDataFrame:
    frame = pd.read_feather(path)
    if "geometry" not in frame.columns:
        raise ValueError(f"checkpoint has no geometry: {path}")
    frame["geometry"] = frame["geometry"].map(
        lambda value: wkb.loads(bytes(value)) if isinstance(value, (bytes, bytearray)) else value
    )
    return gpd.GeoDataFrame(frame, geometry="geometry", crs="EPSG:3005")


def _screen_with_ids(screen_path: Path, checkpoint_path: Path) -> gpd.GeoDataFrame:
    screen = pd.read_csv(screen_path)
    missing = [field for field in EXPECTED_SCREEN_FIELDS if field not in screen.columns]
    if missing:
        raise ValueError(f"screen is missing fields: {', '.join(missing)}")
    checkpoint = _load_checkpoint(checkpoint_path)
    calibrated = pd.to_numeric(checkpoint["thlb_raw_calibrated"], errors="coerce").fillna(0.0)
    checkpoint = checkpoint[calibrated > 0].copy().reset_index(drop=True)
    if len(checkpoint) != len(screen):
        raise ValueError(
            f"screen rows ({len(screen)}) do not match checkpoint THLB rows "
            f"({len(checkpoint)}); rerun the screen with feature IDs"
        )
    area_ha = pd.to_numeric(checkpoint["FEATURE_AREA_SQM"], errors="coerce") / 10_000.0
    thlb_ha = (
        area_ha
        * pd.to_numeric(checkpoint["thlb_raw_calibrated"], errors="coerce").fillna(0.0)
        / 100.0
    )
    volume = (
        pd.to_numeric(checkpoint["LIVE_STAND_VOLUME_125"], errors="coerce").fillna(0.0) * thlb_ha
    )
    if not np.allclose(screen["thlb_ha"].to_numpy(), thlb_ha.to_numpy(), rtol=1e-9, atol=1e-9):
        raise ValueError("screen THLB rows do not align with the checkpoint order")
    if not np.allclose(screen["volume_m3"].to_numpy(), volume.to_numpy(), rtol=1e-9, atol=1e-9):
        raise ValueError("screen volume rows do not align with the checkpoint order")
    matched = checkpoint[
        [
            "FEATURE_ID",
            "POLYGON_ID",
            "tsa_code",
            "au",
            "stratum",
            "si_level",
            "geometry",
        ]
    ].copy()
    for field in EXPECTED_SCREEN_FIELDS:
        matched[field] = screen[field].to_numpy()
    matched["screen_area_ha"] = area_ha.to_numpy()
    return gpd.GeoDataFrame(matched, geometry="geometry", crs="EPSG:3005")


def _block_support(path: Path) -> gpd.GeoDataFrame:
    support = gpd.read_file(path)
    support = (
        support.set_crs(3005, allow_override=True) if support.crs is None else support.to_crs(3005)
    )
    blocks = support[["BLOCK", "TSA", "AU", "geometry"]].dissolve(
        by=["BLOCK", "TSA", "AU"], as_index=False
    )
    blocks = blocks.rename(columns={"BLOCK": "block_id", "TSA": "block_tsa", "AU": "block_au"})
    blocks["block_area_ha"] = blocks.geometry.area / 10_000.0
    return blocks


def _allocate(screen: gpd.GeoDataFrame, blocks: gpd.GeoDataFrame) -> pd.DataFrame:
    pieces = gpd.overlay(screen, blocks, how="intersection", keep_geom_type=True)
    pieces["clip_area_ha"] = pieces.geometry.area / 10_000.0
    pieces = pieces[pieces["clip_area_ha"] > 0].copy()
    # If block support overlaps, normalise within each screened polygon so the
    # screened THLB, volume, and net revenue are allocated exactly once.
    pieces["screen_clip_ha"] = pieces.groupby("FEATURE_ID")["clip_area_ha"].transform("sum")
    pieces["weight"] = pieces["clip_area_ha"] / pieces["screen_clip_ha"]
    pieces["thlb_ha"] = pieces["thlb_ha"] * pieces["weight"]
    pieces["volume_m3"] = pieces["volume_m3"] * pieces["weight"]
    pieces["net_base_cad"] = pieces["net_base_per_m3"] * pieces["volume_m3"]

    grouped = pieces.groupby(["block_id", "block_tsa", "block_au"], as_index=False).agg(
        thlb_ha=("thlb_ha", "sum"),
        volume_m3=("volume_m3", "sum"),
        net_base_cad=("net_base_cad", "sum"),
        screened_polygons=("FEATURE_ID", "nunique"),
    )
    op_parts = (
        pieces.groupby(["block_id", "operability"], as_index=False)
        .agg(operability_thlb_ha=("thlb_ha", "sum"))
        .sort_values(["block_id", "operability_thlb_ha"], ascending=[True, False])
        .drop_duplicates("block_id")
        .rename(columns={"operability": "operability_dominant"})
    )
    mixed = (
        pieces.groupby("block_id")["operability"]
        .nunique()
        .rename("operability_count")
        .reset_index()
    )
    grouped = grouped.merge(op_parts, on="block_id", how="left", validate="one_to_one")
    grouped = grouped.merge(mixed, on="block_id", how="left", validate="one_to_one")
    grouped = grouped.merge(
        blocks[["block_id", "block_area_ha"]],
        on="block_id",
        how="left",
        validate="one_to_one",
    )
    grouped["net_base_per_m3"] = grouped["net_base_cad"] / grouped["volume_m3"].where(
        grouped["volume_m3"] > 0
    )
    grouped["positive"] = grouped["net_base_cad"] >= 0
    grouped["gate_status"] = "partial_direct_only"
    grouped["shared_cost_status"] = "unallocated"
    grouped["forced_access"] = False
    return grouped.sort_values(["positive", "net_base_cad"], ascending=[True, True])


def _summaries(
    blocks: pd.DataFrame,
    total_blocks: int,
    screen_thlb_ha: float,
) -> dict[str, object]:
    total = {
        "screened_blocks": len(blocks),
        "total_blocks": total_blocks,
        "block_area_ha": float(blocks["block_area_ha"].sum()),
        "screen_thlb_ha": float(screen_thlb_ha),
        "thlb_ha": float(blocks["thlb_ha"].sum()),
        "volume_m3": float(blocks["volume_m3"].sum()),
        "net_base_cad": float(blocks["net_base_cad"].sum()),
    }
    negative = blocks[~blocks["positive"]]
    total["negative_blocks"] = len(negative)
    total["negative_thlb_ha"] = float(negative["thlb_ha"].sum())
    total["negative_volume_m3"] = float(negative["volume_m3"].sum())
    total["negative_net_base_cad"] = float(negative["net_base_cad"].sum())
    total["unallocated_thlb_ha"] = max(0.0, total["screen_thlb_ha"] - total["thlb_ha"])
    total["allocation_coverage_pct"] = (
        100.0 * total["thlb_ha"] / total["screen_thlb_ha"] if total["screen_thlb_ha"] else 0.0
    )
    total["negative_thlb_share_pct"] = (
        100.0 * total["negative_thlb_ha"] / total["thlb_ha"] if total["thlb_ha"] else 0.0
    )
    by_tsa = (
        blocks.groupby("block_tsa", as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            negative_thlb_ha=(
                "thlb_ha",
                lambda values: values[~blocks.loc[values.index, "positive"]].sum(),
            ),
            net_base_cad=("net_base_cad", "sum"),
        )
        .assign(
            negative_thlb_share_pct=lambda frame: (
                100.0 * frame["negative_thlb_ha"] / frame["thlb_ha"].where(frame["thlb_ha"] > 0)
            )
        )
    )
    by_operability = (
        blocks.groupby("operability_dominant", as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            negative_thlb_ha=(
                "thlb_ha",
                lambda values: values[~blocks.loc[values.index, "positive"]].sum(),
            ),
            net_base_cad=("net_base_cad", "sum"),
        )
        .assign(
            negative_thlb_share_pct=lambda frame: (
                100.0 * frame["negative_thlb_ha"] / frame["thlb_ha"].where(frame["thlb_ha"] > 0)
            )
        )
    )
    worst_au = (
        blocks.groupby(["block_tsa", "block_au"], as_index=False)
        .agg(
            thlb_ha=("thlb_ha", "sum"),
            negative_thlb_ha=(
                "thlb_ha",
                lambda values: values[~blocks.loc[values.index, "positive"]].sum(),
            ),
            net_base_cad=("net_base_cad", "sum"),
        )
        .assign(
            negative_thlb_share_pct=lambda frame: (
                100.0 * frame["negative_thlb_ha"] / frame["thlb_ha"].where(frame["thlb_ha"] > 0)
            )
        )
        .sort_values("negative_thlb_ha", ascending=False)
        .head(10)
    )
    return {
        "total": total,
        "by_tsa": by_tsa.to_dict(orient="records"),
        "by_operability": by_operability.to_dict(orient="records"),
        "worst_au": worst_au.to_dict(orient="records"),
    }


def _report(summary: dict[str, object], path: Path) -> None:
    total = summary["total"]
    lines = [
        "# Block-level diagnostic revenue screen",
        "",
        "This is a partial direct-cost gate. Shared road, landing, terminal,",
        "and overhead costs are **unallocated**; the result is not a sustainable",
        "or financially complete scenario.",
        "",
        "## Summary",
        "",
        f"- Screened blocks: **{total['screened_blocks']:,}** of "
        f"{total['total_blocks']:,} block supports",
        f"- Block area: **{total['block_area_ha'] / 1000:.1f} thousand ha**",
        f"- THLB allocated: **{total['thlb_ha'] / 1000:.1f} thousand ha** "
        f"of {total['screen_thlb_ha'] / 1000:.1f} thousand ha screened "
        f"({total['allocation_coverage_pct']:.1f}%)",
        f"- Unallocated THLB: **{total['unallocated_thlb_ha'] / 1000:.1f} thousand ha**",
        f"- Volume: **{total['volume_m3'] / 1_000_000:.3f} million m3**",
        f"- Direct net revenue: **{total['net_base_cad'] / 1_000_000_000:,.2f} billion CAD**",
        f"- Negative net revenue: "
        f"**{total['negative_net_base_cad'] / 1_000_000:,.1f} million CAD**",
        f"- Negative blocks: **{total['negative_blocks']:,}**",
        f"- Negative THLB: **{total['negative_thlb_ha'] / 1000:.1f} thousand ha "
        f"({total['negative_thlb_share_pct']:.1f}%)**",
        f"- Negative volume: **{total['negative_volume_m3'] / 1_000_000:.3f} million m3**",
        "",
        "## By TSA",
        "",
        "| TSA | Blocks | THLB (kha) | Negative THLB (kha) | Negative share | Net (M CAD) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["by_tsa"]:
        lines.append(
            f"| {row['block_tsa']} | {row['blocks']:,} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['negative_thlb_ha'] / 1000:.1f} | {row['negative_thlb_share_pct']:.1f}% | "
            f"{row['net_base_cad'] / 1_000_000:,.1f} |"
        )
    lines += [
        "",
        "## By dominant operability",
        "",
        "| System | Blocks | THLB (kha) | Negative THLB (kha) | Negative share | Net (M CAD) |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["by_operability"]:
        lines.append(
            f"| {row['operability_dominant']} | {row['blocks']:,} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['negative_thlb_ha'] / 1000:.1f} | {row['negative_thlb_share_pct']:.1f}% | "
            f"{row['net_base_cad'] / 1_000_000:,.1f} |"
        )
    lines += [
        "",
        "## Highest negative THLB by AU",
        "",
        "| TSA | AU | THLB (kha) | Negative THLB (kha) | Negative share |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["worst_au"]:
        lines.append(
            f"| {row['block_tsa']} | {row['block_au']} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['negative_thlb_ha'] / 1000:.1f} | {row['negative_thlb_share_pct']:.1f}% |"
        )
    lines += [
        "",
        "## Use",
        "",
        "- Use the block list to exclude direct loss-makers from a candidate schedule.",
        "- A negative block may be a forced access/infrastructure case only if it is",
        "  explicitly marked and reconciled.",
        "- Do not treat this as the full sustainable gate: shared costs remain",
        "  unallocated and current quotes/recovery are still missing.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--screen",
        type=Path,
        default=Path("runtime/p3/full_thlb_screening.csv"),
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("data/gnn_combined_checkpoint.feather"),
    )
    parser.add_argument(
        "--fragments",
        type=Path,
        default=Path("output/patchworks_gnn/fragments_merged/fragments.shp"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runtime/gnn/block_revenue_screen.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("runtime/gnn/block_revenue_summary.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("notes/reports/block-level-revenue-screen.md"),
    )
    return parser.parse_args()


def main() -> None:
    """Run the block-level diagnostic and write its report."""
    args = _parse_args()
    screen = _screen_with_ids(args.screen, args.checkpoint)
    blocks = _block_support(args.fragments)
    result = _allocate(screen, blocks)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.out, index=False)
    summary = _summaries(result, len(blocks), float(screen["thlb_ha"].sum()))
    summary["input"] = {
        "screen": str(args.screen),
        "checkpoint": str(args.checkpoint),
        "fragments": str(args.fragments),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _report(summary, args.report)
    total = summary["total"]
    print(
        f"blocks={total['screened_blocks']:,} thlb={total['thlb_ha']:.0f} ha "
        f"negative={total['negative_blocks']:,} "
        f"negative_thlb={total['negative_thlb_ha']:.0f} ha"
    )


if __name__ == "__main__":
    main()
