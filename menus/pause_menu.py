import pygame as pg


class PauseMenu:
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    def __init__(self, window, window_width, window_height):
        self.is_game_paused = True
        self.is_game_closed = False
        self.font = pg.font.Font("game_assets/menu_font.ttf", 30)
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        
    def run(self):
        name_text = self.font.render("GAME PAUSED", True, PauseMenu.WHITE)
        name_rectangle = name_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
        self.window.blit(name_text, name_rectangle)
        while self.is_game_paused:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.is_game_paused = False
                    if event.key == pg.K_q:
                        self.is_game_paused = False
                        self.is_game_closed = True
                pg.display.update()
