#!/usr/bin/env python3
"""Quantify GNN AUs and test whether TSA 46/47 curve sets can be merged."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REPORTING_STRATUM = {"CWH_FDC": "CWH_FD", "MH_H": "MH_HM"}


def _value(curves: pd.DataFrame, curve_id: int, age: int) -> float:
    points = curves[curves["curve_id"] == curve_id].sort_values("x")
    if points.empty:
        return float("nan")
    return float(np.interp(age, points["x"], points["y"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--au-table", type=Path, required=True)
    parser.add_argument("--curve-points", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = pd.read_feather(args.checkpoint)
    au = pd.read_csv(args.au_table)
    curves = pd.read_csv(args.curve_points)

    checkpoint["area_ha"] = checkpoint["FEATURE_AREA_SQM"] / 10000.0
    checkpoint["thlb_ha"] = (
        checkpoint["area_ha"]
        * pd.to_numeric(checkpoint["thlb_raw_calibrated"], errors="coerce").fillna(0.0)
        / 100.0
    )
    area = (
        checkpoint.groupby(["tsa_code", "au"], as_index=False)
        .agg(rows=("au", "size"), area_ha=("area_ha", "sum"), thlb_ha=("thlb_ha", "sum"))
        .rename(columns={"tsa_code": "tsa"})
    )
    area = au[["au_id", "tsa", "stratum_code", "si_level"]].merge(
        area, left_on=["au_id", "tsa"], right_on=["au", "tsa"], how="left"
    )
    area = area.drop(columns=["au"])
    for column in ("rows", "area_ha", "thlb_ha"):
        area[column] = area[column].fillna(0)
    total_area = area["area_ha"].sum()
    total_thlb = area["thlb_ha"].sum()
    area["area_share_pct"] = 100.0 * area["area_ha"] / total_area
    area["thlb_share_pct"] = 100.0 * area["thlb_ha"] / total_thlb
    area = area.sort_values(["thlb_ha", "area_ha"], ascending=False)
    area.to_csv(args.out_dir / "gnn_au_area.csv", index=False)

    crosswalk = au[["au_id", "tsa", "stratum_code", "si_level", "untreated_curve_id", "treated_curve_id"]].copy()
    crosswalk["reporting_stratum"] = crosswalk["stratum_code"].replace(
        REPORTING_STRATUM
    )
    crosswalk["reporting_group"] = (
        crosswalk["reporting_stratum"] + "_" + crosswalk["si_level"]
    )
    crosswalk["model_au_kept"] = True
    crosswalk.to_csv(args.out_dir / "gnn_au_reporting_crosswalk.csv", index=False)

    group_area = (
        area.merge(crosswalk[["au_id", "reporting_group"]], on="au_id", how="left")
        .groupby("reporting_group", as_index=False)
        .agg(tsa_count=("tsa", "nunique"), area_ha=("area_ha", "sum"), thlb_ha=("thlb_ha", "sum"))
    )
    group_area["area_share_pct"] = 100.0 * group_area["area_ha"] / total_area
    group_area["thlb_share_pct"] = 100.0 * group_area["thlb_ha"] / total_thlb
    group_area = group_area.sort_values("thlb_ha", ascending=False)
    group_area.to_csv(args.out_dir / "gnn_au_reporting_group_area.csv", index=False)

    rows = []
    for (reporting_group, si), group in crosswalk.groupby(
        ["reporting_group", "si_level"]
    ):
        if group["tsa"].nunique() < 2:
            continue
        for curve_type in ("untreated", "treated"):
            record: dict[str, object] = {
                "reporting_group": reporting_group,
                "si_level": si,
                "curve_type": curve_type,
            }
            for _, row in group.iterrows():
                curve_id = int(row[f"{curve_type}_curve_id"])
                record[f"tsa{int(row['tsa'])}_curve_id"] = curve_id
                for age in (50, 100):
                    record[f"tsa{int(row['tsa'])}_age{age}"] = round(
                        _value(curves, curve_id, age), 1
                    )
            a100 = record.get("tsa46_age100")
            b100 = record.get("tsa47_age100")
            if pd.notna(a100) and pd.notna(b100) and b100:
                record["delta_age100"] = round(float(a100) - float(b100), 1)
                record["delta_age100_pct"] = round(100.0 * (float(a100) - float(b100)) / float(b100), 1)
            rows.append(record)
    comparison = pd.DataFrame(rows).sort_values(
        ["reporting_group", "si_level", "curve_type"]
    )
    comparison.to_csv(args.out_dir / "gnn_au_curve_comparison.csv", index=False)

    print(f"total_area_ha={total_area:.2f} total_thlb_ha={total_thlb:.2f}")
    print(f"aus={len(area)} with_area={int((area['rows'] > 0).sum())}")
    print("top AUs by THLB:")
    print(area.head(12)[["au_id", "tsa", "stratum_code", "si_level", "thlb_ha", "thlb_share_pct"]].to_string(index=False))
    print("matched reporting groups with curve deltas:")
    print(comparison[["reporting_group", "si_level", "curve_type", "delta_age100_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
