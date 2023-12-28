import unittest
from game_system import GameSystem
from character import Character
from user_management import UserManager



class MockCharacter:

    pass

class MockUtils:
    @staticmethod
    def load_data(file):

        return {
            'test_user': {
                'password': 'password123',
                'email': 'test@example.com',
                'characters': []
            }
        }

    @staticmethod
    def save_data(data, file):
        print("Mock save_data called with data:", data)

class TestGameSystem(unittest.TestCase):

    def setUp(self):
        # Initialize GameSystem with mocks
        self.game_system = GameSystem()
        self.game_system.user_manager = UserManager()
        self.game_system.user_manager.users = MockUtils.load_data(None)

    def test_create_user(self):
        # Test the create_user method
        result = self.game_system.create_user("test_user", "password123", "test@example.com")
        self.assertEqual(result, "User created successfully.")
        self.assertIn("test_user", self.game_system.user_manager.users)

    def test_login(self):
        # Test the login method
        self.game_system.create_user("test_user", "password123", "test@example.com")
        result = self.game_system.login("test_user", "password123")
        self.assertEqual(result, "Logged in successfully.")

    def test_reset_password(self):
        # Test the reset_password method
        self.game_system.create_user("test_user", "password123", "test@example.com")
        result = self.game_system.reset_password("test_user", "test@example.com", "newpassword")
        self.assertEqual(result, "Password reset successfully.")

    def test_create_character(self):
        # Test the create_character method
        self.game_system.login("test_user", "password123")
        result = self.game_system.create_character("test_user", "hero", "short", "black", "blue")
        self.assertTrue("Character 'hero' created successfully." in result)



if __name__ == '__main__':
    unittest.main()
