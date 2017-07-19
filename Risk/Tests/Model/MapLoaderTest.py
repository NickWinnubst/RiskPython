import os
from Model.MapLoader import *
import unittest


# Test the MapLoader class
class MapLoaderTest(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.game_map = load_fresh_map(dir_path.replace("Tests\\Model","\\Maps\\TestMap.json"))

    def test_map(self):
        self.assertEquals(self.game_map.name, "TestMap")
        self.assertEquals(self.game_map.army_sizes, [2,3,4,5,6,7])
        self.assertEquals(len(self.game_map.regions), 3)

        self.assertEquals(self.game_map.regions[0].name, "North")
        self.assertEquals(self.game_map.regions[1].name, "South")
        self.assertEquals(self.game_map.regions[2].name, "East")

        self.assertEquals(self.game_map.regions[0].value, 2)
        self.assertEquals(self.game_map.regions[1].value, 3)
        self.assertEquals(self.game_map.regions[2].value, 4)

        self.assertEquals(len(self.game_map.regions[0].territories), 1)
        self.assertEquals(len(self.game_map.regions[1].territories), 2)
        self.assertEquals(len(self.game_map.regions[2].territories), 1)

        self.assertEquals(self.game_map.regions[0].territories[0].name, "Hodor")
        self.assertEquals(self.game_map.regions[1].territories[0].name, "Bran")
        self.assertEquals(self.game_map.regions[1].territories[1].name, "Stark")
        self.assertEquals(self.game_map.regions[2].territories[0].name, "Lannister")

        self.assertCountEqual(self.game_map.regions[0].territories[0].connections, ["Bran","Stark"])
        self.assertCountEqual(self.game_map.regions[1].territories[0].connections, ["Stark","Hodor","Lannister"])
        self.assertCountEqual(self.game_map.regions[1].territories[1].connections, ["Bran","Hodor","Lannister"])
        self.assertCountEqual(self.game_map.regions[2].territories[0].connections, ["Stark","Bran"])
