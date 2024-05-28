import pygame as pg


class StartMenu:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, display, width, height):
        self.is_in_menu = True
        self.is_fresh_game = False
        self.selected_button = 0
        self.display = display
        self.width = width
        self.height = height

    @staticmethod
    def get_sized_font(font_size):
        return pg.font.Font("assets/menu_font.ttf", font_size)

    def run(self):
        self.display.fill(StartMenu.BLACK)
        pg.display.set_caption("Space Invaders")

        font = StartMenu.get_sized_font(self.width // 20)
        name_text = font.render("SPACE INVADERS", True, StartMenu.WHITE)

        font = StartMenu.get_sized_font(self.width // 40)
        new_game_text = font.render("START NEW GAME", True, StartMenu.WHITE)
        continue_text = font.render("CONTINUE", True, StartMenu.WHITE)

        font = StartMenu.get_sized_font(self.width // 60)
        credits_text = font.render("COPYRIGHT @2024 JERBOA_TEAM", True, StartMenu.WHITE)

        name_rectangle = name_text.get_rect(center=(self.width // 2, self.height // 4))
        new_game_rectangle = new_game_text.get_rect(center=(self.width // 2, self.height // 4 * 2))
        continue_rectangle = continue_text.get_rect(center=(self.width // 2, self.height // 4 * 2.5))
        credits_rectangle = credits_text.get_rect(center=(self.width // 2, self.height // 4 * 3.5))

        self.display.blit(name_text, name_rectangle)
        self.display.blit(new_game_text, new_game_rectangle)
        self.display.blit(continue_text, continue_rectangle)
        self.display.blit(credits_text, credits_rectangle)

        while self.is_in_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        pg.quit()
                    if event.key == pg.K_UP or event.key == pg.K_DOWN:
                        self.selected_button += 1
                    if event.key == pg.K_SPACE:
                        self.is_in_menu = False

            if self.selected_button % 2 == 0:
                self.is_fresh_game = True
                pg.draw.circle(self.display, StartMenu.BLACK, (285, 375), 10)
                pg.draw.circle(self.display, StartMenu.WHITE, (220, 298), 10)
            else:
                self.is_fresh_game = False
                pg.draw.circle(self.display, StartMenu.BLACK, (220, 298), 10)
                pg.draw.circle(self.display, StartMenu.WHITE, (285, 375), 10)

            pg.display.update()
