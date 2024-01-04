import utils
from rich import print
from rich.style import Style
from rich.console import Console
import sys
import maskpass

class UserManager:
    def __init__(self, storage_file='users.json'):
        self.storage_file = storage_file
        self.users = utils.load_data(self.storage_file)
        self.console = Console()
        self.leaderboard_file = 'leaderboard.json'
        self.leaderboard = utils.load_data(self.leaderboard_file)

    def colored_input(self, prompt,color="green"):
        self.console.print(prompt, style=color, end="")
        user_input = input()
        return user_input

    def overwrite_last_lines(self, num_lines):
        for _ in range(num_lines):
            sys.stdout.write('\033[F\033[K')

    def create_user(self, username, password, email):
        if username in self.users:
            print("[deep_pink2](⋟﹏⋞)Oops, username already taken.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        else:
            self.users[username] = {'password': password, 'email': email, 'characters': []}
            utils.save_data(self.users, self.storage_file)
            print(f"[dark_slate_gray2]{username} created successfully.[/]")
            print()
            maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")
            return "User created successfully."

    def save_users(self):
        utils.save_data(self.users, self.storage_file)

    def reload_data(self):
        self.users = utils.load_data(self.storage_file)

    def verify_user(self, username, password):
        self.reload_data()
        if username not in self.users:
            return False
        return self.users[username]['password'] == password

    def reset_password(self):
        while True:
            username = input("\033[93mEnter your username: \033[0m")
            if username.lower() == 'back' or username.lower() == 'b':
                return
            if username not in self.users:
                print("[deep_pink2](⋟﹏⋞)Oops, user does not exist.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                self.overwrite_last_lines(3)
                continue
            break
        while True:
            email = input("\033[93mEnter your email address for password reset:  \033[0m")
            if email.lower() == 'back' or email.lower() == 'b':
                return
            if self.users[username]['email'] != email:
                print("[deep_pink2](⋟﹏⋞)Oops, incorrect email.[/]")
                maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
                self.overwrite_last_lines(3)
                continue
            break
        new_password = maskpass.askpass(prompt="\033[93mEnter your new password: \033[0m", mask="*")
        self.users[username]['password'] = new_password
        utils.save_data(self.users, self.storage_file)
        print("[dark_slate_gray2]Password reset successfully.[/]")
        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def delete_account(self, username):
        if username not in self.users:
            print("[deep_pink2](⋟﹏⋞)Oops, user does not exist.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
        del self.users[username]
        self.save_users()

        maskpass.askpass(prompt="\033[92mPress 'Enter' to continue...\033[0m", mask=" ")

    def username_verify(self, username):
        if username in self.users:
            print("[deep_pink2](⋟﹏⋞)Oops, username already taken.[/]")
            maskpass.askpass(prompt="\033[92mPress 'Enter' to try again...\033[0m", mask=" ")
            self.overwrite_last_lines(3)
            return username in self.users
        else:
            pass


