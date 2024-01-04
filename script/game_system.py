from character import Character
from user_management import UserManager
import utils
import platform
from map import Map, paths
import os
import json
from rich import print
from rich.style import Style
from rich.console import Console
import maskpass


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
            print("[deep_pink2](＞﹏＜)Oops, incorrect username or password.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")


    def create_character(self, username, name, hair_length, hair_color, eye_color):
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


    def save_game(self, username, name, current_room, inventory, confidence, rooms):
        # Check if the user exists
        if username not in self.user_manager.users:
            print("[deep_pink2](＞﹏＜)Oops, user not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return

        user_data = self.user_manager.users[username]

        # Check for 'game_state' and 'characters' keys in user_data
        if 'characters' not in user_data:
            user_data['characters'] = []

        # Find the specific character
        character = next((char for char in user_data['characters'] if char['name'] == name), None)

        if character is None:
            print(f"[deep_pink2](＞﹏＜)Oops, character {name} not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
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
            print("[deep_pink2](＞﹏＜)Oops, file not found or inaccessible.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

    def load_game(self, username):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("[deep_pink2](＞﹏＜)Oops, file not found or inaccessible.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return None

        user_data = users_data.get(username, {})

        if 'characters' in user_data and user_data['characters']:
            clear()
            draw()
            print("[light_steel_blue]Select a character to play:[/]")
            for i, character in enumerate(user_data['characters'], start=1):
                print(f"{i}, {character['name']}")
            draw()
            print("[orchid1 italic bold]💡Hints:[/]")
            print("- Type a number to select a character to play")
            print("- Type '(B)ack' to go back to main menu")
            draw()
        else:
            print("[deep_pink2](＞﹏＜)Oops, no characters available for this user.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return None



        choice = input("# ")
        try:
            if choice.lower() == 'back' or choice.lower() == 'b':
                print(choice)
                return 'back'
            elif choice.isdigit():
                choice = int(choice)
                character = user_data['characters'][choice - 1]
            else:
                print("[deep_pink2](＞﹏＜)Oops, I need a [/]'back' [deep_pink2]or a number.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                return None

            if 'game_state' in character and character['game_state']:
                game_state = character['game_state'][-1]
                print(f"[dark_slate_gray2]Game loaded successfully for character '{character['name']}'.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
                current_room = game_state.get('current_room', "Default Room Name")
                inventory = game_state.get('inventory', [])
                rooms = game_state.get('rooms', {})
                confidence = game_state.get('confidence', 100)
                return (character, current_room, inventory,rooms, confidence)
            else:
                print(f"[deep_pink2]No saved game state for character {character['name']}.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                return None
        #handle index out of range error
        except IndexError:
            print("[deep_pink2](＞﹏＜)Oops, character index out of range, please try again.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

    def save_score(self, name, username, bonus):
        data = []
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("[deep_pink2](＞﹏＜)File not found. A new file will be created.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except json.JSONDecodeError:
            print("[deep_pink2](＞﹏＜)Error reading the JSON file. Starting a new leaderboard.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An unexpected error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

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
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An error occurred while writing to the file: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def load_score(self, name, username):
        try:
            with open("leaderboard.json", 'r') as file:
                data = json.load(file)
            for entry in data:
                if entry.get("Player") == username and entry.get("Character name") == name:
                    return entry.get("score", 0)
        except FileNotFoundError:
            print("[deep_pink2](＞﹏＜)Leaderboard file not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except json.JSONDecodeError:
            print("[deep_pink2](＞﹏＜)Error reading the JSON file.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An unexpected error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def load_leaderboard(self):
        try:
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("[deep_pink2](＞﹏＜)Error: File not found or inaccessible.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        except json.JSONDecodeError:
            print("[deep_pink2](＞﹏＜)Error: JSON file is not properly formatted.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        except Exception as e:
            print(f"[deep_pink2](＞﹏＜)An unexpected error occurred: {e}[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        data.sort(key=lambda x: x.get("score", 0), reverse=True)
        print("LEADERBOARD\n"
              "NAME                SCORE")
        for entry in data:
            name = entry.get("Character name", "Unknown")
            username = entry.get("Player", "Unknown")
            score = entry.get("score", 0)
            print(f"{name} ({username})".ljust(20)+ f"{score}")

    def delete_account(self, username):
        if username not in self.user_manager.users:
            print("[deep_pink2](＞﹏＜)Oops, user does not exist.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return
        else:
            print(f"[dark_slate_gray2]{username} has been deleted successfully.[/]")
            return self.user_manager.delete_account(username)
        del self.user_manager.users[username]
        self.delete_leaderboard(username)
        self.save_users()
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def delete_leaderboard(self, username):
        self.leaderboard = utils.load_data(self.user_manager.leaderboard_file)
        self.leaderboard = [entry for entry in self.leaderboard if entry.get("Player") != username]
        utils.save_data(self.leaderboard, self.user_manager.leaderboard_file)

    def save_users(self):
        utils.save_data(self.user_manager.users, self.user_manager.storage_file)

    def delete_character(self, username):
        user_data = self.user_manager.users.get(username, None)
        if user_data is None:
            print("[deep_pink2](＞﹏＜)Oops, user not found.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")

        if not user_data['characters']:
            print("[deep_pink2](＞﹏＜)Oops, no characters available for this user.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            return

        clear()
        draw()
        print("[light_steel_blue]Select a character to delete:[/]")
        for i, character in enumerate(user_data['characters'], start=1):
            print(f"{i}, {character['name']}")
        draw()
        print("[orchid1 italic bold]💡Hints:[/]")
        print("- Type a number to select a character to delete")
        print("- Type '(B)ack' to go back to main menu")
        draw()

        choice = input("# ")
        if choice.lower() == 'back' or 'b':
            print(choice)
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
        self.delete_leaderboard_character(username, character_name)
        # Save the updated user data
        self.user_manager.save_users()
        print("[dark_slate_gray2]Character deleted successfully.[/]")
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def delete_leaderboard_character(self, username, character_name):
        self.leaderboard = utils.load_data(self.user_manager.leaderboard_file)
        self.leaderboard = [entry for entry in self.leaderboard
                            if not (entry.get("Player") == username and entry.get("Character name") == character_name)]
        utils.save_data(self.leaderboard, self.user_manager.leaderboard_file)

    def get_bonus(self, username, character_name):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except IOError:
            print("Error: File not found or inaccessible.")
            return None

        user_data = users_data.get(username, {})
        for character in user_data.get("characters", []):
            if character.get("name") == character_name:
                return character.get('bonus')
        return None

    def reset_bonus(self, username, character_name):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)

            # Reset the bonus for the specific character
            if username in users_data and "characters" in users_data[username]:
                for character in users_data[username]["characters"]:
                    if character["name"] == character_name:
                        character["bonus"] = 0

            # Save the updated data back to users.json
            with open('users.json', 'w') as file:
                json.dump(users_data, file, indent=4)

        except IOError:
            print("Error: File not found or inaccessible.")

    def reset_leaderboard_score(self, character_name):
        try:
            with open('leaderboard.json', 'r') as file:
                leaderboard_data = json.load(file)

            # Reset the score for the specific character
            for entry in leaderboard_data:
                if entry["Character name"] == character_name:
                    entry["score"] = 0

            # Save the updated data back to leaderboard.json
            with open('leaderboard.json', 'w') as file:
                json.dump(leaderboard_data, file, indent=4)

        except IOError:
            print("[deep_pink](＞﹏＜)Error: File not found or inaccessible.[/]")
