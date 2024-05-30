import pygame as pg
import unittest
from unittest.mock import patch
from pause_menu import PauseMenu


class TestPauseMenu(unittest.TestCase):
    def setUp(self):
        self.window = pg.Surface((800, 600))
        pg.font.init()
        self.pause_menu = PauseMenu(self.window, 800, 600)

    def test_init(self):
        self.assertTrue(self.pause_menu.is_game_paused)
        self.assertFalse(self.pause_menu.is_game_closed)
        self.assertIsInstance(self.pause_menu.font, pg.font.Font)
        self.assertEqual(self.pause_menu.window, self.window)
        self.assertEqual(self.pause_menu.window_width, 800)
        self.assertEqual(self.pause_menu.window_height, 600)

    @patch('pause_menu.pg.event.get')
    @patch('pause_menu.pg.display.update')
    def test_run_resume(self, mock_update, mock_event_get):
        mock_event_get.return_value = [pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE)]
        self.pause_menu.run()
        self.assertFalse(self.pause_menu.is_game_paused)
        self.assertFalse(self.pause_menu.is_game_closed)

    @patch('pause_menu.pg.event.get')
    @patch('pause_menu.pg.display.update')
    def test_run_quit(self, mock_update, mock_event_get):
        mock_event_get.return_value = [pg.event.Event(pg.KEYDOWN, key=pg.K_q)]
        self.pause_menu.run()
        self.assertFalse(self.pause_menu.is_game_paused)
        self.assertTrue(self.pause_menu.is_game_closed)