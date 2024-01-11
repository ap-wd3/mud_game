import unittest
from unittest.mock import patch
from user_management import UserManager  # Replace with your actual import
import os

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager('users.json')  # Use a separate file for testing

    @patch('maskpass.askpass')
    def test_create_user_success_and_failure(self, mock_askpass):
        mock_askpass.return_value = '123456'
        result_success = self.user_manager.create_user('newuser', 'password123', 'newuser@example.com')
        self.assertEqual(result_success, "User created successfully.")
        result_failure = self.user_manager.create_user('newuser', 'password123', 'existinguser@example.com')
        self.assertEqual(result_failure, None)


if __name__ == '__main__':
    unittest.main()
