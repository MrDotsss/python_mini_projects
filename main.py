from core.mode_manager import ModeManager
from modes.countdown_timer import CountdownTimer
from modes.madlibs import MadlibsGame
from modes.shopping_cart import ShoppingCart
from modes.simple_calculator import SimpleCalculator
from modes.simple_converter import SimpleConverter
from modes.compound_interest_calculator import CompoundInterestCalculator
from core.tools import get_non_empty_word_input

def main() -> None:
    user_name: str = get_non_empty_word_input("Enter player name: ")
    mode_manager: ModeManager = ModeManager(user_name, [
        MadlibsGame(),
        SimpleCalculator(),
        SimpleConverter(),
        CompoundInterestCalculator(),
        CountdownTimer(),
        ShoppingCart()
    ])
    mode_manager.show_menu()

if __name__ == '__main__':
    main()
