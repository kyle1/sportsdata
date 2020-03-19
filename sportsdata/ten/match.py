import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime
from dateutil import tz


class Match:
    def __init__(self, match_json):
        self._ten_match_id = None
        self._match_date_time = None
        self._match_date = None
        self._match_time = None
        self._ten_player1_id = None
        self._player1_score = None
        self._ten_player2_id = None
        self._player2_score = None
        self._surface_type = None
        self._ten_venue_id = None

        self._set_match(match_json)

    def _set_match(self, match):
        utc = datetime.strptime(match['matchDate'], '%Y-%m-%dT%H:%M:%SZ')
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        match_dt = utc.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)
        setattr(self, '_ten_match_id', match['matchPk'])
        setattr(self, '_match_date_time', match_dt.isoformat())
        setattr(self, '_match_date', match_dt.date().isoformat())
        setattr(self, '_match_time', match_dt.time().isoformat())
        setattr(self, '_ten_player1_id', 'todo')'
        setattr(self, '_player1_score', 'todo')
        setattr(self, '_ten_player2_id', 'todo')'
        setattr(self, '_player2_score', 'todo')
        setattr(self, '_surface_type', 'todo')
        setattr(self, '_ten_venue_id', 'todo')

    @property
    def dataframe(self):
        fields_to_include = {
            'TenMatchId': self._ten_match_id,
            'MatchDateTime': self._match_date_time,
            'MatchDate': self._match_date,
            'MatchTime': self._match_time,
            'MatchStatus': self._match_status,
            'TenPlayer1Id': self._ten_player1_id,
            'Player1Score': self._player1_score,
            'TenPlayer2Id': self._ten_player2_id,
            'Player2Score': self._player2_score,
            'SurfaceType': self._surface_type,
            'TenVenueId': self._ten_venue_id
        }
        return pd.DataFrame([fields_to_include], index=[self._ten_match_id])


class Matches:
    def __init__(self, **kwargs):
        self._matches = []

        if 'range' in kwargs:
            start_date = kwargs['range'][0]
            end_date = kwargs['range'][1]
        elif 'date' in kwargs:
            start_date = kwargs['date']
            end_date = kwargs['date']
        else:
            print('Invalid Game param(s)')
            return

        self._get_matches(start_date, end_date)

    def __repr__(self):
        return self._matches

    def __iter__(self):
        return iter(self.__repr__())

    def _get_matches(self, start_date, end_date):
        url = f'https://www.ultimatetennisstatistics.com/tournamentEvents'
        matches = requests.get(url, verify=VERIFY_REQUESTS).json()
        # TODO

    @property
    def dataframes(self):
        frames = []
        for match in self.__iter__():
            frames.append(match.dataframe)
        return pd.concat(frames)
