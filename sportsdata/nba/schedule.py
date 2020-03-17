import nba.util
import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime, timedelta
from dateutil import tz


class Game:
    """
    A representation of a matchup between two teams.

    Stores all relevant high-level match information for a game in a team's
    schedule including date, time, opponent, and result.

    Parameters
    ----------
    game_json : string
        Dict containing game information.

    season : int
        Season associated with the game.
    """
    def __init__(self, game_json, season):
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

        self._parse_game(game_json, season)

    def _parse_game(self, game, season):
        game_dt = datetime.strptime(game['etm'], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=-3) # EST
        setattr(self, '_nba_game_id', game['gid'])
        setattr(self, '_season', season)
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_time', game_dt.time().isoformat())
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

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Schedule:
    """
    Generates a schedule for the specified time period.
    Includes wins, losses, and scores if applicable.

    Parameters (kwargs)
    ----------
    season : int
        The requested season to pull stats from.
    range : list (strings)
        The requested date range to pull stats from.
    date : string 
        The requested date to pull stats from.
    """
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

    def _get_schedule(self, season, start_date, end_date):
        url = f'http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{season}/league/00_full_schedule.json'
        print('Getting schedule from ' + url)
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

    @property
    def to_dicts(self):
        dics = []
        for game in self.__iter__():
            dics.append(game.to_dict)
        return dics
