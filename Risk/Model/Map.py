

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
        print("*********************")
