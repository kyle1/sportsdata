import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS


class Team:
    """
    MLB team.

    Parameters
    ----------
    team : dict
        Dict that contains team information.
    """
    def __init__(self, team):
        self._mlb_team_id = None
        self._team_name = None
        self._mlb_venue_id = None
        self._team_code = None
        self._team_abbreviation = None
        self._location_name = None
        self._mlb_league_id = None
        self._mlb_division_id = None

        self._set_team(team)

    def _set_team(self, team):
        setattr(self, '_mlb_team_id', team['id'])
        setattr(self, '_team_name', team['teamName'])
        setattr(self, '_mlb_venue_id', team['venue']['id'])
        setattr(self, '_team_code', team['teamCode'])
        setattr(self, '_team_abbreviation', team['abbreviation'])
        setattr(self, '_location_name', team['locationName'])
        setattr(self, '_mlb_league_id', team['league']['id'])
        setattr(self, '_mlb_division_id', team['division']['id'])

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbTeamId': self._mlb_team_id,
            'TeamName': self._team_name,
            'MlbVenueId': self._mlb_venue_id,
            'TeamCode': self._team_code,
            'TeamAbbreviation': self._team_abbreviation,
            'LocationName': self._location_name,
            'MlbLeagueId': self._mlb_league_id,
            'MlbDivisionId': self._mlb_division_id
        }
        return pd.DataFrame([fields_to_include], index=[self._mlb_team_id])


class Teams:
    """
    MLB teams.

    Parameters
    ----------
    None
    """
    def __init__(self):
        self._teams = []

        self._get_teams()

    def __repr__(self):
        return self._teams

    def __iter__(self):
        return iter(self.__repr__())

    def _get_teams(self):
        url = f'https://statsapi.mlb.com/api/v1/teams?sportId=1'
        #print('Getting games from ' + url)
        teams = requests.get(url, verify=VERIFY_REQUESTS).json()
        for team_json in teams['teams']:
            team = Team(team_json)
            self._teams.append(team)

    @property
    def dataframes(self):
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)
