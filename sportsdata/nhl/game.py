import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil import tz


class Game:
    def __init__(self, game_data):
        self._nhl_game_id = None
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
        self._nhl_venue_id = None
        self._nhl_venue_name = None
        self._result_note = None
        self._overtime = None
        self._shootout = None

        self._create_game(game_data)

    def _create_game(self, game):
        utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        game_dt = utc.replace(tzinfo=from_zone).astimezone(to_zone).replace(tzinfo=None)
        has_overtime = False
        result_note = ''
        for period in game['linescore']['periods']:
            if period['num'] >= 4:
                has_overtime = True
                result_note = period['ordinalNum']  # OT, 2OT, etc.
        has_shootout = game['linescore']['hasShootout']
        if has_shootout:
            result_note = "SO"  # Override "OT" note
        setattr(self, '_nhl_game_id', game['gamePk'])
        setattr(self, '_season', int(game['season'][:4])),
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_time', game_dt.time().isoformat())
        setattr(self, '_game_status', game['status']['detailedState'])
        setattr(self, '_away_team_id', game['teams']['away']['team']['id'])
        setattr(self, '_away_team_score', game['teams']['away']['score'])
        setattr(self, '_away_team_record_wins', game['teams']['away']['leagueRecord']['wins'])
        setattr(self, '_away_team_record_losses', game['teams']['away']['leagueRecord']['losses'])
        setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        setattr(self, '_home_team_score', game['teams']['home']['score'])
        setattr(self, '_home_team_record_wins', game['teams']['home']['leagueRecord']['wins'])
        setattr(self, '_home_team_record_losses', game['teams']['home']['leagueRecord']['losses'])
        setattr(self, '_nhl_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        setattr(self, '_nhl_venue_name', game['venue']['name'])
        setattr(self, '_result_note', result_note)
        setattr(self, '_overtime', has_overtime)
        setattr(self, '_shootout', has_shootout)

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlGameId': self._nhl_game_id,
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
            'NhlVenueId': self._nhl_venue_id,
            'NhlVenueName': self._nhl_venue_name,
            'ResultNote': self._result_note,
            'Overtime': self._overtime,
            'Shootout': self._shootout
        }
        return pd.DataFrame([fields_to_include], index=[self._nhl_game_id])


class Games:
    def __init__(self, start_date, end_date):
        self._games = []

        self._get_games(start_date, end_date)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_games(self, start_date, end_date):
        url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&expand=schedule.linescore'
        #print('Getting games from ' + url)
        games = requests.get(url, verify=VERIFY_REQUESTS).json()
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
