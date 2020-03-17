import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from constants import NBA_API_TEAMS, PROXIES, NBA_REQUEST_HEADERS
from time import sleep


class Player:
    """
    NBA player.

    Parameters
    ----------
    player_data : list
        List that contains player stat values.

    stat_headers : list
        List that contains player stat categories.

    team_id : int
        The ID belonging to the player's NBA team, according to NBA's API.
    """
    def __init__(self, player_data, stat_headers, team_id):
        self._nba_player_id = None
        self._full_name = None
        self._first_name = None
        self._last_name = None
        self._birth_date = None
        self._player_height = None
        self._player_weight = None
        self._nba_team_id = None
        self._position = None
        self._debut_date = None

        self._parse_player(player_data, stat_headers)

    def _parse_player(self, player_data, stat_headers, team_id):
        player = {}
        for i in range(len(stat_headers)):
            player[stat_headers[i]] = player_data[i]
        setattr(self, '_nba_player_id', player['PLAYER_ID'])
        setattr(self, '_full_name', player['PLAYER'])
        setattr(self, '_birth_date', player['BIRTH_DATE'].replace(',', '').replace('"', ''))
        setattr(self, '_player_height', player['HEIGHT'])
        setattr(self, '_player_weight', player['WEIGHT'])
        setattr(self, '_nba_team_id', team_id)
        setattr(self, '_position', player['POSITION'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NbaPlayerId': self._nba_player_id,
            'FullName': self._full_name,
            # 'FirstName': self._first_name,
            # 'LastName': self._last_name,
            'BirthDate': self._birth_date,
            'PlayerHeight': self._player_height,
            'PlayerWeight': self._player_weight,
            'NbaTeamId': self._nba_team_id,
            'Position': self._position,
            # 'DebutDate': self._debut_date
        }
        return pd.DataFrame([fields_to_include], index=[self._nba_player_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Players:
    """
    NBA players.

    Parameters
    ----------
    None
    """
    def __init__(self):
        self._players = []

        self._get_players()

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_players(self):
        for team in NBA_API_TEAMS:
            url = f'https://stats.nba.com/stats/commonteamroster?LeagueID=&Season=2019-20&TeamID={team["team_id"]}'
            print(f'Getting roster from {url}')
            roster = requests.get(url, PROXIES, headers=NBA_REQUEST_HEADERS, timeout=10, verify=VERIFY_REQUESTS).json()
            for person in roster['resultSets']:
                if person['name'] != 'CommonTeamRoster':
                    # Skip coaches
                    continue
                stat_headers = results['headers']
                player_rows = results['rowSet']
                for player_row in player_rows:
                    player = Player(player_row, stat_headers)
                    self._players.append(player)
            sleep(3)

    @property
    def dataframes(self):
        frames = []
        for player in self.__iter__():
            frames.append(player.dataframe)
        return pd.concat(frames)
        
    @property
    def to_dicts(self):
        dics = []
        for player in self.__iter__():
            dics.append(player.to_dict)
        return dics