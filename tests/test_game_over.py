import pygame as pg
import unittest
from unittest.mock import patch
from game_over_menu import GameOverMenu


class TestGameOverMenu(unittest.TestCase):
    def setUp(self):
        self.display = pg.Surface((800, 600))
        pg.font.init()
        self.game_over_menu = GameOverMenu(self.display, 800, 600, 100)

    def test_init(self):
        self.assertEqual(self.game_over_menu.display, self.display)
        self.assertEqual(self.game_over_menu.width, 800)
        self.assertEqual(self.game_over_menu.height, 600)
        self.assertEqual(self.game_over_menu.score, 100)

    @patch('game_over_menu.pg.event.get')
    @patch('game_over_menu.pg.display.update')
    @patch('game_over_menu.json.load')
    def test_run_with_high_score(self, mock_json_load, mock_update, mock_event_get):
        mock_event_get.return_value = [pg.event.Event(pg.QUIT)]
        mock_json_load.return_value = {'score': 50}
        self.game_over_menu.run()

    @patch('game_over_menu.pg.event.get')
    @patch('game_over_menu.pg.display.update')
    @patch('game_over_menu.json.load')
    def test_run_with_new_high_score(self, mock_json_load, mock_update, mock_event_get):
        mock_event_get.return_value = [pg.event.Event(pg.QUIT)]
        mock_json_load.return_value = {'score': 50}
        self.game_over_menu = GameOverMenu(self.display, 800, 600, 200)
        self.game_over_menu.run()

