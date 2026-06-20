from typing import Final

from core.mode_manager import BaseMode, ModeManager
from enum import Enum

from core.tools import clear_console, get_non_empty_unit_input, get_non_empty_str_input, get_non_empty_int_range_input, \
    yes_no_query_invoker

CONVERSIONS: Final[dict] = {
    "length": {
        "m": 1.0,         # Base unit: Meter
        "km": 1000.0,
        "cm": 0.01,
        "mm": 0.001,
        "mi": 1609.34,
        "yd": 0.9144,
        "ft": 0.3048,
        "in": 0.0254
    },
    "weight": {
        "kg": 1.0,        # Base unit: Kilogram
        "g": 0.001,
        "mg": 0.000001,
        "lb": 0.45359237,
        "oz": 0.02834952
    },
    "temperature": {
        "c": {"scale": 1.0, "offset": 0.0},
        "f": {"scale": 5 / 9, "offset": -32},
        "k": {"scale": 1.0, "offset": -273.15},
    }
}

class Category(Enum):
    LENGTH = "length"
    WEIGHT = "weight"
    TEMPERATURE = "temperature"

class SimpleConverter(BaseMode):
    def __init__(self):
        super().__init__()
        self.current_category: Category | None = None
        self.current_unit: str = ""
        self.current_value: float = 0.0
        self.converting_unit: str = ""
        self.category_dict: dict | None = None

    def mode_name(self) -> str:
        return "Simple Converter"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        clear_console()
        self.instructions()

        print("\nSelect Category:")
        print("\t1. Length\n\t2. Weight\n\t3. Temperature\n\t4. Exit")
        value: int = get_non_empty_int_range_input("Enter option (number): ", 1, 4)

        if value == 4:
            self.on_exit()
            return

        match value:
            case 1:
                self.current_category: Category = Category.LENGTH
            case 2:
                self.current_category: Category = Category.WEIGHT
            case 3:
                self.current_category: Category = Category.TEMPERATURE

        self.category_dict: dict = CONVERSIONS[self.current_category.value].copy()

        self.current_value, self.current_unit = get_non_empty_unit_input("\nEnter value with unit (e.g. 1m): ", self.category_dict)

        self.category_dict.pop(self.current_unit)

        self.converting_unit: str = get_non_empty_str_input("Enter unit to convert to: ")
        while self.converting_unit not in self.category_dict:
            print(f"\nUnknown unit. Valid units: {', '.join(self.category_dict)}")
            self.converting_unit = get_non_empty_str_input("Enter unit to convert to: ")

        self.build()

    def build(self) -> None:
        if self.converting_unit not in self.category_dict:
            print(f"An error occurred: UNKNOWN unit. Valid units: {', '.join(self.category_dict)}")
            self.on_exit()

        is_temp: bool = self.current_category.value == "temperature"

        if is_temp:
            temp: float = self.__convert_to_temp()
            print(f"Temperature: {self.current_value}{self.converting_unit} => {temp:,.2f}{self.converting_unit}")
        else:
            base_value: float = self.current_value * self.category_dict[self.converting_unit]
            print(f"{self.current_value}{self.current_unit} => {base_value:,.2f}{self.converting_unit}")

        def on_start() -> None:
            self.start(self.mode_manager)

        yes_no_query_invoker("Would you like to convert again?", on_start, self.on_exit)

    def __convert_to_temp(self) -> float:
        temp_dict: dict = CONVERSIONS[self.current_category.value].copy()

        if self.converting_unit not in temp_dict:
            print(f"An error occurred: UNKNOWN unit. Valid units: {', '.join(temp_dict)}")
            self.on_exit()

        current: dict = temp_dict[self.current_unit]
        c: float = (self.current_value + current["offset"]) * current["scale"]

        target: dict = temp_dict[self.converting_unit]

        return (c / target["scale"]) - target["offset"]

    def instructions(self) -> None:
        print(f"\tHi {self.mode_manager.player_name}. Welcome to Simple Converter!")
        print("\tThis can convert between different modes. Length and Weight")
        print("\nLength: meter, kilometer, mile, kilometer, yard, feet, inches.")
        print("Weight: kilogram, gram, milligram, pounds, ounce")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()