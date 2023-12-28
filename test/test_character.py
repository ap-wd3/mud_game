import unittest
from character import Character

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.character = Character("Alice", "Long", "Brown", "Blue")

    def test_view_character(self):
        expected_output = "Name: Alice, Hair Length: Long, Hair Color: Brown,Eye Color: Blue,bonus: 0"
        self.assertEqual(self.character.view_character(), expected_output)

    def test_to_dict(self):
        expected_dict = {
            'name': 'Alice',
            'hair_length': 'Long',
            'hair_color': 'Brown',
            'eye_color': 'Blue',
            'bonus': 0
        }
        self.assertEqual(self.character.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()
