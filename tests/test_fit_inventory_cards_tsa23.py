"""Regression test: the fit pipeline reproduces the published TSA 23 cards."""

from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("numpy") is None or importlib.util.find_spec("pandas") is None,
    reason="numpy and pandas are required for the fit pipeline",
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/inv01_tsa23_training.csv"


def read_fixture() -> list[dict[str, str]]:
    """Read the public TSA 23 training fixture."""
    with FIXTURE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    """Write a small CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def test_pipeline_reproduces_published_tsa23_cards(tmp_path: Path) -> None:
    """The fitted coefficients and scale match the published cards."""
    rows = read_fixture()
    assert len(rows) == 14
    write_csv(
        tmp_path / "plots.csv",
        ["site_identifier", "last_year", "lorey_height_m", "ba_m2_ha", "vol_m3_ha"],
        [
            [
                row["site_identifier"],
                row["last_year"],
                row["lorey_height_m"],
                row["ba_m2_ha"],
                row["vol_m3_ha"],
            ]
            for row in rows
        ],
    )
    write_csv(
        tmp_path / "features.csv",
        ["site_identifier", "Lhmean", "Lhcv", "Lhp95", "CC2m"],
        [
            [
                row["site_identifier"],
                row["Lhmean"],
                row["Lhcv"],
                row["Lhp95"],
                row["CC2m"],
            ]
            for row in rows
        ],
    )
    write_csv(
        tmp_path / "clusters.csv",
        ["site_identifier", "cluster"],
        [[row["site_identifier"], "cluster_1"] for row in rows],
    )
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "pipeline/fit_inventory_cards.py"),
            "--plots",
            str(tmp_path / "plots.csv"),
            "--plot-features",
            str(tmp_path / "features.csv"),
            "--clusters",
            str(tmp_path / "clusters.csv"),
            "--output-dir",
            str(tmp_path / "fit"),
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
    assert summary["cards_written"] is True
    assert summary["attributes"]["height"]["loocv"]["rmse"] == pytest.approx(
        0.6884895720957835, rel=1e-9
    )
    assert summary["attributes"]["ba_m2_ha"]["loocv"]["rmse"] == pytest.approx(
        4.41421558291288, rel=1e-9
    )
    assert summary["attributes"]["vol_m3_ha"]["loocv"]["rmse"] == pytest.approx(
        20.665787282776183, rel=1e-9
    )

    height = json.loads(
        (tmp_path / "fit/cards/als_gnn_private_height_2026.json").read_text(encoding="utf-8")
    )
    assert height["intercept"] == pytest.approx(1.9441063309517714, rel=1e-9)
    assert height["coefficients"]["Lhp95"] == pytest.approx(0.8351084469592212, rel=1e-9)
    assert height["output_scale"] == pytest.approx(1.0, rel=1e-12)

    basal = json.loads(
        (tmp_path / "fit/cards/als_gnn_private_ba_m2_ha_2026.json").read_text(encoding="utf-8")
    )
    assert basal["intercept"] == pytest.approx(-4.724750214946937, rel=1e-9)
    assert basal["coefficients"]["Lhmean"] == pytest.approx(0.8686310009684395, rel=1e-9)
    assert basal["coefficients"]["CC2m"] == pytest.approx(1.3794686095244624, rel=1e-9)
    assert basal["output_scale"] == pytest.approx(1.008780042159369, rel=1e-9)

    volume = json.loads(
        (tmp_path / "fit/cards/als_gnn_private_vol_m3_ha_2026.json").read_text(encoding="utf-8")
    )
    assert volume["intercept"] == pytest.approx(-4.009416713953133, rel=1e-9)
    assert volume["coefficients"]["Lhmean"] == pytest.approx(1.7395991112544076, rel=1e-9)
    assert volume["coefficients"]["CC2m"] == pytest.approx(1.1516782963514058, rel=1e-9)
    assert volume["output_scale"] == pytest.approx(1.004526898452813, rel=1e-9)
