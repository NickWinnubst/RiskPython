

# get the total amount of reinforcements
def get_reinforcements(player_id, map):
    _, territory_armies = get_territory_reinforcements(player_id,map)
    _, region_armies = get_region_reinforcements(player_id, map)

    return territory_armies + region_armies


# get the amount of reinforcement given by the current amount of territories for a specific player
# return: the amount of territories and the reinforcements gotten from this.
def get_territory_reinforcements(player_id, map):
    territories = 0
    for region in map.regions:
        for territory in region.territories:
            territories += (territory.owner == player_id)*1

    return territories, max(3,int(territories/3))


# get the amount of reinforcement given by the controlled regions for a specific player
# return: the controlled regions and the reinforcements gotten from this.
def get_region_reinforcements(player_id, map):
    regions_owned = []
    region_reinforcements = 0

    for region in map.regions:
        region_owned = True
        for territory in region.territories:
            if territory.owner != player_id:
                region_owned = False
                break

        if not region_owned:
            continue

        regions_owned.append(region.name)
        region_reinforcements += region.value

    return regions_owned, region_reinforcements
