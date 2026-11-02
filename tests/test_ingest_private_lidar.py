"""Integration test for the private LiDAR ingest kit."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("laspy")
pytest.importorskip("pyproj")

import laspy
import numpy as np
from pyproj import CRS

ROOT = Path(__file__).resolve().parents[1]


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Build a tiny LAS, AOI, request table, and manifest."""
    las = laspy.LasData(laspy.LasHeader(point_format=3, version="1.2"))
    las.header.add_crs(CRS.from_epsg(3005))
    las.x = np.array([900000.0, 900100.0, 900200.0])
    las.y = np.array([700000.0, 700100.0, 700200.0])
    las.z = np.array([100.0, 101.0, 102.0])
    las.write(tmp_path / "tile.las")

    aoi = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [899000, 699000],
                            [901000, 699000],
                            [901000, 701000],
                            [899000, 701000],
                            [899000, 699000],
                        ]
                    ],
                },
            }
        ],
    }
    (tmp_path / "aoi.geojson").write_text(json.dumps(aoi), encoding="utf-8")
    (tmp_path / "request.csv").write_text(
        "site_identifier,request_priority,x_epsg3005,y_epsg3005,"
        "request_bbox_minx,request_bbox_miny,request_bbox_maxx,request_bbox_maxy\n"
        "1,high,900050,700050,898000,698000,902000,702000\n"
        "2,secondary,950000,750000,948000,748000,952000,752000\n",
        encoding="utf-8",
    )
    digest = hashlib.sha256((tmp_path / "tile.las").read_bytes()).hexdigest()
    (tmp_path / "SHA256SUMS.txt").write_text(f"{digest}  tile.las\n", encoding="utf-8")
    return (
        tmp_path / "tile.las",
        tmp_path / "aoi.geojson",
        tmp_path / "request.csv",
        tmp_path / "SHA256SUMS.txt",
    )


def _run(tmp_path: Path, verify: bool = True) -> subprocess.CompletedProcess[str]:
    """Run the ingest script on the fixture."""
    _fixture(tmp_path)
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "pipeline/ingest_private_lidar.py"),
            "--root",
            str(tmp_path),
            "--aoi",
            str(tmp_path / "aoi.geojson"),
            "--request-csv",
            str(tmp_path / "request.csv"),
            "--output-dir",
            str(tmp_path / "private"),
            "--public-dir",
            str(tmp_path / "public"),
            *(["--verify-hashes"] if verify else []),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_ingest_reports_manifest_coverage_and_public_redaction(tmp_path: Path) -> None:
    """A valid drop is inventoried and the public output has no raw filenames."""
    result = _run(tmp_path)
    assert result.returncode == 0, result.stderr
    private = json.loads((tmp_path / "private/summary_private.json").read_text(encoding="utf-8"))
    assert private["file_count"] == 1
    assert private["manifest"]["hash_mismatches"] == []
    assert private["coverage"]["p13_high_covered"] == 1
    assert private["coverage"]["p13_plot_count"] == 1
    assert private["tiles"][0]["file_name"] == "tile.las"

    public_text = (tmp_path / "public/summary_public.json").read_text(encoding="utf-8")
    assert "tile.las" not in public_text
    assert "file_name" not in public_text
    public = json.loads(public_text)
    assert public["privacy"] == "derived-public"
    assert public["file_count"] == 1
    assert public["tiles"][0]["tile_id"] == "tile_000000"


def test_ingest_flags_a_hash_mismatch(tmp_path: Path) -> None:
    """A changed file is reported as a hash mismatch."""
    result = _run(tmp_path)
    assert result.returncode == 0, result.stderr
    (tmp_path / "tile.las").write_bytes((tmp_path / "tile.las").read_bytes() + b"x")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "pipeline/ingest_private_lidar.py"),
            "--root",
            str(tmp_path),
            "--aoi",
            str(tmp_path / "aoi.geojson"),
            "--request-csv",
            str(tmp_path / "request.csv"),
            "--output-dir",
            str(tmp_path / "private2"),
            "--public-dir",
            str(tmp_path / "public2"),
            "--verify-hashes",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    private = json.loads((tmp_path / "private2/summary_private.json").read_text(encoding="utf-8"))
    assert private["manifest"]["hash_mismatches"] == ["tile.las"]
