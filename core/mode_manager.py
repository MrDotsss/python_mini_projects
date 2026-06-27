from __future__ import annotations
from abc import ABC, abstractmethod
from core.tools import clear_console, get_non_empty_int_range_input

class BaseMode(ABC):
    def __init__(self) -> None:
        self.mode_manager: ModeManager | None = None

    @abstractmethod
    def mode_name(self) -> str:
        pass

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager

    @abstractmethod
    def build(self) -> None:
        pass

    @abstractmethod
    def instructions(self) -> None:
        pass

    @abstractmethod
    def on_exit(self) -> None:
        pass

    @property
    def player_name(self) -> str:
        return self.mode_manager.player_name.upper()

class ModeManager:
    def __init__(self, player_name: str, mode_list: list[BaseMode]) -> None:
        self.player_name: str = player_name
        self.mode_list: list[BaseMode] = mode_list
        self.current_mode: BaseMode | None = None
        self.exit_index: int = len(mode_list) + 1

    def show_menu(self) -> None:
        clear_console()
        print(f"\nHello {self.player_name.upper()}. Welcome to Bro Code Exercises!")
        print("This is based from 12 hour Python Course from BroCode for FREE (with my own implementations).")

        print("\nAvailable modes:")
        self.__generate_choices()
        choice: int = get_non_empty_int_range_input("Enter choice: ", 1, len(self.mode_list) + 1)

        if choice == self.exit_index:
            exit(0)

        self.current_mode = self.mode_list[choice -1]
        self.play_mode()

    def play_mode(self) -> None:
        if self.current_mode is not None:
            clear_console()
            self.current_mode.start(self)

    def exit_mode(self) -> None:
        self.current_mode = None
        self.show_menu()

    def __generate_choices(self) -> None:
        for index, mode in enumerate(self.mode_list):
            print(f"\t{index + 1}. {mode.mode_name()}")
        print(f"\t{self.exit_index}. Quit\n")