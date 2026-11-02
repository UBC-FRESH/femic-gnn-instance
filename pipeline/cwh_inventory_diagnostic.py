#!/usr/bin/env python3
"""Run the GNN CWH INV-01 inventory diagnostic on the bounded LiDAR pilot.

The script derives a 25 m CHM feature table from a validated FEMIC LiDAR bundle,
filters each cell to the published CWH model-card predictor ranges, applies the
three cards through the FEMIC inventory reader, and writes a JSON summary. When
fragment geometry and VRI fragment attributes are supplied, it also writes a
descriptive fragment-level comparison.

This is a report-only diagnostic. It does not rebuild the GNN matrix or change a
curve, THLB, AAC, target, schedule, or release value.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARDS = {
    "cwh_lorey_height": ROOT / "config/inventory/models/als_cwh_lorey_height_2026.json",
    "cwh_basal_area": ROOT / "config/inventory/models/als_cwh_basal_area_2026.json",
    "cwh_gross_volume": ROOT / "config/inventory/models/als_cwh_gross_volume_2026.json",
}
DEFAULT_FRAGMENTS = ROOT / "output/patchworks_gnn/fragments_merged/fragments.shp"
DEFAULT_VRI_FRAGMENTS = ROOT / "runtime/gnn/matrix/fragments.parquet"


def run(command: list[str]) -> None:
    """Run one command and raise on a non-zero exit status.

    Parameters
    ----------
    command : list[str]
        Command and arguments.

    Returns
    -------
    None
    """
    print("+ " + " ".join(command))
    subprocess.run(command, check=True)


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from ``path``.

    Parameters
    ----------
    path : pathlib.Path
        JSON file to read.

    Returns
    -------
    dict[str, Any]
        Parsed JSON object.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def card_mask(frame: pd.DataFrame, card: dict[str, Any]) -> pd.Series:
    """Return the rows inside a model card's declared predictor ranges.

    Parameters
    ----------
    frame : pandas.DataFrame
        Feature table with one row per grid cell.
    card : dict[str, Any]
        FEMIC inventory model card.

    Returns
    -------
    pandas.Series
        Boolean mask of rows inside every declared predictor range.
    """
    mask = pd.Series(True, index=frame.index)
    for predictor, bounds in card.get("predictor_ranges", {}).items():
        if predictor not in frame.columns:
            raise KeyError(f"feature table has no predictor column {predictor!r}")
        low, high = float(bounds[0]), float(bounds[1])
        mask &= frame[predictor].between(low, high)
    return mask


def value_summary(values: pd.Series) -> dict[str, float | int]:
    """Summarise one model card's predictions.

    Parameters
    ----------
    values : pandas.Series
        Predicted values.

    Returns
    -------
    dict[str, float | int]
        Count, mean, median, minimum, and maximum.
    """
    return {
        "rows": int(values.size),
        "mean": float(values.mean()),
        "median": float(values.median()),
        "min": float(values.min()),
        "max": float(values.max()),
    }


def fragment_comparison(
    features: pd.DataFrame,
    predictions: dict[str, pd.DataFrame],
    fragments_path: Path,
    vri_fragments_path: Path,
) -> tuple[dict[str, Any], pd.DataFrame]:
    """Join cell predictions to fragments and compare them with VRI attributes.

    Parameters
    ----------
    features : pandas.DataFrame
        Grid feature table with ``fragment_id``, ``x_center``, and ``y_center``.
    predictions : dict[str, pandas.DataFrame]
        Per-card prediction tables keyed by card name.
    fragments_path : pathlib.Path
        Fragment polygon shapefile.
    vri_fragments_path : pathlib.Path
        Compiled fragment table with ``vri_*`` fields.

    Returns
    -------
    tuple[dict[str, Any], pandas.DataFrame]
        Summary counts and the per-fragment comparison table.
    """
    import geopandas as gpd
    import numpy as np

    points = features.rename(columns={"fragment_id": "cell_id"}).copy()
    points = gpd.GeoDataFrame(
        points,
        geometry=gpd.points_from_xy(points["x_center"], points["y_center"]),
        crs=3005,
    )
    for card_name, table in predictions.items():
        values = table[["fragment_id", "value"]].rename(
            columns={"fragment_id": "cell_id", "value": f"pred_{card_name}"}
        )
        points = points.merge(values, on="cell_id", how="left")

    fragments = gpd.read_file(fragments_path).rename(columns={"FRAGMENT_I": "poly_id"})
    joined = gpd.sjoin(
        points,
        fragments[["poly_id", "BLOCK", "geometry"]],
        how="inner",
        predicate="within",
    )
    comparison = (
        joined.groupby("poly_id")
        .agg(
            cells=("cell_id", "size"),
            **{
                f"pred_{card_name}": (f"pred_{card_name}", "mean")
                for card_name in predictions
            },
        )
        .reset_index()
    )
    vri = pd.read_parquet(vri_fragments_path)[
        [
            "fragment_id",
            "vri_available",
            "vri_height_m",
            "vri_live_volume_125_m3_ha",
        ]
    ]
    comparison = comparison.merge(
        vri, left_on="poly_id", right_on="fragment_id", how="left"
    )

    summary: dict[str, Any] = {
        "joined_cells": int(len(joined)),
        "joined_fragments": int(comparison["poly_id"].nunique()),
        "joined_blocks": int(joined["BLOCK"].nunique()),
        "joined_area_ha": float(len(joined) * 625.0 / 10000.0),
        "vri_comparison": {},
    }
    for prediction, observed, label in (
        ("pred_cwh_lorey_height", "vri_height_m", "lorey_height_m"),
        ("pred_cwh_gross_volume", "vri_live_volume_125_m3_ha", "gross_volume_m3_ha"),
    ):
        subset = comparison.dropna(subset=[prediction, observed])
        subset = subset[subset["vri_available"] == True]  # noqa: E712
        if subset.empty:
            continue
        difference = subset[prediction] - subset[observed]
        summary["vri_comparison"][label] = {
            "fragments": int(len(subset)),
            "predicted_mean": float(subset[prediction].mean()),
            "vri_mean": float(subset[observed].mean()),
            "bias": float(difference.mean()),
            "rmse": float(np.sqrt((difference**2).mean())),
            "correlation": float(subset[[prediction, observed]].corr().iloc[0, 1]),
        }
    return summary, comparison


def main() -> None:
    """Run the diagnostic and write its summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--grid-size-m", type=float, default=25.0)
    parser.add_argument("--min-cover-pct", type=float, default=34.5)
    parser.add_argument(
        "--fragments",
        type=Path,
        default=DEFAULT_FRAGMENTS,
        help="Fragment polygon shapefile for the descriptive VRI comparison.",
    )
    parser.add_argument(
        "--vri-fragments",
        type=Path,
        default=DEFAULT_VRI_FRAGMENTS,
        help="Compiled fragment table carrying vri_* attributes.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = args.bundle.resolve()
    run([sys.executable, "-m", "femic", "lidar", "inspect", str(bundle)])

    features_path = output_dir / "features_25m.csv"
    run(
        [
            sys.executable,
            "-m",
            "femic",
            "lidar",
            "inventory-features",
            "--bundle",
            str(bundle),
            "--output",
            str(features_path),
            "--grid-size-m",
            str(args.grid_size_m),
            "--min-cover-pct",
            str(args.min_cover_pct),
        ]
    )
    features = pd.read_csv(features_path)
    summary: dict[str, Any] = {
        "bundle": str(bundle),
        "bundle_id": load_json(bundle / "manifest.json").get("bundle_id"),
        "bundle_version": load_json(bundle / "manifest.json").get("bundle_version"),
        "grid_size_m": args.grid_size_m,
        "min_cover_pct": args.min_cover_pct,
        "feature_rows": int(len(features)),
        "cards": {},
    }
    predictions: dict[str, pd.DataFrame] = {}
    for card_name, card_path in DEFAULT_CARDS.items():
        card = load_json(card_path)
        mask = card_mask(features, card)
        filtered = features.loc[mask].copy()
        filtered_path = output_dir / f"features_{card_name}_inrange.csv"
        filtered.to_csv(filtered_path, index=False)
        card_output = output_dir / card_name
        run(
            [
                sys.executable,
                "-m",
                "femic",
                "lidar",
                "inventory",
                "--bundle",
                str(bundle),
                "--model",
                str(card_path),
                "--features",
                str(filtered_path),
                "--output-dir",
                str(card_output),
                "--fragment-id-field",
                "fragment_id",
            ]
        )
        table = pd.read_csv(card_output / "inventory_als.csv")
        predictions[card_name] = table
        summary["cards"][card_name] = {
            "model_id": card["model_id"],
            "model_version": card["model_version"],
            "predictor_ranges": card.get("predictor_ranges", {}),
            "retained_cells": int(len(filtered)),
            "dropped_cells": int(len(features) - len(filtered)),
            **value_summary(table["value"]),
        }

    if args.fragments.exists() and args.vri_fragments.exists():
        fragment_summary, comparison = fragment_comparison(
            features, predictions, args.fragments, args.vri_fragments
        )
        summary["fragments"] = fragment_summary
        comparison.to_csv(output_dir / "fragment_comparison.csv", index=False)
    else:
        summary["fragments"] = {
            "status": "skipped",
            "reason": "fragment geometry or VRI fragment table not found",
        }

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"diagnostic summary: {summary_path}")


if __name__ == "__main__":
    main()
