"""Advent of Code 2025 - day 12"""

from common import get_input

shape = list[list[str]]


# Part 1
def main1() -> str | int | None:
    input_data = get_input(12)
    shapes, regions, num_shapes_per_region = parse_input(input_data)
    num_regions_that_can_fit_shapes = 0
    for i, region in enumerate(regions):
        shapes_dont_fit = False
        shapes_do_fit = False
        if shape_area_too_large(shapes, region, num_shapes_per_region[i]):
            shapes_dont_fit = True
        elif shapes_fit_without_overlap(region, num_shapes_per_region[i]):
            shapes_do_fit = True
        assert (
            shapes_dont_fit or shapes_do_fit
        ), f"Couldn't conclude anything for region {i}"
        if shapes_do_fit:
            num_regions_that_can_fit_shapes += 1
    return num_regions_that_can_fit_shapes


def parse_input(
    input_data: list[str],
) -> tuple[list[shape], list[list[int]], list[list[int]]]:
    shapes = []
    regions = []
    num_shapes_per_region = []
    shape = []
    for line in input_data:
        if not "x" in line:
            if ":" in line:
                continue
            elif len(line) == 0:
                shapes.append(shape)
                shape = []
            else:
                shape.append(list(line))
        else:
            region_str, num_shapes = line.split(": ")
            regions.append([int(i) for i in region_str.split("x")])
            num_shapes_per_region.append([int(i) for i in num_shapes.split()])
    return shapes, regions, num_shapes_per_region


def get_shape_area(shape) -> int:
    return sum([1 if char == "#" else 0 for line in shape for char in line])


def shape_area_too_large(
    shapes: list[shape], region: list[int], num_shapes_in_region: list[int]
) -> bool:
    region_area = region[0] * region[1]
    shapes_area = sum(
        [num * get_shape_area(shapes[i]) for i, num in enumerate(num_shapes_in_region)]
    )
    return shapes_area > region_area


def shapes_fit_without_overlap(
    region: list[int], num_shapes_in_region: list[int]
) -> bool:
    region_width, region_height = region
    num_figures_row = region_width // 3
    num_figures_col = region_height // 3
    num_non_overlapping_figures = num_figures_row * num_figures_col
    return sum(num_shapes_in_region) <= num_non_overlapping_figures


if __name__ == "__main__":
    for part, main in enumerate([main1], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
