from entities.entity import Entity
from physics.hit_box import HitBox
from physics.vec2 import Vec2
import unittest
from projectiles.player_bullet import PlayerBullet


class TestPlayerBullet(unittest.TestCase):
    def test_init(self):
        position = Vec2(100, 200)
        direction = Vec2(1, 0)
        speed = 10
        bullet = PlayerBullet(position, direction, speed)

        self.assertIsInstance(bullet, Entity)
        self.assertEqual(bullet.position, position)
        self.assertEqual(bullet.hit_box, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)))
        self.assertEqual(bullet.direction, direction)
        self.assertEqual(bullet.speed, speed)

    def test_equality(self):
        position1 = Vec2(100, 200)
        direction1 = Vec2(1, 0)
        speed1 = 10
        bullet1 = PlayerBullet(position1, direction1, speed1)

        position2 = Vec2(100, 200)
        direction2 = Vec2(1, 0)
        speed2 = 10
        bullet2 = PlayerBullet(position2, direction2, speed2)

        self.assertEqual(bullet1, bullet2)

        position3 = Vec2(200, 300)
        direction3 = Vec2(0, 1)
        speed3 = 20
        bullet3 = PlayerBullet(position3, direction3, speed3)

        self.assertNotEqual(bullet1, bullet3)

    def test_dead_in_conflict(self):
        position = Vec2(100, 200)
        direction = Vec2(1, 0)
        speed = 10
        bullet = PlayerBullet(position, direction, speed)
        from entities.alien import Alien
        from entities.bunker import Bunker
        self.assertTrue(bullet.dead_in_conflict(Alien(Vec2(100, 200), 1)))
        self.assertTrue(bullet.dead_in_conflict(Bunker(Vec2(100, 200))))