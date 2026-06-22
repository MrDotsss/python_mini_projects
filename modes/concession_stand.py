from __future__ import annotations
from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, get_non_empty_int_range_input, get_non_empty_int_input, get_non_empty_str_input, \
    yes_no_query_invoker
from modes.shopping_cart import ShoppingItem
import time

class ConcessionStand(BaseMode):
    def __init__(self) -> None:
        super().__init__()
        self.menu: dict[int, tuple] = {
            1: ("Adobo", 120.00),
            2: ("Sinigang", 140.00),
            3: ("Lechon Kawali", 180.00),
            4: ("Pancit Canton", 100.00),
            5: ("Lumpiang Shanghai", 90.00),
            6: ("Sisig", 160.00),
            7: ("Halo-Halo", 85.00),
            8: ("Turon", 35.00),
            9: ("Iced Tea", 45.00),
            10: ("Rice", 20.00),
        }
        self.cart: dict[int, ShoppingItem] | None = None

    def mode_name(self) -> str:
        return "Concession Stand"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        self.cart = {}
        clear_console()
        self.instructions()
        self.__main_menu()

    def build(self) -> None:
        pass

    def __main_menu(self) -> None:
        menu_length: int = len(self.menu) + 1 if len(self.cart) != 0 else len(self.menu)

        print(f"{"-" * 10} MENU {"-" * 10}")
        for key, value in self.menu.items():
            print(f"{key:^3}: {value[0]:^20} | ${value[1]:,.2f}")

        if len(self.cart) != 0:
            print(f"\n{menu_length:^3}: {"Checkout":^20} | ${self.__get_total_amount():,.2f}")

        print(f"\n{menu_length + 1:^3}: {"Exit":^20}")

        print("-" * 26)

        print()

        print("What would you like for today?")
        choice: int = get_non_empty_int_range_input("Choice (number): ", 1, menu_length + 1)

        if choice == menu_length:
            self.__checkout()
            return
        elif choice == menu_length + 1:
            self.on_exit()
            return

        current_choice: tuple = self.menu[choice]
        print(f"\t{current_choice[0]} | ${current_choice[1]}")

        is_in_cart: bool = choice in self.cart.keys()

        if is_in_cart:
            print("Already in the cart, update quantity instead")
            quantity: int = get_non_empty_int_input(f"Add Quantity ({self.cart[choice].quantity}) + ")
            self.cart[choice].quantity += quantity
            print(self.cart[choice])
        else:
            quantity: int = get_non_empty_int_input("Quantity (number): ")
            item: ShoppingItem = ShoppingItem(item_name=current_choice[0], quantity=quantity, price=current_choice[1])
            self.cart[choice] = item
            print(item)

        yes_no_query_invoker("\nCheckout? ", self.__checkout, self.__main_menu)

    def __checkout(self) -> None:
        clear_console()

        total: float = self.__get_total_amount()

        print(f"{"-" * 10} CART {"-" * 10}")
        for item in self.cart.values():
            print(item)
        print(f"{"-" * 26}")
        print(f"Total: ${total:,.2f}")

        def on_checkout() -> None:
            print(f"Checked out {len(self.cart) + 1} items in total of {total:,.2f}.")
            print(f"Thank you, and enjoy your meal!")
            self.cart.clear()
            time.sleep(3)
            clear_console()
            self.__main_menu()

        def on_cancel() -> None:
            clear_console()
            self.__main_menu()

        yes_no_query_invoker("Proceed to checkout?", on_checkout, on_cancel)

    def __get_total_amount(self) -> float:
        return sum(item.total_price() for item in self.cart.values())

    def instructions(self) -> None:
        print(f"Welcome to Concession Stand, {self.player_name}!\n")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()
