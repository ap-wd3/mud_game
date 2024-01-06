import unittest
from unittest.mock import patch, MagicMock
import user_management

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.user_manager = user_management.UserManager()

    @patch('user_management.utils.load_data', MagicMock(return_value={}))
    @patch('user_management.maskpass.askpass', MagicMock(return_value=''))
    def test_create_user_new_user(self):
        result = self.user_manager.create_user('testuser3', 'password123', 'newuser@example.com')
        self.assertEqual(result, "User created successfully.")
        self.assertIn('testuser3', self.user_manager.users)

    @patch('user_management.utils.save_data')
    def test_save_users(self, mock_save_data):
        self.user_manager.save_users()
        mock_save_data.assert_called_once()

class TestSaveLoad(unittest.TestCase):

    @patch('save_load.UserManager')
    @patch('save_load.utils')
    def setUp(self, mock_utils, mock_user_manager):
        mock_utils.load_data.return_value = {'testuser': {'characters': [{'name': 'NewName'}]}}
        self.save_load = user_management.SaveLoad()

    @patch('save_load.UserManager')
    @patch('save_load.utils')
    def test_save_game_user_not_found(self):
        result = self.save_load.save_game('testuser', 'NewName', 'Room', [], 100, {})
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
