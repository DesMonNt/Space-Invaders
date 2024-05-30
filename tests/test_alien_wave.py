from random import random
from entities.alien import Alien
from physics.vec2 import Vec2
import unittest
from unittest.mock import patch, MagicMock
from alien_wave import AlienWave


class TestAlienWave(unittest.TestCase):
    def setUp(self):
        self.start_position = Vec2(50, 50)
        self.width = 800
        self.height = 600
        self.block_size = 40
        self.alien_wave = AlienWave(self.start_position, self.width, self.height, self.block_size)

    def test_init(self):
        alien_wave = AlienWave(self.start_position, self.width, self.height, self.block_size)
        self.assertEqual(len(alien_wave.aliens), 85)

    @patch('random.random')
    def test_get_aliens_bullets(self, mock_random):
        mock_random.return_value = 0.002
        self.alien_wave.aliens = [MagicMock(spec=Alien)]
        bullets = self.alien_wave.get_aliens_bullets()
        self.assertEqual(len(bullets), 0)

    def test_move_horizontal(self):
        self.alien_wave.aliens = [MagicMock(spec=Alien, position=Vec2(800, 50), speed=1)]
        self.alien_wave.move_horizontal()
        self.alien_wave.aliens[0].move.assert_called_once_with(Vec2(-self.block_size, 0))

        self.alien_wave.aliens = [MagicMock(spec=Alien, position=Vec2(10, 50), speed=1)]
        self.alien_wave.move_horizontal()
        self.alien_wave.aliens[0].move.assert_called_once_with(Vec2(self.block_size, 0))

    def test_move_down(self):
        self.alien_wave.aliens = [MagicMock(spec=Alien, speed=1)]
        self.alien_wave.move_down()
        self.alien_wave.aliens[0].move.assert_called_once_with(Vec2(0, self.block_size))