# OK, WE'RE MAKING A GAME
#
import array
from collections import namedtuple
import random

import art
import colorama

MenuOption = namedtuple("Option", "text, callback")
Menu = namedtuple("menu", "title, menu_options")


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

    _range: (int, int)
    _board: tuple
    _board_size: int
    _random_numbers: list[int]

    def set_random_range(self, max_value: int):
        """ we're allowing for non-zero minimums. Dunno why """
        self._range = (0, max_value)
        return self

    def set_board_size(self, new_size: int):
        """ set the number of spaces in the board to place numbers """
        self._board_size = new_size
        return self

    def reset_game(self):
        """ reset the board using the current game configuration """
        self._board = ([self._DEFAULT_VALUE] * self._board_size)
        self._generate_random_numbers()
        return self

    def print_board(self):
        """ print out a nice copy of the board to look at """
        for index, value in enumerate(self._board):
            print(f'{index}:{value if value else "___"} ', end=" ")
        print()  # add the newline
        return self

    def get_random_number(self):
        """ returns the next random number from the pre-generated list of randoms """
        return self._random_numbers.pop()

    def cheat(self):
        """ you should feel ashamed of yourself """
        print(self._random_numbers)
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
        self._random_numbers = random.sample(range(*self._range), self._board_size)


def in_red(text):
    """ Use a cool library I found to turn some text red """
    return colorama.Fore.RED + text


def prompt(message: str = in_red("YOU MUST CHOOSE"), default: int = None) -> int:
    """ This overload of the prompt method will print a custom message """
    default_string = f' (default {default})' if default else ""
    return int(input(f'{message}{default_string}: ') or default)


def print_menu(menu_options: list[MenuOption]):
    """ print out the menu options, wait for user input, then run the selected option """
    for index, option in enumerate(menu_options, start=1):
        print(f'[{index}]: {option.text}')
    menu_options[prompt() - 1].callback()


def start_new_game():
    """ prompt the user for game configurations and kick off a new round """
    game = Game() \
        .set_random_range(prompt(message="Pick a really big number like", default=1000)) \
        .set_board_size(prompt(message="Now pick a really small number", default=10)) \
        .reset_game() \
        .print_board() \
        .cheat()


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
