"""Synthetic end-to-end test for the private LiDAR fit pipeline."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("numpy") is None or importlib.util.find_spec("pandas") is None,
    reason="numpy and pandas are required for the fit pipeline",
)

ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, header: list[str], rows: list[list[object]]) -> None:
    """Write a small CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def test_fit_pipeline_writes_cards_and_holdouts(tmp_path: Path) -> None:
    """The pipeline fits the three forms and writes stable cards."""
    plots: list[list[object]] = []
    features: list[list[object]] = []
    clusters: list[list[object]] = []
    for index in range(12):
        site = f"plot_{index:02d}"
        cluster = f"cluster_{index % 4}"
        x = 900000.0 + (index % 4) * 6000.0 + (index // 4) * 200.0
        y = 700000.0 + (index % 4) * 6000.0 + (index // 4) * 200.0
        lhmean = 7.0 + index * 0.8
        lhcv = 0.12 + (index % 3) * 0.04
        lhp95 = 10.0 + index * 1.2
        cc2m = 55.0 + (index % 5) * 9.0
        height = 2.0 + 0.9 * lhp95 + 0.1 * math.sin(index)
        ba = math.exp(-3.5 + 0.8 * math.log(lhmean) + 1.0 * math.log(cc2m))
        volume = math.exp(-3.0 + 1.3 * math.log(lhmean) + 1.1 * math.log(cc2m))
        last_year = 2023 if index % 2 == 0 else 2022
        plots.append([site, x, y, last_year, height, ba, volume])
        features.append([f"cell_{index:05d}", x, y, lhmean, lhcv, lhp95, cc2m])
        clusters.append([site, cluster])

    write(
        tmp_path / "plots.csv",
        [
            "site_identifier",
            "x",
            "y",
            "last_year",
            "lorey_height_m",
            "ba_m2_ha",
            "vol_m3_ha",
        ],
        plots,
    )
    write(
        tmp_path / "features.csv",
        ["fragment_id", "x_center", "y_center", "Lhmean", "Lhcv", "Lhp95", "CC2m"],
        features,
    )
    write(tmp_path / "clusters.csv", ["site_identifier", "cluster"], clusters)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "pipeline/fit_inventory_cards.py"),
            "--plots",
            str(tmp_path / "plots.csv"),
            "--features",
            str(tmp_path / "features.csv"),
            "--clusters",
            str(tmp_path / "clusters.csv"),
            "--output-dir",
            str(tmp_path / "fit"),
            "--match-radius-m",
            "25",
            "--temporal-train-year",
            "2023",
            "--temporal-test-year",
            "2022",
            "--min-plots",
            "6",
            "--write-cards",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads((tmp_path / "fit/fit_summary.json").read_text(encoding="utf-8"))
    assert summary["plot_count"] == 12
    assert summary["cards_written"] is True
    assert summary["attributes"]["height"]["loocv"]["n"] == 12
    assert summary["attributes"]["ba_m2_ha"]["spatial_cluster"]["n"] == 12
    assert summary["attributes"]["vol_m3_ha"]["temporal"]["n"] == 6
    assert summary["attributes"]["height"]["loocv"]["coefficient_stability"]["sign_changes"] == 0

    card = json.loads(
        (tmp_path / "fit/cards/als_gnn_private_ba_m2_ha_2026.json").read_text(encoding="utf-8")
    )
    assert card["schema_version"] == "femic.inventory.als.model.v1"
    assert card["attribute"] == "ba_m2_ha"
    assert card["link"] == "log"
    assert card["sample_count"] == 12
    assert "Lhmean" in card["coefficients"]
    assert "CC2m" in card["coefficients"]
    assert (tmp_path / "fit/cards/manifest.json").is_file()
