import random


# set up a new game with random territory and troop assignment
def set_up_game(players, new_map):

    initialized_map, starting_player, remaining_armies = randomly_initialize_territories(players, new_map)
    final_map = randomly_place_remaining_armies(players, initialized_map, starting_player, remaining_armies)
    last_player = len(final_map.get_all_territories())*final_map.army_sizes[len(players)-1] % len(players)

    return final_map, last_player


# randomly assign territories on the map to the players
# return: the new map, the starting players, and the armies that still need to be placed
def randomly_initialize_territories(players, game_map):
    map_size = len(game_map.get_all_territories())
    player_count = len(players)

    list_of_territories = random.sample(list(range(map_size)),map_size)

    # assign territories for each player
    for player in players:
        for i in range(0,int(map_size/player_count)):
            game_map.get_all_territories()[list_of_territories.pop()].set_owner(player, 1)

    # assign the leftover territories
    assigned_players = list(players)
    for remaining in list_of_territories:
        game_map.get_all_territories()[remaining].set_owner(assigned_players.pop(), 1)

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

    return game_map


# randomly place an army on a player owned territory
def randomly_place_army(player, game_map):

    map_size = len(game_map.get_all_territories())
    list_of_territories = random.sample(list(range(map_size)),map_size)

    for territory in list_of_territories:
        if game_map.get_all_territories()[territory].owner == player:
            game_map.get_all_territories()[territory].armies += 1
            break
