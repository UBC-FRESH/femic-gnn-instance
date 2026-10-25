#!/usr/bin/env python3
"""Exercise the FHOPS marine transport path for the GNN instance.

This adapter uses the FHOPS Phase I marine path merged in
``UBC-FRESH/fhops#187`` (commit ``f788d7a6``). The fixture is a synthetic
Sunshine Coast -> Howe Sound case. It is **not** the GNN geography: the GNN AOI
is northern Vancouver Island. This is an API/cost-path test, not a GNN
transport estimate, terminal inventory, or current carrier quote.

The adapter scales the FHOPS fixture to an explicit one-day volume, sizes enough
drayage trucks and barges for that day, solves Phase I, and reports:

- drayage cost from the FHOPS result;
- barge variable cost from the FHOPS result;
- terminal handling cost from the FHOPS result;
- truck and barge fixed dispatch cost from the validated contract (Phase I
  itself excludes fixed costs; Phase II charges them);
- total and per-cubic-metre cost.

The legacy CLEWs/FFCM transport assumption remains a separate comparison path.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO = ROOT / "config/cost_revenue/transport/fhops_marine/scenario.yaml"
DEFAULT_CONFIG = ROOT / "config/cost_revenue/transport/fhops_marine.yaml"
DEFAULT_SOURCE = "UBC-FRESH/fhops#187 / f788d7a6 / examples/hauling_marine; not GNN geography"
DATA_STATUS = "upstream_fhops_fixture_api_test"
COST_TOLERANCE_CAD = 0.01


@dataclass(frozen=True)
class MarineTransportEstimate:
    """One solved FHOPS marine transport case.

    Attributes
    ----------
    case:
        Case label from the transport config, or ``custom``.
    status:
        FHOPS Phase I status.
    volume_m3:
        One-day volume sent through the marine lane.
    horizon_days:
        Hauling horizon length in days.
    barge_capacity_m3:
        Barge cargo capacity from the scenario.
    barge_utilization_pct:
        ``volume_m3 / (barge_trips * barge_capacity_m3)``.
    barge_trips:
        Integer barge trips in the solved plan.
    water_m3:
        Volume carried on the water leg.
    drayage_cost_cad:
        Road pickup and delivery cost from Phase I.
    barge_variable_cost_cad:
        Barge variable cost from Phase I.
    terminal_handling_cost_cad:
        Origin and destination terminal handling cost from Phase I.
    phase_i_cost_cad:
        FHOPS Phase I cost objective.
    contract_fixed_cost_cad:
        Daily truck and barge fixed dispatch cost from the contract.
    total_cost_cad:
        Phase I cost plus contract fixed dispatch cost.
    cost_per_m3_cad:
        ``total_cost_cad / water_m3``.
    trucks_used:
        Drayage trucks made available for the day.
    barges_used:
        Barges made available for the day.
    source:
        Upstream source and commit.
    data_status:
        ``upstream_fhops_fixture_api_test``.
    """

    case: str
    status: str
    volume_m3: float
    horizon_days: int
    barge_capacity_m3: float
    barge_utilization_pct: float
    barge_trips: int
    water_m3: float
    drayage_cost_cad: float
    barge_variable_cost_cad: float
    terminal_handling_cost_cad: float
    phase_i_cost_cad: float
    contract_fixed_cost_cad: float
    total_cost_cad: float
    cost_per_m3_cad: float
    trucks_used: int
    barges_used: int
    source: str
    data_status: str


def _load_fhops() -> tuple[Any, Any, Any, Any, Any]:
    """Import the optional FHOPS API, or exit with an actionable message."""
    try:
        from fhops.hauling.contract import Barge, HaulingDemand, HaulingSupply, PortSide, Truck
        from fhops.hauling.flow import build_flow_problem, solve_flow
        from fhops.scenario.contract.models import CalendarEntry
        from fhops.scenario.io import load_scenario
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "FHOPS is required for the marine transport adapter. Install the local "
            "UBC-FRESH/fhops checkout in the active environment."
        ) from exc
    return (
        Barge,
        HaulingDemand,
        HaulingSupply,
        PortSide,
        Truck,
        CalendarEntry,
        build_flow_problem,
        solve_flow,
        load_scenario,
    )


def _read_config(path: Path) -> dict[str, Any]:
    """Load the marine transport YAML config."""
    import yaml

    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Transport config must be a mapping: {path}")
    return payload


def _case_volumes(config: dict[str, Any], capacity_m3: float) -> list[tuple[str, float]]:
    """Return configured cases as ``(label, volume_m3)`` pairs.

    A case may provide ``volume_m3`` directly or a ``utilization`` fraction of
    the scenario barge capacity.
    """
    cases: list[tuple[str, float]] = []
    for item in config.get("cases", []):
        if not isinstance(item, dict):
            raise ValueError("Each transport case must be a mapping")
        label = str(item.get("id", "")).strip()
        if not label:
            raise ValueError("Each transport case needs an id")
        if "volume_m3" in item:
            volume = float(item["volume_m3"])
        else:
            volume = capacity_m3 * float(item.get("utilization", 0.0))
        if volume <= 0:
            raise ValueError(f"Case {label!r} has a non-positive volume")
        cases.append((label, volume))
    if not cases:
        raise ValueError("Transport config has no cases")
    return cases


def _truck_cycle_minutes(config: Any, route: Any, port_side: Any) -> float:
    """Return the loaded-plus-empty drayage cycle for one route."""
    origin = config.port_leg_for(route, port_side.ORIGIN)
    destination = config.port_leg_for(route, port_side.DESTINATION)
    return (
        origin.travel_minutes
        + (origin.return_travel_minutes or origin.travel_minutes)
        + destination.travel_minutes
        + (destination.return_travel_minutes or destination.travel_minutes)
    )


def _fit_scenario(
    scenario: Any,
    volume_m3: float,
    horizon_days: int,
    *,
    fhops: tuple[Any, ...],
) -> tuple[Any, int, int]:
    """Scale the fixture to one volume and size a feasible day fleet.

    The fixture was built for 180 m3 over three days with two trucks. A
    representative barge-day can exceed that, so this function sizes drayage
    trucks and barges from the validated contract and records the counts. It
    does not change the fixture's unit costs or route geometry.
    """
    (
        Barge,
        HaulingDemand,
        HaulingSupply,
        PortSide,
        Truck,
        CalendarEntry,
        _build_flow_problem,
        _solve_flow,
        _load_scenario,
    ) = fhops

    if volume_m3 <= 0:
        raise ValueError("volume_m3 must be positive")
    if horizon_days < 1:
        raise ValueError("horizon_days must be at least 1")

    config = scenario.hauling
    if config is None:
        raise ValueError("Scenario has no hauling section")
    if len(scenario.blocks) != 1:
        raise ValueError("The GNN marine fixture must have exactly one block")
    if len(config.marine_routes) != 1:
        raise ValueError("The GNN marine fixture must have exactly one marine route")

    route = config.marine_routes[0]
    truck_type = next(
        item for item in config.truck_types if item.id == route.truck_type_id
    )
    barge_type = config.barge_type(config.water_arc(route.water_arc_id).barge_type_id)
    per_day = volume_m3 / horizon_days

    scenario.num_days = horizon_days
    scenario.blocks[0].work_required = volume_m3
    config.planning_horizon_days = horizon_days
    config.start_day = 1
    config.supply = [
        HaulingSupply(
            block_id=scenario.blocks[0].id,
            log_sort_id=config.log_sorts[0].id,
            sorted_m3=volume_m3,
            unsorted_m3=0.0,
        )
    ]
    config.demand = [
        HaulingDemand(
            yard_id=config.sort_yards[0].id,
            log_sort_id=config.log_sorts[0].id,
            day=day,
            volume_m3=per_day if day < horizon_days else volume_m3 - per_day * (horizon_days - 1),
        )
        for day in range(1, horizon_days + 1)
    ]

    # A representative aggregate lane is not a terminal-inventory study. Keep
    # storage unconstrained and daily handling uncapped, and record that.
    for port in config.ports:
        port.storage_m3 = max(volume_m3 * 2.0, 1.0)
        port.daily_handling_m3 = None
    for yard in config.sort_yards:
        yard.unsorted_storage_m3 = max(yard.unsorted_storage_m3, volume_m3 * 2.0)
        yard.sorted_processing_m3_per_day = max(
            yard.sorted_processing_m3_per_day, per_day * 1.1
        )
        yard.unsorted_processing_m3_per_day = max(
            yard.unsorted_processing_m3_per_day, per_day * 1.1
        )
        yard.total_processing_m3_per_day = max(
            yard.total_processing_m3_per_day, per_day * 1.1
        )

    cycle_minutes = _truck_cycle_minutes(config, route, PortSide)
    regular_minutes = config.driver_policy.regular_minutes
    loads = math.ceil(volume_m3 / truck_type.capacity_m3)
    trucks_needed = max(
        2,
        math.ceil(loads * cycle_minutes / (regular_minutes * horizon_days)) + 1,
    )
    existing_trucks = list(config.trucks)
    for index in range(len(existing_trucks), trucks_needed):
        existing_trucks.append(
            Truck(
                id=f"gnn_h{index + 1}",
                contractor_id=config.contractors[0].id,
                truck_type_id=truck_type.id,
            )
        )
    config.trucks = existing_trucks

    barges_needed = max(1, math.ceil(per_day / barge_type.capacity_m3))
    existing_barges = list(config.barges)
    for index in range(len(existing_barges), barges_needed):
        existing_barges.append(
            Barge(
                id=f"gnn_b{index + 1}",
                contractor_id=config.contractors[0].id,
                barge_type_id=barge_type.id,
            )
        )
    config.barges = existing_barges

    scenario.calendar = [
        CalendarEntry(machine_id=machine.id, day=day, available=1)
        for machine in scenario.machines
        for day in range(1, horizon_days + 1)
    ]
    return scenario, len(config.trucks), len(config.barges)


def estimate_marine_transport(
    volume_m3: float,
    *,
    case: str = "custom",
    horizon_days: int = 1,
    scenario_path: Path = DEFAULT_SCENARIO,
    source: str = DEFAULT_SOURCE,
) -> MarineTransportEstimate:
    """Solve one FHOPS marine transport case.

    Parameters
    ----------
    volume_m3:
        One-day-scale volume to move through the marine lane.
    case:
        Label for the estimate.
    horizon_days:
        Hauling horizon length. The default is one representative barge day.
    scenario_path:
        FHOPS scenario bundle.
    source:
        Upstream provenance string.

    Returns
    -------
    MarineTransportEstimate
        Solved cost components and provenance.

    Raises
    ------
    RuntimeError
        When FHOPS does not return an optimal or feasible plan, or when the
        marine cost components do not reconcile with the objective.
    """
    fhops = _load_fhops()
    (
        _Barge,
        _HaulingDemand,
        _HaulingSupply,
        _PortSide,
        _Truck,
        _CalendarEntry,
        build_flow_problem,
        solve_flow,
        load_scenario,
    ) = fhops

    scenario = load_scenario(scenario_path)
    scenario, trucks_used, barges_used = _fit_scenario(
        scenario, volume_m3, horizon_days, fhops=fhops
    )
    result = solve_flow(build_flow_problem(scenario), objective="cost", solver="highs")
    if result.status not in {"optimal", "feasible"}:
        raise RuntimeError(f"FHOPS marine solve did not converge: status={result.status}")
    if result.cost_objective is None:
        raise RuntimeError("FHOPS marine solve returned no cost objective")
    if result.marine_flows.empty or result.barge_trips.empty:
        raise RuntimeError("FHOPS marine solve returned no marine flow or barge trip")

    water_m3 = float(result.marine_flows["water_m3"].sum())
    barge_trips = int(round(float(result.barge_trips["barge_trips"].sum())))
    if water_m3 <= 0 or barge_trips <= 0:
        raise RuntimeError("FHOPS marine solve returned no water volume or barge trip")

    drayage = float(result.marine_flows["drayage_cost"].sum())
    barge_variable = float(result.marine_flows["barge_variable_cost"].sum())
    terminal_handling = float(
        result.marine_flows["origin_handling_cost"].sum()
        + result.marine_flows["destination_handling_cost"].sum()
    )
    components = drayage + barge_variable + terminal_handling
    if abs(components - float(result.cost_objective)) > COST_TOLERANCE_CAD:
        raise RuntimeError(
            "FHOPS marine cost components do not reconcile with the objective: "
            f"{components:.2f} != {float(result.cost_objective):.2f}"
        )

    config = scenario.hauling
    if config is None:
        raise RuntimeError("Scenario lost its hauling config")
    route = config.marine_routes[0]
    truck_type = next(
        item for item in config.truck_types if item.id == route.truck_type_id
    )
    barge_type = config.barge_type(config.water_arc(route.water_arc_id).barge_type_id)
    fixed_cost = (
        trucks_used * truck_type.fixed_cost * horizon_days
        + barges_used * barge_type.fixed_cost * horizon_days
    )
    total = float(result.cost_objective) + fixed_cost
    capacity = barge_type.capacity_m3
    utilization = 100.0 * water_m3 / (barge_trips * capacity)

    return MarineTransportEstimate(
        case=case,
        status=result.status,
        volume_m3=round(volume_m3, 3),
        horizon_days=horizon_days,
        barge_capacity_m3=round(capacity, 3),
        barge_utilization_pct=round(utilization, 3),
        barge_trips=barge_trips,
        water_m3=round(water_m3, 3),
        drayage_cost_cad=round(drayage, 2),
        barge_variable_cost_cad=round(barge_variable, 2),
        terminal_handling_cost_cad=round(terminal_handling, 2),
        phase_i_cost_cad=round(float(result.cost_objective), 2),
        contract_fixed_cost_cad=round(fixed_cost, 2),
        total_cost_cad=round(total, 2),
        cost_per_m3_cad=round(total / water_m3, 6),
        trucks_used=trucks_used,
        barges_used=barges_used,
        source=source,
        data_status=DATA_STATUS,
    )


def estimate_configured_cases(
    config_path: Path = DEFAULT_CONFIG,
    *,
    scenario_path: Path | None = None,
) -> list[MarineTransportEstimate]:
    """Solve every case in the transport config."""
    config = _read_config(config_path)
    scenario_path = Path(scenario_path or config.get("scenario", DEFAULT_SCENARIO))
    if not scenario_path.is_absolute():
        scenario_path = ROOT / scenario_path
    source = str(config.get("source", DEFAULT_SOURCE))
    fhops = _load_fhops()
    scenario = fhops[-1](scenario_path)
    config_model = scenario.hauling
    if config_model is None:
        raise ValueError("Scenario has no hauling section")
    barge_type = config_model.barge_type(config_model.water_arcs[0].barge_type_id)
    cases = _case_volumes(config, barge_type.capacity_m3)
    return [
        estimate_marine_transport(
            volume,
            case=label,
            horizon_days=int(config.get("horizon_days", 1)),
            scenario_path=scenario_path,
            source=source,
        )
        for label, volume in cases
    ]


def configured_cost_lookup(
    config_path: Path = DEFAULT_CONFIG,
    *,
    scenario_path: Path | None = None,
) -> dict[str, float]:
    """Return ``low``, ``base``, and ``high`` costs from the configured cases.

    The config uses ``low_cost``, ``base``, and ``high_cost`` case ids. This
    helper maps them to the screen's low/base/high keys and rejects a partial
    set rather than silently substituting a legacy value.
    """
    estimates = estimate_configured_cases(config_path, scenario_path=scenario_path)
    by_case = {estimate.case: estimate.cost_per_m3_cad for estimate in estimates}
    missing = {"low_cost", "base", "high_cost"} - set(by_case)
    if missing:
        raise ValueError(f"Transport config is missing cases: {sorted(missing)}")
    return {
        "low": by_case["low_cost"],
        "base": by_case["base"],
        "high": by_case["high_cost"],
    }


def write_estimates(estimates: list[MarineTransportEstimate], out_path: Path) -> None:
    """Write solved cases to a CSV file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(estimate) for estimate in estimates]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Run the adapter CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--scenario", type=Path, default=None)
    parser.add_argument("--volume-m3", type=float, default=None)
    parser.add_argument("--horizon-days", type=int, default=1)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if args.volume_m3 is None:
        estimates = estimate_configured_cases(args.config, scenario_path=args.scenario)
    else:
        scenario_path = args.scenario or DEFAULT_SCENARIO
        estimates = [
            estimate_marine_transport(
                args.volume_m3,
                horizon_days=args.horizon_days,
                scenario_path=scenario_path,
            )
        ]

    for estimate in estimates:
        print(
            f"{estimate.case}: {estimate.total_cost_cad:,.2f} CAD / "
            f"{estimate.water_m3:,.0f} m3 = {estimate.cost_per_m3_cad:,.3f} CAD/m3 "
            f"(utilization {estimate.barge_utilization_pct:.1f}%)"
        )
    if args.out is not None:
        write_estimates(estimates, args.out)
        print(f"Wrote {len(estimates)} case(s) to {args.out}")


if __name__ == "__main__":
    main()
