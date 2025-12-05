"""Advent of Code 2025 - day 5"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(5)
    ranges, ingredients = parse_input(input_data)
    num_fresh_ingredients = 0
    for ingredient in ingredients:
        if in_any_range(ingredient, ranges):
            num_fresh_ingredients += 1
    return num_fresh_ingredients


def parse_input(input_data: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    ingredients = []
    read_ingredients = False
    for line in input_data:
        if line == "":
            read_ingredients = True
        elif read_ingredients:
            ingredients.append(int(line))
        else:
            ranges.append(tuple(int(number) for number in line.split("-")))
    return ranges, ingredients


def in_range(ingredient: int, r: tuple[int, int]) -> bool:
    return r[0] <= ingredient <= r[1]


def in_any_range(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    for r in ranges:
        if in_range(ingredient, r):
            return True
    return False


# Part 2
def main2() -> str | int | None:
    input_data = get_input(5)
    ranges = parse_input(input_data)[0]
    merged_ranges = []
    for r in ranges:
        insert(r, merged_ranges)
    return ingredients_sum(merged_ranges)


def insert(r: tuple[int, int], merged_ranges: list[tuple[int, int]]):
    if simple_insert(r, merged_ranges):
        return
    overlapping_range_idx = get_overlapping_range_idx(r, merged_ranges)
    r2 = merged_ranges.pop(overlapping_range_idx)
    r_merged = merge(r, r2)
    insert(r_merged, merged_ranges)


def simple_insert(r: tuple[int, int], ranges: list[tuple[int, int]]) -> bool:
    """
    Insert `r` in `ranges` if possible without overlapping with existing ranges.
    Return True if this succeeds and False otherwise.
    """
    if len(ranges) == 0:
        ranges.append(r)
        return True
    elif r[1] < ranges[0][0]:
        ranges.insert(0, r)
        return True
    elif r[0] > ranges[-1][1]:
        ranges.append(r)
        return True
    for i in range(1, len(ranges)):
        r1 = ranges[i - 1]
        r2 = ranges[i]
        if r[0] > r1[1] and r[1] < r2[0]:
            ranges.insert(i, r)
            return True
    return False


def get_overlapping_range_idx(r: tuple[int, int], ranges: list[tuple[int, int]]) -> int:
    for i, r2 in enumerate(ranges):
        if r2[0] > r[0]:
            if i > 0 and overlapping(r, ranges[i - 1]):
                return i - 1
            return i
    return -1


def overlapping(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    return not (r1[1] < r2[0] or r2[1] < r1[0])


def merge(r1: tuple[int, int], r2: tuple[int, int]) -> tuple[int, int]:
    return (min(r1[0], r2[0]), max(r1[1], r2[1]))


def ingredients_sum(ranges: list[tuple[int, int]]) -> int:
    result = 0
    for r in ranges:
        result += r[1] - r[0] + 1
    return result


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
