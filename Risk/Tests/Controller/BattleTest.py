from Controller.Battle import *
import unittest
import random


# Test the Battle class
class TestBattle(unittest.TestCase):

    def setUp(self):
        self.valid_dice_rolls = [1, 2, 3, 4, 5, 6]

        self.valid_amount_of_attacking_dice = [1,2,3]
        self.valid_amount_of_defending_dice = [1,2]

        self.valid_attack_scores = [[2,0],[1,0],[1,1],[0,1],[0,2]]

        self.faulty_attacking_dice_1 = 4
        self.faulty_attacking_dice_2 = 0

        self.faulty_defending_dice_1 = 3
        self.faulty_defending_dice_2 = 0

        self.attacking_die_1 = 4
        self.defending_die_1 = 3

        self.attacking_die_2 = 6
        self.defending_die_2 = 6

        self.attacking_die_3 = 4
        self.defending_die_3 = 6

        self.amount = 3

    def test_attack(self):

        self.assertEqual(attack(self.faulty_attacking_dice_1, self.faulty_defending_dice_1), [0,0])
        self.assertEqual(attack(self.faulty_attacking_dice_1, self.faulty_defending_dice_2), [0,0])
        self.assertEqual(attack(self.faulty_attacking_dice_2, self.faulty_defending_dice_1), [0,0])
        self.assertEqual(attack(self.faulty_attacking_dice_2, self.faulty_defending_dice_2), [0,0])

        self.assertEqual(attack(self.faulty_attacking_dice_1, random.choice(self.valid_amount_of_defending_dice)), [0,0])
        self.assertEqual(attack(self.faulty_attacking_dice_2, random.choice(self.valid_amount_of_defending_dice)), [0,0])
        self.assertEqual(attack(random.choice(self.valid_amount_of_attacking_dice), self.faulty_defending_dice_1), [0,0])
        self.assertEqual(attack(random.choice(self.valid_amount_of_attacking_dice), self.faulty_defending_dice_2), [0,0])

        self.assertIn(attack(random.choice(self.valid_amount_of_attacking_dice), random.choice(self.valid_amount_of_defending_dice)), self.valid_attack_scores)

    def test_compare_dice(self):
        self.assertEqual(compare_dice(self.attacking_die_1,self.defending_die_1), [0,1])
        self.assertEqual(compare_dice(self.attacking_die_2,self.defending_die_2), [1,0])
        self.assertEqual(compare_dice(self.attacking_die_3,self.defending_die_3), [1,0])

    def test_roll_dice(self):
        dice = throw_dice(self.amount)

        self.assertEqual(len(dice), self.amount)
        self.assertGreaterEqual(dice[0],dice[1])
        self.assertGreaterEqual(dice[1],dice[2])

        self.assertIn(dice[0], self.valid_dice_rolls)
        self.assertIn(dice[1], self.valid_dice_rolls)
        self.assertIn(dice[2], self.valid_dice_rolls)

