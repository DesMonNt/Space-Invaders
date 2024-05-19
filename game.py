import pygame as pg
from entities.mystery_ship import MysteryShip
from entities.player import Player
from entities.bunker import Bunker
from alien_wave import AlienWave
from physics.vec2 import Vec2
from game_state import GameState


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

        self.wave = AlienWave(
            Vec2(self.block_size, self.block_size + self.window_height // 10),
            self.window_width,
            self.window_height,
            self.block_size
        )
        if len(self.game_state.aliens) != 0:
            self.wave.aliens = self.game_state.aliens

    def load_fresh_game(self):
        game_state = GameState()
        game_state.player = Player(Vec2(self.window_width // 2, self.window_height - self.block_size), 1)
        game_state.mystery_ship = MysteryShip(Vec2(self.block_size, self.block_size), 1)
        game_state.bunkers = \
            [Bunker(Vec2(i * self.window_width // 5, 4 * self.window_height // 5)) for i in range(1, 5)]
        game_state.lives = 3

        return game_state

    def load_saved_game(self):
        game_state = GameState()
        game_state.load()

        return game_state

    def update_score(self, points):
        self.game_state.score += points
        pg.display.set_caption(f"Space Invaders Score: {self.game_state.score}")

    def reload_wave(self):
        self.wave = AlienWave(
            Vec2(self.block_size, self.block_size),
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

    def draw_objects(self):
        for alien in self.wave.aliens:
            pg.draw.circle(self.window, Game.WHITE, (alien.position.x, alien.position.y), self.block_size // 2)

        for bunker in self.game_state.bunkers:
            pg.draw.circle(self.window, Game.WHITE, (bunker.position.x, bunker.position.y), self.block_size)

        for bullet in self.game_state.bullets:
            pg.draw.circle(self.window, Game.WHITE, (bullet.position.x, bullet.position.y), self.block_size // 4)
            bullet.move(bullet.direction * bullet.speed * self.block_size)

        if self.game_state.mystery_ship.is_active:
            pg.draw.circle(self.window, Game.WHITE,
                           (self.game_state.mystery_ship.position.x, self.game_state.mystery_ship.position.y),
                           self.block_size // 2)
            self.game_state.mystery_ship.move(
                self.game_state.mystery_ship.direction * self.game_state.mystery_ship.speed * self.block_size)

    def run(self):
        while not self.is_game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_game_over = True
                if event.type == pg.KEYDOWN:
                    dx = 0
                    if event.key == pg.K_q:
                        self.game_state.aliens = self.wave.aliens
                        self.game_state.save()
                    elif event.key == pg.K_LEFT:
                        dx -= 1
                    elif event.key == pg.K_RIGHT:
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

            pg.draw.circle(self.window, Game.WHITE,
                           (self.game_state.player.position.x, self.game_state.player.position.y),
                           self.block_size // 2)

            self.game_state.bullets += self.wave.get_aliens_bullets()

            self.check_collisions()

            self.wave_cooldown += 1

            if self.wave_cooldown % 10 == 0:
                self.wave.move_horizontal()
            if self.wave_cooldown % 120 == 0:
                self.wave.move_down()

            self.draw_objects()

            if self.game_state.mystery_ship.is_ready_to_spawn():
                self.game_state.mystery_ship.get_new_spawn_point()

            if len(self.wave.aliens) == 0:
                self.reload_wave()

            if self.game_state.lives < 0:
                self.is_game_over = True

            if self.wave.aliens[-1].position.y > 4 * self.window_height // 5:
                self.is_game_over = True

            pg.display.update()

            pg.time.wait(50)

        pg.quit()
