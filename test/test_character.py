import unittest
from character import Character
from unittest.mock import patch, MagicMock
from user_management import UserManager

class TestCharacter(unittest.TestCase):

    @patch('user_management.UserManager')
    @patch('display.Display')
    def setUp(self, MockDisplay, MockUserManager):
        self.mock_user_manager = MockUserManager.return_value
        self.mock_display = MockDisplay.return_value
        self.character = Character("TestName", "Long", "Red", "Blue")


    @patch('user_management.maskpass.askpass', MagicMock(return_value=''))
    def test_create_character_new(self):
        self.mock_user_manager.users.get.return_value = {'characters': []}

        result = self.character.create_character('testuser', 'NewName3', 'Long', 'Red', 'Blue')
        self.assertIn("Character created successfully", result)

    @patch('character.maskpass')
    def test_delete_character(self, mock_maskpass):

        self.mock_user_manager.users.get.return_value = {'characters': [{'name': 'TestName'}]}
        mock_maskpass.askpass.return_value = '1'
        self.character.delete_character('testuser')

        self.assertEqual(len(self.mock_user_manager.users.get.return_value['characters']), 1)
    def test_to_dict(self):
        character_dict = self.character.to_dict()
        expected_dict = {
            'name': "TestName",
            'hair_length': "Long",
            'hair_color': "Red",
            'eye_color': "Blue"
        }
        self.assertEqual(character_dict, expected_dict)



if __name__ == '__main__':
    unittest.main()
