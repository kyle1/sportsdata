import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil import tz
#from mlb.constants import VERIFY_REQUESTS
from util import get_dates_by_season


class Game:
    """
    A representation of a matchup between two teams.

    Stores all relevant high-level match information for a game in a team's
    schedule including date, time, opponent, and result.

    Parameters
    ----------
    game_data : string
        The row containing the specified game information.
        
    year : string
        The year of the current season.
    """

    def __init__(self, game_data):
        self._mlb_game_id = None
        self._season = None
        self._game_date = None
        self._game_date_time = None
        self._away_team_id = None
        self._home_team_id = None
        self._mlb_venue_id = None
        self._day_night = None
        self._series_description = None
        self._series_game_number = None
        self._games_in_series = None

        self._set_game(game_data)  # todo ??

    def _set_game(self, game):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)
        game_dt = pst.replace(tzinfo=None)
        setattr(self, '_mlb_game_id', game['gamePk'])
        setattr(self, '_season', game['seasonDisplay'])
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_away_team_id', game['teams']['away']['team']['id'])
        setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        setattr(self, '_mlb_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        setattr(self, '_day_night', game['dayNight'])
        setattr(self, '_series_description', game['seriesDescription'])
        setattr(self, '_series_game_number', game['seriesGameNumber'])
        setattr(self, '_games_in_series', game['gamesInSeries'])

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbGameId': self._mlb_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'AwayTeamId': self._away_team_id,
            'HomeTeamId': self._home_team_id,
            'MlbVenueId': self._mlb_venue_id,
            'DayNight': self._day_night,
            'SeriesDescription': self._series_description,
            'SeriesGameNumber': self._series_game_number,
            'GamesInSeries': self._games_in_series
        }
        return pd.DataFrame([fields_to_include], index=[self._mlb_game_id])


class Schedule:
    """
    Generates a schedule for the specified time period.
    Includes wins, losses, and scores if applicable.

    Parameters
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
            start_date, end_date = get_dates_by_season(season)
        elif 'range' in kwargs:
            start_date = kwargs['range'][0]
            end_date = kwargs['range'][1]
        elif 'date' in kwargs:
            start_date = kwargs['date']
            end_date = kwargs['date']
        else:
            print('Invalid Schedule param(s)')
            return

        self._get_schedule(start_date, end_date)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_schedule(self, start_date, end_date):
        url = f'https://statsapi.mlb.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1'
        print('Getting schedule from ' + url)
        games = requests.get(url, verify=False).json()
        for date in games['dates']:
            for game_data in date['games']:
                game = Game(game_data)
                self._games.append(game)

    @property
    def dataframes(self):
        frames = []
        for game in self.__iter__():
            frames.append(game.dataframe)
        return pd.concat(frames)
