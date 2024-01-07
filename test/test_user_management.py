import unittest
from unittest.mock import patch
from user_management import UserManager

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager('users.json')

    @patch('maskpass.askpass')
    def test_create_user_success(self, mock_askpass):
        mock_askpass.return_value = '123456'
        result = self.user_manager.create_user('newuser', 'password123', 'newuser@example.com')
        self.assertEqual(result, "User created successfully.")

    @patch('maskpass.askpass')
    def test_create_user_failure(self, mock_askpass):
        mock_askpass.return_value = '123456'
        self.user_manager.create_user('newuser', 'password123', 'existinguser@example.com')
        result = self.user_manager.create_user('newuser', 'password123', 'existinguser@example.com')
        self.assertEqual(result, None )

if __name__ == '__main__':
    unittest.main()
