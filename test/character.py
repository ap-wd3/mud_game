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
        characters = user_data.get('characters', [])
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


    def to_dict(self):
        return {
            'name': self.name,
            'hair_length': self.hair_length,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color
        }

