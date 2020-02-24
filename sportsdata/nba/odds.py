import pandas as pd
import requests
#from ..constants import VERIFY_REQUESTS
from datetime import datetime


class GameOdds:
    def __init__(self, odds):
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

    def _set_odds(self, odds):
        setattr(self, '_event_description', odds['description'])
        setattr(self, '_event_start_time', datetime.fromtimestamp(odds['startTime']/1000).isoformat())

        # Game Lines, Alternative Lines, Score Props, etc.
        for display_group in odds['displayGroups']:
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
                setattr(self, '_away_moneyline_odds_american', outcome['price']['american'])
                setattr(self, '_away_moneyline_odds_decimal', outcome['price']['decimal'])
            if outcome['type'] == 'H':
                setattr(self, '_home_team_name', outcome['description'])
                setattr(self, '_home_moneyline_odds_american', outcome['price']['american'])
                setattr(self, '_home_moneyline_odds_decimal', outcome['price']['decimal'])

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
    def __init__(self):
        self._odds = []

        self._get_odds()

    def __repr__(self):
        return self._odds

    def __iter__(self):
        return iter(self.__repr__())

    def _get_odds(self):
        url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba'
        print('Getting odds from ' + url)
        odds_json = requests.get(url, verify=False).json()
        if len(odds_json) == 0:
            print(f'No NHL odds found.')
            return
        for event in odds_json[0]['events']:
            if event['type'] != 'GAMEEVENT' or datetime.fromtimestamp(event['startTime']/1000) < datetime.now():
                # Skip odds for season-long bets (i.e. Atlantic Division - Odds to Win)
                continue
            odds = GameOdds(event)
            if odds._away_team_name is not None:  # todo?
                self._odds.append(odds)

    @property
    def dataframes(self):
        frames = []
        for odds in self.__iter__():
            frames.append(odds.dataframe)
        return pd.concat(frames)
