# Python Calculator
from core.mode_manager import BaseMode, ModeManager
from core.tools import get_non_empty_equation_input, clear_console
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

class SimpleCalculator (BaseMode):
    def __init__(self) -> None:
        super().__init__()
        self.equation: str = ""

    def mode_name(self) -> str:
        return "Simple Calculator"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        self.instructions()
        while True:
            self.equation: str = get_non_empty_equation_input("Enter equation: ")

            if self.equation == "7848":
                self.on_exit()
                return

            try:
                clear_console()
                print(f"{self.equation} = {eval(self.equation)}")
            except (SyntaxError, NameError, ZeroDivisionError, TypeError) as e:
                print(f"Invalid equation")

            print("\ntype 7848 to EXIT the calculator and return to main menu")

    def build(self) -> None:
        pass

    def instructions(self) -> None:
        print(f"\tHi {self.mode_manager.player_name}. Welcome to Simple Calculator!")
        print("\tThis calculator allows addition, subtraction, multiplication, division and other operators")
        print("\nAVAILABLE OPERATORS: + - * / ** // ( )")
        print("type 7848 to EXIT the calculator and return to main menu\n")

    def on_exit(self) -> None:
        print("\nThank you for checking this out!")
        self.mode_manager.exit_mode()