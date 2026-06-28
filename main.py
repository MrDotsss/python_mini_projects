from core.mode_manager import ModeManager, BaseMode
from modes import *
from core.tools import get_non_empty_word_input, clear_console

def main() -> None:
    clear_console()
    user_name: str = get_non_empty_word_input("Enter player name: ")
    mode_manager: ModeManager = ModeManager(user_name, [])

    mode_list: list[BaseMode] = [
        MadlibsGame(mode_manager),
        SimpleCalculator(mode_manager),
        SimpleConverter(mode_manager),
        CompoundInterestCalculator(mode_manager),
        CountdownTimer(mode_manager),
        ShoppingCart(mode_manager),
        QuizGame(mode_manager),
        ConcessionStand(mode_manager),
        NumberGuessingGame(mode_manager),
        RockPaperScissorsMode(mode_manager),
        LuckDiceRoller(mode_manager),
        BankingProgram(mode_manager),
        SlotMachineGame(mode_manager),
        MessageEncryption(mode_manager),
        HangmanGame(mode_manager),
    ]

    mode_manager.mode_list = mode_list

    mode_manager.show_menu()

if __name__ == '__main__':
    main()
