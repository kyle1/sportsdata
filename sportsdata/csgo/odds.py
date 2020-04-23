import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime


class MatchOdds:
    """
    GMatch-level betting information for an individual CSGO match.

    Parameters
    ----------
    event : dict
        Dict that contains the betting event data.
    """

    def __init__(self, odds):
        self._event_description = None
        self._event_start_time = None
        self._team1_name = None
        self._team1_moneyline_odds_american = None
        self._team1_moneyline_odds_decimal = None
        self._team1_handicap = None
        self._team2_name = None
        self._team2_moneyline_odds_american = None
        self._team2_moneyline_odds_decimal = None
        self._team2_handicap = None
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
                    if market['description'] == 'Moneyline' and market['period']['description'] == 'Game':
                        self._get_moneyline(market)
                    if market['description'] == 'Point Spread' and market['period']['description'] == 'Game':
                        self._get_point_spread(market)
                    if market['description'] == 'Total' and market['period']['description'] == 'Game':
                        self._get_totals(market)

    def _get_moneyline(self, market):
        for outcome in market['outcomes']:
            if outcome['type'] == 'A':
                setattr(self, '_team1_name', outcome['description'])
                setattr(self, '_team1_moneyline_odds_american', outcome['price']['american'])
                setattr(self, '_team1_moneyline_odds_decimal', outcome['price']['decimal'])
            if outcome['type'] == 'H':
                setattr(self, '_team2_name', outcome['description'])
                setattr(self, '_team2_moneyline_odds_american', outcome['price']['american'])
                setattr(self, '_team2_moneyline_odds_decimal', outcome['price']['decimal'])

    def _get_point_spread(self, market):
        for outcome in market['outcomes']:
            if outcome['type'] == 'A':
                setattr(self, '_team1_handicap', outcome['price']['handicap'])
            if outcome['type'] == 'H':
                setattr(self, '_team2_handicap', outcome['price']['handicap'])

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
            'Team1Name': self._team1_name,
            'Team1MoneylineOddsAmerican': self._team1_moneyline_odds_american,
            'Team1MoneylineOddsDecimal': self._team1_moneyline_odds_decimal,
            'Team1Handicap': self._team1_handicap,
            'Team2Name': self._team2_name,
            'Team2MoneylineOddsAmerican': self._team2_moneyline_odds_american,
            'Team2MoneylineOddsDecimal': self._team2_moneyline_odds_decimal,
            'Team2Handicap': self._team2_handicap,
            'OverUnder': self._over_under
        }
        return pd.DataFrame([fields_to_include], index=[self._event_description])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        #dic['EventStartTime'] = dic['EventStartTime'].isoformat()
        return dic


class MatchesOdds:
    """
    Match-level betting information for multiple CSGO matches.

    Parameters
    ----------
    None
    """

    def __init__(self):
        self._odds = []

        self._get_odds()

    def __repr__(self):
        return self._odds

    def __iter__(self):
        return iter(self.__repr__())

    def _get_odds(self):
        url = 'https://www.bovada.lv/services/sports/event/v2/events/A/description/esports'
        print('Getting odds from ' + url)
        odds_json = requests.get(url, verify=VERIFY_REQUESTS).json()
        if len(odds_json) == 0:
            print(f'No CSGO odds found.')
            return

        # Bovada's esports odds url contains data for games other than CSGO. Get CSGO objects.
        csgo_items = []
        for item in odds_json:
            description = item['path'][0]['description'].upper()
            if 'CS:GO' in description or 'CSGO' in description or 'COUNTER-STRIKE' in description:
                csgo_items.append(item)

        print(len(csgo_items))

        for item in csgo_items:
            for event in item['events']:
                if event['type'] != 'GAMEEVENT' or datetime.fromtimestamp(event['startTime']/1000) < datetime.now():
                    # Skip odds that are not for match-level events. Skip odds for matches in the past.
                    continue
                odds = MatchOdds(event)
                if odds._team1_name is not None:  # todo?
                    self._odds.append(odds)

    @property
    def dataframes(self):
        frames = []
        for odds in self.__iter__():
            frames.append(odds.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for odds in self.__iter__():
            dics.append(odds.to_dict)
        return dics
