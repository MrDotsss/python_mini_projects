from core.mode_manager import ModeManager
from modes import *
from core.tools import get_non_empty_word_input, clear_console

def main() -> None:
    clear_console()
    user_name: str = get_non_empty_word_input("Enter player name: ")
    mode_manager: ModeManager = ModeManager(user_name, [
        MadlibsGame(),
        SimpleCalculator(),
        SimpleConverter(),
        CompoundInterestCalculator(),
        CountdownTimer(),
        ShoppingCart(),
        QuizGame(),
        ConcessionStand(),
        NumberGuessingGame(),
        RockPaperScissorsMode(),
        LuckDiceRoller(),
        BankingProgram(),
        SlotMachineGame(),
        MessageEncryption(),
        HangmanGame()
    ])
    mode_manager.show_menu()

if __name__ == '__main__':
    main()
