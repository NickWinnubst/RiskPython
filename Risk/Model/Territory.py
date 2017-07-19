

# This class defines the Territory objects, which govern the a single territory.
# This class describes it's name, owner, army occupation, and connections.
class Territory(object):

    name = "NaN"
    owner = 0
    armies = 0
    connections = []

    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def set_owner(self, new_owner, army_count):
        self.owner = new_owner
        self.armies = army_count