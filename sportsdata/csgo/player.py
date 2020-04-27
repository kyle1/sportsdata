import pandas as pd
import requests
from pyquery import PyQuery as pq


class Player:
    """
    CSGO Player.

    Parameters
    ----------
    tr : dict
        HTML table row that is parsed for player data.
    """

    def __init__(self, tr):
        self._csgo_player_id = None
        self._player_name = None
        self._csgo_team_id = None

        self._parse_player(tr)

    def _parse_player(self, tr):
        for td in tr('td').items():
            if 'player' in td.attr['class']:
                player_name = td.text()
                setattr(self, '_player_name', player_name)
                for a in td('a').items():
                    player_url = a.attr['href']
                    player_id = player_url.split('/')[3]
                    setattr(self, '_csgo_player_id', player_id)
                # print(player_name)
            if 'team' in td.attr['class']:
                for a in td('a').items():
                    team_url = a.attr['href']
                    team_id = team_url.split('/')[3]
                    setattr(self, '_csgo_team_id', team_id)
                    # The first team listed is the player's current team
                    break

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoPlayerId': self._csgo_player_id,
            'PlayerName': self._player_name,
            'CsgoTeamId': self._csgo_team_id,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Players:
    """
    CSGO players.

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
        url = 'https://www.hltv.org/stats/players?startDate=all'
        players_html = pq(url, verify=False)
        #players_html = requests.get(url, verify=False).content
        for table in players_html('table').items():
            first_row = True
            for tr in table('tr').items():
                if first_row:
                    first_row = False
                    continue
                player = Player(tr)
                self._players.append(player)

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
