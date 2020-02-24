from constants import MLB_SEASONS


def get_dates_by_season(season):
    for dates in MLB_SEASONS:
        if dates['season'] == season:
            start_date = dates['start_date']
            end_date = dates['end_date']
            break
    return start_date, end_date


def get_missing_players(new_players, existing_players):
    new_players_upper = []
    for player in new_players:
        if 'BirthDate' in player:
            del player['BirthDate']
        if 'DebutDate' in player:
            del player['DebutDate']
        new_players_upper.append({k.upper(): v for k, v in player.items()})

    existing_players_upper = []
    for player in existing_players:
        if 'battingOrder' in player:
            del player['battingOrder']
        if 'teamAbbrev' in player:
            del player['teamAbbrev']
        if 'birthDate' in player:
            del player['birthDate']
        if 'debutDate' in player:
            del player['debutDate']
        existing_players_upper.append({k.upper(): v for k, v in player.items()})

    missing_players = [p for p in new_players_upper if p not in existing_players_upper]

    return missing_players
