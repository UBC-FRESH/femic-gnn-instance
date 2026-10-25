#!/usr/bin/env python3
"""Summarize the TSA 46/47 ground-plot validation inside the GNN AOI."""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

METRICS = ("volume", "dbh", "height", "stems")
AGE_BINS = (5, 15, 30, 50, 80, 200)
AGE_LABELS = ("5-15", "16-30", "31-50", "51-80", "81-200")


def _site_set(*, header: Path, aoi: gpd.GeoDataFrame) -> set[str]:
    frame = pd.read_csv(header).dropna(subset=["BC_ALBERS_X", "BC_ALBERS_Y"])
    points = gpd.GeoDataFrame(
        frame,
        geometry=gpd.points_from_xy(frame["BC_ALBERS_X"], frame["BC_ALBERS_Y"]),
        crs="EPSG:3005",
    )
    joined = gpd.sjoin(points, aoi[["geometry"]], predicate="within", how="inner")
    return {str(value) for value in joined["SITE_IDENTIFIER"].unique()}


def _summarize(frame: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    frame = frame.copy()
    frame["age_class"] = pd.cut(
        frame["age"],
        bins=list(AGE_BINS),
        labels=list(AGE_LABELS),
        include_lowest=True,
    )
    for keys, group in frame.groupby(
        ["source_tsa", "sample_type", "local_au", "age_class"], observed=True
    ):
        for metric in METRICS:
            observed = group[f"observed_{metric}"]
            predicted = group[f"predicted_{metric}"]
            valid = pd.concat([observed, predicted], axis=1).dropna()
            valid = valid[(valid.iloc[:, 0] > 0) & (valid.iloc[:, 1] > 0)]
            if valid.empty:
                continue
            errors = valid.iloc[:, 1] - valid.iloc[:, 0]
            records.append(
                {
                    "source_tsa": keys[0],
                    "sample_type": keys[1],
                    "local_au": keys[2],
                    "age_class": keys[3],
                    "metric": metric,
                    "n": len(valid),
                    "mean_observed": round(float(valid.iloc[:, 0].mean()), 2),
                    "mean_predicted": round(float(valid.iloc[:, 1].mean()), 2),
                    "bias": round(float(errors.mean()), 2),
                    "mae": round(float(errors.abs().mean()), 2),
                    "rmse": round(float(np.sqrt(np.mean(np.square(errors)))), 2),
                    "relative_bias": round(
                        float(errors.mean() / valid.iloc[:, 0].mean()), 3
                    ),
                }
            )
    return pd.DataFrame(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aoi", type=Path, required=True)
    parser.add_argument("--tsa46-validation", type=Path, required=True)
    parser.add_argument("--tsa47-validation", type=Path, required=True)
    parser.add_argument("--tsa46-header", type=Path, required=True)
    parser.add_argument("--tsa47-header", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()

    aoi = gpd.read_file(args.aoi).to_crs(3005)
    site_sets = {
        46: _site_set(header=args.tsa46_header, aoi=aoi),
        47: _site_set(header=args.tsa47_header, aoi=aoi),
    }
    frames = []
    for tsa, path in ((46, args.tsa46_validation), (47, args.tsa47_validation)):
        frame = pd.read_csv(path)
        frame["site_identifier"] = frame["site_identifier"].astype(str)
        frame = frame[frame["site_identifier"].isin(site_sets[tsa])].copy()
        frame["source_tsa"] = tsa
        frames.append(frame)
    combined = pd.concat(frames, ignore_index=True)
    if combined.empty:
        raise SystemExit("no ground-plot rows fall inside the GNN AOI")
    summary = _summarize(combined)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(args.out, index=False)
    summary.to_csv(args.summary_out, index=False)
    print(
        f"rows={len(combined)} sites={combined.site_identifier.nunique()} "
        f"sources={combined.source_tsa.value_counts().to_dict()}"
    )
    print(combined.groupby(["source_tsa", "sample_type"]).size().to_string())


if __name__ == "__main__":
    main()
