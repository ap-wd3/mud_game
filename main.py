import os
import platform
import json
import colorama

from account import Account
from game_system import GameSystem
from colorama import Fore, Back, Style
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'
colorama.init()

run = True
menu1 = True
menu2 = True
play = False
rules = False

confidence = 100
ATK = 10

# Map
rooms = {
    'Maple Sanctuary': {'East': 'Moonlit Timberland', 'Item': 'Mirror'},
    'Moonlit Timberland': {'West': 'Maple Sanctuary', 'North': 'Maple Sanctuary', 'South': 'Dewdrop Dell',
                           'East': 'Emerald Canopy', 'Monster': 'Overthinking monster'},
    'Whispering Pines': {'South': 'Moonlit Timberland', 'East': 'Pine Haven', 'Monster': 'Idol monster'},
    'Dewdrop Dell': {'North': 'Moonlit Timberland', 'East': 'Redwood Haven', 'Monster': 'Sad monster'},
    'Pine Haven': {'South': 'Emerald Canopy', 'East': 'Walnut Retreat', 'West': 'Whispering Pines',
                   'Item': ['Heel', 'Soccer']},
    'Emerald Canopy': {'West': 'Moonlit Timberland', 'North': 'Pine Haven', 'South': 'Redwood Haven',
                       'East': 'Cypress Cottage', 'Monster': 'Overthinking monster'},
    'Redwood Haven': {'West': 'Dewdrop Dell', 'East': 'Silver Birch Copse', 'North': 'Emerald Canopy',
                      'Item': ['Book', 'Pizza']},
    'Walnut Retreat': {'West': 'Pine Haven', 'South': 'Cypress Cottage', 'Monster': 'Insecure monster'},
    'Cypress Cottage': {'West': 'Emerald Canopy', 'South': 'Silver Birch Copse', 'North': 'Walnut Retreat',
                        'East': 'Forest Haven', 'Monster': 'Angry monster'},
    'Silver Birch Copse': {'West': 'Redwood Haven', 'North': 'Cypress Cottage', 'Monster': 'Numb monster'},
    'Forest Haven': {'West': 'Cypress Cottage', 'Item': ['Jumping rope', 'Lipstick']}
}

# track current room
current_room = "Maple Sanctuary"

# List of vowels
vowels = ['a', 'e', 'i', 'o', 'u']

# list of inventory
inventory = []

# tracks last move
message = ""

def clear():
    if platform == 'Windows':
        os.system("cls")
    else:
        os.system("clear")


def draw():
    print("++------------------------++")


def save():
    list = [
        name,
        str(confidence),
        str(ATK)
    ]

    f = open("load.txt", "w")

    for item in list:
        f.write(item + "\n")
    f.close()



while run:
    if menu1:
        clear()
        draw()
        print("1, LOGIN")
        print("2, NEW REGISTRATION")
        print("3, RESET PASSWORD")
        draw()
        menu2 = False

        choice = input("# ")
        game_system = GameSystem()

        if choice == "1":
            clear()
            menu2 = False
            while not menu2:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                result = game_system.login(username, password)

                if result == 'Logged in successfully.':
                    print(result)
                    menu2 = True
                else:
                    print(result)
                    print("Incorrect username or password, please try again")

        elif choice == "2":
            clear()
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            email = input("Enter your email address: ")
            print(game_system.create_user(username, password, email))
            menu2 = True

        elif choice == "3":
            username = input("Enter your username: ")
            email = input("Enter your email address for password reset: ")
            new_password = input("Enter your new password: ")
            print(game_system.reset_password(username, email, new_password))
    else:
        print("Invalid Input")

    while menu2:
        clear()
        draw()
        print("1, NEW GAME")
        print("2, LOAD GAME")
        print("3, LEADERBOARD")
        print("4, RULES")
        print("5, QUIT GAME")
        draw()

        if rules:
            print("Collect the right item(s) to defeat monsters. Find more hint by observing each monster")
            rules = False
            choice = ""
            input("> ")
        else:
            choice = input("# ")

        if choice == "1":
            clear()

            logged_in_username = username

            while True:
                name = input("Enter your character's name: ").strip()
                user_data = game_system.user_manager.users.get(username, {'characters': []})
                if any(char['name'] == name for char in user_data['characters']):
                    print("Error: Character name already exists. Please choose a different name.")
                else:
                    break

            while True:

                hair_length = input("Choose hair length (long/short): ").strip().lower()
                if hair_length not in ["short", "long"]:
                    print("Invalid hair length, please choose again.")
                else:
                    break

            hair_color = 'Unknown'
            while hair_color == 'Unknown':
                print("Choose hair color:")
                print("1: Pink")
                print("2: Blue")
                print("3: White")
                color_options = {'1': 'Pink', '2': 'Blue', '3': 'White'}
                hair_color_choice = input("Select option (1, 2, or 3): ").strip()
                hair_color = color_options.get(hair_color_choice, "Unknown")
                if hair_color == 'Unknown':
                    print("Invalid option, please choose again.")

            eye_color = 'Unknown'
            while eye_color == 'Unknown':
                print("Choose eye color:")
                print("1:Yellow")
                print("2: Green")
                print("3: Red")
                color_options = {'1': 'Yellow', '2': 'Green', '3': 'Red'}
                eye_color_choice = input("Select option (1, 2, or 3): ").strip()
                eye_color = color_options.get(eye_color_choice, "Unknown")
                if eye_color == 'Unknown':
                    print("Invalid option, please choose again.")

            result = game_system.create_character(username, name, hair_length, hair_color, eye_color)
            print(result)
            menu2 = False
            play = True
        elif choice == "2":
            f = open("load.txt", "r")
            load_list = f.readlines()
            name = load_list[0][:-1]
            confidence = load_list[1][:-1]
            ATK = load_list[2][:-1]
            clear()
            print("Welcome back, " + name + "!")
            input("> ")
            menu2 = False
            play = True
        elif choice == "3":
            f = open("leaderboard.txt", "r")
        elif choice == "4":
            rules = True
        elif choice == "5":
            quit()

    while play:
        save()
        clear()
        print(f"You are in the {current_room}\nInventory : {inventory}\n{'-' * 27}")
        print(message)

        if "Item" in rooms[current_room].keys():
            nearby_item = rooms[current_room]["Item"]
            if nearby_item not in inventory:
                if nearby_item[0] in vowels:
                    print(f"You see an {nearby_item}")
                else:
                    print(f"You see a {nearby_item}")

        if "Monster" in rooms[current_room].keys():
            print(f"You encounter {rooms[current_room]['Monster']}!")

        user_input = input("Enter your move: ")

        next_move = user_input.split(' ')

        action = next_move[0].title()

        item = "Item"
        direction = "null"

        if len(next_move) > 1:
            item = next_move[1:]
            direction = next_move[1].title()

            item = " ".join(item).title()

        if action == "Go":
            try:
                current_room = rooms[current_room][direction]
                message = f"You travel {direction}"
            except:
                message = "You can't go that way."

        elif action == "Get":
            try:
                if item == rooms[current_room]["Item"]:
                    if item not in inventory:
                        inventory.append(rooms[current_room]["Item"])
                        message = f"{item} retrieved!"
                    else:
                        message = f"You already have the {item}."
                else:
                    message = f"Can't find {item}"
            except:
                message = f"Can't find {item}"

        elif action == "0":
            save()
            break

        else:
            message = "Invalid Command"


        # draw()
        # print("0 - SAVE and QUIT")
        # draw()
        #
        # dest = input("# ")
        #
        # if dest == "0":
        #     play = False
        #     menu = True
        #     save()
