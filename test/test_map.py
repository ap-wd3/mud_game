import unittest
from map import Map,paths

class TestMap(unittest.TestCase):

    def setUp(self):
        self.paths =  paths
        self.map = Map(3, 6, 1, 1, self.paths)

    def test_initialization(self):
        self.assertEqual(self.map.height, 3)
        self.assertEqual(self.map.width, 6)
        self.assertEqual(self.map.x, 1)
        self.assertEqual(self.map.y, 1)

    def test_move_north_valid(self):
        self.map.move("north")
        self.assertEqual(self.map.x, 0)
        self.assertEqual(self.map.y, 0)

    def test_move_north_invalid(self):
        self.map.move("north")
        self.map.move("north")  # Move north again, should be invalid
        self.assertEqual(self.map.x, 0)
        self.assertEqual(self.map.y, 0)  # Position should not change

    def test_move_south_valid(self):
        self.map.move("south")
        self.assertEqual(self.map.x, 2)
        self.assertEqual(self.map.y, 1)

    def test_move_south_invalid(self):
        self.map.move("south")
        self.map.move("south")  # Move south again, should be invalid
        self.assertEqual(self.map.x, 2)
        self.assertEqual(self.map.y, 1)  # Position should not change

    def test_move_east_valid(self):
        self.map.move("east")
        self.assertEqual(self.map.x, 2)
        self.assertEqual(self.map.y, 1)

    def test_move_east_invalid(self):
        # Assuming 6 is the width boundary
        for _ in range(6):
            self.map.move("east")
        self.map.move("east")  # Move east again, should be invalid
        self.assertNotEqual(self.map.x, 7)  # Position should not exceed boundary

    def test_move_west_valid(self):
        self.map.move("west")
        self.assertEqual(self.map.x, 0)
        self.assertEqual(self.map.y, 1)

    def test_move_west_invalid(self):
        self.map.move("west")
        self.map.move("west")  # Move west again, should be invalid
        self.assertEqual(self.map.x, 0)  # Position should not change


if __name__ == '__main__':
    unittest.main()
