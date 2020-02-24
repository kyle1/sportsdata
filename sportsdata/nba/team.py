import pandas as pd
import requests
#from ..constants import VERIFY_REQUESTS
from nba.constants import NBA_API_TEAMS


class Team:
    def __init__(self, team):
        self._nba_team_id = None
        self._team_name = None
        #self._nba_venue_id = None
        self._simple_name = None
        self._team_abbreviation = None
        self._location_name = None
        #self._nba_conference_id = None
        #self._nba_division_id = None

        self._set_team(team)

    def _set_team(self, team):
        setattr(self, '_nba_team_id', team['team_id'])
        setattr(self, '_team_name', team['team_name'])
        #setattr(self, '_nba_venue_id', team['venue']['id']) #TODO
        setattr(self, '_simple_name', team['simple_name'])
        setattr(self, '_team_abbreviation', team['abbreviation'])
        setattr(self, '_location_name', team['location'])
        # setattr(self, '_nba_conference_id', team['conference']['id'])
        # setattr(self, '_nba_division_id', team['division']['id'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NbaTeamId': self._nba_team_id,
            'TeamName': self._team_name,
            #'NbaVenueId': self._mlb_venue_id,
            'SimpleName': self._simple_name,
            'TeamAbbreviation': self._team_abbreviation,
            'LocationName': self._location_name,
            #'NbaConferenceId': self._nba_conference_id,
            #'NbaDivisionId': self._nba_division_id
        }
        return pd.DataFrame([fields_to_include], index=[self._nba_team_id])


class Teams:
    def __init__(self):
        self._teams = []

        self._get_teams()

    def __repr__(self):
        return self._teams

    def __iter__(self):
        return iter(self.__repr__())

    def _get_teams(self):
        for team_json in NBA_API_TEAMS:
            team = Team(team_json)
            self._teams.append(team)

    @property
    def dataframes(self):
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)
