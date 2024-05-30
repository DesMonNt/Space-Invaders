from physics.hit_box import HitBox
from projectiles.player_bullet import PlayerBullet
from physics.vec2 import Vec2
import unittest
from entities.mystery_ship import MysteryShip


class TestMysteryShip(unittest.TestCase):
    def setUp(self):
        self.position = Vec2(400, 300)
        self.speed = 10
        self.mystery_ship = MysteryShip(self.position, self.speed)

    def test_init(self):
        self.assertEqual(self.mystery_ship.position, self.position)
        self.assertEqual(self.mystery_ship.speed, self.speed)
        self.assertEqual(self.mystery_ship.hit_box, HitBox(Vec2(390, 290), Vec2(410, 310)))
        self.assertEqual(self.mystery_ship.direction, Vec2(0, 1))
        self.assertEqual(self.mystery_ship.is_active, False)

    def test_dead_in_conflict(self):
        player_bullet = PlayerBullet(Vec2(0, 0), Vec2(0, 1), 20)
        self.assertTrue(self.mystery_ship.dead_in_conflict(player_bullet))