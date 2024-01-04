import maskpass
from user_management import UserManager
from rich import print
import utils
from display import Display


class Character:
    def __init__(self, name, hair_length, hair_color, eye_color):
        self.name = name
        self.hair_length = hair_length
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.user_manager = UserManager()
        self.logged_in_user = None
        self.display = Display()

    def create_character(self, username, name, hair_length, hair_color, eye_color):
        self.logged_in_user = username
        user_data = self.user_manager.users.get(username)
        if any(char['name'] == name for char in user_data['characters']):
            print("[deep_pink2](＞﹏＜)Oops: character name already exists.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        new_character = Character(name, hair_length, hair_color, eye_color)
        user_data['characters'].append(new_character.to_dict())

        if not user_data or 'characters' not in user_data:
            print("[deep_pink2](＞﹏＜)Oops, you must be logged in to create a character.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        if username != self.logged_in_user:
            print("[deep_pink2](＞﹏＜)Oops, you can only create characters for your logged-in account.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        self.user_manager.save_users()
        return f"Character '{name}' has '{hair_length}' and '{hair_color}' hair, and her eyes are '{eye_color}'"
    
    def delete_character(self, username):
        user_data = self.user_manager.users.get(username, None)
        if user_data is None:
            print("[deep_pink2](＞﹏＜)Oops, user not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        if not user_data['characters']:
            print("[deep_pink2](＞﹏＜)Oops, no characters available for this user.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return

        self.display.clear_screen()
        self.display.draw()
        print("[light_steel_blue]Select a character to delete:[/]")
        for i, character in enumerate(user_data['characters'], start=1):
            print(f"{i}, {character['name']}")
        self.display.draw()
        print("[orchid1 italic bold]💡Hints:[/]")
        print("- Type a number to select a character to delete")
        print("- Type '(B)ack' to go back to main menu")
        self.display.draw()

        choice = input("# ")
        if choice.lower() == 'back' or choice.lower() == 'b':
            return 'back'
        elif choice.isdigit():
            choice = int(choice)
            assert 1 <= choice <= len(user_data['characters'])
        else:
            print("[deep_pink2](＞﹏＜)Oops, invalid selection.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        # try:
        #     choice = int(input("# "))
        #     assert 1 <= choice <= len(user_data['characters'])
        # except (ValueError, AssertionError):
        #     print("[deep_pink2]Invalid selection.[/]")
        #     maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

        # Delete the selected character
        character_name = user_data['characters'][choice - 1]['name']
        del user_data['characters'][choice - 1]
        self.leaderboard = utils.load_data(self.user_manager.leaderboard_file)
        self.leaderboard = [entry for entry in self.leaderboard
                            if not (entry.get("Player") == username and entry.get("Character name") == character_name)]
        utils.save_data(self.leaderboard, self.user_manager.leaderboard_file)
        # Save the updated user data
        self.user_manager.save_users()
        print("[dark_slate_gray2]Character deleted successfully.[/]")
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")



    def to_dict(self):
        return {
            'name': self.name,
            'hair_length': self.hair_length,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color
        }
