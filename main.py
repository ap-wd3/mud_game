# Importing ASCII art and misogynistic phrases from external modules
from ascii_graphics import monster_ascii
from misogynistic_phrases import misogynistic_phrases
import random

# Defining a Player class
class Player:
    # Constructor method initializing the player with a confidence attribute
    def __init__(self, confidence):
        self.confidence = confidence

    # Method representing the player's attack, reducing confidence by a specified damage amount
    def attack(self, damage):
        self.confidence -= damage

    # Method representing the player's defense, increasing confidence by a specified boost amount
    def defend(self, boost):
        self.confidence += boost

    def rolldice(self, increaseAttack):
        self.

# Defining a Monster class
class Monster:
    # Constructor method initializing the monster with a name and damage attribute
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    # Method representing the monster's attack
    def attack(self, player):
        # Randomly selecting a misogynistic phrase for the monster's dialogue
        misogynistic_phrase = random.choice(misogynistic_phrases)
        # Displaying the monster's dialogue
        print(f"{self.name} says: '{misogynistic_phrase}'")
        # Displaying the monster's ASCII art before the attack
        self.show_before_attack_ascii()
        # Player gets attacked, reducing player's confidence
        player.attack(self.damage)
        # Displaying the monster's ASCII art after the attack
        self.show_hurt_ascii()
    
    # Method to display the monster's ASCII art before the attack
    def show_before_attack_ascii(self):
        print(monster_ascii[self.name]["before_attack"])
    
    # Method to display the monster's ASCII art after the attack
    def show_hurt_ascii(self):
        print(monster_ascii[self.name]["after_attack"])

# Main game function
def main():
    # Creating a player with an initial confidence level
    player = Player(confidence=100)
    
    # Creating a dictionary of monsters with names and damage levels
    monsters = {
        "Misogynic Male Student": Monster("Misogynic Male Student", damage=15),
        "Immatured Female Student": Monster("Immatured Female Student", damage=12),
        "Authority Teacher": Monster("Authority Teacher", damage=20)
    }

    # Displaying game introduction
    print("Welcome to the Empowerment Dungeon!")
    print("Defeat the monsters using the power of will, pens, and feminism books.")

    # Main game loop, continues until player's confidence is depleted
    while player.confidence > 0:
        # Randomly selecting a monster from the dictionary
        current_monster = random.choice(list(monsters.values()))
        # Displaying the encounter message and the monster's ASCII art before the attack
        print(f"\nYou encounter a {current_monster.name}!")
        print(monster_ascii[current_monster.name]["before_attack"])

        # Asking the player to choose an action (attack or defend)
        action = input("Choose your action (1: Attack, 2: Defend): ")

        # Handling player actions
        if action == "1":
            current_monster.attack(player)
        elif action == "2":
            # Player chooses to defend, increasing confidence
            player.defend(boost=10)
            print("You defend with the power of feminism books! Your confidence increases.")

        # Displaying the player's remaining confidence after the action
        print(f"Your confidence: {player.confidence}")

    # Displaying the game over message when the player runs out of confidence
    print("Game over. You ran out of confidence. Keep fighting for empowerment!")

# Ensuring that the main function is called when the script is run
if __name__ == "__main__":
    main()
