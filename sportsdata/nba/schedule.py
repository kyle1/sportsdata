import nba.util
import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime, timedelta
from dateutil import tz


class Game:
    def __init__(self, game_data, season):
        self._nba_game_id = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        self._game_time = None
        self._away_team_id = None
        self._away_team_score = None
        self._home_team_id = None
        self._nba_venue_id = None
        self._nba_venue_name = None

        self._set_game(game_data, season)

    def _set_game(self, game, season):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        est = datetime.strptime(game['etm'], '%Y-%m-%dT%H:%M:%S')
        dt = est + timedelta(hours=-3)
        setattr(self, '_nba_game_id', game['gid'])
        setattr(self, '_season', season)
        setattr(self, '_game_date_time', dt.isoformat())
        setattr(self, '_game_date', dt.date().isoformat())
        setattr(self, '_game_time', dt.time().isoformat())
        setattr(self, '_away_team_id', game['v']['tid'])
        setattr(self, '_home_team_id', game['h']['tid'])
        #setattr(self, '_nba_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        setattr(self, '_nba_venue_name', game['an'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NbaGameId': self._nba_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'AwayTeamId': self._away_team_id,
            'HomeTeamId': self._home_team_id,
            # 'NbaVenueId': self._nba_venue_id,
            'NbaVenueName': self._nba_venue_name
        }
        return pd.DataFrame([fields_to_include], index=[self._nba_game_id])


class Schedule:
    def __init__(self, **kwargs):
        self._games = []

        if 'season' in kwargs:
            season = kwargs['season']
            start_date, end_date = nba.util.get_dates_by_season(season)
        elif 'range' in kwargs:
            start_date = kwargs['range'][0]
            end_date = kwargs['range'][1]
        elif 'date' in kwargs:
            start_date = kwargs['date']
            end_date = kwargs['date']
        else:
            print('Invalid Schedule param(s)')
            return

        self._get_games(season, start_date, end_date)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_games(self, season, start_date, end_date):
        url = f'http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{season}/league/00_full_schedule.json'
        #print('Getting games from ' + url)
        schedule = requests.get(url, verify=VERIFY_REQUESTS).json()
        begin = datetime.strptime(start_date, '%m/%d/%Y').date()
        end = datetime.strptime(end_date, '%m/%d/%Y').date()
        for item in schedule['lscd']:
            for game_json in item['mscd']['g']:
                date = datetime.strptime(game_json['etm'], '%Y-%m-%dT%H:%M:%S').date()
                if date < begin or date > end:
                    continue
                game = Game(game_json, season)
                self._games.append(game)

    @property
    def dataframes(self):
        frames = []
        for game in self.__iter__():
            frames.append(game.dataframe)
        return pd.concat(frames)
