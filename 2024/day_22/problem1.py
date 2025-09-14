"""
Advent of Code 2024
Day: 22
Problem: 01
Author: Nathan Rand
Date: 12.25.24
"""

_INPUT_FILE_NAME = "input.txt"
_NUM_NEW_SECRET_NUMBERS = 2000


def mix(number_to_mix_in: int, secret_number: int):
    """Mix a number with the secret number (this is just a 
    wrapper for readability with python Bitwise XOR).

    Parameters
    ----------
    number_to_mix_in: int
        The number we want to mix into the secret number
    secret_number: int
        The secret number we want to mix the other number into.

    Returns
    -------
    int
        The mixed secret number
    """
    return number_to_mix_in ^ secret_number


def prune(secret_number: int):
    """Prune a secret number.

    Parameters
    ----------
    secret_number: int
        The secret number we want to prune

    Returns
    -------
    int
        The pruned secret number
    """
    return secret_number % 16777216


def evolve_secret_number(secret_number: int):
    """Evolve our secret number based on a defined set of processes.

    Parameters
    ----------
    secret_number: int
        Secret number that we want to evolve into a new secret number

    Returns
    -------
    int
        The new secret number.

    Notes
    -----
    Defined secret number evolution processes:

    1. Multiply by 64, mix, and then prune
    2. Divide by 32, round down, mix, then prune
    3. Multiply by 2048, mix, then prune.
    """
    # Process 1
    secret_number = prune(mix(secret_number*64, secret_number))

    # Process 2
    secret_number = prune(mix(secret_number//32, secret_number))

    # Process 3
    secret_number = prune(mix(secret_number*2048, secret_number))

    return secret_number


def main():
    """Advent of Code - Day 22 - Part 01 [Monkey Market]"""
    # Read in our initial_secret_numbers
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        secret_numbers = [int(num) for num in f.read().split("\n")]

    secret_number_memo = {}
    for _ in range(_NUM_NEW_SECRET_NUMBERS):
        new_secret_numbers = [None] * len(secret_numbers)
        for i, secret_number in enumerate(secret_numbers):
            if secret_number in secret_number_memo:
                new_secret_numbers[i] = secret_number_memo[secret_number]
                continue

            new_secret_numbers[i] = evolve_secret_number(secret_number)
            secret_number_memo[secret_number] = new_secret_numbers[i]
        secret_numbers = new_secret_numbers

    # Output the resulting sum of all our secret numbers
    print(
        f"After {_NUM_NEW_SECRET_NUMBERS} new secret numbers were generated "
        f"their resulting sum is: {sum(secret_numbers)}"
    )


if __name__ == "__main__":
    main()
