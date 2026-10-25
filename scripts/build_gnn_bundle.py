#!/usr/bin/env python3
"""Combine the TSA 46 and TSA 47 FEMIC bundles for the GNN prototype."""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tsa46-bundle", type=Path, required=True)
    parser.add_argument("--tsa47-bundle", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    for filename in ("au_table.csv", "curve_table.csv", "curve_points_table.csv"):
        frames = []
        for bundle in (args.tsa46_bundle, args.tsa47_bundle):
            frame = pd.read_csv(bundle / filename)
            frame = frame.drop(
                columns=[c for c in frame.columns if str(c).startswith("Unnamed")],
                errors="ignore",
            )
            frames.append(frame)
        combined = pd.concat(frames, ignore_index=True)
        combined.to_csv(args.out / filename, index=False)


if __name__ == "__main__":
    main()
