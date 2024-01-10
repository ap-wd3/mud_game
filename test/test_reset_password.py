import unittest
from unittest.mock import patch
from user_management import UserManager


class TestResetPassword(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.username = 'newuser'
        self.email = 'newuser@example.com'
        self.new_password = 'password123'


class TestInit(TestResetPassword):
    def test_init_username(self):
        self.assertIn(self.username, self.user_manager.users)

    def test_init_email(self):
        self.assertEqual(self.user_manager.users[self.username]['email'], self.email)


class TestReset(TestResetPassword):
    @patch('user_management.input', create=True)
    @patch('user_management.maskpass.askpass', create=True)
    def test_reset_password(self, mock_askpass, mock_input):
        mock_input.side_effect = [self.username, self.email]
        mock_askpass.side_effect = [self.new_password, '']
        self.user_manager.reset_password()
        self.assertEqual(self.user_manager.users[self.username]['password'], self.new_password)
