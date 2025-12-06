"""Advent of Code 2025 - day 6"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(6)
    columns = parse_input(input_data)
    total = 0
    for col in columns:
        total += evaluate(col)
    return total


def evaluate(column: list[str]) -> int:
    assert all([entry.isnumeric() or entry in {"+", "*"} for entry in column])
    return eval(column[-1].join(column[:-1]))


def parse_input(input_data: list[str]) -> list[list[str]]:
    columns = []
    for line in input_data:
        for i, entry in enumerate(line.split()):
            if len(columns) < i + 1:
                columns.append([entry])
            else:
                columns[i].append(entry)
    return columns


# Part 2
def main2() -> str | int | None:
    input_data = get_input(6)
    columns = parse_input2(input_data)
    total = 0
    for col in columns:
        total += evaluate(col)
    return total


def parse_input2(input_data: list[str]) -> list[list[str]]:
    columns = []
    column_idx = 0
    while column_idx < len(input_data[0]):
        col, column_idx = read_column(input_data, column_idx)
        if not col:
            break
        columns.append(col)
    return columns


def read_column(input_data: list[str], start_idx: int) -> tuple[list[str], int]:
    i = start_idx
    symbol = input_data[-1][i]
    col = []
    while not (i == len(input_data[0]) or is_column_space(input_data, i)):
        number = ""
        for line in input_data[:-1]:
            number += line[i]
        col.append(number.strip())
        i += 1
    i += 1
    col.append(symbol)
    return col, i


def is_column_space(input_data: list[str], idx: int) -> bool:
    for line in input_data:
        if line[idx] != " ":
            return False
    return True


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
