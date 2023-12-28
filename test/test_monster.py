import unittest
from monster import Monster, monsters

class TestMonster(unittest.TestCase):

    def test_monster_initialization(self):
        # Testing the initialization of a Monster
        diet_monster = Monster('Diet Monster', 'Description', 100, 20, 'Cloak of Self-Acceptance', ['Pizza', 'Jumping Rope'], 'Hint', 20)
        self.assertEqual(diet_monster.name, 'Diet Monster')
        self.assertEqual(diet_monster.health, 100)
        self.assertEqual(diet_monster.attack, 20)
        self.assertEqual(diet_monster.loot, 'Cloak of Self-Acceptance')
        self.assertEqual(diet_monster.items_required, ['Pizza', 'Jumping Rope'])
        self.assertEqual(diet_monster.hint, 'Hint')
        self.assertEqual(diet_monster.bonus, 20)

    def test_monsters_dictionary(self):
        # Testing the attributes of predefined monsters
        self.assertTrue('Diet Monster' in monsters)
        self.assertTrue('Insecure Monster' in monsters)
        # Add additional checks for other monsters

        # Checking attributes of a specific monster
        insecure_monster = monsters['Insecure Monster']
        self.assertEqual(insecure_monster.name, 'Insecure Monster')
        self.assertEqual(insecure_monster.health, 100)
        self.assertEqual(insecure_monster.attack, 20)
        self.assertEqual(insecure_monster.loot, 'Amulet of Confidence')
        self.assertEqual(insecure_monster.items_required, ['Book'])
        self.assertEqual(insecure_monster.hint, 'To defeat the Insecure Monster, you need a book. With the book you can equip yourself with knowledge and feel secured.')
        self.assertEqual(insecure_monster.bonus, 10)



if __name__ == '__main__':
    unittest.main()
