"""Advent of Code 2025 - day 8"""

import math
from common import get_input

coord = tuple[int, int, int]
box_pair = tuple[coord, coord]


# Part 1
def main1() -> str | int | None:
    input_data = get_input(8)
    num_connections = 1000
    boxes = parse_input(input_data)
    distances = get_sorted_distances(boxes)
    connections, _ = get_connections(num_connections, boxes, distances)
    circuits = get_circuits(connections)
    circuit_sizes = sorted([len(circuit) for circuit in circuits], reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def parse_input(input_data: list[str]) -> list[coord]:
    return [tuple(int(i) for i in line.split(",")) for line in input_data]


def get_sorted_distances(boxes: list[coord]) -> dict[box_pair, int]:
    box_pairs = {
        (b1, b2) for i, b1 in enumerate(boxes) for j, b2 in enumerate(boxes) if i < j
    }
    distances = {(box1, box2): dist(box1, box2) for (box1, box2) in box_pairs}
    return dict(sorted(distances.items(), key=lambda x: x[1]))


def dist(box1: coord, box2: coord) -> float:
    diff = tuple(box2[i] - box1[i] for i in range(3))
    return math.sqrt(sum(diff[i] ** 2 for i in range(3)))


def get_connections(
    num_connections: int, boxes: list[coord], distances: dict[box_pair, int]
) -> tuple[dict[coord, set[coord]], box_pair]:
    connections = {box: set() for box in boxes}
    for i, (box1, box2) in enumerate(distances.keys()):
        if i == num_connections:
            break
        connect(connections, box1, box2)
    last_connected = (box1, box2)
    return connections, last_connected


def connect(connections: dict[coord, set[coord]], box1: coord, box2: coord):
    connections[box1].add(box2)
    connections[box2].add(box1)


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
    distances = get_sorted_distances(boxes)

    min_num_connections = 1
    max_num_connections = get_max_num_connections(boxes, distances)
    num_connections = find_num_connections(
        min_num_connections, max_num_connections, boxes, distances
    )
    _, last_connection = get_connections(num_connections, boxes, distances)
    box1, box2 = last_connection
    return box1[0] * box2[0]


def get_num_circuits(
    num_connections: int,
    boxes: list[coord],
    distances: dict[box_pair, int],
) -> int:
    connections, _ = get_connections(num_connections, boxes, distances)
    circuits = get_circuits(connections)
    return len(circuits)


def get_max_num_connections(
    boxes: list[coord],
    distances: dict[box_pair, int],
) -> int:
    num_circuits = None
    max_num_connections = 1
    while not num_circuits or num_circuits > 1:
        max_num_connections = max_num_connections * 2
        num_circuits = get_num_circuits(max_num_connections, boxes, distances)
    return max_num_connections


def find_num_connections(
    min_num: int,
    max_num: int,
    boxes: list[coord],
    distances: dict[box_pair, int],
) -> int:
    if min_num == max_num or min_num == max_num - 1:
        return min_num
    middle_num = math.ceil((max_num + min_num) / 2)
    middle_num_circuits = get_num_circuits(middle_num, boxes, distances)
    if middle_num_circuits > 1:
        min_num = middle_num
    else:
        max_num = middle_num
    return find_num_connections(min_num, max_num, boxes, distances)


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
