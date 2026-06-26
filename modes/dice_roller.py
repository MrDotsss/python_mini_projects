import random
import time

from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, get_int_range_input, yes_no_query_invoker


class LuckDiceRoller(BaseMode):
    def __init__(self):
        super().__init__()
        self.dice_art = {
            1: ("┌─────────┐",
                "│         │",
                "│    ●    │",
                "│         │",
                "└─────────┘"),
            2: ("┌─────────┐",
                "│  ●      │",
                "│         │",
                "│      ●  │",
                "└─────────┘"),
            3: ("┌─────────┐",
                "│  ●      │",
                "│    ●    │",
                "│      ●  │",
                "└─────────┘"),
            4: ("┌─────────┐",
                "│  ●   ●  │",
                "│         │",
                "│  ●   ●  │",
                "└─────────┘"),
            5: ("┌─────────┐",
                "│  ●   ●  │",
                "│    ●    │",
                "│  ●   ●  │",
                "└─────────┘"),
            6: ("┌─────────┐",
                "│  ●   ●  │",
                "│  ●   ●  │",
                "│  ●   ●  │",
                "└─────────┘")
        }
        self.player_roll: list[int] = []
        self.computer_roll: list[int] = []
        self.max_dice: int = 3

    def mode_name(self) -> str:
        return "Lucky Dice Roller"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        clear_console()
        self.player_roll.clear()
        self.computer_roll.clear()
        self.instructions()
        print()
        self.max_dice = get_int_range_input(f"Enter max dice to roll: ", self.max_dice, 1, 12)
        self.build()

    def build(self) -> None:
        clear_console()
        input("Press Enter to roll your dice!:_-_-")

        for die in range(self.max_dice):
            self.player_roll.append(random.randint(1, 6))
            self.computer_roll.append(random.randint(1, 6))

        self.__roll_dice()

    def __roll_dice(self) -> None:
        self.__simulate_dice_roll()

        print("Player:")
        for line in range(5):
            for die in self.player_roll:
                print(self.dice_art.get(die)[line], end="")
            print()

        print("-----------" * self.max_dice)

        print("CPU:")
        for line in range(5):
            for die in self.computer_roll:
                print(self.dice_art.get(die)[line], end="")
            print()

        print("-----------" * self.max_dice)
        time.sleep(0.5)

        cpu_total: int = sum(self.computer_roll)
        player_total: int = sum(self.player_roll)

        print(f"{self.player_name}: {player_total} | Computer: {cpu_total}")

        if player_total == cpu_total:
            print("DRAW!")
        else:
            player_win: bool = player_total > cpu_total

            if player_win:
                print(f"{self.player_name} WINS!")
            else:
                print("CPU WINS!")

        time.sleep(1)

        def on_start():
            self.start(self.mode_manager)

        yes_no_query_invoker("Play again?", on_start, self.on_exit)

    def __simulate_dice_roll(self) -> None:
        for i in range(random.randint(10, 20)):
            print("ROLLING")
            rand_die_one: list = []
            rand_die_two: list = []
            for j in range(self.max_dice):
                rand_die_one.append(random.randint(1, 6))
                rand_die_two.append(random.randint(1, 6))

            print(self.player_name)
            for line in range(5):
                for die in rand_die_one:
                    print(self.dice_art.get(die)[line], end="")
                print()

            print("-----------" * self.max_dice)

            print("CPU:")
            for line in range(5):
                for die in rand_die_two:
                    print(self.dice_art.get(die)[line], end="")
                print()

            print("-----------" * self.max_dice)

            time.sleep(0.1)
            clear_console()

    def instructions(self) -> None:
        print(f"\tHi {self.player_name}. Welcome to Lucky Dice Roller!")
        print("Roll set of dice and beat CPU's roll. The higher the total wins")
        input("Press ENTER to start the game.")

    def on_exit(self) -> None:
        print("Thank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()
