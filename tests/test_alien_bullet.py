from entities.entity import Entity
from entities.alien import Alien
from physics.hit_box import HitBox
from physics.vec2 import Vec2
import unittest
from projectiles.alien_bullet import AlienBullet


class TestAlienBullet(unittest.TestCase):
    def test_init(self):
        position = Vec2(100, 200)
        direction = Vec2(1, 0)
        speed = 10
        bullet = AlienBullet(position, direction, speed)
        self.assertEqual(bullet.position, position)
        self.assertEqual(bullet.hit_box, HitBox(Vec2(90, 190), Vec2(110, 210)))
        self.assertEqual(bullet.direction, direction)
        self.assertEqual(bullet.speed, speed)

    def test_eq(self):
        bullet1 = AlienBullet(Vec2(100, 200), Vec2(1, 0), 10)
        bullet2 = AlienBullet(Vec2(100, 200), Vec2(1, 0), 10)
        self.assertEqual(bullet1, bullet2)

        bullet3 = AlienBullet(Vec2(100, 201), Vec2(1, 0), 10)
        self.assertNotEqual(bullet1, bullet3)

    def test_dead_in_conflict(self):
        bullet = AlienBullet(Vec2(100, 200), Vec2(1, 0), 10)
        from entities.player import Player
        self.assertTrue(bullet.dead_in_conflict(Player(Vec2(100, 200), 1)))
        self.assertFalse(bullet.dead_in_conflict(Alien(Vec2(100, 200), 1)))
