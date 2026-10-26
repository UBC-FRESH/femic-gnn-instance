#!/usr/bin/env python3
"""Write the direct-positive block candidate list from the block revenue screen."""

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
        "--out",
        type=Path,
        default=Path("runtime/gnn/schedules/positive_blocks.csv"),
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("runtime/gnn/positive_blocks_summary.json"),
    )
    return parser.parse_args()


def main() -> None:
    """Write the positive block list and a small summary."""
    args = _parse_args()
    screen = pd.read_csv(args.block_screen)
    if not {"block_id", "positive"}.issubset(screen.columns):
        raise ValueError("block screen lacks block_id/positive")
    positive = (
        screen.loc[screen["positive"].astype(bool), ["block_id"]]
        .drop_duplicates()
        .sort_values("block_id")
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    positive.to_csv(args.out, index=False)
    summary = {
        "block_screen": str(args.block_screen),
        "out": str(args.out),
        "positive_blocks": len(positive),
        "negative_blocks": int((~screen["positive"].astype(bool)).sum()),
        "positive_thlb_ha": float(screen.loc[screen["positive"].astype(bool), "thlb_ha"].sum()),
        "negative_thlb_ha": float(screen.loc[~screen["positive"].astype(bool), "thlb_ha"].sum()),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
