import unittest
from character import Character
from unittest.mock import patch, MagicMock

class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character("TestName", "Long", "Red", "Blue")

    @patch('user_management.UserManager')
    @patch('display.Display')
    @patch('user_management.maskpass.askpass', MagicMock(return_value=''))
    def test_create_character_new_existing(self, MockDisplay, MockUserManager):
        mock_user_manager = MockUserManager.return_value
        mock_user_manager.users.get.return_value = {'characters': []}
        result = self.character.create_character('newuser', 'NewName', 'Long', 'Red', 'Blue')
        self.assertEqual("Character created successfully", result)
        result_failure = self.character.create_character('newuser', 'NewName', 'Long', 'Red', 'Blue')
        self.assertEqual(None, result_failure)




if __name__ == '__main__':
    unittest.main()
