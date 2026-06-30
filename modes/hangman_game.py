import random
import string

from core.mode_manager import ModeManager, BaseMode
from core.save_manager import save_state, save_exists, load_state, clear_save
from core.tools import clear_console, get_non_empty_char_range_input, yes_no_query_invoker


class HangmanGame(BaseMode):
    def __init__(self, mode_manager: ModeManager):
        super().__init__(mode_manager)
        self.guess_count: int = 0
        self.current_word: str | None = None
        self.current_guess: list[str] = []
        self.is_running: bool = False
        self.hangman: dict[int, tuple[str, ...]] = {
            0: ("   ",
                "   ",
                "   "),
            1: (" O ",
                "   ",
                "   "),
            2: (" O ",
                "/  ",
                "   "),
            3: (" O ",
                "/| ",
                "   "),
            4: (" O ",
                "/|\\",
                "   "),
            5: (" O ",
                "/|\\",
                "/  "),
            6: (" O ",
                "/|\\",
                "/ \\")
        }
        self.words: tuple[str, ...] = (
            "python", "computer", "keyboard", "monitor", "internet",
            "software", "hardware", "developer", "programming", "algorithm",
            "function", "variable", "constant", "compiler", "interpreter",
            "database", "network", "security", "encryption", "decryption",
            "password", "username", "terminal", "console", "command",
            "library", "package", "module", "project", "repository",
            "version", "github", "gitlab", "bitbucket", "framework",
            "django", "flask", "fastapi", "javascript", "typescript",
            "java", "kotlin", "swift", "golang", "rust",
            "cplusplus", "html", "css", "bootstrap", "react",
            "angular", "vue", "backend", "frontend", "fullstack",
            "testing", "debugging", "exception", "recursion", "iteration",
            "sorting", "searching", "binary", "decimal", "hexadecimal",
            "operator", "operand", "boolean", "integer", "floating",
            "character", "string", "dictionary", "tuple", "set",
            "object", "class", "inheritance", "polymorphism", "encapsulation",
            "abstraction", "instance", "method", "attribute", "constructor",
            "robot", "satellite", "galaxy", "planet", "volcano",
            "mountain", "ocean", "forest", "desert", "thunder",
            "hurricane", "tornado", "penguin", "elephant", "kangaroo"
        )
        self.keyboard: tuple[tuple[str, ...], ...] = (
            ("Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"),
            ("A", "S", "D", "F", "G", "H", "J", "K", "L"),
            ("Z", "X", "C", "V", "B", "N", "M"),
        )

    def reset(self) -> None:
        if save_exists(self.mode_name):
            clear_save(self.mode_name)
        self.current_word = None
        self.current_guess.clear()
        self.guess_count = 0

    def start(self) -> None:
        clear_console()

        if save_exists(self.mode_name) and self._load_object():
            yes_no_query_invoker("Would you like to continue last game? ", None, self.reset)
        else:
            self.reset()

        self.is_running = True
        self.instructions()
        self.build()

    @property
    def mode_name(self) -> str:
        return "Hangman Game"

    def build(self) -> None:
        clear_console()
        self.current_word = random.choice(self.words)

        while self.is_running:
            print("="*8)
            self._display_hangman()
            print("=" * 8)

            if self.guess_count >= 6:
                for letter in self.current_word:
                    if letter in self.current_guess:
                        print(letter, end=" ")
                    else:
                        print(letter.upper(), end=" ")
                print("\nYOU LOST HIM, POOR MAN")
                self.is_running = False
                break
            elif all(letter in self.current_guess for letter in self.current_word):
                print(self.current_word.upper())
                print("YOU SAVED THE MAN!")
                self.is_running = False
                break

            for letter in self.current_word:
                if letter in self.current_guess:
                    print(letter, end=" ")
                else:
                    print("_", end=" ")

            print()
            self._display_keyboard()
            print()

            guess: str = get_non_empty_char_range_input("Enter your guess letter (type 0 to quit): ", string.ascii_lowercase + "0", False)

            if guess == "0":
                self.is_running = False
                break

            self.current_guess.append(guess)

            if guess not in self.current_word:
                self.guess_count += 1

            save_state(self._save_object(), self.mode_name)
            clear_console()

        if not self.is_running:
            def on_start():
                self.start()
            yes_no_query_invoker("Would you like to play again?", on_start, self.on_exit)

    def _display_hangman(self) -> None:
        for line in self.hangman[self.guess_count]:
            print(line)

    def _display_keyboard(self):
        for row in self.keyboard:
            for letter in row:
                if letter.lower() in self.current_guess:
                    print("💥", end=" | ")
                else:
                    print(letter, end=" | ")
            print()
    
    def _save_object(self) -> dict:
        return {
            "current_word": self.current_word,
            "current_guess": self.current_guess,
            "guess_count": self.guess_count,
        }

    def _load_object(self) -> bool:
        load = load_state(self.mode_name)
        if load[0]:
            self.current_word = load[1]["current_word"]
            self.current_guess = load[1]["current_guess"]
            self.guess_count = load[1]["guess_count"]
            return True
        else:
            return False

    def instructions(self) -> None:
        print(f"\tHi {self.player_name}. Welcome to Hangman Game!")
        print("Figure out the secret word before the drawing of the hangman is completed.")
        input("Press ENTER to continue...")

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()