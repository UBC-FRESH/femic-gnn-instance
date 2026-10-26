#!/usr/bin/env python3
"""Remove direct loss-making blocks from a candidate schedule.

This is a diagnostic sensitivity. The base schedule and benchmark are not
modified. Shared road/landing/terminal costs remain unallocated.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schedule",
        type=Path,
        default=Path("runtime/gnn/schedules/opening_first.csv"),
    )
    parser.add_argument(
        "--block-screen",
        type=Path,
        default=Path("runtime/gnn/block_revenue_screen.csv"),
    )
    parser.add_argument(
        "--out-schedule",
        type=Path,
        default=Path("runtime/gnn/schedules/opening_first_block_gate.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("runtime/gnn/block_exclusion_summary.json"),
    )
    return parser.parse_args()


def main() -> None:
    """Filter the schedule and write a summary of the excluded blocks."""
    args = _parse_args()
    schedule = pd.read_csv(args.schedule)
    screen = pd.read_csv(args.block_screen)
    required_schedule = {"block_id", "treatment", "offset"}
    required_screen = {"block_id", "positive", "thlb_ha", "volume_m3", "net_base_cad"}
    if not required_schedule.issubset(schedule.columns):
        raise ValueError("schedule lacks block_id/treatment/offset")
    if not required_screen.issubset(screen.columns):
        raise ValueError("block screen lacks required fields")
    negative = screen.loc[~screen["positive"].astype(bool)].copy()
    negative_ids = set(negative["block_id"].astype(int))
    scheduled_negative = schedule[schedule["block_id"].astype(int).isin(negative_ids)]
    filtered = schedule[~schedule["block_id"].astype(int).isin(negative_ids)].copy()
    args.out_schedule.parent.mkdir(parents=True, exist_ok=True)
    filtered.to_csv(args.out_schedule, index=False)
    excluded_blocks = negative[
        negative["block_id"].astype(int).isin(set(schedule["block_id"].astype(int)))
    ]
    summary = {
        "schedule": str(args.schedule),
        "block_screen": str(args.block_screen),
        "out_schedule": str(args.out_schedule),
        "scheduled_rows_before": len(schedule),
        "scheduled_rows_after": len(filtered),
        "scheduled_blocks_before": int(schedule["block_id"].nunique()),
        "scheduled_blocks_after": int(filtered["block_id"].nunique()),
        "excluded_schedule_rows": len(scheduled_negative),
        "excluded_scheduled_blocks": int(scheduled_negative["block_id"].nunique()),
        "excluded_block_screen_rows": len(excluded_blocks),
        "excluded_thlb_ha": float(excluded_blocks["thlb_ha"].sum()),
        "excluded_volume_m3": float(excluded_blocks["volume_m3"].sum()),
        "excluded_net_base_cad": float(excluded_blocks["net_base_cad"].sum()),
        "gate_status": "partial_direct_only",
        "shared_cost_status": "unallocated",
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
