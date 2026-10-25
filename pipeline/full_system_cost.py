#!/usr/bin/env python3
"""Screening full-system harvest cost from the FHOPS harvest-system registry.

The system cost uses all registry roles and machine rates, with the primary
transport role as the system bottleneck. It is a screening estimate, not a
solved FHOPS shift schedule.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd


def _registry(fhops_src: Path):
    sys.path.insert(0, str(fhops_src))
    from fhops.costing.machine_rates import get_machine_rate
    from fhops.scheduling.systems.models import default_system_registry

    return default_system_registry(), get_machine_rate


def _primary_productivity(
    *,
    fhops_src: Path,
    system_id: str,
    role: str,
    overrides: dict[str, object],
    volume_per_ha: float,
    stems_per_ha: float,
    avg_stem: float,
    slope: float,
) -> float:
    command = [
        sys.executable,
        "-m",
        "fhops.cli.main",
        "dataset",
        "estimate-productivity",
        "--machine-role",
        role,
        "--harvest-system-id",
        system_id,
        "--avg-stem-size",
        str(avg_stem),
        "--volume-per-ha",
        str(volume_per_ha),
        "--stem-density",
        str(stems_per_ha),
        "--ground-slope",
        str(slope),
        "--allow-out-of-range",
    ]
    if role == "grapple_yarder":
        command += [
            "--grapple-turn-volume-m3",
            str(overrides.get("grapple_yarder_turn_volume_m3", 3.1)),
            "--grapple-yard-distance-m",
            str(overrides.get("grapple_yarder_yarding_distance_m", 82.0)),
            "--grapple-stems-per-cycle",
            str(overrides.get("grapple_yarder_stems_per_cycle", 2.9)),
        ]
    elif role == "grapple_skidder":
        command += [
            "--skidder-extraction-distance",
            str(overrides.get("skidder_extraction_distance_m", 85.0)),
            "--skidder-piece-volume",
            str(avg_stem),
            "--skidder-empty-distance",
            str(overrides.get("skidder_extraction_distance_m", 85.0)),
            "--skidder-loaded-distance",
            str(overrides.get("skidder_extraction_distance_m", 85.0)),
            "--skidder-pieces-per-cycle",
            "3",
        ]
    elif role == "helicopter_longline":
        command += [
            "--helicopter-model",
            str(overrides.get("helicopter_model", "bell214b")),
            "--helicopter-flight-distance-m",
            str(overrides.get("helicopter_flight_distance_m", 900.0)),
            "--helicopter-load-factor",
            str(overrides.get("helicopter_load_factor", 0.7)),
            "--helicopter-delay-minutes",
            str(overrides.get("helicopter_delay_minutes", 0.5)),
        ]
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as handle:
        telemetry = Path(handle.name)
    command += ["--telemetry-log", str(telemetry)]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(fhops_src)
    result = subprocess.run(command, capture_output=True, text=True, env=env, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr + result.stdout)
    lines = [line for line in telemetry.read_text().splitlines() if line.strip()]
    telemetry.unlink(missing_ok=True)
    if lines:
        payload = json.loads(lines[-1])
        outputs = payload.get("outputs", {})
        for key, value in outputs.items():
            if "productivity" in key and isinstance(value, (int, float)):
                return float(value)
    for line in result.stdout.splitlines():
        if "Productivity" in line and "│" in line:
            values = re.findall(r"\d+(?:\.\d+)?", line)
            if values:
                return float(values[-1])
    raise RuntimeError("could not parse productivity from FHOPS output")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fhops-src", type=Path, required=True)
    parser.add_argument("--blocks", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    registry, get_machine_rate = _registry(args.fhops_src)
    blocks = pd.read_csv(args.blocks)
    records: list[dict[str, object]] = []
    for row in blocks.itertuples(index=False):
        system = registry[row.system_id]
        primary = next(job for job in system.jobs if job.name == "primary_transport")
        overrides = dict(primary.productivity_overrides or {})
        productivity = _primary_productivity(
            fhops_src=args.fhops_src,
            system_id=system.system_id,
            role=primary.machine_role,
            overrides=overrides,
            volume_per_ha=row.volume_per_ha,
            stems_per_ha=row.stems_per_ha,
            avg_stem=row.avg_stem_size_m3,
            slope=row.slope_percent,
        )
        rates = []
        move_in = 0.0
        hand_fall_cost = 0.0
        for job in system.jobs:
            if job.machine_role in {"hand_faller", "hand_or_mech_faller"}:
                hand_fall_cost += 1.11  # TN98 cedar, one faller; screening
                continue
            rate_role = {
                "helicopter_longline": "helicopter_bell214b",
            }.get(job.machine_role, job.machine_role)
            rate = get_machine_rate(rate_role)
            if rate is None:
                continue
            rates.append(rate.total_cost_per_smh / rate.default_utilization)
            move_in += rate.move_in_cost
        total_rate = sum(rates)
        cost_per_m3 = (
            total_rate / productivity
            + hand_fall_cost
            + (move_in / row.volume_m3 if row.volume_m3 else 0.0)
        )
        records.append(
            {
                "block_id": row.block_id,
                "system_id": system.system_id,
                "primary_role": primary.machine_role,
                "system_productivity_m3_per_pmh": round(productivity, 2),
                "machine_rate_per_pmh": round(total_rate, 2),
                "hand_fall_cost_per_m3": round(hand_fall_cost, 2),
                "move_in_per_m3": round(move_in / row.volume_m3, 2) if row.volume_m3 else None,
                "system_cost_per_m3": round(cost_per_m3, 2),
                "data_status": "screening_registry_bottleneck",
            }
        )
    frame = pd.DataFrame.from_records(records)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    print(frame.to_string(index=False))


if __name__ == "__main__":
    main()
