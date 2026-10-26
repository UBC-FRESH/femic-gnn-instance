#!/usr/bin/env python3
"""Combine candidate headroom and access exposure into a risk register."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--access",
        type=Path,
        default=Path("runtime/gnn/access_exposure.csv"),
    )
    parser.add_argument(
        "--block-screen",
        type=Path,
        default=Path("runtime/gnn/block_revenue_screen.csv"),
    )
    parser.add_argument(
        "--schedule",
        type=Path,
        default=Path("runtime/gnn/schedules/opening_first_positive.csv"),
    )
    parser.add_argument("--headroom-threshold", type=float, default=10.0)
    parser.add_argument("--road-threshold", type=float, default=500.0)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runtime/gnn/candidate_risk_register.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("runtime/gnn/candidate_risk_summary.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("notes/reports/candidate-risk-register.md"),
    )
    return parser.parse_args()


def _priority(row: pd.Series, headroom_threshold: float, road_threshold: float) -> str:
    low = row["headroom_per_m3"] < headroom_threshold
    far = row["road_distance_m"] > road_threshold
    stream = row["stream_crossings"] > 0
    if low and far and stream:
        return "A"
    if low and (far or stream):
        return "B"
    if low:
        return "C"
    if far or stream:
        return "D"
    return "E"


def _summaries(frame: pd.DataFrame) -> dict[str, object]:
    total = {
        "blocks": len(frame),
        "thlb_ha": float(frame["thlb_ha"].sum()),
        "volume_m3": float(frame["volume_m3"].sum()),
        "headroom_threshold_cad_m3": float(frame["headroom_threshold"].iloc[0]),
        "road_threshold_m": float(frame["road_threshold"].iloc[0]),
    }
    by_priority = (
        frame.groupby("priority", as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            volume_m3=("volume_m3", "sum"),
            net_base_cad=("net_base_cad", "sum"),
        )
        .sort_values("priority")
    )
    by_tsa = (
        frame.groupby(["priority", "block_tsa"], as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            volume_m3=("volume_m3", "sum"),
        )
        .sort_values(["priority", "block_tsa"])
    )
    by_operability = (
        frame.groupby(["priority", "operability_dominant"], as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            volume_m3=("volume_m3", "sum"),
        )
        .sort_values(["priority", "operability_dominant"])
    )
    top = (
        frame[frame["priority"].isin(["A", "B"])]
        .sort_values(["priority", "headroom_per_m3", "thlb_ha"], ascending=[True, True, False])
        .head(25)
    )
    return {
        "total": total,
        "by_priority": by_priority.to_dict(orient="records"),
        "by_tsa": by_tsa.to_dict(orient="records"),
        "by_operability": by_operability.to_dict(orient="records"),
        "top_blocks": top[
            [
                "block_id",
                "block_tsa",
                "block_au",
                "operability_dominant",
                "priority",
                "thlb_ha",
                "volume_m3",
                "headroom_per_m3",
                "road_distance_m",
                "stream_crossings",
            ]
        ].to_dict(orient="records"),
    }


def _report(summary: dict[str, object], path: Path) -> None:
    total = summary["total"]
    lines = [
        "# Candidate risk register",
        "",
        "Status: screening flags only. No road, crossing, terminal, haul, or barge",
        "cost is assigned.",
        "",
        f"Low-headroom flag: **< {total['headroom_threshold_cad_m3']:.0f} CAD/m3**. "
        f"Far-road flag: **> {total['road_threshold_m']:.0f} m**. "
        "Stream flag: at least one mapped FWA stream intersects the block.",
        "",
        "## Summary",
        "",
        f"- Candidate blocks: **{total['blocks']:,}**",
        f"- Candidate THLB: **{total['thlb_ha'] / 1000:.1f} thousand ha**",
        "",
        "| Priority | Meaning | Blocks | THLB (kha) |",
        "| --- | --- | ---: | ---: |",
    ]
    meanings = {
        "A": "low headroom + far road + stream",
        "B": "low headroom + far road or stream",
        "C": "low headroom only",
        "D": "far road or stream, headroom okay",
        "E": "neither flag",
    }
    for row in summary["by_priority"]:
        lines.append(
            f"| {row['priority']} | {meanings[row['priority']]} | {row['blocks']:,} | "
            f"{row['thlb_ha'] / 1000:.1f} |"
        )
    lines += [
        "",
        "## Priority blocks for the data request",
        "",
        "| Block | TSA | AU | System | Priority | THLB (ha) | "
        "Headroom (CAD/m3) | Road (m) | Streams |",
        "| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["top_blocks"]:
        lines.append(
            f"| {row['block_id']} | {row['block_tsa']} | {row['block_au']} | "
            f"{row['operability_dominant']} | {row['priority']} | {row['thlb_ha']:.1f} | "
            f"{row['headroom_per_m3']:.2f} | {row['road_distance_m']:.0f} | "
            f"{row['stream_crossings']} |"
        )
    lines += [
        "",
        "## By TSA and priority",
        "",
        "| Priority | TSA | Blocks | THLB (kha) |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in summary["by_tsa"]:
        lines.append(
            f"| {row['priority']} | {row['block_tsa']} | {row['blocks']:,} | "
            f"{row['thlb_ha'] / 1000:.1f} |"
        )
    lines += [
        "",
        "## Limits",
        "",
        "- Headroom is the selected-block screen, not a schedule-level NPV.",
        "- Road distance is straight-line to DRA, not a route or haul distance.",
        "- A stream intersection is not a confirmed culvert, bridge, or fish-passage requirement.",
        "- Thresholds are screening choices, not actual costs.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Build the candidate risk register and report."""
    args = _parse_args()
    access = pd.read_csv(args.access).drop(columns=["geometry"], errors="ignore")
    screen = pd.read_csv(args.block_screen)[["block_id", "volume_m3", "net_base_cad"]]
    schedule = pd.read_csv(args.schedule)
    candidate_ids = set(schedule["block_id"].astype(int))
    frame = access[access["block_id"].astype(int).isin(candidate_ids)].copy()
    frame = frame.merge(screen, on="block_id", how="left", validate="one_to_one")
    missing = frame["net_base_cad"].isna()
    if missing.any():
        raise ValueError(f"{int(missing.sum())} candidate blocks lack revenue rows")
    frame["headroom_per_m3"] = frame["net_base_cad"] / frame["volume_m3"].where(
        frame["volume_m3"] > 0
    )
    frame["headroom_threshold"] = args.headroom_threshold
    frame["road_threshold"] = args.road_threshold
    frame["low_headroom"] = frame["headroom_per_m3"] < args.headroom_threshold
    frame["far_road"] = frame["road_distance_m"] > args.road_threshold
    frame["stream_flag"] = frame["stream_crossings"] > 0
    frame["priority"] = frame.apply(
        _priority,
        axis=1,
        headroom_threshold=args.headroom_threshold,
        road_threshold=args.road_threshold,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    summary = _summaries(frame)
    summary["inputs"] = {
        "access": str(args.access),
        "block_screen": str(args.block_screen),
        "schedule": str(args.schedule),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _report(summary, args.report)
    counts = {row["priority"]: row["blocks"] for row in summary["by_priority"]}
    print(
        f"candidate_blocks={len(frame):,} "
        f"priority_A={counts.get('A', 0):,} priority_B={counts.get('B', 0):,}"
    )


if __name__ == "__main__":
    main()
