import pygame as pg
import unittest
from unittest.mock import patch
from start_menu import StartMenu


class TestStartMenu(unittest.TestCase):
    def setUp(self):
        self.display = pg.Surface((800, 600))
        pg.font.init()
        self.start_menu = StartMenu(self.display, 800, 600)

    def test_init(self):
        self.assertTrue(self.start_menu.is_in_menu)
        self.assertFalse(self.start_menu.is_fresh_game)
        self.assertEqual(self.start_menu.selected_button, 0)
        self.assertEqual(self.start_menu.display, self.display)
        self.assertEqual(self.start_menu.width, 800)
        self.assertEqual(self.start_menu.height, 600)

    @patch('start_menu.pg.font.Font')
    def test_get_sized_font(self, mock_font):
        font_size = 20
        StartMenu.get_sized_font(font_size)
        mock_font.assert_called_once_with("assets/menu_font.ttf", font_size)

    @patch('start_menu.pg.event.get')
    @patch('start_menu.pg.display.update')
    def test_run_new_game(self, mock_update, mock_event_get):
        mock_event_get.return_value = [pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE)]
        self.start_menu.run()
        self.assertFalse(self.start_menu.is_in_menu)
        self.assertTrue(self.start_menu.is_fresh_game)

    @patch('start_menu.pg.event.get')
    @patch('start_menu.pg.display.update')
    def test_run_continue_game(self, mock_update, mock_event_get):
        mock_event_get.return_value = [pg.event.Event(pg.KEYDOWN, key=pg.K_UP),
                                       pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE)]
        self.start_menu.run()
        self.assertFalse(self.start_menu.is_in_menu)
        self.assertFalse(self.start_menu.is_fresh_game)
