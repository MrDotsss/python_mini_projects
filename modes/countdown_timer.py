import time
from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, get_non_empty_str_input, get_non_empty_int_input, yes_no_query_invoker


class CountdownTimer(BaseMode):
    def __init__(self):
        super().__init__()
        self.countdown: int = 0
        self.end_message: str = ""

    def mode_name(self) -> str:
        return "Countdown Timer"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        clear_console()
        self.end_message: str = get_non_empty_str_input("Enter timer message: ")

        self.countdown: int = get_non_empty_int_input("Enter time in seconds: ")
        while self.countdown <= 0:
            print("Time must be greater than 0.")
            self.countdown = get_non_empty_int_input("Enter time in seconds: ")

        self.build()

    def build(self) -> None:
        for x in range(self.countdown, 0, -1):
            seconds: int = x % 60
            minutes: int = int(x / 60) % 60
            hours: int = int(x / 3600)
            print(f"{hours:02}:{minutes:02}:{seconds:02}")
            time.sleep(1)
            clear_console()

        print(f"{self.end_message}\n")

        def on_start() -> None:
            self.start(self.mode_manager)

        yes_no_query_invoker("Would you like to try again?", on_start, self.on_exit)

    def instructions(self) -> None:
        print(f"\tHi {self.player_name}. Welcome to Countdown Timer!")
        print("A simple countdown timer.\n")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()