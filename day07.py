"""Advent of Code 2025 - day 7"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(7)
    positions = {get_start_pos(input_data)}
    grid = Grid(input_data)
    total_num_splits = 0
    while True:
        positions, num_splits = get_next_positions(grid, positions)
        total_num_splits += num_splits
        if len(positions) == 0:
            break
    return total_num_splits


def get_start_pos(input_data: list[str]) -> tuple[int, int]:
    col = input_data[0].find("S")
    assert col >= 0, "Start position 'S' was not found on first line in input"
    return (0, col)


class Grid:
    def __init__(self, input_data: list[str]):
        self.grid = [list(line) for line in input_data]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __call__(self, pos: tuple[int, int]) -> str | None:
        row, col = pos
        if self.out_of_bounds(row, col):
            return None
        return self.grid[row][col]

    def out_of_bounds(self, row, col) -> bool:
        return row < 0 or row >= self.height or col < 0 or col >= self.width


def get_next_positions(
    grid: Grid, positions: set[tuple[int, int]]
) -> tuple[set[tuple[int, int]], int]:
    next_positions = set()
    num_splits = 0
    for pos in positions:
        row, col = pos
        new_pos = (row + 1, col)
        match grid(new_pos):
            case ".":
                next_positions.add(new_pos)
            case "^":
                num_splits += 1
                new_row, new_col = new_pos
                new_pos1 = (new_row, new_col - 1)
                new_pos2 = (new_row, new_col + 1)
                if grid(new_pos1):
                    next_positions.add(new_pos1)
                if grid(new_pos2):
                    next_positions.add(new_pos2)
    return next_positions, num_splits


# Part 2
def main2() -> str | int | None:
    input_data = get_input(7)
    positions = {get_start_pos(input_data): 1}
    grid = Grid(input_data)
    total_num_splits = 0
    while True:
        positions, num_splits = get_next_quantum_positions(grid, positions)
        total_num_splits += num_splits
        if sum(positions.values()) == 0:
            break
    num_timelines = total_num_splits + 1
    return num_timelines


def get_next_quantum_positions(
    grid: Grid, positions: dict[tuple[int, int], int]
) -> tuple[dict[tuple[int, int], int], int]:
    next_positions = {}
    num_splits = 0
    for pos, duplication in positions.items():
        row, col = pos
        new_pos = (row + 1, col)
        match grid(new_pos):
            case ".":
                add_to_dict(next_positions, new_pos, duplication)
            case "^":
                num_splits += duplication
                new_row, new_col = new_pos
                new_pos1 = (new_row, new_col - 1)
                new_pos2 = (new_row, new_col + 1)
                if grid(new_pos1):
                    add_to_dict(next_positions, new_pos1, duplication)
                if grid(new_pos2):
                    add_to_dict(next_positions, new_pos2, duplication)
    return next_positions, num_splits


def add_to_dict(dict: dict, key: tuple[int, int], value: int):
    if key in dict:
        dict[key] += value
    else:
        dict[key] = value


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
