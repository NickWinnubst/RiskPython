from Controller.Reinforce import *
import unittest
from Model.Territory import *
from Model.Region import *
from Model.Map import *
import random


class TestBattle(unittest.TestCase):

    def setUp(self):
        self.territory_a = Territory("A", ["B","C"])
        self.territory_a.set_owner(1,1)
        self.territory_b = Territory("B", ["A"])
        self.territory_b.set_owner(2,1)
        self.territory_c = Territory("C", ["A"])
        self.territory_c.set_owner(3,1)


        self.territory_d = Territory("D", ["A"])
        self.territory_d.set_owner(3,1)
        self.territory_e = Territory("E", ["A"])
        self.territory_e.set_owner(3,1)
        self.territory_f = Territory("F", ["A"])
        self.territory_f.set_owner(3,1)
        self.territory_g = Territory("G", ["A"])
        self.territory_g.set_owner(3,1)
        self.territory_h = Territory("H", ["A"])
        self.territory_h.set_owner(3,1)
        self.territory_i = Territory("I", ["A"])
        self.territory_i.set_owner(3,1)
        self.territory_j = Territory("J", ["A"])
        self.territory_j.set_owner(3,1)
        self.territory_k = Territory("K", ["A"])
        self.territory_k.set_owner(3,1)
        self.territory_l = Territory("L", ["A"])
        self.territory_l.set_owner(3,1)
        self.territory_m = Territory("M", ["A"])
        self.territory_m.set_owner(3,1)
        self.territory_n = Territory("N", ["A"])
        self.territory_n.set_owner(3,1)
        self.territory_o = Territory("O", ["A"])
        self.territory_o.set_owner(3,1)

        self.north_value = 5
        self.south_value = 2

        self.region_north = Region("North", self.north_value, [self.territory_a, self.territory_b])
        self.region_south = Region("South", self.south_value, [self.territory_c])
        self.region_south_2 = Region("South", self.south_value, [self.territory_c, self.territory_d, self.territory_e, self.territory_f, self.territory_g, self.territory_h, self.territory_i, self.territory_j, self.territory_k, self.territory_l, self.territory_m, self.territory_n, self.territory_o])

        self.map = Map("TestMap", [self.region_north, self.region_south], [self.territory_a, self.territory_b, self.territory_c])
        self.map_2 = Map("TestMap", [self.region_north, self.region_south_2])
        self.players = [1,2,3]

    def test_region_reinforcements(self):
        self.assertEquals(get_region_reinforcements(1, self.map), ([],0))
        self.assertEquals(get_region_reinforcements(2, self.map), ([],0))
        self.assertEquals(get_region_reinforcements(3, self.map), (["South"], self.south_value))

        self.assertEquals(get_region_reinforcements(1, self.map_2), ([],0))
        self.assertEquals(get_region_reinforcements(2, self.map_2), ([],0))
        self.assertEquals(get_region_reinforcements(3, self.map_2), (["South"], self.south_value))

    def test_territory_reinforcements(self):
        self.assertEquals(get_territory_reinforcements(1, self.map), (1,3))
        self.assertEquals(get_territory_reinforcements(2, self.map), (1,3))
        self.assertEquals(get_territory_reinforcements(3, self.map), (1,3))

        self.assertEquals(get_territory_reinforcements(1, self.map_2), (1,3))
        self.assertEquals(get_territory_reinforcements(2, self.map_2), (1,3))
        self.assertEquals(get_territory_reinforcements(3, self.map_2), (13,4))






