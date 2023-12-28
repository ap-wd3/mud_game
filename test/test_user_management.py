import unittest
from user_management import UserManager

# Mock version of the utils module
class MockUtils:
    data = {}

    @staticmethod
    def load_data(_):
        return MockUtils.data

    @staticmethod
    def save_data(data, _):
        MockUtils.data = data

class TestUserManager(unittest.TestCase):

    def setUp(self):
        # Use the mock utility class for tests
        self.user_manager = UserManager()
        self.user_manager.users = MockUtils.load_data(None)

    def test_create_user(self):
        # Testing user creation
        result = self.user_manager.create_user("testuser", "password123", "test@example.com")
        self.assertEqual(result, "User created successfully.")
        self.assertIn("testuser", self.user_manager.users)

    def test_verify_user(self):
        # Testing user verification
        self.user_manager.create_user("testuser", "password123", "test@example.com")
        self.assertTrue(self.user_manager.verify_user("testuser", "password123"))
        self.assertFalse(self.user_manager.verify_user("testuser", "wrongpassword"))

    def test_reset_password(self):
        # Testing password reset
        self.user_manager.create_user("testuser", "password123", "test@example.com")
        result = self.user_manager.reset_password("testuser", "test@example.com", "newpassword")
        self.assertEqual(result, "Password reset successfully.")
        self.assertTrue(self.user_manager.verify_user("testuser", "newpassword"))

    def test_delete_account(self):
        # Testing account deletion
        self.user_manager.create_user("testuser", "password123", "test@example.com")
        result = self.user_manager.delete_account("testuser")
        self.assertEqual(result, "Account deleted successfully.")
        self.assertNotIn("testuser", self.user_manager.users)



if __name__ == '__main__':
    unittest.main()
