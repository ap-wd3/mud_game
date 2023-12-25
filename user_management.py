import utils

class UserManager:
    def __init__(self, storage_file='users.json'):
        self.storage_file = storage_file
        self.users = utils.load_data(self.storage_file)

    def create_user(self, username, password, email):
        if username in self.users:
            return "Error: Username already taken."
        self.users[username] = {'password': password, 'email': email, 'characters': []}
        utils.save_data(self.users, self.storage_file)
        return "User created successfully."

    def save_users(self):
        utils.save_data(self.users, self.storage_file)

    def verify_user(self, username, password):
        if username not in self.users:
            return False
        return self.users[username]['password'] == password

    def reset_password(self, username, email, new_password):
        if username not in self.users:
            return "Error: User does not exist."
        if self.users[username]['email'] != email:
            return "Error: Incorrect email."
        self.users[username]['password'] = new_password
        utils.save_data(self.users, self.storage_file)
        return "Password reset successfully."

    def delete_account(self, username):
        if username not in self.users:
            return "Error: User does not exist."

        del self.users[username]

        self.save_users()
        return "Account deleted successfully."