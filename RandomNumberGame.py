# OK, WE'RE MAKING A GAME
#
import array
import dataclasses
from collections import namedtuple
import random

import art
import colorama
import itertools
from enum import Enum

MenuOption = namedtuple("Option", "text, callback")
Menu = namedtuple("menu", "title, menu_options")


class GameStateException(Exception):
    """Raised when an action would cause an invalid game state"""
    pass

class GameOver(Exception):
    """ An easy way to pass a game over message to the game handler """
    pass


class Game:
    """
    This will hold onto all things relating to the state of the current game and offer some utility functions that
    operate on the game state.

    Note: This is written with a fluent interface to allow method cascading. Check out the links below if you want to
    learn more.

    Fluent Interface: https://en.wikipedia.org/wiki/Fluent_interface Method Cascading:
    https://en.wikipedia.org/wiki/Method_cascading
    """

    _DEFAULT_VALUE = None

    __range: (int, int)
    __board: tuple
    __board_size: int
    __random_numbers: list[int]

    __current_number: int = _DEFAULT_VALUE

    def set_random_range(self, max_value: int):
        """ we're allowing for non-zero minimums. Dunno why """
        self.__range = (0, max_value)
        return self

    def set_board_size(self, new_size: int):
        """ set the number of spaces in the board to place numbers """
        self.__board_size = new_size
        return self

    def reset_game(self):
        """ reset the board using the current game configuration """
        self.__board = ([self._DEFAULT_VALUE] * self.__board_size)
        self._generate_random_numbers()
        return self

    def _is_board_filled(self) -> bool:
        return all(self.__board)

    def _is_board_ordered(self) -> bool:
        """ algorithm to validate that the board state is currently in order. the game ends when this returns false """
        for first, second in pairwise(filter(lambda x: x is not None, self.__board)):
            if first > second:
                print("FAILURE")
                return False
        return True

    def game_over(self) -> bool:
        if not self._is_board_ordered():
            raise GameOver(in_red("YOU HAVE FAILED, BETTER LUCK NEXT TIME"))
        if self._is_board_filled():
            raise GameOver()

        return self._is_board_filled() or not self._is_board_ordered()

    def place_current_number(self, index: int):
        """ place the current number on the board and change the current to default to indicate it's processed """
        self.__board[index] = self.__current_number
        self.__current_number = self._DEFAULT_VALUE
        return self

    def print_board(self):
        """ print out a nice copy of the board to look at """
        for index, value in enumerate(self.__board):
            print(f'{in_magenta(str(index))}:{value or "___"} ', end=" ")
        print()  # add the newline
        return self

    def prompt_next_move(self):
        """ displays the current state and prompts the user for the next move """
        self.print_board()
        index = prompt(f'{in_red("PLACE YOUR NUMBER:")} {self.__current_number}')
        self.place_current_number(index)

    def get_random_number(self):
        """ load the next pre-generated random number and return the value """
        if self.__current_number:
            raise GameStateException("Current number must be consumed before the next can be provided")
        self.__current_number = self.__random_numbers.pop()
        return self.__current_number

    def cheat(self):
        """ you should feel ashamed of yourself """
        print(self.__random_numbers)
        return self

    def _generate_random_numbers(self):
        """
        Seed the random numbers which will be provided during the game.

                Notes:
                    There's a cute trick here called "range(*self._range)" called unpacking which converts the
                    tuple into multiple arguments.

                    Learn More: https://www.geeksforgeeks.org/packing-and-unpacking-arguments-in-python/

                    The use of "random.sample(range())" will not actually mean that the full range of numbers (
                    0-1000) will actually be created. range() uses lazy evaluation which only generates the
                    referenced numbers

                    Learn More: https://www.tutorialspoint.com/functional_programming/functional_programming_lazy_evaluation.htm
        """
        self.__random_numbers = random.sample(range(*self.__range), self.__board_size)


def pairwise(values: iter):
    """
    generator function to return consecutive pairs from an iterator [ABCDE] -> AB, BC, CD, DE
    Learn More: https://www.geeksforgeeks.org/generators-in-python/
    """
    current = None
    for index in values:
        last = current
        current = index
        if last is not None and current is not None:
            yield last, current

def in_red(text):
    """ Use a cool library I found to turn some text red """
    return colorama.Fore.RED + text + colorama.Fore.RESET


def in_magenta(text):
    """ Use a cool library I found to turn some text magenta """
    return colorama.Fore.MAGENTA + text + colorama.Fore.RESET


def prompt(message: str = in_red("YOU MUST CHOOSE"), default: int = None) -> int:
    """ This overload of the prompt method will print a custom message """
    default_string = f' (default {default})' if default else ""
    return int(input(f'{message}{default_string}: ') or default)


def print_menu(menu_options: list[MenuOption]):
    """ print out the menu options, wait for user input, then run the selected option """
    for index, option in enumerate(menu_options, start=1):
        print(f'[{index}]: {option.text}')
    menu_options[prompt() - 1].callback()


def run_game(game: Game):
    game.reset_game()
    while not game.game_over():
        next_number = game.get_random_number()
        game.print_board()
        index = prompt(f'{in_red("PLACE YOUR NUMBER:")} {next_number}')
        game.place_current_number(index)
    print("GAME OVER")
    print_main_menu()


def start_new_game():
    """ prompt the user for game configurations and kick off a new round """
    game = Game() \
        .set_random_range(prompt(message="Pick a really big number like", default=1000)) \
        .set_board_size(prompt(message="Now pick a really small number", default=10)) \
        .reset_game()
    run_game(game)


def print_main_menu():
    """ print some flashy graphics and launch into the menu system """
    art.tprint("I WANT TO PLAY A GAME")
    print_menu([
        MenuOption(text="HELL YEAH, LETS DO THIS!!!", callback=start_new_game),
        MenuOption(text="Sure, that sounds like fun", callback=start_new_game),
        MenuOption(text="Eh, ok", callback=start_new_game),
        MenuOption(text="No Thanks", callback=exit)
    ])


def __init__():
    """ Basic setup stuff for the module """
    colorama.init(autoreset=True)  # Resets color on each new line


if __name__ == '__main__':
    __init__()
    print_main_menu()