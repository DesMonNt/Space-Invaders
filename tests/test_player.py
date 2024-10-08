from projectiles.alien_bullet import AlienBullet
from entities.alien import Alien
from physics.vec2 import Vec2
import unittest
from unittest.mock import patch, MagicMock
from entities.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.position = Vec2(0, 0)
        self.direction = Vec2(0, -1)
        self.speed = 10
        self.player = Player(self.position, self.speed)

    def test_init(self):
        self.assertEqual(self.player.position, self.position)
        self.assertEqual(self.player.speed, self.speed)
        self.assertEqual(self.player.direction, Vec2(0, -1))

    def test_dead_in_conflict(self):
        alien_bullet = AlienBullet(Vec2(0, 0), Vec2(0, 1), 20)
        self.assertTrue(self.player.dead_in_conflict(alien_bullet))
        entity = Alien(Vec2(0, 0), 15)
        self.assertFalse(self.player.dead_in_conflict(entity))
