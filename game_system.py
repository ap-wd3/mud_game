from character import Character
from user_management import UserManager
import platform
from map import Map, paths
import os
# from room import Room
# from monster import Monster
# from player import Player
import json


def clear():
    if platform == 'windows':
        os.system("cls")
    else:
        os.system("clear")


def draw():
    print("++------------------------++")

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

    def create_character(self, username, name, bmi_category, hair_length, hair_color):
        if not self.logged_in_user:
            return "Error: You must be logged in to create a character."
        if username != self.logged_in_user:
            return "Error: You can only create characters for your logged-in account."

        user_data = self.user_manager.users.get(username)

        if any(char['name'] == name for char in user_data['characters']):
            return "Error: Character name already exists."

        new_character = Character(name, bmi_category, hair_length, hair_color)
        user_data['characters'].append(new_character.to_dict())
        self.user_manager.save_users()
        return f"Character '{name}' created successfully."

    def logout(self):
        self.logged_in_user = None
        return "Logged out successfully."

    def save_game(self, username, name, current_room, inventory, confidence, rooms):
        # Check if the user exists
        if username not in self.user_manager.users:
            print("Error: User not found.")
            return

        user_data = self.user_manager.users[username]

        # Check for 'game_state' and 'characters' keys in user_data
        if 'characters' not in user_data:
            user_data['characters'] = []

        # Find the specific character
        character = next((char for char in user_data['characters'] if char['name'] == name), None)

        if character is None:
            print(f"Error: Character {name} not found.")
            return

        # Replace old game state with the new game state
        new_game_state = {
            'current_room': current_room,
            'inventory': inventory,
            'confidence': confidence,
            'rooms': rooms
        }

        character['game_state'] = [new_game_state]  # Replaces old game states

        # Save to file
        try:
            with open('users.json', 'w') as file:  # Adjust file name as necessary
                json.dump(self.user_manager.users, file, indent=4)
        except IOError:
            print("Error: File not found or inaccessible.")

    def load_game(self, username):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("Error: File not found or inaccessible.")
            return None

        user_data = users_data.get(username, {})
        if 'characters' in user_data and user_data['characters']:
            clear()
            draw()
            print("Select a character to play:")
            for i, character in enumerate(user_data['characters'], start=1):
                print(f"{i}, {character['name']}")
            draw()
        else:
            print("No characters available for this user.")
            return None

        try:
            choice = int(input("# "))
            character = user_data['characters'][choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return None

        if 'game_state' in character and character['game_state']:
            game_state = character['game_state'][-1]
            print(f"Game loaded successfully for character {character['name']}.")
            # Ensure that the game state includes 'current_room' and 'inventory'
            current_room = game_state.get('current_room', "Default Room Name")
            inventory = game_state.get('inventory', [])
            rooms = game_state.get('rooms', {})
            return (character, current_room, inventory,rooms)
        else:
            print(f"No saved game state for character {character['name']}.")
            return None

    def save_score(self, name, username, bonus):
        data = []
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("File not found. A new file will be created.")
        except json.JSONDecodeError:
            print("Error reading the JSON file. Starting a new leaderboard.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        entry_found = False
        for entry in data:
            if entry.get("Player") == username and entry.get("Charactor name") == name:
                entry["score"] = bonus
                entry_found = True
                break

        if not entry_found:
            data.append({"Player": username, "Charactor name": name, "score": bonus})
        try:
            with open("leaderboard.json", 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Score for {name} saved successfully.")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    def load_score(self, name, username):
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
            for entry in data:
                if entry.get("Player") == username and entry.get("Character name") == name:
                    return entry.get("score", 0)
        except FileNotFoundError:
            print("Leaderboard file not found.")
        except json.JSONDecodeError:
            print("Error reading the JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def load_leaderboard(self):
        try:
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Error: File not found or inaccessible.")
            return
        except json.JSONDecodeError:
            print("Error: JSON file is not properly formatted.")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return
        data.sort(key=lambda x: x.get("score", 0), reverse=True)
        print("LEADERBOARD\n"
              "NAME                SCORE")
        for entry in data:
            name = entry.get("Charactor name", "Unknown")
            username = entry.get("Player", "Unknown")
            score = entry.get("score", 0)
            print(f"{name} ({username})".ljust(20)+ f"{score}")

    def delete_account(self, username):
        if self.logged_in_user != username:
            return "Error: You can only delete your own account."
        else:
            print(f"{username} has been deleted successfully.")
            return self.user_manager.delete_account(username)

    def delete_character(self, username):
        user_data = self.user_manager.users.get(username, None)
        if user_data is None:
            return "Error: User not found."

        if not user_data['characters']:
            return "No characters available for this user."

        clear()
        draw()
        print("Select a character to delete:")
        for i, character in enumerate(user_data['characters'], start=1):
            print(f"{i}, {character['name']}")
        draw()

        try:
            choice = int(input("# "))
            assert 1 <= choice <= len(user_data['characters'])
        except (ValueError, AssertionError):
            return "Invalid selection."

        # Delete the selected character
        del user_data['characters'][choice - 1]

        # Save the updated user data
        self.user_manager.save_users()
        print(f"Character deleted successfully.")