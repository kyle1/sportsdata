import mlb.util
import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime, timedelta
from dateutil import tz


class Game:
    def __init__(self, **kwargs):
        self._mlb_game_id = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        self._game_time = None
        self._game_status = None
        self._away_team_id = None
        self._away_team_score = None
        self._away_team_record_wins = None
        self._away_team_record_losses = None
        self._away_team_record_pct = None
        self._home_team_id = None
        self._home_team_score = None
        self._home_team_record_wins = None
        self._home_team_record_losses = None
        self._home_team_record_pct = None
        self._mlb_venue_id = None
        self._day_night = None
        self._series_description = None
        self._series_game_number = None
        self._games_in_series = None
        self._extra_innings = None

        if 'json' in kwargs:
            self._set_game(kwargs['json'])
        elif 'id' in kwargs:
            self._set_game(kwargs['id'])

    def _set_game(self, game):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)
        game_dt = pst.replace(tzinfo=None)
        setattr(self, '_mlb_game_id', game['gamePk'])
        setattr(self, '_season', game['seasonDisplay'])
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_time', game_dt.time().isoformat())
        setattr(self, '_game_status', game['status']['detailedState'])
        setattr(self, '_away_team_id', game['teams']['away']['team']['id'])
        setattr(self, '_away_team_score', game['teams']['away']['score'])
        setattr(self, '_away_team_record_wins', game['teams']['away']['leagueRecord']['wins'])
        setattr(self, '_away_team_record_losses', game['teams']['away']['leagueRecord']['losses'])
        setattr(self, '_away_team_record_pct', game['teams']['away']['leagueRecord']['pct'])
        setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        setattr(self, '_home_team_score', game['teams']['home']['score'])
        setattr(self, '_home_team_record_wins', game['teams']['home']['leagueRecord']['wins'])
        setattr(self, '_home_team_record_losses', game['teams']['home']['leagueRecord']['losses'])
        setattr(self, '_home_team_record_pct', game['teams']['home']['leagueRecord']['pct'])
        setattr(self, '_mlb_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        setattr(self, '_day_night', game['dayNight'])
        setattr(self, '_series_description', game['seriesDescription'])
        setattr(self, '_series_game_number', game['seriesGameNumber'])
        setattr(self, '_games_in_series', game['gamesInSeries'])
        setattr(self, '_extra_innings', 'todo')

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbGameId': self._mlb_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'GameStatus': self._game_status,
            'AwayTeamId': self._away_team_id,
            'AwayTeamScore': self._away_team_score,
            'AwayTeamRecordWins': self._away_team_record_wins,
            'AwayTeamRecordLosses': self._away_team_record_losses,
            'AwayTeamRecordPct': self._away_team_record_pct,
            'HomeTeamId': self._home_team_id,
            'HomeTeamScore': self._home_team_score,
            'HomeTeamRecordWins': self._home_team_record_wins,
            'HomeTeamRecordLosses': self._home_team_record_losses,
            'HomeTeamRecordPct': self._home_team_record_pct,
            'MlbVenueId': self._mlb_venue_id,
            'DayNight': self._day_night,
            'SeriesDescription': self._series_description,
            'SeriesGameNumber': self._series_game_number,
            'GamesInSeries': self._games_in_series,
            'ExtraInnings': self._extra_innings
        }
        return pd.DataFrame([fields_to_include], index=[self._mlb_game_id])


class Games:
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
            print('Invalid Game param(s)')
            return

        self._get_games(start_date, end_date)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_games(self, start_date, end_date):
        url = f'https://statsapi.mlb.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1'
        #print('Getting games from ' + url)
        games = requests.get(url, verify=VERIFY_REQUESTS).json()
        for date in games['dates']:
            for game_data in date['games']:
                series_desc = game_data['seriesDescription']

                if 'Training' in series_desc or 'Exhibition' in series_desc or 'All-Star' in series_desc:
                    continue

                if game_data['status']['codedGameState'] != 'F':
                    continue  # Game is not over
                # todo- games that were completed early?

                # todo?
                # if game['gamePk'] not i game_ids:
                #     continue

                game = Game(json=game_data)
                self._games.append(game)

    @property
    def dataframes(self):
        frames = []
        for game in self.__iter__():
            frames.append(game.dataframe)
        return pd.concat(frames)
