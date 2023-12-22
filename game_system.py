from character import Character
from user_management import UserManager
# from room import Room
# from monster import Monster
# from player import Player
import json
class GameSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.logged_in_user = None
        # self.player = Player()
        # self.rooms = {}
        # self.create_world()


    def create_user(self, username, password, email):
        return self.user_manager.create_user(username, password, email)

    def login(self, username, password):
        if self.user_manager.verify_user(username, password):
            self.logged_in_user = username
            return "Logged in successfully."
        return "Error: Incorrect username or password."

    def reset_password(self, username, email, new_password):
        return self.user_manager.reset_password(username, email, new_password)

    def create_character(self, username, name, hair_length, hair_color, eye_color):
        if not self.logged_in_user:
            return "Error: You must be logged in to create a character."
        if username != self.logged_in_user:
            return "Error: You can only create characters for your logged-in account."

        user_data = self.user_manager.users.get(username)
        name_exists = False
        for char in user_data['characters']:
            if char['name'] == name:
                name_exists = True
                break
        if name_exists:
            print("Error: Character name already exists.")

        new_character = Character(name, hair_length, hair_color, eye_color)
        user_data['characters'].append(new_character.to_dict())
        self.user_manager.save_users()
        return f"Character '{name}' created successfully. This character has {hair_length} {hair_color} hair and {eye_color} eyes."

    def logout(self):
        self.logged_in_user = None
        return "Logged out successfully."

    def create_world(self):
        west_room = Room("West", "A room full of childhood memories.")
        self.rooms = {"West": west_room}
        self.player.current_room = self.rooms['West']


        parents = Monster("Parents",
                          "What toy do you want? 1: Barbie Doll, 2: Toy Gun",
                          "Toy Gun Dressed in Pink")
        west_room.set_monster(parents)

        # Create the items in the upper room
        upper_room = Room("Upper Room", "A small, hidden room.")
        upper_room.add_item("Toy Gun Dressed in Pink")
        upper_room.add_item("Barbie Doll with Filthy Face")
        west_room.set_exit("up", upper_room)
    def move_player(self, direction):
        if self.player.move(direction):
            return f"You moved to the {self.player.current_room.name}."
        return "You can't go that way."

    def save_game(self,username):

        if username not in self.user_manager.users:
            print("Error: User not found.")
            return


        self.user_manager.users[username]['game_state'] = {
            'current_room': self.player.current_room.name,
            'confidence': self.player.confidence,
            'inventory': self.player.inventory
        }


        with open('users.json', 'w') as file:
            json.dump(self.user_manager.users, file, indent=4)

        print("Game saved successfully.")