import json
from game import Game


def load_max_score():
    try:
        with open("score.json", 'r') as file:
            return json.load(file)

    except FileNotFoundError:
        return 0


def save_max_score(score):
    with open("score.json", 'w') as file:
        json.dump(score, file)


def execute_game():
    game = Game(800, 600, 20)
    max_score = load_max_score()
    game.run()

    score = game.score

    if score > max_score:
        max_score = score
        save_max_score(max_score)


if __name__ == '__main__':
    execute_game()
