import unittest
from unittest.mock import patch
from user_management import SaveLoad
from user_management import UserManager


class TestLoadGame(unittest.TestCase):
    def setUp(self):
        self.save_load = SaveLoad()
        self.user_manager = UserManager()


class TestLoad(TestLoadGame):
    @patch('user_management.SaveLoad.load_game', create=True)
    @patch('user_management.maskpass.askpass', create=True)
    def test_load_game(self, mock_askpass, mock_load_game):
        mock_askpass.side_effect = ['']
        mock_character = {
            "name": "test",
            "hair_length": "long",
            "hair_color": "cyan",
            "eye_color": "green",
            "game_state": [
                {
                    "current_room": "Forest Haven",
                    "inventory": [
                        "Smart Planner",
                        "Jumping Rope",
                        "Book"
                    ],
                    "confidence": 100,
                    "rooms": {
                        "Maple Sanctuary": {
                            "East": "Moonlit Timberland",
                            "Item": "Confidence Booster"
                        },
                        "Moonlit Timberland": {
                            "West": "Maple Sanctuary",
                            "North": "Maple Sanctuary",
                            "South": "Dewdrop Dell",
                            "East": "Emerald Canopy"
                        },
                        "Whispering Pines": {
                            "South": "Moonlit Timberland",
                            "East": "Pine Haven",
                            "Monster": "Diet Monster"
                        },
                        "Dewdrop Dell": {
                            "North": "Moonlit Timberland",
                            "East": "Redwood Haven",
                            "Monster": "Balance Monster"
                        },
                        "Pine Haven": {
                            "South": "Emerald Canopy",
                            "East": "Walnut Retreat",
                            "West": "Whispering Pines",
                            "Item": "Mirror"
                        },
                        "Emerald Canopy": {
                            "West": "Moonlit Timberland",
                            "North": "Pine Haven",
                            "South": "Redwood Haven",
                            "East": "Cypress Cottage",
                            "Monster": "Overthinking Monster"
                        },
                        "Redwood Haven": {
                            "West": "Dewdrop Dell",
                            "East": "Silver Birch Copse",
                            "North": "Emerald Canopy",
                            "Item": "Clock"
                        },
                        "Walnut Retreat": {
                            "West": "Pine Haven",
                            "South": "Cypress Cottage",
                            "Monster": "Insecure Monster"
                        },
                        "Cypress Cottage": {
                            "West": "Emerald Canopy",
                            "South": "Silver Birch Copse",
                            "North": "Walnut Retreat",
                            "East": "Forest Haven",
                            "Monster": "Glass Ceiling Monster"
                        },
                        "Silver Birch Copse": {
                            "West": "Redwood Haven",
                            "North": "Cypress Cottage",
                            "Monster": "Harassment Monster"
                        },
                        "Forest Haven": {
                            "West": "Cypress Cottage"
                        },
                        "Mystic Moss Grove": {
                            "West": "Silver Birch Copse",
                            "North": "Forest Haven",
                            "Item": "Pizza"
                        },
                        "Enchanted Thicket": {
                            "West": "Walnut Retreat",
                            "South": "Forest Haven",
                            "Item": "Key"
                        },
                        "Sunbeam Glade": {
                            "West": "Forest Haven"
                        }
                    }
                }
            ]
            }
        game_state = mock_character['game_state'][0]
        # Mock the load_game method to return the mock character data
        mock_load_game.return_value = (mock_character,)

        username = "Mint"

        loaded_character = self.save_load.load_game(username)[-1]
        self.assertEqual(loaded_character['game_state'][-1], game_state)
