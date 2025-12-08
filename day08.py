"""Advent of Code 2025 - day 8"""

import math
from common import get_input

coord = tuple[int, int, int]


# Part 1
def main1() -> str | int | None:
    input_data = get_input(8)
    num_connections = 1000
    boxes = parse_input(input_data)
    connections = {box: set() for box in boxes}
    distances = {(box1, box2): dist(box1, box2) for box1 in boxes for box2 in boxes}
    for i in range(num_connections):
        print(f"Connection {i+1} of {num_connections}")
        box1, box2 = closest_non_connected(connections, distances)
        connect(connections, box1, box2)
    circuits = get_circuits(connections)
    circuit_sizes = sorted([len(circuit) for circuit in circuits], reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def parse_input(input_data: list[str]) -> list[coord]:
    return [tuple(int(i) for i in line.split(",")) for line in input_data]


def dist(box1: coord, box2: coord) -> float:
    diff = tuple(box2[i] - box1[i] for i in range(3))
    return math.sqrt(sum(diff[i] ** 2 for i in range(3)))


def connect(connections: dict[coord, set[coord]], box1: coord, box2: coord):
    connections[box1].add(box2)
    connections[box2].add(box1)


def are_connected(
    connections: dict[coord, set[coord]], box1: coord, box2: coord
) -> bool:
    if box1 == box2:
        return True
    return box2 in connections[box1]


def closest_non_connected(
    connections: dict[coord, set[coord]], distances: dict[tuple[coord, coord], float]
) -> tuple[coord, coord] | None:
    boxes = list(connections.keys())
    min_dist = math.inf
    result = None
    for box1 in boxes:
        for box2 in boxes:
            connected = are_connected(connections, box1, box2)
            if distances[(box1, box2)] < min_dist and not connected:
                min_dist = dist(box1, box2)
                result = (box1, box2)
    return result


def get_circuits(connections: dict[coord, set[coord]]) -> list[set[coord]]:
    circuits = []
    not_in_circuit = list(connections.keys())
    while len(not_in_circuit) > 0:
        box = not_in_circuit.pop()
        circuit = get_connected(box, connections, not_in_circuit)
        circuit.add(box)
        circuits.append(circuit)
    return circuits


def get_connected(
    box: coord,
    connections: dict[coord, set[coord]],
    not_in_circuit: list[dict[coord, set[coord]]],
) -> set[coord]:
    connected = set()
    for box_other in connections[box]:
        if box_other in not_in_circuit:
            connected.add(box_other)
            not_in_circuit.remove(box_other)
            connected.update(get_connected(box_other, connections, not_in_circuit))
    return connected


# Part 2
def main2() -> str | int | None:
    input_data = get_input(8)
    boxes = parse_input(input_data)
    connections = {box: set() for box in boxes}
    distances = {(box1, box2): dist(box1, box2) for box1 in boxes for box2 in boxes}
    num_connections = 0
    while True:
        box1, box2 = closest_non_connected(connections, distances)
        connect(connections, box1, box2)
        num_connections += 1
        circuits = get_circuits(connections)
        print(f"Num connections: {num_connections}, Num circuits: {len(circuits)}")
        if len(circuits) == 1:
            last_connection = (box1, box2)
            break
    box1, box2 = last_connection
    return box1[0] * box2[0]


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
