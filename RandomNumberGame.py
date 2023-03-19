# OK, WE'RE MAKING A GAME
#
import dataclasses
import random
from collections import namedtuple
from enum import Enum

import art
import colorama

import inspect

MenuOption = namedtuple("Option", "text, callback")
Menu = namedtuple("menu", "title, menu_options")


class GameStateException(Exception):
    """Raised when an action would cause an invalid game state"""
    pass


class Outcome(Enum):
    """ used for tracking exceptions explicitly """
    WIN = 1,
    LOSE = 0


class GameOver(Exception):
    """ An easy way to pass a game over message to the game handler """
    def __init__(self, outcome: Outcome, message: str):
        self.message = message
        self.outcome = outcome


class Game:
    """
    This will hold onto all things relating to the state of the current game and offer some utility functions that
    operate on the game state.

    Note: This is written with a fluent interface to allow method cascading. Check out the links below if you want to
    learn more.

    Fluent Interface: https://en.wikipedia.org/wiki/Fluent_interface Method Cascading:
    https://en.wikipedia.org/wiki/Method_cascading
    """

    range: (int, int)
    board_size: int

    __board: list[int]
    __random_numbers: list[int]
    __current_number: int = None

    def reset_game(self):
        """ reset the board using the current game configuration """
        self.__board = [None] * self.board_size
        self._generate_random_numbers()
        return self

    def _is_board_filled(self) -> bool:
        """ return true if all the board indices have been filled """
        return all([i is not None for i in self.__board])

    def _is_board_ordered(self) -> bool:
        """ algorithm to validate that the board state is currently in order. the game ends when this returns false """
        for first, second in pairwise(filter(lambda x: x is not None, self.__board)):
            if first > second:
                return False
        return True

    def _check_game_over(self):
        """ raise exceptions to indicate GameOver if certain conditions have been met"""
        if not self._is_board_ordered():
            raise GameOver(Outcome.LOSE, in_red("YOU HAVE FAILED, BETTER LUCK NEXT TIME"))
        if self._is_board_filled():
            raise GameOver(Outcome.WIN, in_green("YOU HAVE WON! CONGRATS! YOU WIN AT NUMBERS!"))

    def place_current_number(self, index: int):
        """ place the current number on the board and change the current to default to indicate it's processed """
        if index not in range(0, self.board_size):
            raise GameStateException("Chosen number was outside the list range")
        if self.__board[index] is not None:
            raise GameStateException("Chosen board index is already occupied")

        self.__board[index] = self.__current_number
        self.__current_number = None
        self._check_game_over()
        return self

    def print_board(self):
        """ print out a nice copy of the board to look at """
        print()  # blank line before board
        for index, value in enumerate(self.__board):
            print(f'{in_magenta(str(index))}: {value if value is not None else "___"} ', end=" ")
        print()  # add the newline
        return self

    def get_random_number(self):
        """ load the next pre-generated random number and return the value """
        if self.__current_number is None:
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
        self.__random_numbers = random.sample(range(*self.range), self.board_size)


def pairwise(values: iter):
    """
    generator function to return consecutive pairs from an iterator [ABCDE] -> AB, BC, CD, DE
    Learn More: https://www.geeksforgeeks.org/generators-in-python/
    """
    current = None
    for index in values:
        last = current
        current = index
        if last is not None:
            yield last, current


def in_red(text):
    """ Use a cool library I found to turn some text red """
    return colorama.Fore.RED + str(text) + colorama.Fore.RESET


def in_magenta(text):
    """ Use a cool library I found to turn some text magenta """
    return colorama.Fore.MAGENTA + str(text) + colorama.Fore.RESET


def in_blue(text):
    """ Use a cool library I found to turn some text blue """
    return colorama.Fore.BLUE + str(text) + colorama.Fore.RESET


def in_green(text):
    """ Use a cool library I found to turn some text green """
    return colorama.Fore.GREEN + str(text) + colorama.Fore.RESET


def prompt(message: str = in_blue("YOU MUST CHOOSE"), default: int = None) -> int:
    """ This overload of the prompt method will print a custom message """
    default_string = f' (default {default})' if default else ""
    return int(input(f'{message}{default_string}: ') or default)


def print_menu(menu_options: list[MenuOption]):
    """ print out the menu options, wait for user input, then run the selected option """
    for index, option in enumerate(menu_options, start=1):
        print(f'[{index}]: {option.text}')
    menu_options[prompt() - 1].callback()


def print_game_over(message: str):
    print(f"\nGAME OVER: {message}")


def run_game(game: Game):
    """ basic game loop for user input. this is done outside the Game class so a framework for automated solutions
    can be overloaded. This should be able to run multiple times on the same game instance without issue """
    game.reset_game()
    while True:
        try:
            next_number = game.get_random_number()
            game.print_board()
            index = prompt(f'{in_blue("PLACE YOUR NUMBER:")} {next_number}')
            game.place_current_number(index)
        except GameOver as e:
            print_game_over(e.message)
            break
        except GameStateException as e:
            print(in_red(f'\nGameStateException: {e}\nTry Again'))


def start_new_game():
    """ prompt the user for game configurations and kick off a new round """
    game = Game()
    game.range = 0, prompt(message="Pick a really big number like", default=1000)
    game.board_size = prompt(message="Now pick a really small number", default=10)
    run_game(game)


def print_main_menu():
    """ print some flashy graphics and launch into the menu system """
    while True:
        print('\n')  # give a little space to the banner
        art.tprint("I WANT TO PLAY A GAME")
        print(f'stack_depth: {len(inspect.stack())}')
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
