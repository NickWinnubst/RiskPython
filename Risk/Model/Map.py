from Model.Territory import *

# This class defines the Map objects, which govern the whole map and own it's internal regions.
# This also contain the allowed army sizes for the map.
class Map(object):

    name = "NaN"
    regions = []
    army_sizes = []

    def __init__(self, name, regions, army_sizes = [0, 40, 35, 30, 25, 20]):
        self.name = name
        self.regions = regions
        self.army_sizes = army_sizes

    def get_all_territories(self):
        territories = []
        for region in self.regions:
            for territory in region.territories:
                territories.append(territory)
        return territories

    def get_territory(self, name):
        for region in self.regions:
            for territory in region.territories:
                if territory.name == name:
                    return territory

        return None

    def has_a_territory(self,player):
        for territory in self.get_all_territories():
            if territory.owner == player:
                return True
        return False

    def get_closest_territory(self,location):

        # create an impossibly far territory
        closest = Territory("Null",location=[-100000,-100000])
        list_of_territories = self.get_all_territories()

        def squared_distance(point_a, point_b):
            return (point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2

        for territory in list_of_territories:
            if squared_distance(territory.location,location) < squared_distance(closest.location,location):
                closest = territory

        return closest


    def print(self):
        print("*********************")
        print("Map name: " + self.name)
        print("Army sizes: " + str(self.army_sizes))
        for reg in self.regions:
            print("*********************")
            print("Region name: " + reg.name)
            print("Region value: " + str(reg.value))
            for ter in reg.territories:
                print("-----------------------")
                print("Territory name: " + ter.name)
                print("Territory connections: " + str(ter.connections))
                print("Territory owner: " + str(ter.owner))
                print("Territory occupation: " + str(ter.armies))
                print("Territory location: " + str(ter.location))
        print("*********************")
