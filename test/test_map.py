import unittest
from unittest.mock import patch
from map import Map

class TestMap(unittest.TestCase):

    def setUp(self):
        self.paths = [

            # Horizontal paths
            ((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)),  # First row

            ((0, 1), (1, 1)), ((1, 1), (2, 1)), ((2, 1), (3, 1)
                                                 ), ((3, 1), (4, 1)), ((4, 1), (5, 1)),  # Second row

            ((0, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (3, 2)),  # Third row

            # Vertical paths
            ((1, 1), (0, 0)), ((2, 1), (1, 0)), ((3, 1), (2, 0)), ((
                                                                       4, 1), (3, 0)),
            # Northward paths (second to first row
            ((0, 0), (1, 1)), ((1, 0), (2, 1)), ((2, 0), (3, 1)), ((
                                                                       3, 0), (4, 1)),
            # Southward paths (first to second row
            ((0, 2), (1, 1)), ((1, 2), (2, 1)), ((2, 2), (3, 1)), ((
                                                                       3, 2), (4, 1)),
            # Northward paths (third to second row
            ((1, 1), (0, 2)), ((2, 1), (1, 2)), ((3, 1), (2, 2)), ((
                                                                       4, 1), (3, 2)),
            # Southward paths (second to third row

        ]
        self.map = Map(6, 4, 0, 0, self.paths)

    def test_initialization(self):
        self.assertEqual(self.map.height, 6)
        self.assertEqual(self.map.width, 4)
        self.assertEqual(self.map.x, 0)
        self.assertEqual(self.map.y, 0)

    def test_move_north_valid(self):
        self.map.x, self.map.y = 1, 1
        self.map.move("n")
        self.assertEqual((self.map.x, self.map.y), (0, 0))

    def test_move_north_invalid(self):
        self.map.x, self.map.y = 0, 1
        self.map.move("n")
        self.assertEqual((self.map.x, self.map.y), (0, 1))

    def test_move_south_valid(self):
        self.map.x, self.map.y = 1, 1
        self.map.move("s")
        self.assertEqual((self.map.x, self.map.y), (0, 2))
    def test_move_south_invalid(self):
        self.map.x, self.map.y = 0, 1
        self.map.move("s")
        self.assertEqual((self.map.x, self.map.y), (0, 1))

    def test_move_west_valid(self):
        self.map.x, self.map.y = 1, 1
        self.map.move("w")
        self.assertEqual((self.map.x, self.map.y), (0, 1))

    def test_move_west_invalid(self):
        self.map.x, self.map.y = 0, 1
        self.map.move("w")
        self.assertEqual((self.map.x, self.map.y), (0, 1))

    def test_move_east_valid(self):
        self.map.x, self.map.y = 0, 1
        self.map.move("e")
        self.assertEqual((self.map.x, self.map.y), (1, 1))

    def test_move_west_invalid(self):
        self.map.x, self.map.y = 5, 1
        self.map.move("e")
        self.assertEqual((self.map.x, self.map.y), (5, 1))

    def test_get_coordinates_from_room_name(self):
        coords = self.map.get_coordinates_from_room_name("Whispering Pines")
        self.assertEqual(coords, (0, 0))


if __name__ == '__main__':
    unittest.main()
