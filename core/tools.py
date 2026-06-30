import os
import re
from typing import Callable
from collections.abc import Iterable
import pwinput
import time

def get_int_input(query: str, pre_value: int) -> int:
    while True:
        user_input: str = input(f"Current value: {pre_value} enter empty value to accept current\n {query}: ")
        try:
            if not user_input.strip():
                return pre_value

            value:int = int(user_input)
            return value
        except ValueError:
            print("Please enter a valid number")

def get_int_range_input(query: str, pre_value: int, start: int, end: int) -> int:
    while True:
        print(f"Current value: {pre_value} | ENTER EMPTY value to accept current")
        user_input: str = input(query)
        try:
            if not user_input.strip():
                return pre_value

            value: int = int(user_input)

            if value < start or value > end:
                print(f"Please enter a number between {start} and {end}.")
            else:
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

def get_non_empty_char_range_input(query: str, word_range: Iterable[str], case_sensitive: bool = False) -> str:
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

        if len(user_input) > 1 or not check_input.strip():
            print("You entered an empty or non single value value. Try again.")
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

def get_non_empty_pass_input(query: str, mask: str) -> str:
    while True:
        user_input: str = pwinput.pwinput(prompt=query, mask=mask)
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

def yes_no_query_invoker(query: str, func_yes: Callable[[], None] | None, func_no: Callable[[], None] | None) -> None:
    q: str = get_non_empty_str_input(f"{query} Y/N: ")
    while q.lower() != "y" and q.lower() != "n":
        print("\n\tPlease enter Y or N.\n")
        q: str = get_non_empty_str_input(f"{query} Y/N: ")

    if q.lower() == "y" and func_yes is not None:
        func_yes()
    elif q.lower() == "n" and func_no is not None:
        func_no()

def display_loading_seq(message: str, visual: str, load_range: range, time_step: float) -> None:
    for i in load_range:
        print(f"{message} | {visual*i}")
        time.sleep(time_step)
        clear_console()

def animated_print_line(message: str, time_step: float = 0.05) -> None:
    for i in range(len(message)):
        print(message[i], end="")
        time.sleep(time_step)
    print()

def animated_print_replace_line(original: str, replace: str, time_step: float = 0.05, confirm_input: bool = True, status: str = "Replacing") -> None:
    for i in range(len(original)):
        print(status)
        print(f"{replace[:i]}-{original[i+1:]}")
        time.sleep(time_step)
        clear_console()
    print(replace)
    time.sleep(1)
    if confirm_input:
        input("\nPress enter to continue...")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')