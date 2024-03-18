"""Re-usable compute functions."""

import heapq as heap
from collections import defaultdict
from typing import Dict, List, Tuple, Union

Coord = Tuple[int, int]


def run_intcode(code: List[int]) -> List[int]:
    """Run intcode program with addition an multiplication."""
    index = 0
    while code[index] != 99:
        opcode = code[index]
        if opcode == 1:
            code[code[index + 3]] = code[code[index + 1]] + code[code[index + 2]]
        elif opcode == 2:
            code[code[index + 3]] = code[code[index + 1]] * code[code[index + 2]]
        index += 4
    return code


def dijkstra(
    graph: Dict[Coord, Dict[Coord, int]], start: Coord
) -> Tuple[Dict[Coord, Coord], Dict[Coord, Union[float, int]]]:
    """
    Dijkstra algorithm implementation.

    Taken from:
    https://levelup.gitconnected.com/dijkstra-algorithm-in-python-8f0e75e3f16e
    """
    visited = set()
    parents_map = {}
    pq: List[Tuple[int, Coord]] = []
    node_costs: Dict[Coord, Union[float, int]] = defaultdict(lambda: float("inf"))
    node_costs[start] = 0
    heap.heappush(pq, (0, start))

    while pq:
        _, node = heap.heappop(pq)
        visited.add(node)

        for adj_node, weight in graph[node].items():
            if adj_node in visited:
                continue

            new_cost = node_costs[node] + weight
            if node_costs[adj_node] > new_cost:
                parents_map[adj_node] = node
                node_costs[adj_node] = new_cost
                heap.heappush(pq, (int(new_cost), adj_node))
    return parents_map, node_costs
