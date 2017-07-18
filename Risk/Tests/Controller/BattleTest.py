from Controller.Battle import *
import unittest
import random


class TestBattle(unittest.TestCase):

    def setUp(self):
        self.amount = 3
        self.possible_dice_rolls = [1,2,3,4,5,6]

        self.attacking_die_1 = 4
        self.defending_die_1 = 3

        self.attacking_die_2 = 6
        self.defending_die_2 = 6

        self.attacking_die_3 = 4
        self.defending_die_3 = 6


    def test_compare_dice(self):
        self.assertEqual(compare_dice(self.attacking_die_1,self.defending_die_1), 1)
        self.assertEqual(compare_dice(self.attacking_die_2,self.defending_die_2), -1)
        self.assertEqual(compare_dice(self.attacking_die_3,self.defending_die_3), -1)

    def test_roll_dice(self):
        dice = throw_dice(self.amount)

        self.assertEqual(len(dice), self.amount)
        self.assertGreaterEqual(dice[0],dice[1])
        self.assertGreaterEqual(dice[1],dice[2])

        self.assertIn(dice[0], self.possible_dice_rolls)
        self.assertIn(dice[1], self.possible_dice_rolls)
        self.assertIn(dice[2], self.possible_dice_rolls)

