

# This class defines the Region objects, which govern a region and own it's internal territories.
class Region(object):

    name = "NaN"
    value = 0
    territories = []

    def __init__(self, name, value, territories):
        self.name = name
        self.value = value
        self.territories = territories
