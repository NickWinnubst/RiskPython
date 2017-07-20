import json
from Model.Map import Map
from Model.Region import Region
from Model.Territory import Territory


# load in map files from JSON format
def load_fresh_map(path):

    regions = []

    with open(path) as file:
        data = json.loads(file.read())

        for region in data['regions']:
            territories = []
            for territory in region['territories']:
                territories.append(Territory(territory['name'],territory['connections'],territory['location']))
            regions.append(Region(region['name'],region['value'],territories))

        try:
            game_map = Map(data['name'], regions, data['army_sizes'])
        except KeyError:
            game_map = Map(data['name'], regions)

    return game_map

