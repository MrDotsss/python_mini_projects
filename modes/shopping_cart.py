from __future__ import  annotations
import time

from core.mode_manager import ModeManager, BaseMode
from core.save_manager import save_exists, load_state, clear_save, save_state
from core.tools import clear_console, get_non_empty_int_range_input, get_non_empty_word_input, \
    get_non_empty_float_input, get_non_empty_int_input, get_non_empty_str_input, yes_no_query_invoker


class ShoppingItem:
    def __init__(self, item_name: str, quantity: int, price: float) -> None:
        self.item_name = item_name
        self.quantity = quantity
        self.price = price

    def __str__(self) -> str:
        return f'x{self.quantity} - {self.item_name} (${self.price:,.2f}) | ${self.price * self.quantity:,.2f}'

    def __dict__(self) -> dict:
        return {
            'item_name': self.item_name,
            'quantity': self.quantity,
            'price': self.price,
        }

    def total_price(self) -> float:
        return self.price * self.quantity

class ShoppingCart(BaseMode):
    def __init__(self, mode_manager: ModeManager):
        super().__init__(mode_manager)
        self.items: list[ShoppingItem] = []
        self.total: float = 0

    @property
    def mode_name(self) -> str:
        return 'Shopping Cart'

    def reset(self) -> None:
        if save_exists(self.mode_name):
            clear_save(self.mode_name)
        self.items: list[ShoppingItem] = []

    def start(self) -> None:
        clear_console()

        self.instructions()

        if save_exists(self.mode_name) and self._load_object() and len(self.items) != 0:
            print("You still have items in your cart")
            yes_no_query_invoker("Continue shopping? ", None, self.reset)
            clear_console()
        else:
            self.reset()

        self._main_menu()

    def build(self) -> None:
        pass

    def _main_menu(self) -> None:
        print("\nMenu")
        print("1. Add Shopping Item")
        print("2. Edit Shopping Item")
        print("3. Delete Shopping Item")
        print("4. Checkout")
        print("5. Exit")

        query: int = get_non_empty_int_range_input("Enter choice: ", 1, 5)
        match query:
            case 1:
                self._add_to_cart()
            case 2:
                self._edit_cart()
            case 3:
                self._delete_cart()
            case 4:
                self._checkout()
            case 5:
                self.on_exit()

    def _display_cart(self, only_name: bool = True) -> None:
        print("Current Shopping List")
        for i, item in enumerate(self.items):
            print(f"{i + 1:03}. {item.item_name}") if only_name else  print(f"{i + 1:03}. {item}")

    def _get_total_amount(self) -> float:
        return sum(item.total_price() for item in self.items)

    def _add_to_cart(self) -> None:
        item_name: str = get_non_empty_word_input("Item name: ")
        price: float = get_non_empty_float_input("Item base price: ")
        quantity: int = get_non_empty_int_input("Item quantity: ")

        item: ShoppingItem = ShoppingItem(item_name, quantity, price)
        self.items.append(item)

        save_state(self._save_object(), self.mode_name)

        print(f"{item.item_name} added to cart")
        time.sleep(1)
        clear_console()
        self._main_menu()

    def _edit_cart(self) -> None:
        if len(self.items) == 0:
            clear_console()
            print("No items added to cart")
            self._main_menu()

        self._display_cart()
        print(f"{len(self.items) + 1:03}. Return to main menu")

        choice: int = get_non_empty_int_range_input("\nEnter choice: ", 1, len(self.items) + 1)

        if choice == len(self.items) + 1:
            clear_console()
            self._main_menu()
            return

        item: ShoppingItem = self.items[choice - 1]

        edit_choice: int = 0
        while edit_choice != 4:
            clear_console()
            print(f"Item: {item}\n")
            print(f"1. Edit Name: {item.item_name}")
            print(f"2. Edit Base Price: ${item.price:,.2f}")
            print(f"3. Edit Quantity: {item.quantity}")
            print(f"4. cancel")

            edit_choice: int = get_non_empty_int_range_input("\nEnter choice: ", 1, 4)

            match edit_choice:
                case 1:
                    item.item_name = get_non_empty_word_input("Item name: ")
                    save_state(self._save_object(), self.mode_name)
                case 2:
                    item.price = get_non_empty_float_input("Item base price: ")
                    save_state(self._save_object(), self.mode_name)
                case 3:
                    item.quantity = get_non_empty_int_input("Item quantity: ")
                    save_state(self._save_object(), self.mode_name)
                case 4:
                    clear_console()
                    self._edit_cart()
                    break

    def _delete_cart(self) -> None:
        if len(self.items) == 0:
            clear_console()
            print("No items added to cart")
            self._main_menu()

        self._display_cart()
        print(f"{len(self.items) + 1:03}. Return to main menu")

        choice: int = get_non_empty_int_range_input("\nEnter choice: ", 1, len(self.items) + 1)

        if choice == len(self.items) + 1:
            clear_console()
            self._main_menu()
            return

        item: ShoppingItem = self.items[choice - 1]
        print(f"Item to delete: {item}")

        def on_delete() -> None:
            del_item: ShoppingItem = self.items.pop(choice - 1)
            save_state(self._save_object(), self.mode_name)
            print(f"Item {del_item.item_name} deleted from cart.")
            time.sleep(1)
            clear_console()
            self._main_menu()

        def on_cancel() -> None:
            clear_console()
            self._delete_cart()

        yes_no_query_invoker("Proceed", on_delete, on_cancel)

    def _checkout(self):
        if len(self.items) == 0:
            clear_console()
            print("No items added to cart")
            self._main_menu()

        print(f"SHOPPING CART".center(50, "-"))
        print("----------")
        self._display_cart(False)
        print("----------")
        total: float = self._get_total_amount()
        print(f"Total: ${total:,.2f}")

        query: str = get_non_empty_str_input("Proceed to checkout? Y/N\n")
        while query.lower() != "y" and query.lower() != "n":
            print("\n\tPlease enter Y or N.\n")
            query: str = get_non_empty_str_input("Proceed? Y/N\n")

        def on_checkout() -> None:
            print(f"Checked out {len(self.items) + 1} items in total of {total:,.2f}.")
            print(f"Thank you for shopping with us.")
            self.items.clear()
            save_state(self._save_object(), self.mode_name)
            time.sleep(3)
            clear_console()
            self._main_menu()

        def on_cancel() -> None:
            clear_console()
            self._main_menu()

        yes_no_query_invoker("Proceed to checkout?", on_checkout, on_cancel)

    def _save_object(self) -> dict:
        return {
            "items": [item.__dict__() for item in self.items],
        }

    def _load_object(self) -> bool:
        load = load_state(self.mode_name)
        if load[0]:
            for item in load[1]["items"]:
                self.items.append(ShoppingItem(**item))
            return True
        else:
            return False

    def instructions(self) -> None:
        print(f"\tHi {self.player_name}. Welcome to Shopping Cart!")
        print("A simple Shopping Cart.\n")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()