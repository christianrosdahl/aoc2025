"""Advent of Code 2025 - day 3"""

from common import get_input


# Part 1
def main1() -> str | int | None:
    input_data = get_input(3)
    banks = parse_input(input_data)
    ans = 0
    for bank in banks:
        first_digit = get_max_digit(bank, start_idx=0, remaining_digits=1)
        first_idx = bank.index(first_digit, 0)
        second_digit = get_max_digit(bank, start_idx=first_idx + 1, remaining_digits=0)
        number = int(str(first_digit) + str(second_digit))
        ans += number
    return ans


def parse_input(input_data: list[str]) -> list[list[int]]:
    return [[int(digit) for digit in line] for line in input_data]


def get_max_digit(bank: list[int], start_idx: int, remaining_digits: int) -> int:
    if remaining_digits > 0:
        return max(bank[start_idx:-remaining_digits])
    return max(bank[start_idx:])


# Part 2
def main2() -> str | int | None:
    num_digits = 12
    input_data = get_input(3)
    banks = parse_input(input_data)
    ans = 0
    for bank in banks:
        digits = []
        prev_digit_idx = None
        for digit_num in range(num_digits):
            start_idx = 0 if prev_digit_idx is None else prev_digit_idx + 1
            remaining_digits = num_digits - digit_num - 1
            digit = get_max_digit(bank, start_idx, remaining_digits)
            digits.append(digit)
            prev_digit_idx = bank.index(digit, start_idx)
        number = int("".join([str(digit) for digit in digits]))
        ans += number
    return ans


if __name__ == "__main__":
    for part, main in enumerate([main1, main2], 1):
        if ans := main():
            print(f"The answer to part {part} is: {ans}")
