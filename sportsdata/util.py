from datetime import datetime


def get_season_by_date_range(date_strings, seasons):
    begin = datetime.strptime(date_strings[0], '%m/%d/%Y')
    end = datetime.strptime(date_strings[1], '%m/%d/%Y')
    for season in seasons:
        if begin >= datetime.strptime(season['start_date'], '%m/%d/%Y') and end <= datetime.strptime(season['end_date'], '%m/%d/%Y'):
            return season['season']
    print('Unable to find season for the specified date range')
    return None


def get_season_by_date(date_string, seasons):
    date = datetime.strptime(date_string, '%m/%d/%Y')
    for season in seasons:
        if date >= datetime.strptime(season['start_date'], '%m/%d/%Y') and date <= datetime.strptime(season['end_date'], '%m/%d/%Y'):
            return season['season']
    print('Unable to find season for the specified date range')
    return None


def get_start_and_end_dates_by_season(season, seasons):
    for season in seasons:
        if season['season'] == args.season:
            return season['start_date'], season['end_date']
    print('Unable to find start and end dates for ' + season)


def set_odds(GameOdds, odds):
    setattr(GameOdds, '_event_description', odds['description'])
    setattr(GameOdds, '_event_start_time', datetime.fromtimestamp(odds['startTime']/1000))

    # Game Lines, Alternative Lines, Score Props, etc.
    for display_group in odds['displayGroups']:
        if display_group['description'] == 'Game Lines':
            # Moneyline, Point Spread, Total
            for market in display_group['markets']:
                if market['description'] == 'Moneyline' and market['period']['description'] == 'Match':
                    get_moneyline(GameOdds, market)
                if market['description'] in ['Point Spread', 'Puck Line'] and market['period']['description'] == 'Match':
                    get_point_spread(GameOdds, market)
                if market['description'] == 'Total' and market['period']['description'] == 'Match':
                    get_totals(GameOdds, market)


def get_moneyline(GameOdds, market):
    for outcome in market['outcomes']:
        if outcome['type'] == 'A':
            setattr(GameOdds, '_away_team_name', outcome['description'])
            setattr(GameOdds, '_away_moneyline_american', outcome['price']['american'])
            setattr(GameOdds, '_away_moneyline_decimal', outcome['price']['decimal'])
        if outcome['type'] == 'H':
            setattr(GameOdds, '_home_team_name', outcome['description'])
            setattr(GameOdds, '_home_moneyline_american', outcome['price']['american'])
            setattr(GameOdds, '_home_moneyline_decimal', outcome['price']['decimal'])


def get_point_spread(GameOdds, market):
    for outcome in market['outcomes']:
        if outcome['type'] == 'A':
            setattr(GameOdds, '_away_handicap', outcome['price']['handicap'])
        if outcome['type'] == 'H':
            setattr(GameOdds, '_home_handicap', outcome['price']['handicap'])


def get_totals(GameOdds, market):
    for outcome in market['outcomes']:
        if outcome['description'] == 'Over':
            # totals['Over'] = outcome['price']['handicap']
            setattr(GameOdds, '_over_under', outcome['price']['handicap'])
        # if outcome['description'] == 'Under':
            # totals['Under'] = outcome['price']['handicap']
