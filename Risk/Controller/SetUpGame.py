import random


# set up a new game with random territory and troop assignment
def set_up_game(players, new_map):

    initialized_map, starting_player, remaining_armies = randomly_initialize_territories(players, new_map)
    final_map = randomly_place_remaining_armies(players, initialized_map, starting_player, remaining_armies)

    return final_map


# randomly assign territories on the map to the players
# return: the new map, the starting players, and the armies that still need to be placed
def randomly_initialize_territories(players, game_map):
    map_size = len(game_map.territories)
    player_count = len(players)

    list_of_territories = random.shuffle(range(0, map_size+1))

    # assign territories for each player
    for player in players:
        for i in range(0,int(map_size/player_count)):
            game_map.territories[list_of_territories.pop()].set_owner(player, 1)

    # assign the leftover territories
    assigned_players = players
    for remaining in list_of_territories:
        game_map.territories[remaining].set_owner(assigned_players.pop(), 1)

    # determine the starting player
    starting_player = assigned_players.pop()

    # determine the remaining armies
    remaining_armies = game_map.army_sizes[len(players) - 1] - int(map_size / player_count) - int(len(assigned_players) / player_count) + 1

    return game_map, starting_player, remaining_armies


# randomly place remaining armies
def randomly_place_remaining_armies(players, game_map, starting_player, remaining_armies):

    if starting_player != players[0]:
        randomly_place_remaining_armies(players[1:], game_map, starting_player, 1)

    for player in players:
        for i in range(0,remaining_armies):
            randomly_place_army(player, game_map)

    return map


# randomly place an army on a player owned territory
def randomly_place_army(player, game_map):

    map_size = len(game_map.territories)
    list_of_territories = random.shuffle(range(0, map_size+1))

    for territory in list_of_territories:
        if game_map.territories[territory].owner == player:
            game_map.territories[territory].armies += 1
            break
