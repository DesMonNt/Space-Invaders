import pygame as pg

from projectiles.player_bullet import PlayerBullet
from entities.mystery_ship import MysteryShip
from entities.player import Player
from entities.bunker import Bunker
from alien_wave import AlienWave
from physics.vec2 import Vec2
from game_state import GameState
import unittest
from unittest.mock import patch, MagicMock
from game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.window = pg.Surface((800, 600))
        pg.init()
        self.game = Game(self.window, 800, 600, 50, is_fresh=True)

    def test_init(self):
        self.assertEqual(self.game.window_width, 800)
        self.assertEqual(self.game.window_height, 600)
        self.assertEqual(self.game.block_size, 50)
        self.assertEqual(self.game.window, self.window)
        self.assertIsInstance(self.game.game_state, GameState)
        self.assertEqual(self.game.wave_cooldown, 0)
        self.assertEqual(self.game.player_cooldown, 0)
        self.assertFalse(self.game.is_game_over)
        self.assertFalse(self.game.is_game_closed)
        self.assertIsInstance(self.game.wave, AlienWave)

    def test_load_fresh_game(self):
        game_state = self.game.load_fresh_game()
        self.assertIsInstance(game_state.player, Player)
        self.assertIsInstance(game_state.mystery_ship, MysteryShip)
        self.assertEqual(len(game_state.bunkers), 4)
        self.assertEqual(game_state.lives, 3)

    @patch('game.path.exists')
    @patch('game.path.isfile')
    @patch('game.open')
    def test_load_saved_game(self, mock_open, mock_isfile, mock_exists):
        mock_exists.return_value = True
        mock_isfile.return_value = True
        game_state = self.game.load_saved_game()
        self.assertIsInstance(game_state, GameState)

    def test_update_score(self):
        self.game.update_score(100)
        self.assertEqual(self.game.game_state.score, 100)

    def test_check_collisions(self):
        self.game.game_state.player = Player(Vec2(400, 550), 1)
        self.game.game_state.bullets = [PlayerBullet(Vec2(400, 500), Vec2(0, -1), 1)]
        self.game.wave.aliens = [MagicMock()]
        self.game.game_state.bunkers = [Bunker(Vec2(100, 500))]
        self.game.game_state.mystery_ship = MysteryShip(Vec2(200, 100), 1)

        self.game.check_collisions()