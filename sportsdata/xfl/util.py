def get_game_ids_by_season_and_week(season, week):
    #todo- use season

    # Week 1 has game IDs 1 through 4
    # Week 2 has game IDS 5 through 8 ...
    game_ids = []
    for i in range(1, 5):
        game_id = (week - 1) * 4 + i
        game_ids.append(game_id)
    return game_ids