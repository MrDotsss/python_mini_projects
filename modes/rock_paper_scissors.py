import time
import random
from time import sleep

from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, get_non_empty_int_input, get_non_empty_int_range_input, \
    get_non_empty_word_range_input, yes_no_query_invoker


class RockPaperScissorsMode(BaseMode):
    def __init__(self):
        super().__init__()
        self.cpu_choice: str = ""
        self.player_choice: str = ""
        self.rounds: int = 0
        self.cpu_score: int = 0
        self.player_score: int = 0
        self.player_name: str = ""
        self.max_score = 5
        self.selection: tuple = ("ROCK", "PAPER", "SCISSORS")

    def mode_name(self) -> str:
        return "Rock Paper Scissors"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        self.player_name = mode_manager.player_name
        clear_console()
        self.instructions()

    def build(self) -> None:
        self.cpu_score = 0
        self.player_score = 0
        self.rounds = 0

        while self.cpu_score < self.max_score and self.player_score < self.max_score:
            clear_console()
            self.rounds += 1

            print(f"ROUND {self.rounds}")
            print(f"{self.player_name}: {self.player_score} | CPU: {self.cpu_score}")

            self.cpu_choice = random.choice(self.selection)
            self.player_choice = get_non_empty_word_range_input("Decide: ", self.selection).upper()

            clear_console()

            for i in range(0, 3):
                print(self.selection[i])
                time.sleep(0.5)
                clear_console()

            self.__resolve()
            time.sleep(1)

        if self.player_score > self.cpu_score:
            print("CONGRATULATIONS YOU BEAT THE CPU!")
        else:
            print("YOU LOSE! WAHAHAHAHAA")

        def on_start():
            self.start(self.mode_manager)

        yes_no_query_invoker("Play again?", on_start, self.on_exit)

    def __resolve(self):
        print(f"{self.player_name}: {self.player_choice} | CPU: {self.cpu_choice}")

        player_index: int = self.selection.index(self.player_choice)
        cpu_index: int = self.selection.index(self.cpu_choice)
        time.sleep(1)

        if player_index == cpu_index:
            print("DRAW!")
            return

        player_win: bool = (player_index - cpu_index) % 3 == 1

        if player_win:
            self.player_score += 1
            print(f"{self.player_name} WINS!")
        else:
            self.cpu_score += 1
            print("CPU WINS!")



    def __settings(self):
        print(f"Current Max Score: {self.max_score}")
        self.max_score = get_non_empty_int_input("Enter max score: ")
        print(f"Max Score has been set to {self.max_score}")
        time.sleep(0.5)
        self.start(self.mode_manager)

    def instructions(self) -> None:
        print(f"\tHi {self.mode_manager.player_name}. Welcome to Number Guessing Game!")
        print("Beat CPU into rock paper scissors.")
        print("Choices:")
        print("1. Start Game")
        print("2. Set Max Score")

        user_input: int = get_non_empty_int_range_input("Choice: ", 1, 2)
        self.build() if user_input == 1 else self.__settings()

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()