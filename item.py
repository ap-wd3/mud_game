from colorama import Fore, Style


class Item:
    def __init__(self, item_data, color_mapping):
        self.item_data = item_data
        self.color_mapping = color_mapping

    def display(self):
        for row in self.item_data:
            for char in row:
                if char == ' ':
                    # Print spaces without color formatting
                    print(char, end=' ')
                else:
                    # Print characters with specified color formatting from the mapping
                    color = self.color_mapping.get(char, Fore.WHITE)
                    print(f"{color}{char}{Style.RESET_ALL}", end=' ')
            print()


if __name__ == "__main__":
    lip_sword_data = [
        " /|",
        " ||",
        " ##",
        " ##",
        "####",
        "####"
    ]

    color_mapping = {
        '/': Fore.RED,
        '|': Fore.RED,
        '#': Fore.LIGHTYELLOW_EX,
        '=': Fore.WHITE
    }

    lipstick = Item(lip_sword_data, color_mapping)

    print("Lip Sword:")
    lipstick.display()
    print()
