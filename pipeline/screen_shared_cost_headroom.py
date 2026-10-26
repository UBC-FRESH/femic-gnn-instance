#!/usr/bin/env python3
"""Measure shared-cost headroom for the positive-block candidate schedule.

The block screen covers direct harvest and transport costs only. This script
adds a hypothetical uniform shared cost per cubic metre as a sensitivity; it
does not invent an actual road, landing, terminal, or overhead rate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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
    parser.add_argument(
        "--costs",
        default="0,10,20,30,50,75,100",
        help="Comma-separated shared-cost sensitivity levels in CAD/m3.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("runtime/gnn/positive_screen_shared_cost.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("runtime/gnn/shared_cost_headroom.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("notes/reports/shared-cost-headroom.md"),
    )
    return parser.parse_args()


def _summaries(selected: pd.DataFrame, costs: list[float]) -> dict[str, object]:
    total = {
        "blocks": len(selected),
        "thlb_ha": float(selected["thlb_ha"].sum()),
        "volume_m3": float(selected["volume_m3"].sum()),
        "direct_net_cad": float(selected["net_base_cad"].sum()),
        "break_even_per_m3": float(selected["net_base_cad"].sum() / selected["volume_m3"].sum()),
        "break_even_per_ha": float(selected["net_base_cad"].sum() / selected["thlb_ha"].sum()),
    }
    by_tsa = (
        selected.groupby("block_tsa", as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            volume_m3=("volume_m3", "sum"),
            net_base_cad=("net_base_cad", "sum"),
        )
        .assign(break_even_per_m3=lambda frame: frame["net_base_cad"] / frame["volume_m3"])
    )
    by_operability = (
        selected.groupby("operability_dominant", as_index=False)
        .agg(
            blocks=("block_id", "size"),
            thlb_ha=("thlb_ha", "sum"),
            volume_m3=("volume_m3", "sum"),
            net_base_cad=("net_base_cad", "sum"),
        )
        .assign(break_even_per_m3=lambda frame: frame["net_base_cad"] / frame["volume_m3"])
    )
    sensitivity = []
    for cost in costs:
        after = selected["net_base_cad"] - cost * selected["volume_m3"]
        positive = after >= 0
        sensitivity.append(
            {
                "shared_cost_per_m3": cost,
                "positive_blocks": int(positive.sum()),
                "positive_thlb_ha": float(selected.loc[positive, "thlb_ha"].sum()),
                "positive_volume_m3": float(selected.loc[positive, "volume_m3"].sum()),
                "total_net_after_cad": float(after.sum()),
                "negative_blocks": int((~positive).sum()),
                "negative_thlb_ha": float(selected.loc[~positive, "thlb_ha"].sum()),
            }
        )
    headroom = selected["net_base_cad"] / selected["volume_m3"]
    lowest = selected.assign(headroom_per_m3=headroom).sort_values("headroom_per_m3").head(10)
    return {
        "total": total,
        "by_tsa": by_tsa.to_dict(orient="records"),
        "by_operability": by_operability.to_dict(orient="records"),
        "sensitivity": sensitivity,
        "lowest_headroom_blocks": lowest[
            [
                "block_id",
                "block_tsa",
                "block_au",
                "operability_dominant",
                "thlb_ha",
                "volume_m3",
                "net_base_cad",
                "headroom_per_m3",
            ]
        ].to_dict(orient="records"),
        "headroom_stats": {
            "min_per_m3": float(headroom.min()),
            "p10_per_m3": float(headroom.quantile(0.10)),
            "median_per_m3": float(headroom.median()),
        },
    }


def _report(summary: dict[str, object], path: Path) -> None:
    total = summary["total"]
    lines = [
        "# Positive-block candidate: shared-cost headroom",
        "",
        "Status: candidate-scenario sensitivity. Shared costs are a test axis, not",
        "actual road, landing, terminal, or overhead rates.",
        "",
        "## Selected block screen",
        "",
        f"- Scheduled blocks: **{total['blocks']:,}**",
        f"- THLB: **{total['thlb_ha'] / 1000:.1f} thousand ha**",
        f"- Screen volume: **{total['volume_m3'] / 1_000_000:.3f} million m3**",
        f"- Direct net revenue: **{total['direct_net_cad'] / 1_000_000_000:.2f} billion CAD**",
        f"- Break-even shared cost: **{total['break_even_per_m3']:.2f} CAD/m3**",
        f"- Break-even per ha: **{total['break_even_per_ha'] / 1000:.1f} thousand CAD/ha**",
        "",
        "The screen volume is the selected blocks' checkpoint volume; the",
        "simulated harvest volume can differ because it uses future yield.",
        "",
        "## Shared-cost sensitivity",
        "",
        "| Shared cost (CAD/m3) | Positive blocks | Positive THLB (kha) | "
        "Positive volume (Mm3) | Total net after cost (billion CAD) |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["sensitivity"]:
        lines.append(
            f"| {row['shared_cost_per_m3']:.0f} | {row['positive_blocks']:,} | "
            f"{row['positive_thlb_ha'] / 1000:.1f} | {row['positive_volume_m3'] / 1_000_000:.3f} | "
            f"{row['total_net_after_cad'] / 1_000_000_000:.2f} |"
        )
    lines += [
        "",
        "## By TSA",
        "",
        "| TSA | Blocks | THLB (kha) | Screen volume (Mm3) | Break-even (CAD/m3) |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["by_tsa"]:
        lines.append(
            f"| {row['block_tsa']} | {row['blocks']:,} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['volume_m3'] / 1_000_000:.3f} | {row['break_even_per_m3']:.2f} |"
        )
    lines += [
        "",
        "## By dominant operability",
        "",
        "| System | Blocks | THLB (kha) | Screen volume (Mm3) | Break-even (CAD/m3) |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["by_operability"]:
        lines.append(
            f"| {row['operability_dominant']} | {row['blocks']:,} | {row['thlb_ha'] / 1000:.1f} | "
            f"{row['volume_m3'] / 1_000_000:.3f} | {row['break_even_per_m3']:.2f} |"
        )
    lines += [
        "",
        "## Lowest-headroom blocks",
        "",
        "| Block | TSA | AU | System | THLB (ha) | Headroom (CAD/m3) |",
        "| ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in summary["lowest_headroom_blocks"]:
        lines.append(
            f"| {row['block_id']} | {row['block_tsa']} | {row['block_au']} | "
            f"{row['operability_dominant']} | {row['thlb_ha']:.1f} | "
            f"{row['headroom_per_m3']:.2f} |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "- The average shared-cost headroom is high, but individual blocks can flip",
        "  at much lower costs.",
        "- The sensitivity levels are not actual rates. Replace them with current",
        "  road, landing, terminal, and overhead data when available.",
        "- This is still a candidate scenario, not the base or a sustainable plan.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Run the headroom analysis and write its report."""
    args = _parse_args()
    screen = pd.read_csv(args.block_screen)
    schedule = pd.read_csv(args.schedule)
    required = {
        "block_id",
        "thlb_ha",
        "volume_m3",
        "net_base_cad",
        "block_tsa",
        "block_au",
        "operability_dominant",
    }
    if not required.issubset(screen.columns):
        raise ValueError("block screen lacks required fields")
    scheduled_ids = set(schedule["block_id"].astype(int))
    selected = screen[screen["block_id"].astype(int).isin(scheduled_ids)].copy()
    if selected.empty:
        raise ValueError("no scheduled blocks matched the screen")
    missing = scheduled_ids - set(selected["block_id"].astype(int))
    if missing:
        raise ValueError(f"{len(missing)} scheduled blocks are missing from the screen")
    costs = [float(item) for item in args.costs.split(",") if item.strip()]
    summary = _summaries(selected, costs)
    summary["inputs"] = {
        "block_screen": str(args.block_screen),
        "schedule": str(args.schedule),
    }
    summary["output"] = str(args.out)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    selected.assign(headroom_per_m3=selected["net_base_cad"] / selected["volume_m3"]).to_csv(
        args.out, index=False
    )
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _report(summary, args.report)
    total = summary["total"]
    print(
        f"blocks={total['blocks']:,} volume={total['volume_m3'] / 1_000_000:.3f} Mm3 "
        f"direct_net={total['direct_net_cad'] / 1_000_000_000:.2f}B "
        f"break_even={total['break_even_per_m3']:.2f} CAD/m3"
    )


if __name__ == "__main__":
    main()
