import json


class PlayerAccount:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        try:
            with open('user_data.json', 'r') as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.users = []
            self.save_users()

    def save_users(self):
        with open('user_data.json', 'w') as file:
            json.dump(self.users, file)

    def create_account(self):
        print("Let's get you ready before adventure!")
        new_username = input("Username (This will be your name in the game): ")

        while any(user[0] == new_username for user in self.users):
            print("Sorry, this username has been taken. Please choose a different one.")
            new_username = input("Username: ")

        new_password = input("Password: ")

        self.users.append((new_username, new_password))
        self.save_users()
        print(f"Welcome {new_username}! Let's pick up your item")

    def login(self):
        while True:
            print("Enter your username or type 'C' to create a new account")
            username = input("Username: ")

            if username.upper() == 'C':
                self.create_account()
                break

            if any(user[0] == username for user in self.users):
                password = input("Password: ")

                if any(pw[1] == password for pw in self.users):
                    print(f"Welcome back {username}!")
                    print("Do you want to start a new game or return to the saved area?")
                    before_start = input("[1] Go to the saved area\n[2] Start a new game\nYour answer: ")

                    if before_start == '2':
                        self.create_character()
                        return
                    elif before_start == '1':
                        self.load_game()
                        return
                    else:
                        print("Invalid input. Please try again")
                        print(before_start)
                    break

            print("Invalid username or password. Please try again or Type 'C' to create a new account.")

    def create_character(self):
        print("Please choose your initial item")

    def load_game(self):
        print("loading...")


if __name__ == "__main__":
    player_account = PlayerAccount()
    player_account.login()
