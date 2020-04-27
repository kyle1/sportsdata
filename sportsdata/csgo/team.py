import pandas as pd
import requests
from pyquery import PyQuery as pq


class Team:
    """
    CSGO Team.

    Parameters
    ----------
    tr : dict
        HTML table row that is parsed for team data.
    """

    def __init__(self, tr):
        self._team_id = None
        self._team_name = None

        self._parse_team(tr)

    def _parse_team(self, tr):
        for td in tr('td').items():
            if 'teamCol-teams-overview' in td.attr['class']:
                setattr(self, '_team_name', td.text())
                for a in td('a').items():
                    team_url = a.attr['href']
                    team_id = team_url.split('/')[3]
                    setattr(self, '_csgo_team_id', team_id)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoTeamId': self._csgo_team_id,
            'TeamName': self._team_name,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Teams:
    """
    CSGO teams.

    Parameters
    ----------
    None
    """

    def __init__(self):
        self._teams = []

        self._get_teams()

    def _get_teams(self):
        url = 'https://www.hltv.org/stats/teams'
        teams_html = pq(url, verify=False)
        #teams_html = requests.get(url, verify=False)

        for table in teams_html('table').items():
            # print(table)
            first_row = True
            for tr in table('tr').items():
                if first_row:
                    first_row = False
                    continue
                team = Team(tr)
                self._teams.append(team)

    def __repr__(self):
        return self._teams

    def __iter__(self):
        return iter(self.__repr__())

    @property
    def dataframes(self):
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for team in self.__iter__():
            dics.append(team.to_dict)
        return dics
