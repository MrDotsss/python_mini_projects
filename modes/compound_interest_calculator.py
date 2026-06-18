from core.mode_manager import BaseMode, ModeManager
from core.tools import clear_console, get_non_empty_float_input, get_non_empty_int_input, get_non_empty_str_input


class CompoundInterestCalculator(BaseMode):
    def __init__(self):
        super().__init__()
        self.principal_balance: float = 0.0
        self.interest_rate: float = 0.0
        self.period: int = 0
        self.final_amount: float = 0.0


    def mode_name(self) -> str:
        return "Compound Interest Calculator"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        clear_console()
        self.instructions()

        self.principal_balance: float = get_non_empty_float_input("Enter the principal balance: ")
        while self.principal_balance <= 0:
            print("Principal balance must be greater than 0")
            self.principal_balance = get_non_empty_float_input("Enter the principal balance: ")

        self.interest_rate: float = get_non_empty_float_input("Enter interest rate: ")
        while self.interest_rate <= 0:
            print("Interest rate must be greater than 0")
            self.interest_rate = get_non_empty_float_input("Enter interest rate: ")

        self.period: int = get_non_empty_int_input("Enter period in years: ")
        while self.period <= 0:
            print("Period must be greater than 0")
            self.period = get_non_empty_int_input("Enter period in years: ")

        self.build()



    def build(self) -> None:
        clear_console()
        print(f"Principal: ${self.principal_balance:,}")
        print(f"Rate: {self.interest_rate}%")
        print(f"Period: {self.period} years")

        self.final_amount: float = self.principal_balance * pow(1 + self.interest_rate / 100, self.period)

        print(f"\nFinal Amount: $1{self.final_amount:,.2f} after {self.period} years.")

        query: str = get_non_empty_str_input("Would you like to calculate again? Y/N\n")
        while query.lower() != "y" and query.lower() != "n":
            print("\n\tPlease enter Y or N.\n")
            query: str = get_non_empty_str_input("Would you like to calculate again? Y/N\n")

        self.start(self.mode_manager) if query.lower() == 'y' else self.on_exit()

    def instructions(self) -> None:
        print(f"\tHi {self.mode_manager.player_name}. Welcome to Compound Interest Calculator!")
        print("Which calculates the total accumulated amount, including both the initial principal and the interest it has accrued over time.\n")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()