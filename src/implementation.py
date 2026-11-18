"""Cooperative inference scheduling for intermittent sensor nodes."""

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Node:
    node_id: str
    available_energy: float
    compute_units: int
    wake_window: int


def feasible_schedule(nodes: Iterable[Node], jobs: int, horizon: int) -> dict[str, int]:
    """Greedy assignment of jobs to nodes that can finish inside the horizon."""
    capacity = {}
    for node in sorted(nodes, key=lambda n: (-n.available_energy, n.node_id)):
        units = max(0, min(node.compute_units, horizon // max(node.wake_window, 1)))
        if units:
            capacity[node.node_id] = units

    assigned = {node_id: 0 for node_id in capacity}
    remaining = jobs
    for node_id in sorted(capacity, key=lambda n: -capacity[n]):
        while remaining > 0 and assigned[node_id] < capacity[node_id]:
            assigned[node_id] += 1
            remaining -= 1
    if remaining > 0:
        raise RuntimeError("not enough aggregate capacity inside the horizon")
    return assigned
