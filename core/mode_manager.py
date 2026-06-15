from __future__ import annotations
from abc import ABC, abstractmethod
from core.tools import *

class BaseMode(ABC):
    def __init__(self) -> None:
        self.mode_manager: ModeManager | None = None

    @abstractmethod
    def mode_name(self) -> str:
        pass

    @abstractmethod
    def start(self, mode_manager: ModeManager) -> None:
        pass

    @abstractmethod
    def build(self) -> None:
        pass

    @abstractmethod
    def instructions(self) -> str:
        pass

    @abstractmethod
    def on_exit(self) -> None:
        pass

class ModeManager:
    def __init__(self, player_name: str, mode_list: list[BaseMode]) -> None:
        self.player_name: str = player_name
        self.mode_list: list[BaseMode] = mode_list
        self.current_mode: BaseMode | None = None

    def show_menu(self) -> None:
        print(f"\nHello {self.player_name}. Welcome to Bro Code Exercises!")
        print("This came from 12 hour Python Course from BroCode for FREE")

        print("\nAvailable modes:")
        self.__generate_choices()
        choice: int = get_non_empty_int_range_input("Enter choice: ", 1, len(self.mode_list))
        self.current_mode = self.mode_list[choice -1]
        self.play_mode()

    def play_mode(self) -> None:
        if self.current_mode is not None:
            self.current_mode.start(self)

    def exit_mode(self) -> None:
        self.show_menu()

    def __generate_choices(self) -> None:
        for index, mode in enumerate(self.mode_list):
            print(f"\t{index + 1}. {mode.mode_name()}")