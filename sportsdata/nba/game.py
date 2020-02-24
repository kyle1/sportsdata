import pandas as pd
import requests
from datetime import datetime, timedelta


class Game:
    def __init__(self, season, game_data):
        self._nba_game_id = None
        self._nba_game_id_str = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        self._game_time = None
        self._game_status = None
        self._away_team_id = None
        self._away_team_score = None
        self._away_team_record_wins = None
        self._away_team_record_losses = None
        self._home_team_id = None
        self._home_team_score = None
        self._home_team_record_wins = None
        self._home_team_record_losses = None
        self._nba_venue_name = None

        self._create_game(season, game_data)

    def _create_game(self, season, game):
        game_dt = datetime.strptime(game['etm'], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=-3)
        game_date = game_dt.date()
        game_time = game_dt.time()
        setattr(self, '_nba_game_id', int(game['gid']))
        setattr(self, '_nba_game_id_str', game['gid'])
        setattr(self, '_season', season)  # todo?
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_date.isoformat())
        setattr(self, '_game_time', game_time.isoformat())
        setattr(self, '_game_status', game['stt'])
        setattr(self, '_away_team_id', int(game['v']['tid']))
        setattr(self, '_away_team_score', int(game['v']['s']))
        setattr(self, '_away_team_record_wins', int(game['v']['re'].split('-')[0]))
        setattr(self, '_away_team_record_losses', int(game['v']['re'].split('-')[1]))
        setattr(self, '_home_team_id', int(game['h']['tid']))
        setattr(self, '_home_team_score', int(game['h']['s']))
        setattr(self, '_home_team_record_wins', int(game['h']['re'].split('-')[0]))
        setattr(self, '_home_team_record_losses', int(game['h']['re'].split('-')[1]))
        setattr(self, '_nba_venue_name', game['an'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NbaGameId': self._nba_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'GameStatus': self._game_status,
            'AwayTeamId': self._away_team_id,
            'AwayTeamScore': self._away_team_score,
            'AwayTeamRecordWins': self._away_team_record_wins,
            'AwayTeamRecordLosses': self._away_team_record_losses,
            'HomeTeamId': self._home_team_id,
            'HomeTeamScore': self._home_team_score,
            'HomeTeamRecordWins': self._home_team_record_wins,
            'HomeTeamRecordLosses': self._home_team_record_losses,
            'NbaVenueName': self._nba_venue_name
        }
        return pd.DataFrame([fields_to_include], index=[self._nba_game_id])


class Games:
    def __init__(self, season, start_date, end_date):
        self._games = []

        self._get_games(season, start_date, end_date)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_games(self, season, start_date, end_date):
        url = f'http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{season}/league/00_full_schedule.json'  # todo
        games = requests.get(url).json()
        begin = datetime.strptime(start_date, '%m/%d/%Y').date()
        end = datetime.strptime(end_date, '%m/%d/%Y').date()
        for item in games['lscd']:
            for game_data in item['mscd']['g']:
                game_dt = datetime.strptime(game_data['etm'], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=-3)
                game_date = game_dt.date()
                game_time = game_dt.time()
                if game_date < begin or game_date > end or game_data['stt'] == 'PPD':
                    # Only get games in the specified date range that were not postponed.
                    continue
                game = Game(season, game_data)
                self._games.append(game)

    @property
    def dataframes(self):
        frames = []
        for game in self.__iter__():
            frames.append(game.dataframe)
        return pd.concat(frames)

    @property
    def dicts(self):
        df = self.dataframes
        dicts = df.to_dict('records')
        return dicts
