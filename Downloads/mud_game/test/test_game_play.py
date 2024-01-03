import unittest
from unittest.mock import patch
from game_play import GamePlay

class TestGamePlay(unittest.TestCase):
    def setUp(self):
        self.game = GamePlay()

    @patch('builtins.input', side_effect=['1', 'test_user', 'password123'])
    def test_handle_login(self, mock_input):
        self.game.handle_login()


if __name__ == '__main__':
    unittest.main()
