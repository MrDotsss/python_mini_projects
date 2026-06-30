from __future__ import annotations
import time
from datetime import datetime
from enum import Enum

from core.mode_manager import ModeManager, BaseMode
from core.save_manager import save_state, load_state, save_exists, clear_save
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
    def __init__(self, transaction_type: str, amount: float, date: datetime) -> None:
        self.transaction_type: str = transaction_type
        self.amount: float = amount
        self.date: datetime = date

    def __str__(self) -> str:
        return f"Date: {self.date:%A, %B %d, %Y, %I:%M %p}\nTransaction Type: {self.transaction_type}\nAmount: {self._get_amount_by_type()}"

    def __dict__(self) -> dict:
        return {
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "date": self.date.isoformat(),
        }

    def _get_amount_by_type(self) -> str:
        if self.transaction_type == States.DEPOSIT.value:
            return f"+${self.amount:,.2f}"
        elif self.transaction_type == States.WITHDRAW.value:
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

    @property
    def mode_name(self) -> str:
        return "BANK PROGRAM - ATM"

    def reset(self) -> None:
        self.is_authenticated = False
        self.current_state: States = States.LOGIN
        self.transaction_history: list[TransactionHistory] = []
        self.balance: float = 0
        self.pin: str = ""

    def start(self) -> None:
        if save_exists(self.mode_name):
            self._load_object()

        self.is_authenticated = False
        clear_console()
        self.instructions()
        self.build()

    def build(self) -> None:
        while self.is_running:
            match self.current_state:
                case States.LOGIN:
                    self._login()
                case States.MENU:
                    self._menu()
                case States.BALANCE:
                    self._balance()
                case States.WITHDRAW:
                    self._withdraw()
                case States.DEPOSIT:
                    self._deposit()
                case States.HISTORY:
                    self._history()

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

    def _login(self) -> None:
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
                self.transaction_history.append(TransactionHistory(States.LOGIN.value, self.balance, datetime.now()))
                self.is_authenticated = True
                save_state(self._save_object(), self.mode_name)
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
                    print("YOU'VE REACHED MAXIMUM TRIES. YOUR ACCOUNT WILL BE REVOKED AND DELETED")

                    if save_exists(self.mode_name):
                        clear_save(self.mode_name)
                    self.reset()

                    time.sleep(1)
                    self.is_running = False
                    return

                print(f"Welcome back! {self.player_name}")
                self.transaction_history.append(TransactionHistory(States.LOGIN.value, self.balance, datetime.now()))
                save_state(self._save_object(), self.mode_name)
                self.is_authenticated = True
                time.sleep(1)
                self.current_state = States.MENU

    def _menu(self) -> None:
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

    def _balance(self) -> None:
        clear_console()
        if not self.is_authenticated:
            self.current_state = States.LOGIN
            return

        display_loading_seq("CHECKING BALANCE", "=-=", range(1, 10), 0.1)

        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)
        self.transaction_history.append(TransactionHistory(States.BALANCE.value, self.balance, datetime.now()))
        save_state(self._save_object(), self.mode_name)
        time.sleep(1)

        input("\nPress ENTER to return to main menu.")
        self.current_state = States.MENU

    def _deposit(self) -> None:
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
        self.transaction_history.append(TransactionHistory(States.DEPOSIT.value, deposit, datetime.now()))
        save_state(self._save_object(), self.mode_name)
        print("DEPOSIT COMPLETE\n")
        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)

        time.sleep(1)
        input("Press ENTER to return to main menu.")
        self.current_state = States.MENU

    def _withdraw(self) -> None:
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
        self.transaction_history.append(TransactionHistory(States.WITHDRAW.value, withdraw, datetime.now()))
        save_state(self._save_object(), self.mode_name)
        print("WITHDRAW COMPLETE\n")
        print("Your balance is:")
        print(f"\t${self.balance:,.2f}")
        print("=" * 50)

        time.sleep(1)
        input("Press ENTER to return to main menu.")
        self.current_state = States.MENU

    def _history(self) -> None:
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
    
    def _save_object(self) -> dict:
        return {
            "pin": self.pin,
            "balance": self.balance,
            "history": [history.__dict__() for history in self.transaction_history],
        }

    def _load_object(self) -> None:
        load = load_state(self.mode_name)
        if load[0]:
            self.pin = load[1]["pin"]
            self.balance = load[1]["balance"]
            for history in load[1]["history"]:
                self.transaction_history.append(
                    TransactionHistory(
                        history["transaction_type"],
                        history["amount"],
                        datetime.fromisoformat(history["date"]),
                    )
                )