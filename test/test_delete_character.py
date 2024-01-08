import unittest
from unittest.mock import patch
from user_management import UserManager


class TestDeleteAccount(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()


class TestInit(TestDeleteAccount):
    def test_initial_storage_file(self):
        self.assertEqual(self.user_manager.storage_file, 'users.json')

    def test_initial_leaderboard_file(self):
        self.assertEqual(self.user_manager.leaderboard_file, 'leaderboard.json')


class TestDeleteC(TestDeleteAccount):
    @patch('user_management.maskpass.askpass', create=True)
    def test_delete_character_character_found(self, mock_askpass):
        mock_askpass.side_effect = ['']
        username = "Mint"
        character_name = "test"
        self.user_manager.delete_character(username)
        self.assertNotIn(character_name, self.user_manager.users[username]['characters'])

    @patch('user_management.maskpass.askpass', create=True)
    def test_delete_character_character_not_found(self, mock_askpass):
        mock_askpass.side_effect = ['']
        username = "Mint"
        character_name = "Test_Not_Found"
        self.user_manager.delete_character(username)
        self.assertNotIn(character_name, self.user_manager.users[username]['characters'])

