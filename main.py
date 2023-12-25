
import os
import platform
import json
from map import Map, paths
from game_system import GameSystem
from monster import Monster, monsters


from account import Account
from game_system import GameSystem
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'


run = True
menu1 = True
menu2 = True
play = False
rules = False

m = Map(3, 6, 0, 1, paths)

# track current room
current_room = "Maple Sanctuary"

# list of inventory
inventory = []

# tracks last move
message = ""

confidence = 100

bonus = 0

rooms = {
    'Maple Sanctuary': {'East': 'Moonlit Timberland', 'Item': 'Smart Planner'},
    'Moonlit Timberland': {'West': 'Maple Sanctuary', 'North': 'Maple Sanctuary', 'South': 'Dewdrop Dell',
                           'East': 'Emerald Canopy'},
    'Whispering Pines': {'South': 'Moonlit Timberland', 'East': 'Pine Haven', 'Monster': 'Diet Monster'},
    'Dewdrop Dell': {'North': 'Moonlit Timberland', 'East': 'Redwood Haven', 'Monster': 'Balance Monster'},
    'Pine Haven': {'South': 'Emerald Canopy', 'East': 'Walnut Retreat', 'West': 'Whispering Pines',
                   'Item': 'Mirror'},
    'Emerald Canopy': {'West': 'Moonlit Timberland', 'North': 'Pine Haven', 'South': 'Redwood Haven',
                       'East': 'Cypress Cottage', 'Monster': 'Overthinking Monster'},
    'Redwood Haven': {'West': 'Dewdrop Dell', 'East': 'Silver Birch Copse', 'North': 'Emerald Canopy',
                      'Item': 'Clock'},
    'Walnut Retreat': {'West': 'Pine Haven', 'South': 'Cypress Cottage', 'Monster': 'Insecure Monster'},
    'Cypress Cottage': {'West': 'Emerald Canopy', 'South': 'Silver Birch Copse', 'North': 'Walnut Retreat',
                        'East': 'Forest Haven', 'Monster': 'Glass Ceiling Monster'},
    'Silver Birch Copse': {'West': 'Redwood Haven', 'North': 'Cypress Cottage', 'Monster': 'Harassment Monster'},
    'Forest Haven': {'West': 'Cypress Cottage', 'Item': 'Book'},
    'Mystic Moss Grove': {'West': 'Silver Birch Copse', 'North': 'Forest Haven', 'Item': 'Pizza'},
    'Enchanted Thicket': {'West': 'Walnut Retreat', 'South': 'Forest Haven', 'Item': 'Key'},
    'Sunbeam Glade': {'West': 'Forest Haven', 'Item': 'Jumping Rope'},
}

def clear():
    if platform == 'Windows':
        os.system("cls")
    else:
        os.system("clear")


