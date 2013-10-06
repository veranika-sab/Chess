from django.utils.functional import empty

players_elo_ratings = {1: 11, 2: 22, 3: 33, 4: 44, 5: 55, 6: 66, 7: 77, 8: 88, 9: 99, 10: 111, 11: 112}
players_ids_and_points_in_tournament = {1: 0.5, 2: 2.5, 3: 2.5, 4: 2, 5: 1, 6: 1.5, 7: 1, 8: 0, 9: 0, 10: 0, 11: 99}

def generate_pairs(players_elo_ratings, players_ids_and_points_in_tournament):
    points_group_list = sorted(set(players_ids_and_points_in_tournament.values()), reverse=True)

    players_list_grouped_by_points = [[] for all in points_group_list] # create empty lists for point groups

    for player_id, player_points in players_ids_and_points_in_tournament.items(): # add players to groups
        players_list_grouped_by_points[points_group_list.index(player_points)].append(player_id)

    for index, point_group in enumerate(players_list_grouped_by_points): # sort players in point groups
        point_group.sort(key = lambda x: players_elo_ratings[x], reverse=True)
        if len(point_group) % 2 == 1: # move player to lower point group if not odd number of players
            if index+1 < len(players_list_grouped_by_points):
                players_list_grouped_by_points[index+1].append(point_group.pop())
            else:
                point_group.append(None)
    print players_list_grouped_by_points
    pairs = []
    for point_group in players_list_grouped_by_points:
        for player in point_group:
            if point_group:
                pair = [point_group.pop(), point_group.pop()]
                pairs.append(pair)
    print pairs
    return pairs

generate_pairs(players_elo_ratings, players_ids_and_points_in_tournament)