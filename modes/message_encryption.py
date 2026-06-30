import string
import random
import time

from core.mode_manager import ModeManager, BaseMode
from core.tools import animated_print_replace_line, display_loading_seq, clear_console, get_non_empty_str_input


class MessageEncryption(BaseMode):
    def __init__(self, mode_manager: ModeManager):
        super().__init__(mode_manager)
        self.chars: tuple = tuple(" " + string.punctuation + string.digits + string.ascii_letters)
        self.keys: list[str] = list(self.chars)
        self.cpu_lines: tuple = (
            "Agent, we've intercepted an encrypted message. What should we do?",
            "Only someone with the correct key can read an encrypted message.",
            "Encryption helps keep sensitive information private.",
            "Decryption is the process of turning encrypted text back into readable text.",
            "Strong encryption makes it difficult for attackers to read intercepted messages.",
            "Should important messages always be encrypted?",
            "What should happen after a message is decrypted?",
            "Can encrypted data be transmitted over public networks?",
            "Why should encryption keys be kept secret?",
            "Excellent. Understanding encryption and decryption is essential for every secret agent."
        )

    def start(self) -> None:
        
        random.shuffle(self.keys)
        self.instructions()
        self.build()


    @property
    def mode_name(self) -> str:
        return "Agent! Message Encryption"

    def build(self) -> None:
        for index, line in enumerate(self.cpu_lines):
            self._play_decrypt(f"Agent C: {line}", 0.5, 0, False)

            if index == len(self.cpu_lines) - 1:
                time.sleep(1)
                input("Press enter to end conversation...")
                break

            reply: str = get_non_empty_str_input("Reply (type exit to end conversation): ")

            if reply.lower() == "exit":
                break

            clear_console()

            self._play_encrypt(reply, 0.5, 0, False)
            print("Message sent!")
            time.sleep(1)
            clear_console()

        self.on_exit()


    def _encrypt(self, message: str) -> str:
        result = ""
        for letter in message:
            index = self.chars.index(letter)
            result += self.keys[index]

        return result

    def _decrypt(self, message: str) -> str:
        result = ""
        for letter in message:
            index = self.keys.index(letter)
            result += self.chars[index]

        return result

    def _play_decrypt(self, message: str, sleep_time: float = 0.1, delay: float = 0, confirm_input: bool = True) -> None:
        if delay != 0:
            print(message)
            time.sleep(delay)

        display_loading_seq("Receiving message", ".", range(1, 10), 0.1)
        time.sleep(sleep_time)

        animated_print_replace_line(self._encrypt(message), message, 0.05, confirm_input, "DECRYPTING...")

    def _play_encrypt(self, message: str, sleep_time: float = 0.5, delay: float = 0, confirm_input: bool = True) -> None:
        if delay != 0:
            print(message)
            time.sleep(delay)

        animated_print_replace_line(message, self._decrypt(message), 0.1, confirm_input, "ENCRYPTING...")

        display_loading_seq("Sending message", ".", range(1, 10), 0.1)
        time.sleep(sleep_time)

    def instructions(self) -> None:
        self._play_decrypt(f"Hello Agent {self.player_name}!", 1)
        self._play_decrypt("You are now in a mission to send and receive messages from another agent!")
        self._play_decrypt("Make sure to encrypt and decrypt their messages!")

    def on_exit(self) -> None:
        display_loading_seq("CLOSING CONNECTION", "=", range(1, 20), 0.1)
        print("Conversation ended. Connection closed.")
        time.sleep(1)
        clear_console()
        print("\n\tThank you for checking this out!")
        input("Press ENTER to return to main menu.")
        self.mode_manager.exit_mode()