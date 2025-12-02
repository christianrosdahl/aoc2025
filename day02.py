"""Advent of Code 2025 - day 2"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(2)
    ranges = parse_input(input_data)
    invalid_ids_per_range = [get_invalid_ids(r) for r in ranges]
    invalid_ids = [num for nums in invalid_ids_per_range for num in nums]
    return sum(invalid_ids)


def parse_input(input_data: list[str]) -> list[list[int]]:
    range_strings = input_data[0].split(",")
    return [[int(num) for num in r.split("-")] for r in range_strings]


def get_invalid_ids(r: list[int]) -> list[int]:
    return [num for num in range(r[0], r[1] + 1) if is_invalid(num)]


def is_invalid(num: int) -> bool:
    num_str = str(num)
    num_len = len(num_str)
    if not is_even(num_len):
        return False
    half1 = num_str[: int(num_len / 2)]
    half2 = num_str[int(num_len / 2) :]
    return half1 == half2


def is_even(num: int) -> bool:
    return num % 2 == 0


# Part 2
def main2() -> str | int | None:
    input_data = get_input(2)
    ranges = parse_input(input_data)
    invalid_ids_per_range = [get_invalid_ids2(r) for r in ranges]
    invalid_ids = [num for nums in invalid_ids_per_range for num in nums]
    return sum(invalid_ids)


def get_invalid_ids2(r: list[int]) -> list[int]:
    return [num for num in range(r[0], r[1] + 1) if is_invalid2(num)]


def is_invalid2(num: int) -> bool:
    num_len = len(str(num))
    for divisor in range(2, num_len + 1):
        if not is_divisible(num_len, divisor):
            continue
        parts = get_parts(num, divisor)
        if parts_equal(parts):
            return True
    return False


def parts_equal(parts: list[str]) -> bool:
    if len(parts) == 1:
        return True
    return all(parts[i] == parts[0] for i in range(len(parts)))


def get_parts(num: int, divisor: int) -> list[str]:
    part_len = int(len(str(num)) / divisor)
    num_str = str(num)
    return [num_str[i * part_len : (i + 1) * part_len] for i in range(divisor)]


def is_divisible(num: int, divisor: int) -> bool:
    return num % divisor == 0


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
