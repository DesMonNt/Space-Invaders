import pygame as pg

from projectiles.player_bullet import PlayerBullet
from entities.mystery_ship import MysteryShip
from entities.player import Player
from entities.bunker import Bunker
from alien_wave import AlienWave
from physics.vec2 import Vec2
from game_state import GameState
from pause_menu import PauseMenu
from game_over_menu import GameOverMenu
from os import path, makedirs


class Game:
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    def __init__(self, window, window_width, window_height, block_size, is_fresh=True):
        self.window_width = window_width
        self.window_height = window_height
        self.block_size = block_size
        self.window = window

        if is_fresh:
            self.game_state = self.load_fresh_game()
        else:
            self.game_state = self.load_saved_game()

        self.wave_cooldown = 0
        self.player_cooldown = 0
        self.is_game_over = False
        self.is_game_closed = False

        self.wave = AlienWave(
            Vec2(self.block_size, self.block_size + self.window_height // 10),
            self.window_width,
            self.window_height,
            self.block_size
        )

        if len(self.game_state.aliens) != 0:
            self.wave.aliens = self.game_state.aliens

    def pause_game(self):
        self.game_state.aliens = self.wave.aliens
        self.game_state.save()

        pause = PauseMenu(self.window, self.window_width, self.window_height)
        pause.run()
        self.is_game_closed = pause.is_game_closed

        self.game_state = self.load_saved_game()
        self.run()

    def load_fresh_game(self):
        game_state = GameState()
        game_state.player = Player(Vec2(self.window_width // 2, self.window_height - self.block_size), 1)
        game_state.mystery_ship = MysteryShip(Vec2(self.block_size, self.block_size * 3), 0.5)
        game_state.bunkers = \
            [Bunker(Vec2(i * self.window_width // 5, 4 * self.window_height // 5)) for i in range(1, 5)]
        game_state.lives = 3

        return game_state

    def load_saved_game(self):
        game_state = GameState()
        if not path.exists('json'):
            makedirs('json')
        if not path.isfile('json/game_state.json'):
            with open('json/game_state.json', 'w'):
                pass
            game_state = self.load_fresh_game()
            game_state.save()
        game_state.load()
        return game_state

    def update_score(self, points):
        self.game_state.score += points

    def reload_wave(self):
        self.wave = AlienWave(
            Vec2(self.block_size, self.block_size + self.window_height // 10),
            self.window_width,
            self.window_height,
            self.block_size
        )

    def check_collisions(self):
        for bullet in self.game_state.bullets:
            for alien in self.wave.aliens:
                if alien.is_intersecting(bullet):
                    if alien.dead_in_conflict(bullet):
                        self.update_score(2)
                        self.wave.aliens.remove(alien)
                    if bullet.dead_in_conflict(alien):
                        self.game_state.bullets.remove(bullet)

            for bunker in self.game_state.bunkers:
                if bunker.is_intersecting(bullet):
                    if bunker.dead_in_conflict(bullet):
                        self.game_state.bunkers.remove(bunker)
                    if bullet.dead_in_conflict(bunker):
                        self.game_state.bullets.remove(bullet)

            if self.game_state.player.is_intersecting(bullet):
                if self.game_state.player.dead_in_conflict(bullet):
                    self.game_state.lives -= 1
                if bullet.dead_in_conflict(bullet):
                    self.game_state.bullets.remove(bullet)

            if self.game_state.mystery_ship.is_intersecting(bullet):
                if self.game_state.mystery_ship.dead_in_conflict(bullet):
                    self.update_score(100)
                    self.game_state.mystery_ship.is_active = False
                if bullet.dead_in_conflict(bullet):
                    self.game_state.bullets.remove(bullet)

    @staticmethod
    def get_bunker_sprite(bunker):
        if bunker.health > 7:
            return pg.image.load("assets/bunker/bunker.png")
        elif bunker.health > 2:
            return pg.image.load("assets/bunker/scratched_bunker.png")
        return pg.image.load("assets/bunker/damaged_bunker.png")

    def draw_objects(self):

        font = pg.font.Font("tests/assets/menu_font.ttf", 15)
        game_over_text = font.render(f"SCORE:{self.game_state.score}", True, Game.WHITE)
        game_over_rectangle = game_over_text.get_rect(center=(self.block_size * 4, self.block_size))
        self.window.blit(game_over_text, game_over_rectangle)

        lives_image = pg.image.load("assets/player.png")
        for i in range(self.game_state.lives):
            self.window.blit(lives_image, lives_image.get_rect(
                center=(self.window_width - ((self.block_size + 10) * i + self.block_size * 4), self.block_size)))

        for alien in self.wave.aliens:
            alien_image = pg.image.load("assets/alien.png")
            self.window.blit(alien_image, alien_image.get_rect(center=(alien.position.x, alien.position.y)))
            # pg.draw.circle(self.window, Game.WHITE, (alien.position.x, alien.position.y), self.block_size // 2)

        for bunker in self.game_state.bunkers:
            bunker_image = self.get_bunker_sprite(bunker)
            self.window.blit(bunker_image, bunker_image.get_rect(center=(bunker.position.x, bunker.position.y)))
            # pg.draw.circle(self.window, "green", (bunker.position.x, bunker.position.y), self.block_size)

        for bullet in self.game_state.bullets:
            if not (0 < bullet.position.y < self.window_height) or not (0 < bullet.position.x < self.window_width):
                self.game_state.bullets.remove(bullet)
            if isinstance(bullet, PlayerBullet):
                bullet_image = pg.image.load("assets/player_bullet.png")
            else:
                bullet_image = pg.image.load("assets/alien_bullet.png")
            self.window.blit(bullet_image, bullet_image.get_rect(center=(bullet.position.x, bullet.position.y)))
            # pg.draw.circle(self.window, Game.WHITE, (bullet.position.x, bullet.position.y), self.block_size // 4)
            bullet.move(bullet.direction * bullet.speed * self.block_size)

        if self.game_state.mystery_ship.is_active:
            mystery_image = pg.image.load("assets/mystery.png ")
            self.window.blit(mystery_image, mystery_image.get_rect(
                center=(self.game_state.mystery_ship.position.x,
                        self.game_state.mystery_ship.position.y)))
            # pg.draw.circle(self.window, Game.WHITE,
            #                (self.game_state.mystery_ship.position.x, self.game_state.mystery_ship.position.y),
            #                self.block_size // 2)
            self.game_state.mystery_ship.move(
                self.game_state.mystery_ship.direction * self.game_state.mystery_ship.speed * self.block_size)

    def run(self):

        while not (self.is_game_over or self.is_game_closed):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_game_closed = True
                if event.type == pg.KEYDOWN:
                    dx = 0
                    if event.key == pg.K_q:
                        self.game_state.aliens = self.wave.aliens
                        self.game_state.save()
                        self.is_game_closed = True
                    elif event.key == pg.K_ESCAPE:
                        self.pause_game()
                    elif event.key == pg.K_LEFT and self.game_state.player.position.x > 0:
                        dx -= 1
                    elif event.key == pg.K_RIGHT and self.game_state.player.position.x < self.window_width:
                        dx += 1
                    elif event.key == pg.K_SPACE:
                        if self.player_cooldown == 0:
                            self.game_state.bullets.append(self.game_state.player.shoot())
                            self.game_state.bullets[-1].move(
                                self.game_state.player.direction * 2 * self.game_state.player.speed * self.block_size)
                            self.player_cooldown = 5

                    self.game_state.player.move(Vec2(dx, 0) * self.game_state.player.speed * self.block_size)

                if self.player_cooldown > 0:
                    self.player_cooldown -= 1

            self.window.fill(Game.BLACK)

            player_image = pg.image.load("assets/player.png")
            self.window.blit(player_image, player_image.get_rect(
                center=(self.game_state.player.position.x, self.game_state.player.position.y)))
            # pg.draw.circle(self.window, Game.WHITE, (self.game_state.player.position.x,
            # self.game_state.player.position.y), self.block_size // 2)

            self.game_state.bullets += self.wave.get_aliens_bullets()

            self.check_collisions()

            self.wave_cooldown += 1

            if self.wave_cooldown % 15 == 0:
                self.wave.move_horizontal()
            if self.wave_cooldown % 180 == 0:
                self.wave.move_down()

            self.draw_objects()

            if self.game_state.mystery_ship.is_ready_to_spawn():
                self.game_state.mystery_ship.get_new_spawn_point()

            if len(self.wave.aliens) == 0:
                self.reload_wave()

            if self.game_state.lives == 0:
                self.is_game_over = True

            if self.wave.aliens[-1].position.y > 3.5 * self.window_height // 5:
                self.is_game_over = True

            pg.display.update()

            pg.time.wait(50)

        if self.is_game_over:
            game_over = GameOverMenu(self.window, self.window_width, self.window_height, self.game_state.score)
            game_over.run()

        pg.quit()
