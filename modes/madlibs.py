from core.mode_manager import BaseMode, ModeManager
from core.tools import clear_console, get_non_empty_word_input, get_non_empty_int_input

# Madlibs game
# word game where you create a story
# by filling in the blanks with random words

class MadlibsGame(BaseMode):
    def __init__(self) -> None:
        super().__init__()
        self.adjective_1: str = ""
        self.adjective_2: str = ""
        self.adjective_3: str = ""
        self.adjective_4: str = ""

        self.noun_1: str = ""
        self.noun_2: str = ""
        self.noun_3: str = ""
        self.noun_4: str = ""
        self.noun_5: str = ""
        self.noun_6: str = ""

        self.animal_1: str = ""
        self.silly_phrase_1: str = ""
        self.object_1: str = ""

        self.verb_ing_1: str = ""
        self.verb_ing_2: str = ""

        self.famous_person_1: str = ""
        self.place_1: str = ""
        self.vehicle_1: str = ""

        self.number_1: int = -1
        self.number_2: int = -1

        self.plural_noun_1: str = ""
        self.plural_noun_2: str = ""
        self.plural_noun_3: str = ""

        self.food_1: str = ""
        self.mythical_creature_1: str = ""
        self.emotion_1: str = ""
        self.funny_title_1: str = ""

    def mode_name(self) -> str:
        return "Madlibs Game"
    
    def start(self, mode_manager: ModeManager) -> None:
        self.mode_manager = mode_manager
        self.instructions()
        self.__get_inputs()
        clear_console()
        self.build()

    
    def instructions(self) -> None:
        print("""
            Welcome to MadLibs Game
            - Mad Libs is a classic word game where one player asks others for a list of words to fill in the blanks of a story. 
            The fun part? The words are provided before anyone knows what the story is about, resulting in hilarious and absurd combinations.
        """)
        input("Press ENTER to continue...")

    
    def __get_inputs(self) -> None:
        self.adjective_1: str = get_non_empty_word_input("Enter Adjective (HINT: feeling): ")
        self.noun_1: str = get_non_empty_word_input("Enter Noun (HINT: item): ")
        self.animal_1: str = get_non_empty_word_input("Enter Animal: ")
        self.noun_2: str = get_non_empty_word_input("Enter Noun: ")
        self.silly_phrase_1: str = get_non_empty_word_input("Enter Silly Phrase: ")
        self.object_1: str = get_non_empty_word_input("Enter Object: ")

        self.verb_ing_1: str = get_non_empty_word_input("Enter Verb ending in -ing: ")
        while not self.verb_ing_1.endswith("ing") or self.verb_ing_1 == "ing":
            self.verb_ing_1 = get_non_empty_word_input("Verb should end with -ing and not literally 'ing': ")

        self.famous_person_1: str = get_non_empty_word_input("Enter Famous Person: ")
        self.noun_3: str = get_non_empty_word_input("Enter certain area/place: ")
        self.adjective_2: str = get_non_empty_word_input("Enter adjective of an item: ")
        self.noun_4: str = get_non_empty_word_input("Enter noun of an item: ")
        self.place_1: str = get_non_empty_word_input("Enter place: ")
        self.vehicle_1: str = get_non_empty_word_input("Enter vehicle: ")

        self.number_1: int = get_non_empty_int_input("Enter quantity: ")
        while self.number_1 <= 0:
            self.number_1 = int(input("Enter quantity must be greater than 0: "))

        self.plural_noun_1: str = get_non_empty_word_input("Enter plural noun: ")

        self.verb_ing_2: str = get_non_empty_word_input("Enter verb ending in -ing: ")
        while not self.verb_ing_2.endswith("ing") or self.verb_ing_2 == "ing":
            self.verb_ing_2 = get_non_empty_word_input("Verb should end with -ing and not literally 'ing': ")

        self.food_1: str = get_non_empty_word_input("Enter food: ")
        self.adjective_3: str = get_non_empty_word_input("Enter adjective: ")
        self.mythical_creature_1: str = get_non_empty_word_input("Enter mythical creature: ")
        self.plural_noun_2: str = get_non_empty_word_input("Enter plural noun: ")
        self.noun_5: str = get_non_empty_word_input("Enter noun: ")
        self.emotion_1: str = get_non_empty_word_input("Enter emotion: ")
        self.adjective_4: str = get_non_empty_word_input("Enter adjective: ")

        self.number_2: int = get_non_empty_int_input("Enter quantity: ")
        while self.number_2 <= 0:
            self.number_2 = int(input("Enter quantity must be greater than 0: "))

        self.plural_noun_3: str = get_non_empty_word_input("Enter plural noun: ")
        self.noun_6: str = get_non_empty_word_input("Enter noun: ")
        self.funny_title_1: str = get_non_empty_word_input("Enter funny title: ")

    
    def build(self) -> None:
        print(f"""
        Today, I woke up feeling {self.adjective_1}.
        I quickly grabbed my {self.noun_1} and ran outside.
        A {self.animal_1} was standing next to a {self.noun_2}.
        It looked at me and said, "{self.silly_phrase_1}!"
        Shocked, I dropped my {self.object_1}.
        The {self.animal_1} started doing a {self.verb_ing_1} dance.
        Suddenly, {self.famous_person_1} appeared from behind a {self.noun_3}.
        They handed me a {self.adjective_2} {self.noun_4}.
        "You must take this to {self.place_1} immediately!" they shouted.
        I jumped onto a {self.vehicle_1} and sped away.
        Along the way, I met {self.number_1} {self.plural_noun_1}.
        They were busy {self.verb_ing_2} a giant {self.food_1}.
        Together, we crossed a {self.adjective_3} bridge.
        At the end of the bridge stood a {self.mythical_creature_1}.
        The creature demanded {self.plural_noun_2} as payment.
        I offered my {self.noun_5} instead.
        To my surprise, the creature became {self.emotion_1}.
        It rewarded me with a {self.adjective_4} treasure chest.
        Inside were {self.number_2} {self.plural_noun_3} and a magical {self.noun_6}.
        From that day on, everyone called me "{self.funny_title_1}."
        """)
        self.on_exit()

    def on_exit(self) -> None:
        print("\n\tThank you for playing!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()
