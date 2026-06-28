import math
import random
import time

from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, yes_no_query_invoker, get_non_empty_int_range_input, get_non_empty_float_input


class SlotMachineGame(BaseMode):
    def __init__(self, mode_manager: ModeManager):
        super().__init__(mode_manager)
        self.max_slots: int = 3
        self.spin_cost: float = 1
        self.starting_balance: float = 0
        self.current_score: float = 0
        self.current_multiplier: int = 1
        self.slot_icons: list[str] = ["🍕", "🍗", "🍉", "🌭", "🍔", "🎉", "🧨"]
        self.current_spin_slot: list[str] = []
        self.current_bet_slot: int | None = None
        self.is_running: bool = False

    def mode_name(self) -> str:
        return "Luck Slot Machine"

    def start(self) -> None:
        
        clear_console()
        self.starting_balance = 0
        self.current_multiplier = 1
        self.current_bet_slot = None
        self.current_spin_slot.clear()
        self.is_running = True

        self.instructions()

        self.current_score = self.starting_balance
        for i in range(self.max_slots):
            self.current_spin_slot.append(random.choice(self.slot_icons))

        self.spin_cost = self.max_slots / 3

        self.build()

    def build(self) -> None:
        while self.is_running:
            self.__display_status()
            self.__ask_bet()
            self.__spinner()
            self.__resolve()

        if not self.is_running:
            self.on_exit()

    def __display_status(self) -> None:
        print("SPIN TO WIN!")
        print(f"Slots: {self.max_slots} | Spin Cost: {self.spin_cost:,.2f}\n")
        print(f"Balance: {self.current_score:,.2f}")
        print(f"Multiplier: {self.current_multiplier:.2f}")
        if self.current_bet_slot is not None:
            print(f"Bet slot: {self.current_bet_slot}")
        print("="*(5*self.max_slots))

    def __ask_bet(self) -> None:
        clear_console()
        self.__display_status()

        for slot in range(self.max_slots):
            print("  ", end=" | ")

        print()
        for slot_num in range(self.max_slots):
            print(f"{slot_num+1:02d}", end=" | ")

        print()
        for slot_icon in self.current_spin_slot:
            print(slot_icon, end=" | ")

        print("\n")
        self.current_bet_slot: int = get_non_empty_int_range_input(f"Select slot to bet (1-{self.max_slots}): ", 1, self.max_slots)
        self.current_score -= self.spin_cost

    def __spinner(self) -> None:
        spin_range: int = random.randint(25, 50)

        for _ in range(spin_range):
            clear_console()
            self.__display_status()
            random_spins: list[str] = [random.choice(self.slot_icons) for _ in range(self.max_slots)]

            self.__display_bet_slots(False)

            print()
            for slot_num in range(self.max_slots):
                print(f"{slot_num + 1:02d}", end=" | ")

            print()
            for slot_icon in random_spins:
                print(slot_icon, end=" | ")

            time.sleep(0.05)

    def __display_bet_slots(self, is_determined: bool = False) -> None:
        match_icon, non_match_icon = "💥", "💢"
        for slot in range(self.max_slots):
            if is_determined:
                bet_icon: str = self.current_spin_slot[self.current_bet_slot - 1]
                slot_icon: str = self.current_spin_slot[slot]
                print(f"{match_icon if bet_icon == slot_icon else non_match_icon}", end=" | ")
            else:
                print(f"{match_icon if slot + 1 == self.current_bet_slot else "  "}", end=" | ")

    def __resolve(self) -> None:
        clear_console()

        self.__display_status()

        # decide slots
        for slot in range(self.max_slots):
            self.current_spin_slot[slot] = random.choice(self.slot_icons)

        matches: list[str] = []
        bet_icon: str = self.current_spin_slot[self.current_bet_slot - 1]

        for icon in self.current_spin_slot:
            if icon == bet_icon:
                matches.append(icon)

        # display one by one
        self.__display_bet_slots(False)

        print()
        for slot_num in range(self.max_slots):
            print(f"{slot_num + 1:02d}", end=" | ")

        print()
        for slot_icon in self.current_spin_slot:
            print(slot_icon, end=" | ")
            time.sleep(0.5)

        clear_console()

        self.__display_status()

        # display resolve
        self.__display_bet_slots(True)

        print()
        for slot_num in range(self.max_slots):
            print(f"{slot_num + 1:02d}", end=" | ")

        print()
        for slot_icon in self.current_spin_slot:
            print(slot_icon, end=" | ")

        print()
        print("="*(5*self.max_slots))
        if len(matches) > 1 or bet_icon == self.slot_icons[-1]:
            icon_value: float = self.slot_icons.index(bet_icon) + 1 * (3 / self.max_slots)
            score_to_add: float = icon_value * len(matches)

            print(f"{bet_icon} value: {icon_value}")
            print(f"Amazing! {len(matches)}x {bet_icon} | {score_to_add:,.2f} x {self.current_multiplier:,.2f}")
            self.current_score += score_to_add * self.current_multiplier
            self.current_multiplier += 0.5 * (3/self.max_slots)
        else:
            print("Pfft! Try again, multiplier resets to x1")
            self.current_multiplier = 1

        yes_no_query_invoker("Spin Again?", None, self.on_exit)

    def instructions(self) -> None:
        print(f"HI {self.player_name}")
        print("WELCOME TO SLOT MACHINE GAME")
        print("To gain points, it should match the slot you bet on!")
        print(f"Spinning {self.slot_icons[-1]} to bet slot automatically gain {len(self.slot_icons)} even without match!\n")
        time.sleep(0.5)
        print("More slots: High chance, low points | Less Slots: Low change, high points")
        self.max_slots = get_non_empty_int_range_input("How many slots do you want to bet on? (3-5): ", 3, 5)
        self.starting_balance = get_non_empty_float_input("Input starting balance: ")
        input("Press ENTER to Play the Game!\n")
        clear_console()
        time.sleep(1)

    def on_exit(self) -> None:
        clear_console()
        if self.current_score <= 0:
            print("STOP IT, GET SOME HELP!")
            print(f"YOU ARE IN DEPT OF {self.current_score:,.2f}") if self.current_score < 0 else print(f"YOU HAVE NOTHING LEFT! ZERO BALANCE")
        elif self.starting_balance > self.current_score:
            print(f"You start at {self.starting_balance:,.2f}, yet you only left with {self.current_score:,.2f}!")
            print(f"You lost {self.starting_balance - self.current_score:,.2f}!")
            print("Don't Gamble Again!")
        else:
            print(f"You start at {self.starting_balance:,.2f}, and left with {self.current_score:,.2f}!")
            print(f"You won! {self.current_score - self.starting_balance:,.2f}!")

            if int(self.current_score / self.starting_balance) > 1:
                print(f"You multiplied your balance by {(self.current_score / self.starting_balance):,.2f} times!")
                print("Lucky hooman")
            else:
                print("Pfft not that much :P")

        time.sleep(2)
        print("\nThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()