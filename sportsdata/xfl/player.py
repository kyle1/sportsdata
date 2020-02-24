# TODO: setup nba player classes
import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from constants import ROSTER_URLS
from pyquery import PyQuery as pq
from time import sleep


class Player:
    def __init__(self, tr, team_id):
        self._xfl_player_id = None
        self._full_name = None
        self._player_height = None
        self._player_weight = None
        self._xfl_team_id = None
        self._position = None
        self._jersey_number = None
        self._college = None

        self._set_player(tr, team_id)

    def _set_player(self, tr, team_id):
        # Determine if row has first name and last name as one column or two columns.
        td_list = list(tr('td').items())
        separate_name_cols = len(td_list) == 7
        setattr(self, '_jersey_number', td_list[0].text())
        if separate_name_cols:
            name = td_list[1].text() + ' ' + td_list[2].text()
            offset = 1
        else:
            name = td_list[1].text()
            offset = 0
        setattr(self, '_full_name', name)
        setattr(self, '_position', td_list[2 + offset].text())
        setattr(self, '_player_height', td_list[3 + offset].text())
        setattr(self, '_player_weight', td_list[4 + offset].text())
        setattr(self, '_college', td_list[5 + offset].text())
        setattr(self, '_xfl_team_id', team_id)

    @property
    def dataframe(self):
        fields_to_include = {
            'XflPlayerId': self._xfl_player_id,
            'FullName': self._full_name,
            'Position': self._position,
            'PlayerHeight': self._player_height,
            'PlayerWeight': self._player_weight,
            'XflTeamId': self._xfl_team_id,
            'JerseyNumber': self._jersey_number,
            'College': self._college
        }
        return pd.DataFrame([fields_to_include], index=[self._xfl_player_id])


class Players:
    def __init__(self):
        self._players = []

        self._get_players()

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_players(self):
        for roster in ROSTER_URLS:
            roster_html = pq(roster['url'])
            table = list(roster_html('table').items())[0]
            first_row = True
            for tr in table('tr').items():
                if first_row:
                    first_row = False
                    continue
                player = Player(tr, roster['team_id'])
                self._players.append(player)

    @property
    def dataframes(self):
        frames = []
        for player in self.__iter__():
            frames.append(player.dataframe)
        return pd.concat(frames)
