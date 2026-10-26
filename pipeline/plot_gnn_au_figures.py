#!/usr/bin/env python3
"""Generate the SI violin figure and all AU curve plots for the GNN docs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SI_STRATA = ("CWH_CW", "CWH_HW", "CWH_YC", "CWH_BA")
SI_LEVELS = ("L", "M", "H")
COLORS = {46: "#4477AA", 47: "#EE6677"}


def _load_checkpoint(path: Path) -> pd.DataFrame:
    frame = pd.read_feather(path)
    frame["SITE_INDEX"] = pd.to_numeric(frame["SITE_INDEX"], errors="coerce")
    return frame


def _si_summary(checkpoint: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for stratum in SI_STRATA:
        for si_level in SI_LEVELS:
            for tsa in (46, 47):
                values = checkpoint.loc[
                    (checkpoint["stratum"] == stratum)
                    & (checkpoint["si_level"] == si_level)
                    & (checkpoint["tsa_code"] == tsa),
                    "SITE_INDEX",
                ].dropna()
                values = values[values > 0]
                rows.append(
                    {
                        "stratum": stratum,
                        "si_level": si_level,
                        "tsa": tsa,
                        "n": int(values.size),
                        "median_si_m": float(values.median()) if values.size else None,
                        "p10_si_m": float(np.percentile(values, 10)) if values.size else None,
                        "p90_si_m": float(np.percentile(values, 90)) if values.size else None,
                    }
                )
    return pd.DataFrame(rows)


def _plot_si_violin(
    checkpoint: pd.DataFrame,
    *,
    output_path: Path,
    summary_path: Path,
) -> None:
    summary = _si_summary(checkpoint)
    summary.to_csv(summary_path, index=False)
    fig, axes = plt.subplots(
        len(SI_STRATA),
        len(SI_LEVELS),
        figsize=(13.5, 12.0),
        sharey=True,
    )
    for row, stratum in enumerate(SI_STRATA):
        for col, si_level in enumerate(SI_LEVELS):
            ax = axes[row, col]
            groups: list[np.ndarray] = []
            for tsa in (46, 47):
                values = checkpoint.loc[
                    (checkpoint["stratum"] == stratum)
                    & (checkpoint["si_level"] == si_level)
                    & (checkpoint["tsa_code"] == tsa),
                    "SITE_INDEX",
                ].dropna()
                values = values[values > 0].to_numpy()
                groups.append(values)
            parts = ax.violinplot(
                groups,
                positions=[1, 2],
                widths=0.8,
                showextrema=False,
                showmedians=True,
            )
            for body, tsa in zip(parts["bodies"], (46, 47), strict=True):
                body.set_facecolor(COLORS[tsa])
                body.set_edgecolor(COLORS[tsa])
                body.set_alpha(0.55)
            medians = parts["cmedians"]
            medians.set_color("black")
            medians.set_linewidth(1.2)
            for position, values, _tsa in zip((1, 2), groups, (46, 47), strict=True):
                ax.text(
                    position,
                    0.98,
                    f"n={values.size}",
                    transform=ax.get_xaxis_transform(),
                    ha="center",
                    va="top",
                    fontsize=8,
                )
            ax.set_title(f"{stratum} — {si_level}", fontsize=10)
            ax.set_xticks([1, 2], ["TSA 46", "TSA 47"])
            ax.set_ylim(0, 40)
            ax.grid(axis="y", alpha=0.25)
            if col == 0:
                ax.set_ylabel("Checkpoint site index (m)")
    fig.suptitle(
        "Checkpoint SI distributions for same-named strata, by TSA and SI level",
        fontsize=14,
        y=0.995,
    )
    fig.text(
        0.5,
        0.005,
        "Violin width shows the distribution; black line is the median. Source: GNN checkpoint.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.98))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _curve_arrays(curves: pd.DataFrame) -> dict[int, np.ndarray]:
    return {
        int(curve_id): group.sort_values("x")[["x", "y"]].to_numpy()
        for curve_id, group in curves.groupby("curve_id")
    }


def _plot_one_au(
    *,
    ax: plt.Axes,
    row: pd.Series,
    curves: dict[int, np.ndarray],
    show_legend: bool,
) -> None:
    untreated = curves.get(int(row["untreated_curve_id"]))
    treated = curves.get(int(row["treated_curve_id"]))
    if untreated is not None:
        ax.plot(untreated[:, 0], untreated[:, 1], color="#4477AA", lw=1.4, label="untreated")
    if treated is not None:
        ax.plot(
            treated[:, 0],
            treated[:, 1],
            color="#EE6677",
            lw=1.4,
            ls="--",
            label="treated",
        )
    ax.set_xlim(0, 300)
    all_y = [values[:, 1] for values in (untreated, treated) if values is not None and values.size]
    upper = max((float(np.nanmax(values)) for values in all_y), default=100.0)
    ax.set_ylim(0, max(50.0, math.ceil(upper / 50.0) * 50.0))
    ax.set_title(
        f"{int(row['au_id'])} | TSA {int(row['tsa'])} | {row['stratum_code']} {row['si_level']}",
        fontsize=8,
    )
    ax.grid(alpha=0.2)
    ax.tick_params(labelsize=7)
    if show_legend:
        ax.legend(fontsize=7, loc="upper left")


def _plot_au_curves(
    *,
    au_table: Path,
    curve_points: Path,
    area_csv: Path,
    output_dir: Path,
    index_csv: Path,
    grid_path: Path,
) -> pd.DataFrame:
    au = pd.read_csv(au_table)
    curves = _curve_arrays(pd.read_csv(curve_points))
    area = pd.read_csv(area_csv)[["au_id", "area_ha", "thlb_ha"]]
    au = au.merge(area, on="au_id", how="left")
    au["area_ha"] = au["area_ha"].fillna(0.0)
    au["thlb_ha"] = au["thlb_ha"].fillna(0.0)
    au = au.sort_values(["tsa", "au_id"]).reset_index(drop=True)
    plot_dir = output_dir / "au_curves"
    plot_dir.mkdir(parents=True, exist_ok=True)

    for _, row in au.iterrows():
        fig, ax = plt.subplots(figsize=(5.2, 3.4))
        _plot_one_au(ax=ax, row=row, curves=curves, show_legend=True)
        ax.set_xlabel("Age")
        ax.set_ylabel("Volume (m3/ha)")
        fig.tight_layout()
        fig.savefig(plot_dir / f"{int(row['au_id'])}.png", dpi=160)
        plt.close(fig)

    cols = 6
    rows = math.ceil(len(au) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(24, 24), sharex=True, sharey=False)
    flat_axes = axes.ravel()
    for index, (_, row) in enumerate(au.iterrows()):
        _plot_one_au(
            ax=flat_axes[index],
            row=row,
            curves=curves,
            show_legend=index == 0,
        )
        flat_axes[index].text(
            0.98,
            0.04,
            f"{row['area_ha']:.0f} ha | {row['thlb_ha']:.0f} THLB",
            transform=flat_axes[index].transAxes,
            ha="right",
            va="bottom",
            fontsize=6,
        )
    for ax in flat_axes[len(au) :]:
        ax.set_visible(False)
    fig.suptitle("TSA-prefixed AU yield curves used in the GNN prototype", fontsize=18)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    grid_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(grid_path, dpi=150)
    plt.close(fig)

    index = au[
        [
            "au_id",
            "tsa",
            "stratum_code",
            "si_level",
            "area_ha",
            "thlb_ha",
            "untreated_curve_id",
            "treated_curve_id",
        ]
    ].copy()
    index["plot_path"] = index["au_id"].map(
        lambda au_id: f"_static/figures/au_curves/{int(au_id)}.png"
    )
    index.to_csv(index_csv, index=False)
    return index


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("data/gnn_combined_checkpoint.feather"),
    )
    parser.add_argument(
        "--au-table",
        type=Path,
        default=Path("data/model_input_bundle_gnn/au_table.csv"),
    )
    parser.add_argument(
        "--curve-points",
        type=Path,
        default=Path("data/model_input_bundle_gnn/curve_points_table.csv"),
    )
    parser.add_argument(
        "--area-csv",
        type=Path,
        default=Path("config/tsr/gnn_au/gnn_au_area.csv"),
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("docs/_static/figures"),
    )
    parser.add_argument(
        "--summary-dir",
        type=Path,
        default=Path("config/tsr/gnn_au"),
    )
    return parser.parse_args()


def main() -> None:
    """Generate the SI violin figure, AU plots, and index CSVs."""
    args = _parse_args()
    args.figures_dir.mkdir(parents=True, exist_ok=True)
    args.summary_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = _load_checkpoint(args.checkpoint)
    _plot_si_violin(
        checkpoint,
        output_path=args.figures_dir / "si_stratum_violin.png",
        summary_path=args.summary_dir / "gnn_si_stratum_summary.csv",
    )
    index = _plot_au_curves(
        au_table=args.au_table,
        curve_points=args.curve_points,
        area_csv=args.area_csv,
        output_dir=args.figures_dir,
        index_csv=args.summary_dir / "gnn_au_curve_plot_index.csv",
        grid_path=args.figures_dir / "au_curves_grid.png",
    )
    print(f"wrote {len(index)} AU plots and SI violin panels")


if __name__ == "__main__":
    main()
