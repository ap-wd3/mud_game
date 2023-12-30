import os
import platform
from map import Map, paths, rooms
from game_system import GameSystem
from monster import monsters
from user_management import UserManager
from rich import print
from rich.style import Style
from rich.console import Console


class GamePlay:
    def __init__(self):
        self.run = True
        self.menu1 = True
        self.menu2 = False
        self.play = False
        self.rules = False
        self.map = Map(3, 6, 0, 1, paths)
        self.current_room = "Maple Sanctuary"
        self.inventory = []
        self.confidence = 100
        self.bonus = 0
        self.game_system = GameSystem()
        self.username = ""
        self.character_name = ""
        self.room_info = rooms.get(self.current_room, {})
        self.message = ""
        self.rooms = rooms
        self.user_manager = UserManager()
        self.console = Console()
        self.instruction = f"Welcome to the wood, [green]{self.character_name}[/]!\n" \
                           f"Our wood is under attack by monsters\n" \
                           f"Each [salmon1]monster[/] can be defeated by [pink3]specific item(s)[/]\n" \
                           f"Please find those items and [red]defeat all monsters[/] to bring peace back to the wood...\n"
        self.keyCommand = f"[cyan1]COMMAND                             DESCRIPTIONS[/]\n" \
                          f"Go <East/West/North/South>----------Move between areas\n" \
                          f"Get <item>--------------------------Pick up the item\n" \
                          f"Look--------------------------------See monster's details including hints\n" \
                          f"Attack------------------------------Attack the monster\n" \
                          f"Help--------------------------------See game's rules and command\n" \
                          f"Quit--------------------------------Save and Exit the game\n"
        self.book_path = 'resource/book.txt'

    def colored_input(self, prompt, color="green"):
        self.console.print(prompt, style=color, end="")
        user_input = input()
        return user_input

    def clear_screen(self):
        if platform.system() == 'Windows':
            os.system("cls")
        else:
            os.system("clear")

    def draw_separator(self):
        print("[aquamarine3]++------------------------++[/]")

    def print_colorized_ascii_art(self, file_path, hair_color,  eye_color):
        with open(file_path, 'r') as file:
            ascii_art = file.read()
            ascii_art = ascii_art.replace('@', f'[{hair_color}]@[/{hair_color}]')
            ascii_art = ascii_art.replace('0', f'[{eye_color}]0[/{eye_color}]')
            print(ascii_art)

    def print_ascii_items(self, file_path):
        with open(file_path, 'r') as file:
            ascii = file.read()

            # Replace each character with a unique placeholder
            placeholders = {
                '0': '<0>',
                'A': '<A>',
                'H': '<H>',
                '|': '<|>',
                '/': '</>',
                '-': '<->',
                '▆': '<▆>',
                'U': '<U>',
                '█': '<█>',
                '#': '<#>',
                '▄': '<▄>',
                'W': '<W>',
                'V': '<V>',
            }

            for char, placeholder in placeholders.items():
                ascii = ascii.replace(char, placeholder)

            # Replace placeholders with formatted strings
            formatted_strings = {
                '<0>': '[bright_white]0[/]',
                '<A>': '[cyan1]A[/]',
                '<H>': '[gold3]H[/gold3]',
                '<|>': '[red]|[/red]',
                '</>': '[red]/[/red]',
                '<->': '[red]-[/red]',
                '<▆>': '[bright_white]▆[/bright_white]',
                '<U>': '[yellow]U[/yellow]',
                '<█>': '[black]█[/black]',
                '<#>': '[grey50]#[/grey50]',
                '<▄>': '[green]▄[/green]',
                '<W>': '[light_pink4]W[/light_pink4]',
                '<V>': '[orange3]V[/orange3]',
            }

            for placeholder, formatted in formatted_strings.items():
                ascii = ascii.replace(placeholder, formatted)

            return ascii

    def print_ascii_monsters(self, file_path):
        with open(file_path, 'r') as file:
            ascii = file.read()
            ascii = ascii.replace('i', f'[light_slate_blue]i[/]')
            ascii = ascii.replace('@', f'[pink1]@[/]')
            ascii = ascii.replace('D', f'[pale_turquoise1]D[/]')
            return ascii

    def main_menu(self):
        self.clear_screen()
        self.draw_separator()
        print("1, [thistle3]LOGIN[/]\n"
              "2, [thistle3]NEW REGISTRATION[/]\n"
              "3, [thistle3]RESET PASSWORD[/]\n"
              "4, [thistle3]QUIT[/]")
        self.draw_separator()
        choice = self.colored_input("# ", color="sandy_brown")
        if choice == "1":
            self.handle_login()
        elif choice == "2":
            self.handle_registration()
        elif choice == "3":
            self.handle_password_reset()
        elif choice == "4":
            self.handle_quit_menu1()
        else:
            print("[deep_pink2]Invalid Input[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def handle_login(self):
        username = self.colored_input("Enter your username: ", color="light_steel_blue")
        password = self.colored_input("Enter your password: ", color="light_steel_blue")
        self.draw_separator()
        result = self.game_system.login(username, password)
        if result == 'Logged in successfully.':
            print(f'[slate_blue3]{result}[/]')
            self.colored_input("Press Enter to continue...", color="pale_green1")
            self.username = username
            self.menu1 = False
            self.menu2 = True
        else:
            self.menu1 = True
            self.menu2 = False

    def handle_registration(self):
        self.clear_screen()
        self.draw_separator()
        print("Create new account or type 'back' to go back to main menu.")
        self.draw_separator()
        username = self.colored_input("Choose your username: ", color="light_steel_blue")
        if username.lower() == "back":
            self.menu1 = True
            self.menu2 = False
        else:
            password = self.colored_input("Choose your password: ", color="light_steel_blue")
            if password.lower() == "back":
                self.menu1 = True
                self.menu2 = False
            else:
                if password.lower() == "back":
                    self.menu1 = True
                    self.menu2 = False
                else:
                    email = self.colored_input("Enter your email address: ", color="light_steel_blue")
                    self.user_manager.create_user(username, password, email)

    def handle_password_reset(self):
        username = self.colored_input("Enter your username: ", color="light_steel_blue")
        email = self.colored_input("Enter your email address for password reset:  ", color="light_steel_blue")
        new_password = self.colored_input("Enter your new password: ", color="light_steel_blue")
        self.user_manager.reset_password(username, email, new_password)

    def handle_quit_menu1(self):
        exit(0)

    def secondary_menu(self):
        self.clear_screen()
        self.draw_separator()
        print("1, [thistle3]NEW GAME[/]\n"
              "2, [thistle3]LOAD GAME[/]\n"
              "3, [thistle3]LEADERBOARD[/]\n"
              "4, [thistle3]RULES[/]\n"
              "5, [thistle3]DELETE ACCOUNT[/]\n"
              "6, [thistle3]DELETE CHARACTERS[/]\n"
              "7, [thistle3]QUIT GAME[/]")
        self.draw_separator()
        print("or type 'BACK' to go back to main menu")
        self.draw_separator()
        choice = self.colored_input("# ", color="sandy_brown")
        if choice == "1":
            self.handle_new_game()
        elif choice == "2":
            self.handle_load_game()
        elif choice == "3":
            self.handle_leaderboard()
        elif choice == "4":
            self.handle_rules()
        elif choice == "5":
            self.handle_delete_account()
        elif choice == "6":
            self.handle_delete_character()
        elif choice == "7":
            self.handle_quit()
        elif choice.lower() == "back":
            self.menu2 = False
            self.menu1 = True
        else:
            print("[deep_pink2]Invalid Input[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def handle_new_game(self):
        self.clear_screen()

        logged_in_username = self.username
        while True:
            self.draw_separator()
            print("Create the new character or type 'BACK' to go back to the menu")
            self.draw_separator()
            name = input("Enter your character's name: ").strip()
            if name.lower() == "back":
                self.menu2 = True
                return
            self.character_name = name
            user_data = self.game_system.user_manager.users.get(self.username, {'characters': []})
            if any(char['name'] == name for char in user_data['characters']):
                print("[deep_pink2]Error: Character name already exists. Please choose a different name.[/]")
                self.colored_input("Press Enter to continue...", color="pale_green1")
            else:
                break

        while True:
            hair_length = input("Choose hair length (Long/Short): ").strip().lower()
            if hair_length.lower() == "back":
                self.menu2 = True
                return
            elif hair_length not in ["short", "long"]:
                print("[deep_pink2]Invalid hair length, please choose again.[/]")
                self.colored_input("Press Enter to continue...", color="pale_green1")
            else:
                break

        hair_color = 'Unknown'
        while hair_color == 'Unknown':
            print("Choose hair color:")
            print("1: Cyan")
            print("2: Red")
            print("3: Yellow")
            color_options = {'1': 'cyan', '2': 'red', '3': 'yellow'}
            hair_color_choice = input("Select option (1, 2, or 3): ").strip()
            hair_color = color_options.get(hair_color_choice, "Unknown")
            if hair_color_choice.lower() == "back":
                self.menu2 = True
                return
            elif hair_color == 'Unknown':
                print("[deep_pink2]Invalid option, please choose again.[/]")
                self.colored_input("Press Enter to continue...", color="pale_green1")

        eye_color = 'Unknown'
        while eye_color == 'Unknown':
            print("Choose eye color:")
            print("1: Blue")
            print("2: Green")
            print("3: Red")
            color_options = {'1': 'blue', '2': 'green', '3': 'red'}
            eye_color_choice = input("Select option (1, 2, or 3): ").strip()
            eye_color = color_options.get(eye_color_choice, "Unknown")
            if eye_color_choice.lower() == "back":
                self.menu2 = True
                return
            elif eye_color == 'Unknown':
                print("Invalid option, please choose again.")
                self.colored_input("Press Enter to continue...", color="pale_green1")
        result = self.game_system.create_character(self.username, name, hair_length, hair_color, eye_color)
        short_hair_file_path = 'resource/short_hair.txt'
        long_hair_file_path = 'resource/long_hair.txt'
        if hair_length == 'short':
            self.print_colorized_ascii_art(short_hair_file_path, hair_color, eye_color)
        elif hair_length == 'long':
            self.print_colorized_ascii_art(long_hair_file_path, hair_color, eye_color)
        print(f'[light_pink1]{result}[/]')
        self.colored_input("Press Enter to continue...", color="pale_green1")
        self.game_introduction()
        self.play = True
        self.menu2 = False

    def handle_load_game(self):
        loaded_data = self.game_system.load_game(self.username)
        if loaded_data:
            if loaded_data == 'back':
                self.play = False
                self.menu2 = True
            else:
                character, current_room, inventory, rooms = loaded_data
                self.character_name = character['name']
                # print(self.character_name)
                # input("Press enter to continue...")
                self.current_room = current_room
                self.inventory = inventory
                self.rooms = rooms
                # Update map coordinates based on current room
                self.map.x, self.map.y = self.map.get_coordinates_from_room_name(self.current_room)
                self.play = True
                self.menu2 = False

        else:
            self.play = False
            self.menu2 = True
        loaded_score = self.game_system.load_score(self.character_name, self.username)
        if loaded_score is not None:
            self.bonus = loaded_score
        else:
            print("Error")
            self.bonus = 0

    def handle_leaderboard(self):
        self.clear_screen()
        self.draw_separator()
        self.game_system.load_leaderboard()
        self.draw_separator()
        self.colored_input("Press Enter to continue...", color="pale_green1")

    def handle_rules(self):
        print("Collect the right item(s) to defeat monsters. Find more hints by observing each monster\n")
        print(self.keyCommand)
        self.colored_input("Press Enter to continue...", color="pale_green1")

    def handle_delete_account(self):
        self.game_system.delete_account(self.username)
        input("Press 'Enter' to continue...")
        self.menu2 = False
        self.menu1 = True

    def handle_delete_character(self):
        self.game_system.delete_character(self.username)
        input("Press 'Enter' to continue...")

    def handle_quit(self):
        quit()

    def game_introduction(self):
        self.clear_screen()
        print(self.instruction)
        print(self.keyCommand)
        self.colored_input("Press Enter to continue...", color="pale_green1")

    def game_loop(self):
        while self.play and self.confidence > 0:
            self.current_room = self.map.room_map.get((self.map.x, self.map.y), "Unknown room")
            self.room_info = self.rooms.get(self.current_room, {})
            self.clear_screen()
            self.map.print_map()
            print(f"You are in the {self.current_room}\nInventory : {self.inventory}\n{'-' * 27}")
            print("Hint: You can enter 'help' for command information.")
            print(f"Confidence: {self.confidence}")
            print(self.message)

            if "Monster" in self.room_info:
                encountered_monster = self.room_info['Monster']
                print(f"You encounter a {encountered_monster}!")
                if len(encountered_monster.split()) == 3:
                    print(self.print_ascii_monsters(f'resource/{encountered_monster.split()[0].lower()}{encountered_monster.split()[1].lower()}_monster.txt'))
                elif len(encountered_monster.split()) == 2:
                    print(self.print_ascii_monsters(f'resource/{encountered_monster.split()[0].lower()}_monster.txt'))
                print("Enter 'look' to see the information of the monster")
            elif "Item" in self.room_info:
                item = self.room_info["Item"]
                if item[0] in 'AEIOUaeiou':
                    print(f"You see an {self.room_info['Item']}!")

                else:
                    print(f"You see a {self.room_info['Item']}")

            else:
                print("There's nothing special here.")

            user_input = input("Enter your command: ").lower().split(' ')
            self.process_command(user_input)

    def process_command(self, user_input):
        if not user_input:
            return

        action = user_input[0]
        argument = " ".join(user_input[1:]).title() if len(user_input) > 1 else ""

        if action == "go":
            direction = argument.lower()
            result = self.map.move(direction)
            if result != "invalid input":
                self.current_room = self.map.room_map.get((self.map.x, self.map.y), "Unknown room")
                self.message = "You moved " + direction
            else:
                self.message = "[red]Invalid command. Please use 'Go <East/West/North/South'[/]"

        elif action == "get":
            item = argument
            if item:
                if len(item.split()) == 2:
                    ascii_item = self.print_ascii_items(f'resource/{item.split()[0].lower()}_{item.split()[1].lower()}.txt')
                elif len(item.split()) == 1:
                    ascii_item = self.print_ascii_items(f'resource/{item.split()[0].lower()}.txt')
            if item == self.rooms[self.current_room].get("Item", "") and item not in self.inventory:
                self.inventory.append(item)
                self.message = f"{ascii_item} \n{item} retrieved!"
                self.rooms[self.current_room].pop("Item", None)

            elif item in self.inventory:
                self.message = f"You already have {item}."
            else:
                self.message = f"{item} cannot be picked up."

        elif action == "look":
            monster_name = self.room_info.get("Monster")
            if monster_name:
                monster = monsters.get(monster_name)
                if monster:
                    print(f"Name: {monster.name}")
                    print(f"Description: {monster.description}")
                    print(f"Health: {monster.health}")
                    print(f"Attack: {monster.attack}")
                    print(f"Items Required: {', '.join(monster.items_required)}")
                    print(f"Hint: {monster.hint}")
                    input("Press 'Enter' to continue...")
                else:
                    print("There's no monster here.")
            else:
                print("Sorry, there is nothing to look at. :(")

        elif action == "quit":
            answer = input("Save and Exit game? Y/N\nYour answer: ").upper()
            if answer == "Y":
                self.game_system.save_game(self.username, self.character_name, self.current_room, self.inventory, self.confidence, self.rooms)
                print("Game Saved Successfully!")
                print("Thank you for playing The Wood, I will see you when I see you again!")
                exit(0)
            elif answer == "N":
                pass
            else:
                print("Invalid Command")

        elif action == "help":
            print(self.keyCommand)
            self.colored_input("Press Enter to continue...", color="pale_green1")

        elif action == "attack":
            monster_name = self.room_info.get("Monster")
            if monster_name:
                self.handle_monster_encounter(monster_name)
            else:
                print("There's no monster to attack here.")
                self.colored_input("Press Enter to continue...", color="pale_green1")
        else:
            print("Invalid Command")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def handle_monster_encounter(self, monster_name):
        monster = monsters.get(monster_name)
        if not monster:
            print("There's no monster here.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return

        # Check if player has required items
        has_required_items = all(item in self.inventory for item in monster.items_required)

        # Calculate damage based on the number of required items
        damage = 100 // len(monster.items_required) if has_required_items else 0

        # Adjust monster's health and player's confidence
        monster.health -= damage
        self.confidence -= 20 if not has_required_items else 0

        # Print current state and check for outcomes
        if monster.health == 0:
            print(f"{monster.name} has been defeated. You've gained {monster.loot} and {monster.bonus} points.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            self.rooms[self.current_room].pop("Monster", None)
            self.bonus += monster.bonus
            self.game_system.save_score(self.character_name, self.username, self.bonus)
        elif self.confidence == 0:
            print("Game over! Maybe next time!")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            self.game_system.save_game(self.username, self.character_name, self.current_room, self.inventory,
                                       self.confidence, self.rooms)
            exit(0)
        else:
            print(f"Monster's health: {monster.health}")
            print(f"Your confidence: {self.confidence}")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def run_game(self):
        while self.run:
            if self.menu1:
                self.main_menu()
            elif self.menu2:
                self.secondary_menu()
            elif self.play:
                self.game_loop()


if __name__ == "__main__":
    game_play = GamePlay()
    game_play.run_game()
