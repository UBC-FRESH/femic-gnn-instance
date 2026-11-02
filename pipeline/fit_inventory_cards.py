#!/usr/bin/env python3
"""Fit research-only INV-01 cards from plot-matched point-cloud features.

The input is a plot table with responses and either a plot-level feature table
(``--plot-features``) or a point-cloud grid feature table plus a nearest-cell match
(``--features`` + ``--plots``). The script reports leave-one-plot-out, spatial-cluster,
and temporal checks, and writes FEMIC model cards only when the coefficient signs are
stable across leave-one-out folds.

This is a research tool. It does not promote a card, publish private data, or change
the GNN model. A card written here remains private until the P15 preregistration and
ADR 0007 review gates are satisfied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

DEFAULT_RECENT_SINCE = 2018


def parse_args() -> argparse.Namespace:
    """Return command-line options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plots", type=Path, required=True)
    parser.add_argument("--features", type=Path)
    parser.add_argument("--plot-features", type=Path)
    parser.add_argument("--clusters", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--match-radius-m", type=float, default=20.0)
    parser.add_argument("--cluster-distance-m", type=float, default=5000.0)
    parser.add_argument("--temporal-train-year", type=int)
    parser.add_argument("--temporal-test-year", type=int)
    parser.add_argument("--min-plots", type=int, default=6)
    parser.add_argument("--write-cards", action="store_true")
    parser.add_argument("--force-cards", action="store_true")
    return parser.parse_args()


def match_features(plots: pd.DataFrame, features: pd.DataFrame, radius_m: float) -> pd.DataFrame:
    """Match each plot to its nearest feature cell within ``radius_m``."""
    x = features["x_center"].to_numpy(dtype=float)
    y = features["y_center"].to_numpy(dtype=float)
    matches: list[pd.Series] = []
    for row in plots.itertuples(index=False):
        distance = np.hypot(x - float(row.x), y - float(row.y))
        index = int(np.argmin(distance))
        if distance[index] > radius_m:
            raise ValueError(f"plot {row.site_identifier} has no feature cell within {radius_m} m")
        match = features.iloc[index].copy()
        match["site_identifier"] = row.site_identifier
        matches.append(match)
    return pd.DataFrame(matches)


def load_analysis_table(args: argparse.Namespace) -> pd.DataFrame:
    """Load and join the plot responses and predictors."""
    plots = pd.read_csv(args.plots)
    if args.plot_features is not None:
        joined = plots.merge(pd.read_csv(args.plot_features), on="site_identifier", how="inner")
    else:
        if args.features is None:
            raise SystemExit("provide --plot-features or --features")
        features = pd.read_csv(args.features)
        joined = match_features(plots, features, args.match_radius_m)
        joined = joined.merge(plots, on="site_identifier", how="left")
    return joined


def response_column(form: str) -> str:
    """Return the response column for a model form."""
    return "lorey_height_m" if form == "height" else form


def build_design(frame: pd.DataFrame, form: str) -> tuple[np.ndarray, np.ndarray]:
    """Return the design matrix and response."""
    if form == "height":
        predictors = np.column_stack([np.ones(len(frame)), frame["Lhp95"].to_numpy(dtype=float)])
        response = frame[response_column(form)].to_numpy(dtype=float)
        return predictors, response
    predictors = np.column_stack(
        [
            np.ones(len(frame)),
            np.log(frame["Lhmean"].to_numpy(dtype=float)),
            np.log(frame["CC2m"].to_numpy(dtype=float)),
        ]
    )
    response = np.log(frame[response_column(form)].to_numpy(dtype=float))
    return predictors, response


def fit_model(frame: pd.DataFrame, form: str, attributes: list[str]) -> dict[str, Any]:
    """Fit one model form and return its parameters and prediction function."""
    matrix, response = build_design(frame, form)
    coefficients, *_ = np.linalg.lstsq(matrix, response, rcond=None)
    fitted = matrix @ coefficients
    residuals = response - fitted
    if form == "height":
        scale = 1.0

        def predict(design: np.ndarray) -> np.ndarray:
            return np.asarray(design @ coefficients, dtype=float)
    else:
        scale = float(np.mean(np.exp(residuals)))

        def predict(design: np.ndarray) -> np.ndarray:
            return np.asarray(np.exp(design @ coefficients) * scale, dtype=float)

    return {
        "form": form,
        "attributes": attributes,
        "intercept": float(coefficients[0]),
        "coefficients": [float(value) for value in coefficients[1:]],
        "output_scale": scale,
        "predict": predict,
    }


def fit_predict(
    frame: pd.DataFrame,
    form: str,
    attributes: list[str],
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> np.ndarray:
    """Fit on ``train`` and predict ``test``."""
    model = fit_model(train, form, attributes)
    matrix, _ = build_design(test, form)
    return np.asarray(model["predict"](matrix), dtype=float)


def metrics(observed: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    """Return RMSE, bias, MAE, and R2."""
    residual = predicted - observed
    total = np.sum((observed - observed.mean()) ** 2)
    return {
        "n": float(len(observed)),
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "bias": float(np.mean(residual)),
        "mae": float(np.mean(np.abs(residual))),
        "r2": float(1.0 - np.sum(residual**2) / total) if total > 0 else float("nan"),
    }


def loocv(
    frame: pd.DataFrame, form: str, attributes: list[str]
) -> tuple[dict[str, Any], pd.DataFrame]:
    """Run leave-one-plot-out CV and collect fold parameters."""
    predictions = []
    fold_parameters: list[dict[str, Any]] = []
    for index in range(len(frame)):
        train = frame.drop(index=index)
        test = frame.iloc[[index]]
        predicted = fit_predict(frame, form, attributes, train, test)[0]
        model = fit_model(train, form, attributes)
        fold_parameters.append(model)
        predictions.append(
            {
                "site_identifier": test.iloc[0]["site_identifier"],
                "attribute": form,
                "observed": float(test.iloc[0][response_column(form)]),
                "predicted": float(predicted),
                "design": "loocv",
            }
        )
    predicted_values = np.array([row["predicted"] for row in predictions])
    observed_values = frame[response_column(form)].to_numpy(dtype=float)
    summary = metrics(observed_values, predicted_values)
    coefficients = np.array([model["coefficients"] for model in fold_parameters], dtype=float)
    summary["coefficient_stability"] = {
        "mean": coefficients.mean(axis=0).tolist(),
        "sd": coefficients.std(axis=0, ddof=1).tolist() if len(coefficients) > 1 else [0.0],
        "min": coefficients.min(axis=0).tolist(),
        "max": coefficients.max(axis=0).tolist(),
        "sign_changes": int(
            np.sum(np.sign(coefficients).min(axis=0) != np.sign(coefficients).max(axis=0))
        ),
    }
    return summary, pd.DataFrame(predictions)


def spatial_cv(
    frame: pd.DataFrame, clusters: pd.Series, form: str, attributes: list[str]
) -> tuple[dict[str, Any], pd.DataFrame]:
    """Run leave-one-cluster-out CV."""
    predictions = []
    for cluster in sorted(clusters.unique()):
        test = frame[clusters == cluster]
        train = frame[clusters != cluster]
        if train.empty or test.empty:
            continue
        predicted = fit_predict(frame, form, attributes, train, test)
        for site, observed, value in zip(
            test["site_identifier"], test[response_column(form)], predicted, strict=True
        ):
            predictions.append(
                {
                    "site_identifier": site,
                    "attribute": form,
                    "observed": float(observed),
                    "predicted": float(value),
                    "design": f"spatial_cluster_{cluster}",
                }
            )
    table = pd.DataFrame(predictions)
    if table.empty:
        return {"status": "skipped", "reason": "no cluster folds"}, table
    summary = metrics(table["observed"].to_numpy(), table["predicted"].to_numpy())
    return summary, table


def temporal_check(
    frame: pd.DataFrame,
    form: str,
    attributes: list[str],
    train_year: int,
    test_year: int,
) -> tuple[dict[str, Any], pd.DataFrame]:
    """Fit on one measurement year and test on another."""
    if "last_year" not in frame.columns:
        return {"status": "skipped", "reason": "last_year missing"}, pd.DataFrame()
    train = frame[frame["last_year"] == train_year]
    test = frame[frame["last_year"] == test_year]
    if train.empty or test.empty:
        return {
            "status": "skipped",
            "reason": "train or test year has no plots",
            "train": len(train),
            "test": len(test),
        }, pd.DataFrame()
    predicted = fit_predict(frame, form, attributes, train, test)
    rows = [
        {
            "site_identifier": site,
            "attribute": form,
            "observed": float(observed),
            "predicted": float(value),
            "design": f"temporal_{train_year}_to_{test_year}",
        }
        for site, observed, value in zip(
            test["site_identifier"], test[response_column(form)], predicted, strict=True
        )
    ]
    table = pd.DataFrame(rows)
    return metrics(test[response_column(form)].to_numpy(), predicted), table


def derive_clusters(frame: pd.DataFrame, distance_m: float) -> pd.Series:
    """Assign clusters by connected components under a distance threshold."""
    count = len(frame)
    parent = list(range(count))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    xs = frame["x"].to_numpy(dtype=float)
    ys = frame["y"].to_numpy(dtype=float)
    for i in range(count):
        for j in range(i + 1, count):
            if np.hypot(xs[i] - xs[j], ys[i] - ys[j]) <= distance_m:
                union(i, j)
    roots = [find(index) for index in range(count)]
    unique = {root: f"cluster_{number + 1}" for number, root in enumerate(sorted(set(roots)))}
    return pd.Series([unique[root] for root in roots], index=frame.index)


def card_for(
    form: str,
    model: dict[str, Any],
    frame: pd.DataFrame,
    loocv_summary: dict[str, Any],
) -> dict[str, Any]:
    """Build a FEMIC model card for one attribute."""
    attribute, unit, link, predictors = {
        "height": ("lorey_height_m", "m", "identity", ["Lhp95"]),
        "ba_m2_ha": ("ba_m2_ha", "m2/ha", "log", ["Lhmean", "CC2m"]),
        "vol_m3_ha": ("vol_m3_ha", "m3/ha", "log", ["Lhmean", "CC2m"]),
    }[form]
    coefficients = dict(zip(predictors, model["coefficients"], strict=True))
    predictor_ranges = {
        predictor: [
            float(frame[predictor].min()),
            float(frame[predictor].max()),
        ]
        for predictor in predictors
    }
    return {
        "schema_version": "femic.inventory.als.model.v1",
        "model_id": f"gnn-private-{attribute}-2026",
        "model_version": "2026.1",
        "attribute": attribute,
        "unit": unit,
        "link": link,
        "output_scale": model["output_scale"],
        "intercept": model["intercept"],
        "coefficients": coefficients,
        "rmse": loocv_summary["rmse"],
        "sample_count": len(frame),
        "training_scope": (
            "Private LiDAR first-return features matched to GNN-area FAIB plots; "
            "research-only, 8-plot primary set."
        ),
        "source": "Private LiDAR upload and public FAIB plots; P16 fit pipeline.",
        "applicability": {
            "regions": ["GNN AOI"],
            "species": [],
            "notes": "Research-only; not an operational inventory. See P15 preregistration.",
        },
        "predictor_ranges": predictor_ranges,
        "caveats": [
            "Eight primary plots; LOOCV and spatial-cluster checks only.",
            "Not an independent P48/P49 validation.",
            "Derived from private raw LiDAR; publication requires partner review.",
            "Do not use for operability, THLB, AAC, or WS4/FHOPS decisions.",
        ],
    }


def main() -> None:
    """Run the fit and write the evaluation and optional cards."""
    args = parse_args()
    frame = load_analysis_table(args).reset_index(drop=True)
    if len(frame) < args.min_plots:
        raise SystemExit(f"only {len(frame)} plots; need at least {args.min_plots}")

    if args.clusters is not None:
        cluster_table = pd.read_csv(args.clusters)
        frame = frame.merge(cluster_table, on="site_identifier", how="left").reset_index(drop=True)
        if frame["cluster"].isna().any():
            raise SystemExit("cluster table does not cover every plot")
        clusters = frame["cluster"].reset_index(drop=True)
    else:
        clusters = derive_clusters(frame, args.cluster_distance_m)

    forms = {
        "height": ["lorey_height_m"],
        "ba_m2_ha": ["ba_m2_ha"],
        "vol_m3_ha": ["vol_m3_ha"],
    }
    summary: dict[str, Any] = {
        "plot_count": len(frame),
        "attributes": {},
        "privacy": "derived-private-until-review",
    }
    predictions = []
    cards: dict[str, dict[str, Any]] = {}
    for form, attributes in forms.items():
        loocv_summary, loocv_predictions = loocv(frame, form, attributes)
        spatial_summary, spatial_predictions = spatial_cv(frame, clusters, form, attributes)
        temporal_summary: dict[str, Any] = {
            "status": "skipped",
            "reason": "not requested",
        }
        temporal_predictions = pd.DataFrame()
        if args.temporal_train_year is not None and args.temporal_test_year is not None:
            temporal_summary, temporal_predictions = temporal_check(
                frame,
                form,
                attributes,
                args.temporal_train_year,
                args.temporal_test_year,
            )
        model = fit_model(frame, form, attributes)
        summary["attributes"][form] = {
            "loocv": loocv_summary,
            "spatial_cluster": spatial_summary,
            "temporal": temporal_summary,
        }
        predictions.append(loocv_predictions)
        predictions.append(spatial_predictions)
        predictions.append(temporal_predictions)
        cards[form] = card_for(form, model, frame, loocv_summary)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.concat(predictions, ignore_index=True).to_csv(
        args.output_dir / "predictions.csv", index=False
    )
    (args.output_dir / "fit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    stable = all(
        summary["attributes"][form]["loocv"]["coefficient_stability"]["sign_changes"] == 0
        for form in forms
    )
    summary["cards_written"] = False
    if args.write_cards:
        if not stable and not args.force_cards:
            summary["cards_reason"] = "coefficient sign changes across LOOCV folds"
        else:
            card_dir = args.output_dir / "cards"
            card_dir.mkdir(parents=True, exist_ok=True)
            manifest: dict[str, Any] = {"cards": {}, "stable": stable}
            for form, card in cards.items():
                path = card_dir / f"als_gnn_private_{form}_2026.json"
                text = json.dumps(card, indent=2, sort_keys=True) + "\n"
                path.write_text(text, encoding="utf-8")
                manifest["cards"][str(path.name)] = hashlib.sha256(text.encode("utf-8")).hexdigest()
            (card_dir / "manifest.json").write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            summary["cards_written"] = True
    (args.output_dir / "fit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
