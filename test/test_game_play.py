import unittest
from unittest.mock import patch, MagicMock
from game_play import GamePlay


class TestGamePlay(unittest.TestCase):
    def setUp(self):
        self.game = GamePlay()
        # Set up necessary initial state
        self.game.current_room = 'Moonlit Timberland'
        self.game.room_info = {
    'Maple Sanctuary': {'East': 'Moonlit Timberland', 'Item': 'Confidence Booster'},
    'Moonlit Timberland': {'West': 'Maple Sanctuary', 'North': 'Maple Sanctuary', 'South': 'Dewdrop Dell',
                           'East': 'Emerald Canopy',  'Item': 'Smart Planner'},
    'Whispering Pines': {'South': 'Moonlit Timberland', 'East': 'Pine Haven', 'Monster': 'Diet Monster'},
    'Dewdrop Dell': {'North': 'Moonlit Timberland', 'East': 'Redwood Haven', 'Monster': 'Balance Monster'},
    'Pine Haven': {'South': 'Emerald Canopy', 'East': 'Walnut Retreat', 'West': 'Whispering Pines',
                   'Item': 'Mirror'},
    'Emerald Canopy': {'West': 'Moonlit Timberland', 'North': 'Pine Haven', 'South': 'Redwood Haven',
                       'East': 'Cypress Cottage', 'Monster': 'Overthinking Monster'},
    'Redwood Haven': {'West': 'Dewdrop Dell', 'East': 'Silver Birch Copse', 'North': 'Emerald Canopy',
                      'Item': 'Clock'},
    'Walnut Retreat': {'West': 'Pine Haven', 'South': 'Cypress Cottage', 'Monster': 'Insecure Monster'},
    'Cypress Cottage': {'West': 'Emerald Canopy', 'South': 'Silver Birch Copse', 'North': 'Walnut Retreat',
                        'East': 'Forest Haven', 'Monster': 'Glass Ceiling Monster'},
    'Silver Birch Copse': {'West': 'Redwood Haven', 'North': 'Cypress Cottage', 'Monster': 'Harassment Monster'},
    'Forest Haven': {'West': 'Cypress Cottage', 'Item': 'Book'},
    'Mystic Moss Grove': {'West': 'Silver Birch Copse', 'North': 'Forest Haven', 'Item': 'Pizza'},
    'Enchanted Thicket': {'West': 'Walnut Retreat', 'South': 'Forest Haven', 'Item': 'Key'},
    'Sunbeam Glade': {'West': 'Forest Haven', 'Item': 'Jumping Rope'},
 }
        self.game.inventory = []
        self.game.map = MagicMock()
        self.game.display = MagicMock()
        self.game.character_name = ''
        self.game.menu2 = False
        self.game.user_manager = MagicMock()
        self.game.user_manager.users.get.return_value = {'characters': []}
        self.game.username = 'newuser'

    def test_get_valid_item(self):
        with patch('builtins.print'), patch('maskpass.askpass', return_value=None):
            self.game.process_command(["get", "Smart Planner"])
            self.assertIn('Smart Planner', self.game.inventory)

    def test_get_invalid_item(self):
        with patch('builtins.print'), patch('maskpass.askpass', return_value=None):
            self.game.process_command(["get", "Nonexistent Item"])
            self.assertNotIn('Nonexistent Item', self.game.inventory)

    def test_look_at_monster(self):
        self.game.room_info['Monster'] = 'Balance Monster'
        monsters = {
            'TestMonster': MagicMock(name='Balance Monster', description='Scary monster', hint='Use silver', health=100,
                                     attack=20, loot='gold', items_required='sword')}
        with patch('builtins.print'), patch('maskpass.askpass', return_value=None), patch('time.sleep',
                                                                                          return_value=None), patch.dict(
                monsters, monsters, clear=True):
            self.game.process_command(["look"])
            self.game.display.clear_screen.assert_called()
            self.game.display.print_ascii_art.assert_called()
            self.game.display.print_monster_info.assert_called_with('Balance Monster', 100, 20, 'Equality', ['Smart Planner', 'Clock'])

    def test_look_without_monster(self):
        self.game.current_room = 'Maple Sanctuary'
        with patch('builtins.print') as mock_print, patch('maskpass.askpass', return_value=None):
            self.game.process_command(["look"])

    def test_attack_monster(self):
        self.game.room_info['Monster'] = 'Balance Monster'
        with patch('builtins.print') as mock_print, patch('maskpass.askpass', return_value=None):
            self.game.process_command(["attack"])

    @patch('maskpass.askpass', return_value=' ')
    @patch('utils.save_data')
    def test_handle_new_game(self, mock_save_data, mock_askpass):
        self.game.display.colored_input.side_effect = ['NewName', 'Long', '1', '2']
        self.game.handle_new_game()

if __name__ == '__main__':
    unittest.main()