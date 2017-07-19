

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

    def get_territory(self, name):
        for region in self.regions:
            for territory in region.territories:
                if territory.name == name:
                    return territory

        return None
