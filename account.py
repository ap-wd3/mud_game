import json
import os


def clear():
    os.system("cls")


class Account:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        try:
            with open("user_accounts.json", "r") as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.users = []
            self.save_users()

    def save_users(self):
        with open("user_accounts.json", "w") as file:
            json.dump(self.users,file)

    def create_account(self):
        new_username = input("Create new username: ")

        while any(user[0] == new_username for user in self.users):
            clear()
            print("This username has been taken. Please choose a different one.")
            new_username = input("Create new Username: ")

        new_password = input("Create new password: ")

        self.users.append((new_username, new_password))
        self.save_users()

    def login(self):
        while True:
            username = input("Username: ")

            user_found = next((user for user in self.users if user[0] == username), None)

            if user_found:
                password = input("Password: ")

                if user_found[1] == password:
                    break
                else:
                    clear()
                    print("Incorrect password. Please try again.")
            else:
                clear()
                print("Username not found. Please try again.")

if __name__ == "__main__":
    player_account = Account()
    player_account.create_account()

