import pygame as pg
from entities.mystery_ship import MysteryShip
from entities.player.player import Player
from entities.bunker import Bunker
from entities.aliens.alien_wave import AlienWave
from physics.vec2 import Vec2


class Game:
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    def __init__(self, window_width, window_height, block_size):
        pg.init()
        pg.display.set_caption("Space Invaders Score: 0")
        self.window_width = window_width
        self.window_height = window_height
        self.block_size = block_size
        self.window = pg.display.set_mode((self.window_width, self.window_height))

        self.player = Player(Vec2(self.window_width // 2, self.window_height - self.block_size), self.block_size)
        self.mystery_ship = MysteryShip(Vec2(self.block_size, self.block_size), 20)
        self.wave = AlienWave(
            Vec2(self.block_size, self.block_size + self.window_height // 10),
            self.window_width,
            self.window_height,
            self.block_size
        )
        self.bunkers = [Bunker(Vec2(i * self.window_width // 5, 4 * self.window_height // 5)) for i in range(1, 5)]
        self.bullets = []

        self.is_game_over = False
        self.player_health = 3
        self.score = 0
        self.wave_cooldown = 0
        self.player_cooldown = 0

    def reload_wave(self):
        self.wave = AlienWave(
            Vec2(self.block_size, self.block_size),
            self.window_width,
            self.window_height,
            self.block_size
        )

    def check_collisions(self):
        for bullet in self.bullets:
            for alien in self.wave.aliens:
                if alien.is_intersecting(bullet):
                    if alien.dead_in_conflict(bullet):
                        self.score += 2
                        self.wave.aliens.remove(alien)
                    if bullet.dead_in_conflict(alien):
                        self.bullets.remove(bullet)

            for bunker in self.bunkers:
                if bunker.is_intersecting(bullet):
                    if bunker.dead_in_conflict(bullet):
                        self.bunkers.remove(bunker)
                    if bullet.dead_in_conflict(bunker):
                        self.bullets.remove(bullet)

            if self.player.is_intersecting(bullet):
                if self.player.dead_in_conflict(bullet):
                    self.player_health -= 1
                if bullet.dead_in_conflict(bullet):
                    self.bullets.remove(bullet)

            if self.mystery_ship.is_intersecting(bullet):
                if self.mystery_ship.dead_in_conflict(bullet):
                    self.score += 100
                    self.mystery_ship.is_active = False
                if bullet.dead_in_conflict(bullet):
                    self.bullets.remove(bullet)

    def draw_objects(self):
        for alien in self.wave.aliens:
            pg.draw.circle(self.window, Game.WHITE, (alien.position.x, alien.position.y), self.block_size // 2)

        for bunker in self.bunkers:
            pg.draw.circle(self.window, Game.WHITE, (bunker.position.x, bunker.position.y), self.block_size)

        for bullet in self.bullets:
            pg.draw.circle(self.window, Game.WHITE, (bullet.position.x, bullet.position.y), self.block_size // 4)
            bullet.move(bullet.direction * bullet.speed)

        if self.mystery_ship.is_active:
            pg.draw.circle(self.window, Game.WHITE, (self.mystery_ship.position.x, self.mystery_ship.position.y),
                           self.block_size // 2)
            self.mystery_ship.move(self.mystery_ship.direction * self.mystery_ship.speed)

    def run(self):
        while not self.is_game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_game_over = True
                if event.type == pg.KEYDOWN:
                    dx = 0

                    if event.key == pg.K_LEFT:
                        dx -= 1
                    elif event.key == pg.K_RIGHT:
                        dx += 1
                    elif event.key == pg.K_SPACE:
                        if self.player_cooldown == 0:
                            self.bullets.append(self.player.shoot())
                            self.bullets[-1].move(self.player.direction * 2 * self.player.speed)
                            self.player_cooldown = 5

                    self.player.move(Vec2(dx, 0) * self.player.speed)

                if self.player_cooldown > 0:
                    self.player_cooldown -= 1

            self.window.fill(Game.BLACK)

            pg.draw.circle(self.window, Game.WHITE, (self.player.position.x, self.player.position.y), self.block_size // 2)

            self.bullets += self.wave.get_aliens_bullets()

            self.check_collisions()

            self.wave_cooldown += 1

            if self.wave_cooldown % 10 == 0:
                self.wave.move_horizontal()
            if self.wave_cooldown % 120 == 0:
                self.wave.move_down()

            self.draw_objects()

            if self.mystery_ship.is_ready_to_spawn():
                self.mystery_ship.get_new_spawn_point()

            if len(self.wave.aliens) == 0:
                self.reload_wave()

            if self.player_health < 0:
                self.is_game_over = True

            if self.wave.aliens[-1].position.y > 4 * self.window_height // 5:
                self.is_game_over = True

            pg.display.set_caption(f"Space Invaders Score: {self.score}")
            pg.display.update()

            pg.time.wait(50)

        pg.quit()


