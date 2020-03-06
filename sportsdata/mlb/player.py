import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS


class Player:
    """
    MLB player.

    Parameters
    ----------
    player_data : dict
        Dict that contains player information.

    season : int
        Season associated with the player's data.
    """
    def __init__(self, player_data, season):
        self._mlb_player_id = None
        self._season = None
        self._full_name = None
        self._first_name = None
        self._last_name = None
        self._birth_date = None
        self._player_height = None
        self._player_weight = None
        self._mlb_team_id = None
        self._position = None
        self._debut_date = None
        self._bat_side = None
        self._pitch_hand = None

        self._parse_player(player_data, season)

    def _parse_player(self, player, season):
        setattr(self, '_mlb_player_id', player['id'])
        setattr(self, '_season', season)
        setattr(self, '_full_name', player['fullName'])
        setattr(self, '_first_name', player['firstName'])
        setattr(self, '_last_name', player['lastName'])
        setattr(self, '_birth_date', player['birthDate'])
        setattr(self, '_player_height', player['height'])
        setattr(self, '_player_weight', player['weight'])
        if 'id' in player['currentTeam']:
            setattr(self, '_mlb_team_id', player['currentTeam']['id'])
        setattr(self, '_position', player['primaryPosition']['abbreviation'])
        setattr(self, '_debut_date', player['mlbDebutDate'])
        setattr(self, '_bat_side', player['batSide']['code'])
        setattr(self, '_pitch_hand', player['pitchHand']['code'])

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbPlayerId': self._mlb_player_id,
            'Season': self._season,
            'FullName': self._full_name,
            'FirstName': self._first_name,
            'LastName': self._last_name,
            'BirthDate': self._birth_date,
            'PlayerHeight': self._player_height,
            'PlayerWeight': self._player_weight,
            'MlbTeamId': self._mlb_team_id,
            'Position': self._position,
            'DebutDate': self._debut_date,
            'BatSide': self._bat_side,
            'PitchHand': self._pitch_hand,
        }
        return pd.DataFrame([fields_to_include], index=[self._mlb_player_id])


class Players:
    """
    Get MLB players

    Parameters
    ----------
    season : int
        Season to get players from.
    """
    def __init__(self, season):
        self._players = []

        self._get_players(season)

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_players(self, season):
        url = f'https://statsapi.mlb.com/api/v1/sports/1/players?season={season}'
        #print('Getting games from ' + url)
        players = requests.get(url, verify=VERIFY_REQUESTS).json()
        for person in players['people']:
            player = Player(person, season)
            self._players.append(player)

    @property
    def dataframes(self):
        frames = []
        for player in self.__iter__():
            frames.append(player.dataframe)
        return pd.concat(frames)
