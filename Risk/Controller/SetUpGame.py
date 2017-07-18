import random


# set up a new game with random territory and troop assignment
def set_up_game(players, map):

    initialized_map, starting_player, remaining_armies = randomly_initialize_territories(players, map)
    final_map = randomly_place_remaining_armies(players, initialized_map, starting_player, remaining_armies)

    return final_map


# randomly assign territories on the map to the players
# return: the new map, the starting players, and the armies that still need to be placed
def randomly_initialize_territories(players, map):
    map_size = map.territories.size()
    player_count = players.size()

    list_of_territories = random.shuffle(range(0, map_size+1))

    # assign territories for each player
    for player in players:
        for i in range(0,int(map_size/player_count)):
            map.territories[list_of_territories.pop()].set_owner(player, 1)

    # assign the leftover territories
    assigned_players = players
    for remaining in list_of_territories:
        map.territories[remaining].set_owner(assigned_players.pop(), 1)

    # determine the starting player
    starting_player = assigned_players.pop()

    # determine the remaining armies
    remaining_armies = map.army_sizes[players.size()-1] - int(map_size/player_count) - int(assigned_players.size()/players.size()) + 1

    return map, starting_player, remaining_armies


# randomly place remaining armies
def randomly_place_remaining_armies(players, map, starting_player, remaining_armies):

    if starting_player != players[0]:
        randomly_place_remaining_armies(players[1:], map, starting_player, 1)

    for player in players:
        for i in range(0,remaining_armies):
            randomly_place_army(player, map)

    return map


# randomly place an army on a player owned territory
def randomly_place_army(player, map):

    map_size = map.territories.size()
    list_of_territories = random.shuffle(range(0, map_size+1))

    for territory in list_of_territories:
        if map.territories[territory].owner == player:
            map.territories[territory].armies += 1
            break
