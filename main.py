from core.mode_manager import ModeManager
from modes.madlibs import MadlibsGame
from modes.simple_calculator import SimpleCalculator
from modes.simple_converter import SimpleConverter
from core.tools import *

def main() -> None:
    user_name: str = get_non_empty_word_input("Enter player name: ")
    mode_manager: ModeManager = ModeManager(user_name, [MadlibsGame(), SimpleCalculator(), SimpleConverter()])
    mode_manager.show_menu()

if __name__ == '__main__':
    main()
