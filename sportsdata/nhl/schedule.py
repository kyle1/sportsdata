import mlb.util
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
    """
    def __init__(self, game_json):
        self._nhl_game_id = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        self._game_time = None
        self._away_team_id = None
        self._away_team_score = None
        self._home_team_id = None
        self._nhl_venue_id = None
        self._nhl_venue_name = None

        self._parse_game(game_json)  # todo ??

    def _parse_game(self, game):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)
        game_dt = pst.replace(tzinfo=None)
        setattr(self, '_nhl_game_id', game['gamePk'])
        setattr(self, '_season', game['season'][:4])
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_time', game_dt.time().isoformat())
        setattr(self, '_away_team_id', game['teams']['away']['team']['id'])
        setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        setattr(self, '_nhl_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        setattr(self, '_nhl_venue_name', game['venue']['name'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlGameId': self._nhl_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'AwayTeamId': self._away_team_id,
            'HomeTeamId': self._home_team_id,
            'NhlVenueId': self._nhl_venue_id,
            'NhlVenueName': self._nhl_venue_name
        }
        return pd.DataFrame([fields_to_include], index=[self._nhl_game_id])

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
            start_date, end_date = mlb.util.get_dates_by_season(season)
        elif 'range' in kwargs:
            start_date = kwargs['range'][0]
            end_date = kwargs['range'][1]
        elif 'date' in kwargs:
            start_date = kwargs['date']
            end_date = kwargs['date']
        else:
            print('Invalid Schedule param(s)')
            return

        self._get_games(start_date, end_date)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_games(self, start_date, end_date):
        url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1'
        print('Getting schedule from ' + url)
        games = requests.get(url, verify=VERIFY_REQUESTS).json()
        for date in games['dates']:
            for game_data in date['games']:
                #TODO
                # series_desc = game_data['seriesDescription']

                # if 'Training' in series_desc or 'Exhibition' in series_desc or 'All-Star' in series_desc:
                #     continue

                game = Game(game_data)
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
