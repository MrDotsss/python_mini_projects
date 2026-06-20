import time

from core.mode_manager import ModeManager, BaseMode
from core.tools import clear_console, get_non_empty_str_input


class QuizGame(BaseMode):
    def __init__(self) -> None:
        super().__init__()
        self.current_score: int = 0
        self.question_index: int = 0
        self.guesses: list[str] = []
        self.questions: tuple = (
            "What does the len() function do in Python?",
            "Which data type is used to store True or False values?",
            "What is the output of the following code?\nx = 5\ny = 3\nprint(x + y)",
            "Which keyword is used to create a function in Python?",
            "What is a list in Python?",
        )
        self.options: tuple = (
            {"A" : "Converts a value to an integer", "B" : "Returns the number of items in an object", "C" : "Sorts a list", "D" : "Creates a new variable"},
            {"A" : "String", "B" : "Integer", "C" : "Boolean", "D" : "Float"},
            {"A" : "53", "B" : "8", "C" : "15", "D" : "Error"},
            {"A" : "func", "B" : "define", "C" : "method", "D" : "def"},
            {"A" : "A collection of items stored in order", "B" : "A type of loop", "C" : "A mathematical operation", "D" : "A file format"}
        )
        self.answers: tuple = ("B", "C", "B", "D", "A")


    def mode_name(self) -> str:
        return "Quiz Game"

    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        self.__reset()

        clear_console()
        self.instructions()
        input("Press ENTER to continue...")
        self.build()

    def __reset(self) -> None:
        self.current_score = 0
        self.guesses.clear()
        self.question_index = 0

    def build(self) -> None:
        clear_console()

        for question in self.questions:
            clear_console()
            correct_answer: str = self.answers[self.question_index]
            print(f"{self.question_index + 1}. {question}\n")
            for key, value in self.options[self.question_index].items():
                print(f"\t{key}. {value}")
            print()

            current_guess: str = get_non_empty_str_input("Answer (letter only): ")
            while current_guess.upper() not in self.options[self.question_index].keys():
                current_guess: str = get_non_empty_str_input("Answer (LETTER ONLY): ")

            self.guesses.append(current_guess.upper())

            if current_guess.upper() == correct_answer:
                self.current_score += 1

            input("Press ENTER to continue...")

            self.question_index += 1

        clear_console()
        input("Well done! Press ENTER to review your results...")
        self.__review_scores()


    def __review_scores(self):
        clear_console()
        for index, question in enumerate(self.questions):
            correct_answer: str = self.answers[index]
            guess: str = self.guesses[index]
            print(f"{index + 1}. {question}")

            if correct_answer == guess:
                print(f"CORRECT: {self.options[index][correct_answer]}")
            else:
                print(f"INCORRECT: {self.options[index][guess]}")
                print(f"ANSWER: {self.options[index][correct_answer]}")

            time.sleep(1)
            print()

        print("="*40)
        print(f"SCORE: {self.current_score}/{len(self.questions)} | {self.__get_score_comment()}")

        print()
        time.sleep(1)
        query: str = get_non_empty_str_input("Would you like to try again? Y/N\n")
        while query.lower() != "y" and query.lower() != "n":
            print("\n\tPlease enter Y or N.\n")
            query: str = get_non_empty_str_input("Would you like to try again? Y/N\n")

        self.start(self.mode_manager) if query.lower() == 'y' else self.on_exit()

    def __get_score_comment(self) -> str:
        if self.current_score == 5:
            return "PERFECTION!"
        elif self.current_score >= 3:
            return "NOT BAD"
        else:
            return "YOU SUCK :P"

    def instructions(self) -> None:
        print(f"\tHi {self.mode_manager.player_name}. Welcome to Python and Programming Quiz!")
        print()

    def on_exit(self) -> None:
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()

