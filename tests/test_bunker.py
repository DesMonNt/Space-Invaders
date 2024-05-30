from projectiles.alien_bullet import AlienBullet
from projectiles.player_bullet import PlayerBullet
from entities.entity import Entity
from physics.hit_box import HitBox
from physics.vec2 import Vec2
import unittest
from entities.bunker import Bunker


class TestBunker(unittest.TestCase):
    def setUp(self):
        self.position = Vec2(100, 500)
        self.bunker = Bunker(self.position)

    def test_init(self):
        self.assertEqual(self.bunker.position, self.position)
        self.assertEqual(self.bunker.hit_box, HitBox(Vec2(80, 490), Vec2(120, 510)))
        self.assertEqual(self.bunker.speed, 0)
        self.assertEqual(self.bunker.direction, Vec2(0, -1))
        self.assertEqual(self.bunker.health, 10)

    def test_dead_in_conflict(self):
        alien_bullet = AlienBullet(Vec2(0, 0), Vec2(0, 1), 10)
        player_bullet = PlayerBullet(Vec2(0, 0), Vec2(0, 1), 10)

        self.bunker.dead_in_conflict(alien_bullet)
        self.assertEqual(self.bunker.health, 9)

        self.bunker.dead_in_conflict(player_bullet)
        self.assertEqual(self.bunker.health, 8)

        for _ in range(8):
            self.bunker.dead_in_conflict(alien_bullet)

        self.assertTrue(self.bunker.dead_in_conflict(alien_bullet))