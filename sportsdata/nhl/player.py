import pandas as pd
import requests
# from ..constants import VERIFY_REQUESTS


class Player:
    def __init__(self, player_data, nhl_team_id):
        self._nhl_player_id = None
        self._full_name = None
        self._first_name = None
        self._last_name = None
        self._birth_date = None
        self._player_height = None
        self._player_weight = None
        self._nhl_team_id = None
        self._position = None
        self._debut_date = None
        self._bat_side = None
        self._pitch_hand = None

        self._set_player(player_data, nhl_team_id)

    def _set_player(self, player, nhl_team_id):
        setattr(self, '_nhl_player_id', player['person']['id'])
        setattr(self, '_full_name', player['person']['fullName'])
        #setattr(self, '_first_name', player['firstName'])
        #setattr(self, '_last_name', player['lastName'])
        #setattr(self, '_birth_date', player['birthDate'])
        #setattr(self, '_player_height', player['height'])
        #setattr(self, '_player_weight', player['weight'])
        setattr(self, '_nhl_team_id', nhl_team_id)
        setattr(self, '_position', player['position']['abbreviation'])
        #setattr(self, '_debut_date', player['mlbDebutDate'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlPlayerId': self._nhl_player_id,
            'FullName': self._full_name,
            # 'FirstName': self._first_name,
            # 'LastName': self._last_name,
            # 'BirthDate': self._birth_date,
            # 'PlayerHeight': self._player_height,
            # 'PlayerWeight': self._player_weight,
            'NhlTeamId': self._nhl_team_id,
            'Position': self._position,
            # 'DebutDate': self._debut_date
        }
        return pd.DataFrame([fields_to_include], index=[self._nhl_player_id])


class Players:
    def __init__(self):
        self._players = []

        self._get_players()

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_players(self):
        # TODO- refer to https://github.com/dword4/nhlapi#teams
        url = f'https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster'
        # print('Getting games from ' + url)
        teams = requests.get(url, verify=False).json()
        for team in teams['teams']:
            nhl_team_id = team['id']
            for person in team['roster']['roster']:
                player = Player(person, nhl_team_id)
                self._players.append(player)

    @property
    def dataframes(self):
        frames = []
        for player in self.__iter__():
            frames.append(player.dataframe)
        return pd.concat(frames)
