from __future__ import annotations
import time
import datetime
from enum import Enum

from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, get_non_empty_pass_input, get_non_empty_int_range_input, get_non_empty_float_input, display_loading_seq

#it stores in memory, for now

class States(Enum):
    LOGIN = "Logged In"
    MENU = "Menu"
    BALANCE = "Checked Balance"
    WITHDRAW = "Withdraw"
    DEPOSIT = "Deposit"
    HISTORY = "History"

class TransactionHistory:
    def __init__(self, transaction_type: States, amount: float) -> None:
        self.transaction_type: States = transaction_type
        self.amount: float = amount
        self.date: datetime.datetime = datetime.datetime.now()

    def __str__(self) -> str:
        return f"Date: {self.date:%A, %B %d, %Y, %I:%M %p}\nTransaction Type: {self.transaction_type.value}\nAmount: {self.__get_amount_by_type()}"

    def __get_amount_by_type(self) -> str:
        if self.transaction_type == States.DEPOSIT:
            return f"+${self.amount:,.2f}"
        elif self.transaction_type == States.WITHDRAW:
            return f"-${self.amount:,.2f}"
        else:
            return f"${self.amount:,.2f}"

class BankingProgram(BaseMode):
    def __init__(self, mode_manager: ModeManager):
        super().__init__(mode_manager)
        self.is_authenticated = False
        self.is_running = False
        self.current_state: States = States.LOGIN
        self.transaction_history: list[TransactionHistory] = []
        self.balance: float = 0
        self.pin: str = ""

    def mode_name(self) -> str:
        return "BANK PROGRAM - ATM"

    def start(self) -> None:
        
        self.is_authenticated = False
        clear_console()
        self.instructions()
        self.build()

    def build(self) -> None:
        while self.is_running:
            match self.current_state:
                case States.LOGIN:
                    self.__login()
                case States.MENU:
                    self.__menu()
                case States.BALANCE:
                    self.__balance()
                case States.WITHDRAW:
                    self.__withdraw()
                case States.DEPOSIT:
                    self.__deposit()
                case States.HISTORY:
                    self.__history()

        if not self.is_running:
            self.on_exit()

    def instructions(self) -> None:
        print("ATM BANK")
        time.sleep(0.5)
        input("Press ENTER to INSERT CARD-----")
        clear_console()

        display_loading_seq("READING CARD", "\/", range(1, 10), 0.1)

        time.sleep(1)
        self.is_running = True
        self.current_state: States = States.LOGIN

    def on_exit(self) -> None:
        print("Thank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.is_authenticated = False
        self.current_state = States.LOGIN
        self.mode_manager.exit_mode()

    def __login(self) -> None:
        clear_console()
        if self.is_authenticated:
            self.current_state = States.MENU
        else:
            if self.pin.strip() == "":
                print("NO PIN CODE YET, CREATE 4 DIGIT PIN")

                pin: str = get_non_empty_pass_input("PIN: ", "*")
                while len(pin) != 4 or not pin.isdigit():
                    print("INVALID PIN")
                    time.sleep(0.5)
                    clear_console()
                    print("NO PIN CODE YET, CREATE 4 DIGIT PIN")
                    pin: str = get_non_empty_pass_input("PIN: ", "*")

                print("RE-ENTER PIN")
                pin_2: str = get_non_empty_pass_input("PIN: ", "*")
                while len(pin_2) != 4 or not pin_2.isdigit() or pin != pin_2:
                    print("PIN NOT MATCHED")
                    time.sleep(0.5)
                    clear_console()
                    print("RE-ENTER PIN")
                    pin_2: str = get_non_empty_pass_input("PIN: ", "*")

                self.pin = pin
                print("PIN SUCCESSFULLY CREATED\n")
                print(f"Hello! {self.player_name}")
                print("Returning to main menu...")
                time.sleep(1)
                self.transaction_history.append(TransactionHistory(States.LOGIN, self.balance))
                self.is_authenticated = True
                self.current_state = States.MENU
            else:
                max_tries: int = 3

                pin: str = get_non_empty_pass_input("PIN: ", "*")
                while max_tries > 0 and (len(pin) != 4 or not pin.isdigit() or self.pin != pin):
                    print(f"INVALID PIN | Tries left: {max_tries}")
                    time.sleep(1)
                    clear_console()
                    pin: str = get_non_empty_pass_input("PIN: ", "*")
                    max_tries -= 1

                if max_tries <= 0:
                    print("YOU'VE REACHED MAXIMUM TRIES. YOUR ACCOUNT WILL BE ON HOLD")
                    time.sleep(1)
                    self.is_running = False
                    return

                print(f"Welcome back! {self.player_name}")
                self.transaction_history.append(TransactionHistory(States.LOGIN, self.balance))
                self.is_authenticated = True
                time.sleep(1)
                self.current_state = States.MENU

    def __menu(self) -> None:
        clear_console()
        if not self.is_authenticated:
            self.current_state = States.LOGIN
            return

        print(f"{"-"*10} ATM MENU {"-"*10}")
        print("1. SHOW BALANCE")
        print("2. DEPOSIT")
        print("3. WITHDRAW")
        print("4. HISTORY")
        print("5. EXIT")

        choice: int = get_non_empty_int_range_input("Select an option: ", 1, 5)
        match choice:
            case 1:
                self.current_state = States.BALANCE
            case 2:
                self.current_state = States.DEPOSIT
            case 3:
                self.current_state = States.WITHDRAW
            case 4:
                self.current_state = States.HISTORY
            case 5:
                self.is_running = False

    def __balance(self) -> None:
        clear_console()
        if not self.is_authenticated:
            self.current_state = States.LOGIN
            return

        display_loading_seq("CHECKING BALANCE", "=-=", range(1, 10), 0.1)

        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)
        self.transaction_history.append(TransactionHistory(States.BALANCE, self.balance))
        time.sleep(1)

        input("\nPress ENTER to return to main menu.")
        self.current_state = States.MENU

    def __deposit(self) -> None:
        clear_console()
        if not self.is_authenticated:
            self.current_state = States.LOGIN
            return

        display_loading_seq("CHECKING BALANCE", "=-=", range(1, 10), 0.1)

        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("="*50)
        time.sleep(0.5)

        deposit: float = get_non_empty_float_input("Amount to deposit (enter 0 to cancel transaction): ")
        while deposit < 0:
            print("Amount must be greater than 0.")
            time.sleep(0.5)
            clear_console()
            print("Your balance is:")
            print(f"\t${self.balance:,.2f}")
            print("=" * 50)
            time.sleep(0.5)
            deposit: float = get_non_empty_float_input("Amount to deposit (enter 0 to cancel transaction): ")

        if deposit == 0:
            self.current_state = States.MENU
            return

        clear_console()
        display_loading_seq(f"PROCESSING | +${deposit:,.2f}", ".,.", range(1, 10), 0.1)

        self.balance += deposit
        self.transaction_history.append(TransactionHistory(States.DEPOSIT, deposit))

        print("DEPOSIT COMPLETE\n")
        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)

        time.sleep(1)
        input("Press ENTER to return to main menu.")
        self.current_state = States.MENU

    def __withdraw(self) -> None:
        clear_console()
        if not self.is_authenticated:
            self.current_state = States.LOGIN
            return

        display_loading_seq("CHECKING BALANCE", "=-=", range(1, 10), 0.1)

        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)
        time.sleep(0.5)

        withdraw: float = get_non_empty_float_input("Amount to withdraw (enter 0 to cancel transaction): ")
        while withdraw < 0 or withdraw > self.balance:
            print("Amount must be greater than 0 and less than the balance.")
            time.sleep(0.5)
            clear_console()
            print("Your balance is:")
            print(f"\t${self.balance:,.2f}")
            print("=" * 50)
            time.sleep(0.5)
            withdraw: float = get_non_empty_float_input("Amount to withdraw (enter 0 to cancel transaction): ")

        if withdraw == 0:
            self.current_state = States.MENU
            return

        clear_console()
        display_loading_seq(f"PROCESSING | -${withdraw:,.2f}", ".,.", range(1, 10), 0.1)

        self.balance -= withdraw
        self.transaction_history.append(TransactionHistory(States.WITHDRAW, withdraw))

        print("WITHDRAW COMPLETE\n")
        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)

        time.sleep(1)
        input("Press ENTER to return to main menu.")
        self.current_state = States.MENU

    def __history(self) -> None:
        clear_console()
        if not self.is_authenticated:
            self.current_state = States.LOGIN
            return

        display_loading_seq("FETCHING ACTIVITY", "0-0", range(1, 10), 0.1)

        for history in self.transaction_history:
            print(history)
            print("=" * 50)

        time.sleep(1)
        input("Press ENTER to return to main menu.")
        self.current_state = States.MENU