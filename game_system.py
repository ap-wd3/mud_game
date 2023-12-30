from character import Character
from user_management import UserManager
import platform
from map import Map, paths
import os
import json
from rich import print
from rich.style import Style
from rich.console import Console


def clear():
    if platform == 'windows':
        os.system("cls")
    else:
        os.system("clear")

def draw():
    print("[aquamarine3]++------------------------++[/]")

class GameSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.logged_in_user = None
        self.console = Console()

    def colored_input(self, prompt,color="green"):
        self.console.print(prompt, style=color, end="")
        user_input = input()
        return user_input
    def login(self, username, password):
        if self.user_manager.verify_user(username, password):
            self.logged_in_user = username
            return "Logged in successfully."

        else:
            print("[deep_pink2]Error: Incorrect username or password.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")


    def create_character(self, username, name, hair_length, hair_color, eye_color):
        if not self.logged_in_user:
            print("[deep_pink2]Error: You must be logged in to create a character.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        if username != self.logged_in_user:
            print("[deep_pink2]Error: You can only create characters for your logged-in account.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

        user_data = self.user_manager.users.get(username)

        if any(char['name'] == name for char in user_data['characters']):
            print("[deep_pink2]Error: Character name already exists.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

        new_character = Character(name, hair_length, hair_color, eye_color)
        user_data['characters'].append(new_character.to_dict())
        self.user_manager.save_users()
        return f"Character '{name}' has {hair_length} and {hair_color} hair, and her eyes are {eye_color}"


    def save_game(self, username, name, current_room, inventory, confidence, rooms):
        # Check if the user exists
        if username not in self.user_manager.users:
            print("[deep_pink2]Error: User not found.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return

        user_data = self.user_manager.users[username]

        # Check for 'game_state' and 'characters' keys in user_data
        if 'characters' not in user_data:
            user_data['characters'] = []

        # Find the specific character
        character = next((char for char in user_data['characters'] if char['name'] == name), None)

        if character is None:
            print(f"[deep_pink2]Error: Character {name} not found.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
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
            print("[deep_pink2]Error: File not found or inaccessible.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def load_game(self, username):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("[deep_pink2]Error: File not found or inaccessible.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return None

        user_data = users_data.get(username, {})
        if 'characters' in user_data and user_data['characters']:
            clear()
            draw()
            print("[light_steel_blue]Select a character to play:[/]")
            for i, character in enumerate(user_data['characters'], start=1):
                print(f"{i}, {character['name']}")
            draw()
            print("or type 'BACK' to go back to main menu")
            draw()
        else:
            print("[deep_pink2]No characters available for this user.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return None

        choice = input("# ")
        if choice.lower() == 'back':
            print(choice)
            return 'back'
        elif choice.isdigit():
            choice = int(choice)
            character = user_data['characters'][choice - 1]
        else:
            print("[deep_pink2]Invalid selection.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return None

        if 'game_state' in character and character['game_state']:
            game_state = character['game_state'][-1]
            print(f"Game loaded successfully for character {character['name']}.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            current_room = game_state.get('current_room', "Default Room Name")
            inventory = game_state.get('inventory', [])
            rooms = game_state.get('rooms', {})
            return (character, current_room, inventory,rooms)
        else:
            print(f"[deep_pink2]No saved game state for character {character['name']}.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return None

    def save_score(self, name, username, bonus):
        data = []
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("[deep_pink2]File not found. A new file will be created.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        except json.JSONDecodeError:
            print("[deep_pink2]Error reading the JSON file. Starting a new leaderboard.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        except Exception as e:
            print(f"[deep_pink2]An unexpected error occurred: {e}[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

        entry_found = False
        for entry in data:
            if entry.get("Player") == username and entry.get("Character name") == name:
                entry["score"] = bonus
                entry_found = True
                break

        if not entry_found:
            data.append({"Player": username, "Character name": name, "score": bonus})
        try:
            with open("leaderboard.json", 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Score for {name} saved successfully!")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        except Exception as e:
            print(f"[deep_pink2]An error occurred while writing to the file: {e}[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def load_score(self, name, username):
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
            for entry in data:
                if entry.get("Player") == username and entry.get("Character name") == name:
                    return entry.get("score", 0)
        except FileNotFoundError:
            print("[deep_pink2]Leaderboard file not found.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        except json.JSONDecodeError:
            print("[deep_pink2]Error reading the JSON file.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        except Exception as e:
            print(f"[deep_pink2]An unexpected error occurred: {e}[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")


    def load_leaderboard(self):
        try:
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("[deep_pink2]Error: File not found or inaccessible.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return
        except json.JSONDecodeError:
            print("[deep_pink2]Error: JSON file is not properly formatted.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
            return
        except Exception as e:
            print(f"[deep_pink2]An unexpected error occurred: {e}[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")
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
            print("[deep_pink2]Error: You can only delete your own account.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

        else:
            print(f"{username} has been deleted successfully.")
            return self.user_manager.delete_account(username)

    def delete_character(self, username):
        user_data = self.user_manager.users.get(username, None)
        if user_data is None:
            print("[deep_pink2]Error: User not found.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

        if not user_data['characters']:
            print("[deep_pink2]No characters available for this user.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

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
            print("[deep_pink2]Invalid selection.[/]")
            self.colored_input("Press Enter to continue...", color="pale_green1")

        # Delete the selected character
        del user_data['characters'][choice - 1]

        # Save the updated user data
        self.user_manager.save_users()
        print(f"Character deleted successfully.")