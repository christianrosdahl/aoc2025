"""Advent of Code 2025 - day 10"""

from common import get_input
import numpy as np
from itertools import combinations_with_replacement
import scipy


# Part 1
def main1() -> str | int | None:
    input_data = get_input(10)
    machines = parse_input(input_data)
    total_num_presses = 0
    for machine in machines:
        indicators, buttons = machine
        total_num_presses += get_num_presses(indicators, buttons)
    return total_num_presses


def get_num_presses(indicators: np.array, buttons: list[np.array]) -> int:
    num_buttons = len(buttons)
    num_presses = 1
    while True:
        for presses in combinations_with_replacement(
            list(range(num_buttons)), num_presses
        ):
            config = get_config(presses, num_buttons)
            config_is_valid = valid_config(config, indicators, buttons)
            if config_is_valid:
                return num_presses
        num_presses += 1


def get_config(presses: tuple[str], num_buttons: int) -> tuple[int]:
    return tuple(presses.count(i) for i in range(num_buttons))


def parse_input(input_data: list[str]) -> list[tuple[np.array, list[np.array]]]:
    result = []
    for line in input_data:
        line = line[: line.find(" {")]
        line_parts = line.split()
        indicator_diagram = line_parts[0][1:-1]
        indicators = np.array([1 if i == "#" else 0 for i in indicator_diagram])
        button_list = line_parts[1:]
        buttons = [
            np.array([1 if str(i) in b else 0 for i in range(len(indicators))])
            for b in button_list
        ]
        result.append((indicators, buttons))
    return result


def valid_config(config: tuple[int], indicators: np.array, buttons: list[np.array]):
    result = 0
    for i, num_presses in enumerate(config):
        result += num_presses * buttons[i]

    for i, value in enumerate(result):
        if value % 2 != indicators[i]:
            return False
    return True


# Part 2
def main2() -> str | int | None:
    input_data = get_input(10)
    machines = parse_input2(input_data)
    total_num_presses = 0
    for machine in machines:
        joltages, buttons = machine
        total_num_presses += get_num_presses2(joltages, buttons)
    return total_num_presses


def parse_input2(input_data: list[str]) -> list[tuple[np.array, list[np.array]]]:
    result = []
    for line in input_data:
        buttons_str = line[line.find("] ") + 2 : line.find(" {")]
        button_list = buttons_str.split()
        joltages_strs = line[line.find("{") + 1 : line.find("}")].split(",")
        joltages = np.array([int(joltage) for joltage in joltages_strs])
        buttons = [
            np.array([1 if str(i) in b else 0 for i in range(len(joltages))])
            for b in button_list
        ]
        result.append((joltages, buttons))
    return result


def get_num_presses2(joltages: np.array, buttons: list[np.array]) -> int:
    button_matrix = np.stack(buttons, axis=1)
    c = [1] * len(buttons)
    sol = scipy.optimize.linprog(c, A_eq=button_matrix, b_eq=joltages, integrality=1).x
    return int(sum(sol))


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
