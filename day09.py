"""Advent of Code 2025 - day 9"""

from common import get_input

point = tuple[int, int]


# Part 1
def main1() -> str | int | None:
    input_data = get_input(9)
    points = parse_input(input_data)
    return max([get_area(p1, p2) for p1 in points for p2 in points])


def parse_input(input_data: list[str]) -> list[point]:
    points = []
    for line in input_data:
        coords = line.split(",")
        assert len(coords) == 2, "Input line does not contain exactly two coordinates"
        points.append((int(coords[0]), int(coords[1])))
    return points


def get_area(point1: point, point2: point) -> int:
    row1, col1 = point1
    row2, col2 = point2
    return (abs(col2 - col1) + 1) * (abs(row2 - row1) + 1)


# Part 2
# The solution assumes that the points are ordered so that the inside is to the right
def main2() -> str | int | None:
    input_data = get_input(9)
    corners = parse_input(input_data)
    border, directions = get_border(corners)
    areas = {(p1, p2): get_area(p1, p2) for p1 in corners for p2 in corners}
    sorted_areas = dict(sorted(areas.items(), key=lambda x: x[1], reverse=True))
    for area_corners, area in sorted_areas.items():
        if is_possible(area_corners, border, directions):
            return area


def get_border(corners: list[point]) -> tuple[set[point], dict[point, str]]:
    border = set()
    directions = {}
    num_corners = len(corners)
    for i in range(num_corners):
        c1, r1 = corners[i]
        c2, r2 = corners[(i + 1) % num_corners]
        direction = get_direction((c1, r1), (c2, r2))
        if r1 == r2:
            for c in range(min(c1, c2), max(c1, c2) + 1):
                border.add((c, r1))
                directions[(c, r1)] = direction
        elif c1 == c2:
            for r in range(min(r1, r2), max(r1, r2) + 1):
                border.add((c1, r))
                directions[(c2, r)] = direction
    return border, directions


def get_direction(corner1: point, corner2: point) -> str:
    c1, r1 = corner1
    c2, r2 = corner2
    assert not (c1 == c2 and r1 == r2), "Corners must be different points"
    if c2 > c1:
        return "right"
    elif c2 < c1:
        return "left"
    elif r2 > r1:
        return "down"
    else:  # r2 < r1
        return "up"


def is_possible(
    corners: tuple[point, point], border: set[point], directions: dict[point, str]
) -> bool:
    if has_border_inside(corners, border):
        return False
    rectangle_points = get_rectangle_points(corners)
    for p in rectangle_points:
        if not neighboring_rectangle_points_inside(
            p, rectangle_points, border, directions
        ):
            return False
    return True


def has_border_inside(corners: tuple[point, point], border: set[point]) -> bool:
    c1, r1 = corners[0]
    c2, r2 = corners[1]
    for p in border:
        c, r = p
        if min(c1, c2) < c < max(c1, c2) and min(r1, r2) < r < max(r1, r2):
            for neighbor in get_neighbors((c, r)):
                if neighbor not in border:
                    return True


def get_neighbors(point: point) -> list[point]:
    c, r = point
    return [(c + dc, r + dr) for dc in [-1, 1] for dr in [-1, 1]]


def get_rectangle_points(corners: tuple[point, point]) -> set[point]:
    points = set()
    c1, r1 = corners[0]
    c2, r2 = corners[1]
    min_c = min(c1, c2)
    max_c = max(c1, c2)
    min_r = min(r1, r2)
    max_r = max(r1, r2)
    points.update({(min_c, r) for r in range(min_r, max_r + 1)})
    points.update({(max_c, r) for r in range(min_r, max_r + 1)})
    points.update({(c, min_r) for c in range(min_c, max_c + 1)})
    points.update({(c, max_r) for c in range(min_c, max_c + 1)})
    return points


def neighboring_rectangle_points_inside(
    point: point,
    rectangle_points: set[point],
    border: set[point],
    directions: dict[point, str],
) -> bool:
    for neighbor in get_neighbors(point):
        if neighbor in rectangle_points and not is_inside(neighbor, border, directions):
            return False
    return True


def is_inside(point: point, border: set[point], directions: dict[point, str]):
    result = is_inside_col(point, border, directions) or is_inside_row(
        point, border, directions
    )
    return result


def is_inside_col(point: point, border: set[point], directions: dict[point, str]):
    if point in border:
        return True
    border_point_above = get_border_point_above(point, border)
    border_point_below = get_border_point_below(point, border)
    if not border_point_above or not border_point_below:
        return False
    dir_above = directions[border_point_above]
    dir_below = directions[border_point_below]
    if dir_above == "right" and dir_below == "left":
        return True
    return False


def is_inside_row(point: point, border: set[point], directions: dict[point, str]):
    if point in border:
        return True
    border_point_left = get_border_point_left(point, border)
    border_point_right = get_border_point_right(point, border)
    if not border_point_left or not border_point_right:
        return False
    dir_left = directions[border_point_left]
    dir_right = directions[border_point_right]
    if dir_left == "up" and dir_right == "down":
        return True
    return False


def get_border_point_above(point: point, border: set[point]) -> point | None:
    points_in_column = [border_p for border_p in border if border_p[0] == point[0]]
    point_above = None
    for border_p in points_in_column:
        if border_p[1] < point[1]:
            if not point_above or border_p[1] > point_above[1]:
                point_above = border_p
    return point_above


def get_border_point_below(point: point, border: set[point]) -> point | None:
    points_in_column = [border_p for border_p in border if border_p[0] == point[0]]
    point_below = None
    for border_p in points_in_column:
        if border_p[1] > point[1]:
            if not point_below or border_p[1] < point_below[1]:
                point_below = border_p
    return point_below


def get_border_point_left(point: point, border: set[point]) -> point | None:
    points_in_row = [border_p for border_p in border if border_p[1] == point[1]]
    point_to_the_left = None
    for border_p in points_in_row:
        if border_p[0] < point[0]:
            if not point_to_the_left or border_p[0] > point_to_the_left[0]:
                point_to_the_left = border_p
    return point_to_the_left


def get_border_point_right(point: point, border: set[point]) -> point | None:
    points_in_row = [border_p for border_p in border if border_p[1] == point[1]]
    point_to_the_right = None
    for border_p in points_in_row:
        if border_p[0] > point[0]:
            if not point_to_the_right or border_p[0] < point_to_the_right[0]:
                point_to_the_right = border_p
    return point_to_the_right


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
