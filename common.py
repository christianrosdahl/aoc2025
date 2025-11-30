"""Common functions, used in several of the solutions"""


def get_input(day: int, example_data=False, example_num=1) -> list[str]:
    dd = str(day).zfill(2)
    if example_data:
        suffix = "" if example_num == 1 else example_num
        return _get_data_lines(f"input{dd}_example{suffix}.txt")
    return _get_data_lines(f"input{dd}.txt")


def _get_data_lines(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()
