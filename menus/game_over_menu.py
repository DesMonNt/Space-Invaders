import pygame as pg
import json


class GameOverMenu:
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, display, width, height, score):
        self.display = display
        self.width = width
        self.height = height
        self.score = score

    def run(self):
        self.display.fill(GameOverMenu.BLACK)
        pg.display.set_caption("Game Over")

        font = pg.font.Font("game_assets/menu_font.ttf", 50)
        game_over_text = font.render("GAME OVER", True, GameOverMenu.WHITE)
        game_over_rectangle = game_over_text.get_rect(center=(self.width // 2, self.height // 4))
        self.display.blit(game_over_text, game_over_rectangle)

        font = pg.font.Font("game_assets/menu_font.ttf", 15)
        current_score_text = font.render(f"YOUR SCORE: {self.score}", True, GameOverMenu.WHITE)
        current_score_rectangle = game_over_text.get_rect(
            center=(self.width // 2 * 1.25, self.height // 4 * 2))
        self.display.blit(current_score_text, current_score_rectangle)

        with open('json/score.json', 'r') as f:
            high_score = json.load(f)['score']
        high_score_text = font.render(f"HIGH SCORE: {max(self.score, high_score)}", True, GameOverMenu.WHITE)
        high_score_rectangle = game_over_text.get_rect(
            center=(self.width // 2 * 1.25, self.height // 4 * 2.5))
        self.display.blit(high_score_text, high_score_rectangle)

        pg.time.wait(200)
        pg.display.update()
        is_here = True
        while is_here:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_here = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        is_here = False
