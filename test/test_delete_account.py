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


class TestDeleteA(TestDeleteAccount):
    @patch('user_management.maskpass.askpass', create=True)
    def test_delete_account_username_found(self, mock_askpass):
        username = "test"
        mock_askpass.side_effect = ['']
        self.user_manager.delete_account(username)
        self.assertNotIn(username, self.user_manager.users)

    @patch('user_management.maskpass.askpass', create=True)
    def test_delete_account_username_not_found(self, mock_askpass):
        username = "Test_Not_Found"
        mock_askpass.side_effect = ['']
        self.user_manager.delete_account(username)
        self.assertNotIn(username, self.user_manager.users)
