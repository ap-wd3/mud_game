from colorama import Fore, Style


class Room:
    def __init__(self, map_data):
        self.map_data = map_data

    def display(self):
        for row in self.map_data:
            for char in row:
                if char == '#':
                    print(Fore.BLUE + '#' + Style.RESET_ALL, end=' ')
                elif char == '.':
                    print(Fore.WHITE + '.' + Style.RESET_ALL, end=' ')
                elif char == 'X':
                    print(Fore.RED + 'X' + Style.RESET_ALL, end=' ')
                elif char == '|':
                    print(Fore.YELLOW + '|' + Style.RESET_ALL, end=' ')
                elif char == '_':
                    print(Fore.YELLOW + '_' + Style.RESET_ALL, end=' ')
                elif char == 'O':
                    print(Fore.GREEN + 'O' + Style.RESET_ALL, end=' ')
                else:
                    print(char, end=' ')
            print()


if __name__ == "__main__":
    wood_data = [
        "     [ ]     ",
        "      |      ",
        "[X]--[ ]--[ ]--",
        "           | ",
        "          [ ]",
    ]

    boss_area_data = [
        "##########",
        "#.......X#",
        "#...##...#",
        "#...##...#",
        "#...##...#",
        "#X..##...|",
        "#_########",
    ]

    monster_area_data = [
        "##########",
        "#.......X#",
        "#........#",
        "#X.......#",
        "#....X...#",
        "#X.......|",
        "#_########",
    ]

    treasure_area_data = [
        "##########",
        "#..O.....#",
        "#.......O#",
        "#........#",
        "#X......O#",
        "#_########",
    ]

    # Create Room objects
    monster_area = Room(monster_area_data)
    treasure_area = Room(treasure_area_data)
    wood = Room(wood_data)
    boss_area = Room(boss_area_data)

    # Display Rooms
    print("Wood Map:")
    wood.display()
    print()

    print("Boss Area:")
    boss_area.display()
    print()

    print("Monster Area:")
    monster_area.display()
    print()

    print("Treasure Area:")
    treasure_area.display()
    print()