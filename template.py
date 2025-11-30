"""Advent of Code 2025 - day D"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(D, example_data=True)


# Part 2
def main2() -> str | int | None:
    input_data = get_input(D, example_data=True)


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
