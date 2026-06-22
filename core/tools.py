import os
import re
from typing import Callable
from collections.abc import Iterable
import copy

def get_int_input(query: str) -> int:
    while True:
        user_input: str = input(query)
        try:
            value:int = int(user_input)
            return value
        except ValueError:
            print("Please enter a valid number")

def get_non_empty_int_input(query: str) -> int:
    while True:
        user_input: str = input(query)
        try:
            if not user_input.strip():
                print("You entered an empty value. Try again")
            else:
                value: int = int(user_input)
                return value
        except ValueError:
            print("Please enter a valid number")

def get_non_empty_float_input(query: str) -> float:
    while True:
        user_input: str = input(query)
        try:
            if not user_input.strip():
                print("You entered an empty value. Try again")
            else:
                value: float = float(user_input)
                return value
        except ValueError:
            print("Please enter a valid number")

def get_non_empty_int_range_input(query: str, start: int, end: int) -> int:
    while True:
        user_input: str = input(query)
        try:
            if not user_input.strip():
                print("You entered an empty value. Try again")
            else:
                value: int = int(user_input)

                if value < start or value > end:
                    print(f"Please enter a number between {start} and {end}.")
                else:
                    return value
        except ValueError:
            print("Please enter a valid number")

def get_non_empty_equation_input(query: str) -> str:
    while True:
        valid_equation: str = r"^[.0-9+\-*/()\s]+$"
        user_input: str = input(query)
        if re.match(valid_equation, user_input):
            return user_input
        else :
            print("Please enter a valid equation")

def get_non_empty_word_input(query: str) -> str:
    while True:
        user_input: str = input(query)
        if not user_input.strip() or user_input.isnumeric():
            print("You entered an empty or numeric value. Try again")
        else:
            return user_input


def get_non_empty_word_range_input(query: str, word_range: Iterable[str], case_sensitive: bool = False) -> str:
    if not case_sensitive:
        valid_words: set[str] = {item.lower() for item in word_range}
        display_words: list[str] = list(word_range)
    else:
        valid_words: set[str] = set(word_range)
        display_words: list[str] = list(valid_words)

    while True:
        print(*display_words, sep=", ")
        user_input: str = input(query)
        check_input = user_input if case_sensitive else user_input.lower()

        if not check_input.strip() or check_input.isnumeric():
            print("You entered an empty or numeric value. Try again.")
        elif check_input not in valid_words:
            print("Invalid Input, must be: ")
        else:
            return user_input

def get_non_empty_str_input(query: str) -> str:
    while True:
        user_input: str = input(query)
        if not user_input.strip():
            print("You entered an empty value. Try again")
        else:
            return user_input

def get_non_empty_unit_input(query: str, unit_dictionary: dict) -> tuple[float, str] | None:
    pattern = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s*$")

    print(f"Valid units: {', '.join(unit_dictionary)}")
    while True:
        user_input = input(query)

        if not user_input.strip():
            print("You entered an empty value. Try again")
            continue

        match = pattern.match(user_input)

        if not match:
            print("Expected format: <number><unit> (e.g. 10kg or 10 kg)")
            continue

        value_str, unit = match.groups()

        value = float(value_str)
        unit = unit.lower()

        if unit not in unit_dictionary:
            print(f"Unknown unit. Valid units: {', '.join(unit_dictionary)}")
            continue

        return value, unit

def yes_no_query_invoker(query: str, func_yes: Callable[[], None], func_no: Callable[[], None]) -> None:
    q: str = get_non_empty_str_input(f"{query} Y/N: ")
    while q.lower() != "y" and q.lower() != "n":
        print("\n\tPlease enter Y or N.\n")
        q: str = get_non_empty_str_input(f"{query} Y/N: ")

    func_yes() if q.lower() == "y" else func_no()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')