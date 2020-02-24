import pandas as pd
import requests
#from ..constants import VERIFY_REQUESTS


class Team:
    def __init__(self, team):
        self._nhl_team_id = None
        self._team_name = None
        self._nhl_venue_id = None
        self._nhl_venue_name = None
        self._team_abbreviation = None
        self._location_name = None
        self._nhl_division_id = None
        self._nhl_conference_id = None

        self._set_team(team)

    def _set_team(self, team):
        setattr(self, '_nhl_team_id', team['id'])
        setattr(self, '_team_name', team['teamName'])
        setattr(self, '_nhl_venue_id', None if 'id' not in team['venue'] else team['venue']['id'])
        setattr(self, '_nhl_venue_name', team['venue']['name'])
        setattr(self, '_team_abbreviation', team['abbreviation'])
        setattr(self, '_location_name', team['locationName'])
        setattr(self, '_nhl_division_id', team['division']['id'])
        setattr(self, '_nhl_conference_id', team['conference']['id'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlTeamId': self._nhl_team_id,
            'TeamName': self._team_name,
            'NhlVenueId': self._nhl_venue_id,
            'NhlVenueName': self._nhl_venue_name,
            'TeamAbbreviation': self._team_abbreviation,
            'LocationName': self._location_name,
            'NhlDivisionId': self._nhl_division_id,
            'NhlConferenceId': self._nhl_conference_id
        }
        return pd.DataFrame([fields_to_include], index=[self._nhl_team_id])


class Teams:
    def __init__(self):
        self._teams = []

        self._get_teams()

    def __repr__(self):
        return self._teams

    def __iter__(self):
        return iter(self.__repr__())

    def _get_teams(self):
        url = f'https://statsapi.web.nhl.com/api/v1/teams?sportId=1'
        #print('Getting games from ' + url)
        teams = requests.get(url, verify=False).json()
        for team_json in teams['teams']:
            team = Team(team_json)
            self._teams.append(team)

    @property
    def dataframes(self):
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)
