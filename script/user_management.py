import utils
from rich import print
from rich.style import Style
from rich.console import Console

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

    def create_user(self, username, password, email):
        if username in self.users:
            print("Error: Username already taken.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        else:
            self.users[username] = {'password': password, 'email': email, 'characters': []}
            utils.save_data(self.users, self.storage_file)
            print("User created successfully.")
            self.colored_input("Press Enter to continue...", color="pale_green1")

    def save_users(self):
        utils.save_data(self.users, self.storage_file)

    def reload_data(self):
        self.users = utils.load_data(self.storage_file)

    def verify_user(self, username, password):
        self.reload_data()
        if username not in self.users:
            return False
        return self.users[username]['password'] == password

    def reset_password(self, username, email, new_password):
        if username not in self.users:
            print("Error: User does not exist.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        if self.users[username]['email'] != email:
            print("Error: Incorrect email.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        self.users[username]['password'] = new_password
        utils.save_data(self.users, self.storage_file)
        print("Password reset successfully.")
        self.colored_input("Press Enter to continue...", color="pale_green1")

    def delete_account(self, username):
        if username not in self.users:
            print("Error: User does not exist.")
            self.colored_input("Press Enter to continue...", color="pale_green1")
        del self.users[username]
        self.save_users()
        self.colored_input("Press Enter to continue...", color="pale_green1")