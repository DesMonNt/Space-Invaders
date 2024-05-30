import unittest
from unittest.mock import patch
from physics.vec2 import Vec2
from entities.player import Player
from entities.bunker import Bunker
from entities.alien import Alien
from entities.mystery_ship import MysteryShip
from projectiles.player_bullet import PlayerBullet
from projectiles.alien_bullet import AlienBullet
from game_state import GameState


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        self.game_state.player = Player(Vec2(100, 200), 1)
        self.game_state.bunkers = [
            Bunker(Vec2(50, 300)),
            Bunker(Vec2(150, 300))
        ]
        self.game_state.aliens = [
            Alien(Vec2(75, 400), 1),
            Alien(Vec2(125, 400), 1)
        ]
        self.game_state.mystery_ship = MysteryShip(Vec2(200, 100), 1)
        self.game_state.bullets = [
            PlayerBullet(Vec2(80, 220), Vec2(1, 0), 1),
            AlienBullet(Vec2(90, 410), Vec2(0, -1), 1)
        ]
        self.game_state.score = 1000
        self.game_state.lives = 3

    def test_save_and_load(self):
        self.game_state.save()

        loaded_game_state = GameState()
        loaded_game_state.load()

        self.assertEqual(self.game_state.player.position, loaded_game_state.player.position)
        self.assertEqual(len(self.game_state.bunkers), len(loaded_game_state.bunkers))
        for i in range(len(self.game_state.bunkers)):
            self.assertEqual(self.game_state.bunkers[i].position, loaded_game_state.bunkers[i].position)
            self.assertEqual(self.game_state.bunkers[i].health, loaded_game_state.bunkers[i].health)
        self.assertEqual(len(self.game_state.aliens), len(loaded_game_state.aliens))
        for i in range(len(self.game_state.aliens)):
            self.assertEqual(self.game_state.aliens[i].position, loaded_game_state.aliens[i].position)
        self.assertEqual(self.game_state.mystery_ship.position, loaded_game_state.mystery_ship.position)
        self.assertEqual(self.game_state.mystery_ship.direction, loaded_game_state.mystery_ship.direction)
        self.assertEqual(self.game_state.mystery_ship.is_active, loaded_game_state.mystery_ship.is_active)
        self.assertEqual(len(self.game_state.bullets), len(loaded_game_state.bullets))
        for i in range(len(self.game_state.bullets)):
            self.assertEqual(self.game_state.bullets[i].position, loaded_game_state.bullets[i].position)
            self.assertEqual(self.game_state.bullets[i].direction, loaded_game_state.bullets[i].direction)
        self.assertEqual(self.game_state.score, loaded_game_state.score)
        self.assertEqual(self.game_state.lives, loaded_game_state.lives)

    @patch('game_state.path.exists')
    @patch('game_state.makedirs')
    def test_save_creates_json_directory(self, mock_makedirs, mock_path_exists):
        mock_path_exists.return_value = False
        self.game_state.save()
        mock_makedirs.assert_called_once_with('json')

