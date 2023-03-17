# import random

from RandomNumberGame import start_new_game, print_menu, prompt
import RandomNumberGame as rng
import art
from collections import namedtuple

MenuOption = namedtuple("Option", "text, callback")
Menu = namedtuple("menu", "title, menu_options")


class Automator:
    # def __init__(self):
    total_num_runs = 0
    attempts = []

def run_games(auto, game):
    for attempt in range(0, auto.total_num_runs):
        game.reset_game()
        index = 0
        while True:
            try:
                next_number = game.get_random_number()
                # game.print_board()
                # index = prompt(f'{in_blue("PLACE YOUR NUMBER:")} {next_number}')
                print(f'Placing value: {next_number} at index: {index}')
                game.place_current_number(index)
                index += 1
            except rng.GameOver as e:
                auto.attempts.append(e.outcome)
                break
            except rng.GameStateException as e:
                print(index, attempt)
                game.print_board()
                print(rng.in_red(f'\nGameStateException: {e}'))
                break
    print(auto.attempts)
    print_main_menu()

def print_main_menu():
    """ print some flashy graphics and launch into the menu system """
    print('\n')  # give a little space to the banner
    art.tprint("I WANT TO AUTOMATE A GAME")
    print_menu([
        MenuOption(text="HELL YEAH, LETS DO THIS!!!", callback=automate_game),
        MenuOption(text="Sure, that sounds like fun", callback=automate_game),
        MenuOption(text="Eh, I'd rather play a game myself", callback=start_new_game),
        MenuOption(text="No Thanks", callback=exit)
    ])


def automate_game():
    game = rng.Game()
    game.range = 0, prompt(message="Pick a really big number like", default=1000)
    game.board_size = prompt(message="Now pick a really small number", default=10)
    auto = Automator()
    auto.total_num_runs = prompt(message="Choose how many games you would like to automate", default=10)
    run_games(auto, game)

if __name__ == '__main__':
    # __init__()
    print_main_menu()
