import json
from game import Game
import pygame as pg

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def load_max_score():
    try:
        with open("score.json", 'r') as file:
            return json.load(file)['score']

    except FileNotFoundError:
        return 0


def save_max_score(score):
    with open("score.json", 'w') as file:
        json.dump({'score': score}, file)


def execute_game():
    pg.init()
    display = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("Space Invaders Score: 0")
    game = Game(display, WINDOW_WIDTH, WINDOW_HEIGHT, 20)
    max_score = load_max_score()
    game.run()

    score = game.score

    if score >= max_score:
        max_score = score
        save_max_score(max_score)


if __name__ == '__main__':
    execute_game()
