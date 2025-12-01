"""Advent of Code 2025 - day 1"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    rotations = get_input(1)
    num_zero_pos = 0
    pos = 50
    for rotation in rotations:
        pos = get_new_pos(pos, rotation)
        if pos == 0:
            num_zero_pos += 1
    return num_zero_pos


def get_new_pos(pos: int, rotation: str) -> int:
    return (pos + sign(rotation) * distance(rotation)) % 100


def sign(rotation: str) -> int:
    return -1 if rotation[0] == "L" else 1


def distance(rotation: str) -> int:
    return int(rotation[1:])


# Part 2
def main2() -> str | int | None:
    rotations = get_input(1)
    num_zero_passes = 0
    pos = 50
    for rotation in rotations:
        num_zero_passes += num_zero_clicks(pos, rotation)
        new_pos = get_new_pos(pos, rotation)
        pos = new_pos
    return num_zero_passes


def num_zero_clicks(pos: int, rotation: str) -> int:
    match direction(rotation):
        case "R":
            return (pos + distance(rotation)) // 100
        case "L":
            num_passes_to_99 = abs((pos - distance(rotation)) // 100)
            num_zero_passes = num_passes_to_99
            if pos == 0:
                num_zero_passes -= 1
            new_pos = get_new_pos(pos, rotation)
            if new_pos == 0:
                num_zero_passes += 1
            return num_zero_passes


def direction(rotation: str) -> str:
    return rotation[0]


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
