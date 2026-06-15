
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

def get_non_empty_word_input(query: str) -> str:
    while True:
        user_input: str = input(query)
        if not user_input.strip() or user_input.isnumeric():
            print("You entered an empty or numeric value. Try again")
        else:
            return user_input

def get_non_empty_str_input(query: str) -> str:
    while True:
        user_input: str = input(query)
        if not user_input.strip():
            print("You entered an empty value. Try again")
        else:
            return user_input

def clear_console():
    pass