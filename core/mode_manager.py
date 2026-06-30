from __future__ import annotations

import time
from abc import ABC, abstractmethod

from core.save_manager import save_exists, clear_save, save_state, load_state
from core.tools import clear_console, get_non_empty_int_range_input, get_non_empty_word_input

class BaseMode(ABC):
    def __init__(self, mode_manager: ModeManager) -> None:
        self.mode_manager: ModeManager = mode_manager

    @property
    def mode_name(self) -> str:
        return ""

    def reset(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

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
    def __init__(self, mode_list: list[BaseMode]) -> None:
        self.player_name: str = ""
        self.mode_list: list[BaseMode] = mode_list
        self.current_mode: BaseMode | None = None

    def show_menu(self) -> None:
        if save_exists("User Save"):
            load = load_state("User Save")
            if load[0]:
                self.player_name = load[1]["user_name"]
        else:
            self.player_name = get_non_empty_word_input("Enter player name: ")
            save_state({"user_name": self.player_name}, "User Save")

        clear_console()
        print(f"\nHello {self.player_name.upper()}. Welcome to Bro Code Exercises!")
        print("This is based from 12 hour Python Course from BroCode for FREE (with my own implementations).")

        print("\nAvailable modes:")
        self._generate_choices()
        choice: int = get_non_empty_int_range_input("Enter choice: ", 1, len(self.mode_list) + 2)

        if choice == self.clear_save_index:
            self._clear_all_save()
            clear_console()
            print("Clearing saves...")
            time.sleep(1)
            self.show_menu()
            return
        elif choice == self.exit_index:
            exit(0)

        self.current_mode = self.mode_list[choice -1]
        self.play_mode()

    def play_mode(self) -> None:
        if self.current_mode is not None:
            clear_console()
            self.current_mode.start()

    def exit_mode(self) -> None:
        self.current_mode = None
        self.show_menu()

    @property
    def exit_index(self) -> int:
        return len(self.mode_list) + 2

    @property
    def clear_save_index(self) -> int:
        return len(self.mode_list) + 1

    def _generate_choices(self) -> None:
        for index, mode in enumerate(self.mode_list):
            print(f"\t{index + 1}. {mode.mode_name}")
        print(f"\t{self.clear_save_index}. Clear All Saves")
        print(f"\t{self.exit_index}. Quit\n")

    def _clear_all_save(self) -> None:
        clear_save("User Save")
        for mode in self.mode_list:
            if save_exists(mode.mode_name):
                clear_save(mode.mode_name)
                mode.reset()