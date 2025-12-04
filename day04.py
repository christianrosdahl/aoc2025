"""Advent of Code 2025 - day 4"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(4)
    grid = Grid(input_data)
    num_accessible = 0
    for row in range(grid.height):
        for col in range(grid.width):
            if grid(row, col) == "@" and grid.num_neighbors(row, col) < 4:
                num_accessible += 1
    return num_accessible


class Grid:
    def __init__(self, input_data: list[str]):
        self.grid = [list(line) for line in input_data]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __call__(self, row: int, col: int) -> str:
        return self.grid[row][col]

    def num_neighbors(self, row: int, col: int) -> int:
        num = 0
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                if d_row == d_col == 0:
                    continue
                neighbor_row = row + d_row
                neighbor_col = col + d_col
                if not self.is_inside_grid(neighbor_row, neighbor_col):
                    continue
                if self(neighbor_row, neighbor_col) == "@":
                    num += 1
        return num

    def is_inside_grid(self, row: int, col: int) -> bool:
        if not 0 <= row < self.width:
            return False
        if not 0 <= col < self.height:
            return False
        return True

    def set(self, row: int, col: int, value: str) -> None:
        self.grid[row][col] = value


# Part 2
def main2() -> str | int | None:
    input_data = get_input(4)
    grid = Grid(input_data)
    num_removed = 0
    while True:
        accessible_indices = get_accessible_indices(grid)
        if len(accessible_indices) == 0:
            break
        remove_rolls_from_indices(grid, accessible_indices)
        num_removed += len(accessible_indices)
    return num_removed


def get_accessible_indices(grid: Grid) -> list[tuple[int, int]]:
    result = []
    for row in range(grid.height):
        for col in range(grid.width):
            if grid(row, col) == "@" and grid.num_neighbors(row, col) < 4:
                result.append((row, col))
    return result


def remove_rolls_from_indices(grid: Grid, indices: list[tuple[int, int]]) -> None:
    for idx in indices:
        row, col = idx
        grid.set(row, col, ".")


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
