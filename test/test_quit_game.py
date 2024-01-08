import unittest
from unittest.mock import patch
from game_play import GamePlay


class TestQuitGame(unittest.TestCase):
    def setUp(self):
        self.game_play = GamePlay()


class TestInitial(TestQuitGame):
    def test_menu2_status(self):
        self.assertEqual(self.game_play.menu2, False)

    def test_play_status(self):
        self.assertEqual(self.game_play.play, False)

    def test_end_game_status(self):
        self.assertEqual(self.game_play.play, False)


class TestQuit(TestQuitGame):
    @patch("game_play.GamePlay.save_game", create=True)
    @patch("game_play.maskpass.askpass", create=True)
    def test_quit(self, mock_askpass, mock_save_game):
        mock_askpass.side_effect = ['']
        self.game_play.process_command(user_input="quit")
        mock_save_game.return_value = ('mock_username', 'mock_character', 'mock_current_room', 'mock_inventory', 100,
                                       'mock_rooms')

        self.assertEqual(self.game_play.play, False)
        self.assertEqual(self.game_play.menu2, True)
        self.assertEqual(self.game_play.quit_game, True)
