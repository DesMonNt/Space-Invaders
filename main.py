import pygame as pg
from mystery_ship import MysteryShip
from player import Player
from bunker import Bunker
from alien_wave import AlienWave
from vec2 import Vec2

pg.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Space Invaders")

hp = 3
bullets = []
player = Player(Vec2(WINDOW_WIDTH // 2, WINDOW_HEIGHT - BLOCK_SIZE), BLOCK_SIZE)
mystery_ship = MysteryShip(Vec2(0, 0), 20)
wave = AlienWave(Vec2(BLOCK_SIZE, BLOCK_SIZE + WINDOW_HEIGHT // 10), WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
bunkers = [
    Bunker(Vec2(1 * WINDOW_WIDTH // 5, 4 * WINDOW_HEIGHT // 5)),
    Bunker(Vec2(2 * WINDOW_WIDTH // 5, 4 * WINDOW_HEIGHT // 5)),
    Bunker(Vec2(3 * WINDOW_WIDTH // 5, 4 * WINDOW_HEIGHT // 5)),
    Bunker(Vec2(4 * WINDOW_WIDTH // 5, 4 * WINDOW_HEIGHT // 5)),
]


a = 0
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            dx = 0

            if event.key == pg.K_LEFT:
                dx -= 1
            elif event.key == pg.K_RIGHT:
                dx += 1
            elif event.key == pg.K_SPACE:
                bullets.append(player.shoot())
                bullets[-1].move(player.direction * 2 * player.speed)

            player.move(Vec2(dx, 0) * player.speed)

    window.fill(BLACK)

    pg.draw.circle(window, WHITE, (player.position.x, player.position.y), BLOCK_SIZE // 2)

    bullets += wave.get_aliens_bullets()

    for bullet in bullets:
        for alien in wave.aliens:
            if alien.is_intersecting(bullet):
                if alien.dead_in_conflict(bullet):
                    wave.aliens.remove(alien)
                if bullet.dead_in_conflict(alien):
                    bullets.remove(bullet)

        for bunker in bunkers:
            if bunker.is_intersecting(bullet):
                if bunker.dead_in_conflict(bullet):
                    bunkers.remove(bunker)
                if bullet.dead_in_conflict(bunker):
                    bullets.remove(bullet)

        if player.is_intersecting(bullet):
            if player.dead_in_conflict(bullet):
                hp -= 1
            if bullet.dead_in_conflict(bullet):
                bullets.remove(bullet)

        if mystery_ship.is_intersecting(bullet):
            if mystery_ship.dead_in_conflict(bullet):
                mystery_ship.is_active = False
            if bullet.dead_in_conflict(bullet):
                bullets.remove(bullet)

    a += 1

    if a % 10 == 0:
        wave.move_horizontal()
    if a % 120 == 0:
        wave.move_down()

    for alien in wave.aliens:
        pg.draw.circle(window, WHITE, (alien.position.x, alien.position.y), BLOCK_SIZE // 2)

    for bunker in bunkers:
        pg.draw.circle(window, WHITE, (bunker.position.x, bunker.position.y), BLOCK_SIZE)

    for bullet in bullets:
        pg.draw.circle(window, WHITE, (bullet.position.x, bullet.position.y), BLOCK_SIZE // 4)
        bullet.move(bullet.direction * bullet.speed)

    if mystery_ship.is_active:
        pg.draw.circle(window, WHITE, (mystery_ship.position.x, mystery_ship.position.y), BLOCK_SIZE // 2)
        mystery_ship.move(mystery_ship.direction * mystery_ship.speed)

    if mystery_ship.is_ready_to_spawn():
        mystery_ship.get_new_spawn_point()

    if len(wave.aliens) == 0:
        wave = AlienWave(Vec2(BLOCK_SIZE, BLOCK_SIZE), WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)

    if hp < 0:
        running = False

    if wave.aliens[-1].position.y > 4 * WINDOW_HEIGHT // 5:
        running = False

    pg.display.update()

    pg.time.wait(50)

pg.quit()
