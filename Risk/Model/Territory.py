class Territory:

    name = "NaN"
    region = "NaN"
    owner = 0
    armies = 0
    connections = []

    def __init__(self, name, region, connections):
        self.name = name
        self.region = region
        self.connections = connections

    def set_owner(self, new_owner, army_count):
        self.owner = new_owner
        self.armies = army_count