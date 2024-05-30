from physics.hit_box import HitBox
from projectiles.player_bullet import PlayerBullet
from physics.vec2 import Vec2
import unittest
from unittest.mock import patch, MagicMock
from entities.alien import Alien


class TestAlien(unittest.TestCase):
    def setUp(self):
        self.position = Vec2(0, 0)
        self.speed = 10
        self.alien = Alien(self.position, self.speed)
        self.direction = Vec2(0,1)

    def test_init(self):
        self.assertEqual(self.alien.position, self.position)
        self.assertEqual(self.alien.speed, self.speed)
        self.assertEqual(self.alien.hit_box, HitBox(Vec2(-10, -10), Vec2(10, 10)))

    def test_dead_in_conflict(self):
        player_bullet = PlayerBullet(Vec2(0, 0), Vec2(0, 1), 20)
        self.assertTrue(self.alien.dead_in_conflict(player_bullet))

    @patch('projectiles.alien_bullet.AlienBullet')
    def test_shoot(self, mock_alien_bullet):
        mock_alien_bullet_instance = MagicMock()
        mock_alien_bullet.return_value = mock_alien_bullet_instance
        bullet = self.alien.shoot()
        self.assertEqual(bullet, mock_alien_bullet_instance)
        mock_alien_bullet.assert_called_once_with(self.position, self.direction, self.speed)