def draw():
    print("++------------------------++")


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
        print("5, DELETE ACCOUNT")
        print("6, DELETE CHARACTERS")
        print("7, QUIT GAME")
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

                hair_length = input("Choose hair length (Long/Short): ").strip().lower()
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
            input("Press enter to continue...")
            menu2 = False
            play = True
        elif choice == "2":
            loaded_data = game_system.load_game(username)
            if loaded_data:
                character, current_room, inventory, rooms = loaded_data
                name = character['name']
                current_room = current_room
                m.x, m.y = m.get_coordinates_from_room_name(current_room)
                inventory = inventory
                rooms = rooms
                menu2 = False
                play = True

            loaded_bonus = game_system.load_score(name, username)
            if loaded_bonus is not None:
                bonus = loaded_bonus
            else:
                print("Error loading score. Starting with score of 0.")
                bonus = 0

        elif choice == "3":
            clear()
            draw()
            game_system.load_leaderboard()
            draw()
            input("Press 'Enter' to continue...")
        elif choice == "4":
            rules = True
        elif choice == "5":
            game_system.delete_account(username)
            input("Press 'Enter' to continue...")
            menu2 = False
            menu1 = True
        elif choice == "6":
            game_system.delete_character(username)
            input("Press 'Enter' to continue...")
        elif choice == "7":
            quit()

    while play and confidence >= 0:
        room_info = rooms.get(current_room, {})
        game_system.save_game(username, name, current_room, inventory,confidence, rooms)

        clear()
        m.print_map()
        print(f"You are in the {current_room}\nInventory : {inventory}\n{'-' * 27}")
        print("Hint: You can enter 'help' for command information.")
        print(f"Confidence: {confidence}")
        print(message)

        if "Monster" in room_info:
            print(f"You encounter a {room_info['Monster']}!")
            print("Enter 'look' to see the information of the monster")
        elif "Item" in room_info:
            item = room_info["Item"]
            if item[0] in 'AEIOUaeiou':
                print(f"You see an {room_info['Item']}!")
            else:
                print(f"You see a {room_info['Item']}")
        else:
            print("There's nothing special here.")

        user_input = input("Enter your command: ").lower().split(' ')
        action = user_input[0]

        if len(user_input) > 1:
            argument = " ".join(user_input[1:]).title()

        if action == "go":
            direction = argument.lower()
            m.move(direction)
            current_room = m.room_map.get((m.x, m.y), "Unknown room")
            message = "You moved " + direction

        elif action == "get":
            item = argument
            if item == rooms[current_room].get("Item", "") and item not in inventory:
                inventory.append(item)
                message = f"{item} retrieved!"
                rooms[current_room].pop("Item", None)

            elif item in inventory:
                message = f"You already have {item}."
            else:
                message = f"{item} cannot be picked up."

        elif action == "look":
            monster_name = room_info.get("Monster")
            if monster_name:
                monster = monsters.get(monster_name)
                if monster:
                    print(f"Name: {monster.name}")
                    print(f"Description: {monster.description}")
                    print(f"Health: {monster.health}")
                    print(f"Attack: {monster.attack}")
                    print(f"Items Required: {', '.join(monster.items_required)}")
                    print(f"Hint: {monster.hint}")
                    input("Press 'Enter' to continue...")
                else:
                    print("There's no monster here.")
            else:
                print("Sorry, there is nothing to look at. :(")


        elif action == "quit":
            answer = input("Save and Exit game? Y/N\nYour answer: ").upper()
            if answer == "Y":
                game_system.save_game(username, name, current_room, inventory,confidence, rooms)
                print("Game Saved Successfully!")
                print("Thank you for playing The Wood, I will see you when I see you again!")
                exit(0)
            elif answer == "N":
                pass
            else:
                print("Invalid Command")

        elif action == "help":
            print("1. Enter 'Go east/west/south/north' to move among rooms. \n")
            print("2. Enter 'Get (the name of the item)' to pick items.\n")
            print("3. Enter 'Look' to get the information of the monsters.\n")
            print("4. Enter 'Quit' to quit the game.")
            input("Press Enter to continue...")

        elif action == "attack":
            monster_name = room_info.get("Monster")
            if monster_name:
                monster = monsters.get(monster_name)
                print(len(monster.items_required))
                print(monster.items_required)
                print(inventory)
                print(monster.items_required[0] in inventory)
                input("Press Enter to continue...")
                if monster:
                    if len(monster.items_required) < 5:
                        if len(monster.items_required) == 1:

                            if monster.items_required[0] in inventory:
                                monster.health -= 100
                                # print(f"Monster health: {monster.health}")
                                # input("Press Enter to continue...")
                                if monster.health == 0:
                                    print(
                                        f"{monster.name} has been defeated, you've got {monster.loot} and {monster.bonus} points goes to your leaderboard.")
                                    rooms[current_room].pop("Monster", None)
                                    input("Press Enter to continue")
                                    bonus += monster.bonus
                                    game_system.save_score(name, username, bonus)

                            else:
                                confidence -= 20
                                # print(f"Confidence: {confidence}")
                                if confidence == 0:
                                    print("Game over! Maybe next time!")
                                    game_system.save_game(username, name, current_room, inventory, confidence, rooms)
                                    exit(0)


                        elif len(monster.items_required) == 2:
                            for item in monster.items_required:
                                if item in inventory:
                                    monster.health -= 50
                                    if monster.health == 0:
                                        print(
                                            f"{monster.name} has been defeated, you've got {monster.loot} and {monster.bonus} points goes to your leaderboard.")
                                        input("Press enter to continue")
                                        rooms[current_room].pop("Monster", None)
                                        bonus += monster.bonus
                                        game_system.save_score(name, username, bonus)
                                        # print(f"Bonus: {bonus}")
                                        # input("Press enter to continue")
                                        # print(f"Bonus: {bonus}")
                                        # input("Press enter to continue")
                                else:
                                    confidence -= 20
                                    print(f"Confidence: {confidence}")
                                    input("Press enter to continue")
                                    if confidence == 0:
                                        print("Game over! Maybe next time!")
                                        input("Press enter to continue")
                                        game_system.save_game(username, name, current_room, inventory, confidence,
                                                              rooms)
                                        exit(0)

                    else:
                        for item in monster.items_required:
                            if item in inventory:
                                monster.health -= 20
                                # print(f"Monster health: {monster.health}")
                                # input("Enter to continue")
                                if monster.health == 0:
                                    print(
                                        f"{monster.name} has been defeated, you've got {monster.loot} and {monster.bonus} points goes to your leaderboard.")
                                    rooms[current_room].pop("Monster", None)
                                    input("Press enter to continue")
                                    bonus += monster.bonus
                                    game_system.save_score(name, username, bonus)
                                    # print(f"Bonus: {bonus}")
                                    # input("Press enter to continue")
                                    # print(f"Bonus: {bonus}")
                                    # input("Press enter to continue")
                            else:
                                confidence -= 20
                                print(f"Confidence: {confidence}")
                                input("Press enter to continue")
                                if confidence == 0:
                                    print("Game over! Maybe next time!")
                                    input("Press enter to continue")
                                    game_system.save_game(username, name, current_room,inventory,confidence, rooms)
                                    exit(0)

    else:
            message = "Invalid Command"

