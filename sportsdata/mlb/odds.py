import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime


class GameOdds:
    """
    Game-level betting odds.

    Parameters
    ----------
    event : dict
        Dict that contains the betting event data.
    """

    def __init__(self, event):
        self._event_description = None
        self._event_start_time = None
        self._away_team_name = None
        self._away_moneyline_odds_american = None
        self._away_moneyline_odds_decimal = None
        self._away_handicap = None
        self._home_team_name = None
        self._home_moneyline_odds_american = None
        self._home_moneyline_odds_decimal = None
        self._home_handicap = None
        self._over_under = None

        self._set_odds(odds)

    def _set_odds(self, event):
        setattr(self, '_event_description', event['description'])
        setattr(self, '_event_start_time', datetime.fromtimestamp(event['startTime']/1000))

        # Game Lines, Alternative Lines, Score Props, etc.
        for display_group in event['displayGroups']:
            if display_group['description'] == 'Game Lines':
                # Moneyline, Point Spread, Total
                for market in display_group['markets']:
                    if market['description'] == 'Moneyline' and market['period']['description'] == 'Match':
                        self._get_moneyline(market)
                    if market['description'] in ['Point Spread', 'Puck Line'] and market['period']['description'] == 'Match':
                        self._get_point_spread(market)
                    if market['description'] == 'Total' and market['period']['description'] == 'Match':
                        self._get_totals(market)

    def _get_moneyline(self, market):
        for outcome in market['outcomes']:
            if outcome['type'] == 'A':
                setattr(self, '_away_team_name', outcome['description'])
                setattr(self, '_away_moneyline_american', outcome['price']['american'])
                setattr(self, '_away_moneyline_decimal', outcome['price']['decimal'])
            if outcome['type'] == 'H':
                setattr(self, '_home_team_name', outcome['description'])
                setattr(self, '_home_moneyline_american', outcome['price']['american'])
                setattr(self, '_home_moneyline_decimal', outcome['price']['decimal'])

    def _get_point_spread(self, market):
        for outcome in market['outcomes']:
            if outcome['type'] == 'A':
                setattr(self, '_away_handicap', outcome['price']['handicap'])
            if outcome['type'] == 'H':
                setattr(self, '_home_handicap', outcome['price']['handicap'])

    def _get_totals(self, market):
        for outcome in market['outcomes']:
            if outcome['description'] == 'Over':
                #totals['Over'] = outcome['price']['handicap']
                setattr(self, '_over_under', outcome['price']['handicap'])
            # if outcome['description'] == 'Under':
                #totals['Under'] = outcome['price']['handicap']

    @property
    def dataframe(self):
        fields_to_include = {
            'EventDescription': self._event_description,
            'EventStartTime': self._event_start_time,
            'AwayTeamName': self._away_team_name,
            'AwayMoneylineOddsAmerican': self._away_moneyline_odds_american,
            'AwayMoneylineOddsDecimal': self._away_moneyline_odds_decimal,
            'AwayHandicap': self._away_handicap,
            'HomeTeamName': self._home_team_name,
            'HomeMoneylineOddsAmerican': self._home_moneyline_odds_american,
            'HomeMoneylineOddsDecimal': self._home_moneyline_odds_decimal,
            'HomeHandicap': self._home_handicap,
            'OverUnder': self._over_under
        }
        return pd.DataFrame([fields_to_include], index=[self._event_description])


class GamesOdds:
    """
    Game-level betting odds for multiple games
    """

    def __init__(self):
        self._odds = []

        self._get_odds()

    def __repr__(self):
        return self._odds

    def __iter__(self):
        return iter(self.__repr__())

    def _get_odds(self):
        url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/baseball/mlb'
        print('Getting odds from ' + url)
        odds_json = requests.get(url, verify=VERIFY_REQUESTS).json()
        if len(odds_json) == 0:
            print(f'No NHL odds found.')
            return
        for event in odds_json[0]['events']:
            if event['type'] != 'GAMEEVENT':
                # Skip odds for season-long bets (i.e. Atlantic Division - Odds to Win)
                continue
            odds = GameOdds(event)
            self._odds.append(odds)

    @property
    def dataframes(self):
        frames = []
        for odds in self.__iter__():
            frames.append(odds.dataframe)
        return pd.concat(frames)
