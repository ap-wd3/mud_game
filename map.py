import sys


class Map:
    def __init__(self, height, width, player_x, player_y, paths):
        self.height = height
        self.width = width
        self.x = player_x
        self.y = player_y
        self.paths = paths

    def move(self, direction):
        new_x, new_y = self.x, self.y

        if direction == "n":
            new_y -= 1
            if new_y >= 0:
                # Check if moving from the second row to the first row
                if self.y == 1 and new_y == 0:
                    new_x -= 1  # Decrease x when moving north from second to first row
                # Check if moving from the third row to the first row
                if self.y == 2 and new_y == 1:
                    new_x += 1

                if new_x >= 0 and ((new_x, new_y), (self.x, self.y)) in self.paths:
                    self.x, self.y = new_x, new_y
                    print(f"Current position of [u]: X={self.x}, Y={self.y}")
                else:
                    print("Cannot go north")
            else:
                print("Out of bound, cannot go north")

        elif direction == "s":
            new_y += 1
            if new_y < self.height:
                # Check if moving from the first row to the second row
                if self.y == 0 and new_y == 1:
                    new_x += 1  # Increase x when moving south from first to second row

                # Check if moving from the second row to the third row
                if self.y == 1 and new_y == 2:
                    new_x -= 1  # Decrease x when moving south from second to third row

                if new_x < self.width and ((self.x, self.y), (new_x, new_y)) in self.paths:
                    self.x, self.y = new_x, new_y
                    print(f"Current position of [u]: X={self.x}, Y={self.y}")
                else:
                    print("Cannot go south")
            else:
                print("Out of bound, cannot go south")

        elif direction == "e":
            new_x += 1
            # Check for a horizontal path to the right
            if new_x < self.width and ((self.x, self.y), (new_x, self.y)) in self.paths:
                self.x = new_x
                print(f"Current position of [u]: X={self.x}, Y={self.y}")
            else:
                  print("Out of bound, cannot go east")

        elif direction == "w":
            new_x -= 1
            # Check for a horizontal path to the left
            if new_x >= 0 and ((new_x, self.y), (self.x, self.y)) in self.paths:
                self.x = new_x
                print(f"Current position of [u]: X={self.x}, Y={self.y}")
            else:
                print("Out of bound, cannot go west")

    def print_map(self):
        for y in range(self.height):
            # Adding an initial offset for the first and third rows
            if y in [0, 2]:
                sys.stdout.write("    ")

            for x in range(self.width):
                # Print rooms in each row
                if y != 1 and x < 4:  # First and third rows have 4 rooms
                    if self.x == x and self.y == y:
                        sys.stdout.write("[u]")  # Player's position
                    else:
                        sys.stdout.write("[ ]")  # Other rooms
                    # Horizontal paths for these rows
                    sys.stdout.write("-" if x < 3 else " ")

                elif y == 1 and x < 6:  # Second row has 6 rooms
                    if self.x == x and self.y == y:
                        sys.stdout.write("[u]")  # Player's position
                    else:
                        sys.stdout.write("[ ]")  # Other rooms
                    # Horizontal paths for this row
                    sys.stdout.write("-" if x < 5 else " ")

            sys.stdout.write("\n")  # New line after each row of rooms

            # Print vertical paths only between the first and second rows, and the second and third rows
            if y == 0 or y == 1:
                # Offset for alignment under the second row
                sys.stdout.write("     ")
                for x in range(1, 5):  # Four vertical paths
                    sys.stdout.write("|   ")
                sys.stdout.write("\n")


paths = [
    # Horizontal paths
    ((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)),  # First row
    ((0, 1), (1, 1)), ((1, 1), (2, 1)), ((2, 1), (3, 1)
                                         ), ((3, 1), (4, 1)), ((4, 1), (5, 1)),  # Second row
    ((0, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (3, 2)),  # Third row

    # Vertical paths
    ((1, 1), (0, 0)), ((2, 1), (1, 0)), ((3, 1), (2, 0)), ((
        4, 1), (3, 0)),  # Northward paths (second to first row
    ((0, 0), (1, 1)), ((1, 0), (2, 1)), ((2, 0), (3, 1)), ((
        3, 0), (4, 1)),  # Southward paths (first to second row
    ((0, 2), (1, 1)), ((1, 2), (2, 1)), ((2, 2), (3, 1)), ((
        3, 2), (4, 1)),  # Northward paths (third to second row
    ((1, 1), (0, 2)), ((2, 1), (1, 2)), ((3, 1), (2, 2)), ((
        4, 1), (3, 2)),  # Southward paths (second to third row
]
