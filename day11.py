"""Advent of Code 2025 - day 11"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(11)
    links = parse_input(input_data)
    num_paths = num_paths_to_out("you", links)
    return num_paths


def num_paths_to_out(device: str, links: dict[str, list[str]]) -> int:
    if device == "out":
        return 1
    return sum([num_paths_to_out(neighbor, links) for neighbor in links[device]])


def parse_input(input_data: list[str]) -> dict[str, list[str]]:
    links = {}
    for line in input_data:
        name, neighbors = line.split(": ")
        links[name] = neighbors.split()
    return links


# Part 2
def main2() -> str | int | None:
    input_data = get_input(11, example_num=2)
    links = parse_input(input_data)
    cache = {}
    num_paths = num_valid_paths_to_out("svr", links, cache)
    return num_paths


def num_valid_paths_to_out(
    device: str,
    links: dict[str, list[str]],
    cache: dict,
    passed_fft: bool = False,
    passed_dac: bool = False,
) -> int:
    if (device, passed_fft, passed_dac) in cache:
        return cache[(device, passed_fft, passed_dac)]

    return_val = None
    if device == "out":
        if passed_fft and passed_dac:
            return_val = 1
        else:
            return_val = 0
    else:
        if device == "fft":
            passed_fft = True
        elif device == "dac":
            passed_dac = True
        return_val = sum(
            [
                num_valid_paths_to_out(neighbor, links, cache, passed_fft, passed_dac)
                for neighbor in links[device]
            ]
        )
    cache[(device, passed_fft, passed_dac)] = return_val
    return return_val


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
