import json
from game import Game
from menus.start_menu import StartMenu
import pygame as pg

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def load_max_score():
    try:
        with open("json/score.json", 'r') as file:
            return json.load(file)['score']

    except FileNotFoundError:
        return 0


def save_max_score(score):
    with open("json/score.json", 'w') as file:
        json.dump({'score': score}, file)


def execute_game():
    pg.init()
    display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    menu = StartMenu(display, WINDOW_WIDTH, WINDOW_HEIGHT)
    menu.run()

    game = Game(display, WINDOW_WIDTH, WINDOW_HEIGHT, 20, menu.is_fresh_game)
    pg.display.set_caption(f"Space Invaders Score: {game.game_state.score}")
    max_score = load_max_score()
    game.run()

    score = game.game_state.score

    if score >= max_score:
        max_score = score
        save_max_score(max_score)

    pg.quit()


if __name__ == '__main__':
    execute_game()
