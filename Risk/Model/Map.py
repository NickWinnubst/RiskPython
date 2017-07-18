class Map:

    name = "NaN"
    regions = []
    territories = []
    army_sizes = []

    def __init__(self, name, regions, territories, army_sizes):
        self.name = name
        self.regions = regions
        self.territories = territories
        self.army_sizes = army_sizes
