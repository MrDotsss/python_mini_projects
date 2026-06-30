import random
import time

from core.mode_manager import BaseMode, ModeManager
from core.tools import clear_console, get_non_empty_int_input, get_non_empty_int_range_input, yes_no_query_invoker


class NumberGuessingGame(BaseMode):
    def __init__(self, mode_manager: ModeManager):
        super().__init__(mode_manager)
        self.number_to_guess: int = 0
        self.guess_count: int = 0

    @property
    def mode_name(self) -> str:
        return "Number Guessing Game"

    def start(self) -> None:
        
        clear_console()
        self.instructions()
        self.build()


    def build(self) -> None:
        clear_console()
        self.number_to_guess = random.randint(1, 100)
        self.guess_count = 0

        guess: int = get_non_empty_int_range_input("Enter your guess: ", 1, 100)
        while guess != self.number_to_guess:
            self.guess_count += 1

            if guess > self.number_to_guess:
                print("Too high! Try again.")
            elif guess < self.number_to_guess:
                print("Too low! Try again.")

            guess: int = get_non_empty_int_range_input("Enter your guess: ", 1, 100)

        clear_console()
        print(f"Perfect! The number was {self.number_to_guess}")
        print(f"Tries: {self.guess_count}")
        time.sleep(1)
        yes_no_query_invoker("\nWould you like to play again?", self.build, self.on_exit)

    def instructions(self) -> None:
        print(f"\tHi {self.player_name}. Welcome to Number Guessing Game!")
        print("Select a number between 1 and 100.")
        input("Press ENTER to start the game.")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()

