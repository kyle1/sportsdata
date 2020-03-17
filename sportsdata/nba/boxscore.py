import pandas as pd
import requests
from constants import PROXIES, NBA_REQUEST_HEADERS
from datetime import datetime, timedelta
from time import sleep


class PlayerBoxscore:
    """
    Player's boxscore data from an individual NBA game.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

    headers : list (string)
        A list of column headers

    row : dict
        Dict that contains the player's boxscore data. todo??
    """
    def __init__(self, game, headers, row):
        self._nba_player_id = None
        self._nba_game_id = None
        self._season = None
        self._away_team_id = None
        self._home_team_id = None
        self._is_away = None
        self._minutes_played = None
        self._field_goals = None
        self._field_goal_attempts = None
        self._field_goal_pct = None
        self._three_point_field_goals = None
        self._three_point_field_goal_attempts = None
        self._three_point_field_goal_pct = None
        self._free_throws = None
        self._free_throw_attempts = None
        self._free_throw_pct = None
        self._offensive_rebounds = None
        self._defensive_rebounds = None
        self._total_rebounds = None
        self._assists = None
        self._steals = None
        self._blocks = None
        self._turnovers = None
        self._personal_fouls = None
        self._points = None
        self._plus_minus = None

        self._get_boxscore_from_row(game, headers, row)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _get_boxscore_from_row(self, game, headers, row):
        box = {}
        for i in range(len(headers)):
            box[headers[i]] = row[i]
        # if box['MIN'] == None:
        #     # Skip records if the player did not play any minutes TODO
        #     continue
        setattr(self, '_nba_player_id', box['PLAYER_ID'])
        setattr(self, '_nba_game_id', box['GAME_ID'])
        setattr(self, '_season', game['Season'])  # todo
        setattr(self, '_away_team_id', game['AwayTeamId'])  # todo
        setattr(self, '_home_team_id', game['HomeTeamId'])  # todo
        setattr(self, '_is_away', int(
            box['TEAM_ID']) == game['AwayTeamId'])  # todo
        setattr(self, '_minutes_played', box['MIN'])
        setattr(self, '_field_goals', box['FGM'])
        setattr(self, '_field_goal_attempts', box['FGA'])
        setattr(self, '_field_goal_pct',
                box['FG_PCT'] if box['FGA'] != 0 else None)
        setattr(self, '_three_point_field_goals', box['FG3M'])
        setattr(self, '_three_point_field_goal_attempts', box['FG3A'])
        setattr(self, '_three_point_field_goal_pct',
                box['FG3_PCT'] if box['FG3A'] != 0 else None)
        setattr(self, '_free_throws', box['FTM'])
        setattr(self, '_free_throw_attempts', box['FTA'])
        setattr(self, '_free_throw_pct',
                None if box['FTA'] == 0 else box['FTM'] / float(box['FTA']))
        setattr(self, '_offensive_rebounds', box['OREB'])
        setattr(self, '_defensive_rebounds', box['DREB'])
        setattr(self, '_total_rebounds', box['REB'])
        setattr(self, '_assists', box['AST'])
        setattr(self, '_steals', box['STL'])
        setattr(self, '_blocks', box['BLK'])
        setattr(self, '_turnovers', box['TO'])
        setattr(self, '_personal_fouls', box['PF'])
        setattr(self, '_points', box['PTS'])
        setattr(self, '_plus_minus',
                None if box['PLUS_MINUS'] == None else int(box['PLUS_MINUS']))

    @property
    def dataframe(self):
        fields_to_include = {
            'NbaPlayerId': self._nba_player_id,
            'NbaGameId': self._nba_game_id,
            'Season': self._season,
            'AwayTeamId': self._away_team_id,
            'HomeTeamId': self._home_team_id,
            'IsAway': self._is_away,
            # 'TeamResult': self._team_result,
            # 'ResultNote': self._result_note,
            # 'Overtime': self._overtime,
            'MinutesPlayed': self._minutes_played,
            'FieldGoals': self._field_goals,
            'FieldGoalAttempts': self._field_goal_attempts,
            'FieldGoalPct': self._field_goal_pct,
            'ThreePointFieldGoals': self._three_point_field_goals,
            'ThreePointFieldGoalAttempts': self._three_point_field_goal_attempts,
            'ThreePointFieldGoalPct': self._three_point_field_goal_pct,
            'FreeThrows': self._free_throws,
            'FreeThrowAttempts': self._free_throw_attempts,
            'FreeThrowPct': self._free_throw_pct,
            'OffensiveRebounds': self._offensive_rebounds,
            'DefensiveRebounds': self._defensive_rebounds,
            'Rebounds': self._rebounds,
            'Assists': self._assists,
            'Steals': self._stelas,
            'Blocks': self._blocks,
            'Turnovers': self._turnovers,
            'PersonalFouls': self._personal_fouls,
            'Points': self._points,
            'PlusMinus': self._plus_minus
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic

class PlayerBoxscores:
    """
    All players' boxscore data from multiple NBA games.

    Parameters
    ----------
    games : GameBoxscore
        List of objects that contain game-level boxscore data.
    """
    def __init__(self, games):
        self._boxscores = []

        self._get_boxscores_by_games(games)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _get_boxscores_by_games(self, games):
        for game in games:
            print(game._nba_game_id_str)
            url = f'https://stats.nba.com/stats/boxscoretraditionalv2/?gameId={game._nba_game_id_str}&startPeriod=1&endPeriod=1&startRange=0&endRange=0&rangeType=0&startRange=0'
            print(url)
            boxscore_data = requests.get(
                url, PROXIES, headers=NBA_REQUEST_HEADERS, timeout=10).json()
            for results in boxscore_data['resultSets']:
                if results['name'] != 'PlayerStats':
                    # Skip team-based stats
                    continue
                stat_headers = results['headers']
                row_set = results['rowSet']
                for row in row_set:
                    player_boxscore = PlayerBoxscore(game, stat_headers, row)
                    self._boxscores.append(player_boxscore)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for boxscore in self.__iter__():
            dics.append(boxscore.to_dict)
        return dics


class GameBoxscore:
    """
    Game stats from an individual NBA game.

    Parameters
    ----------
    season : int
        The NBA season associated with the game.
    
    game_json : dict
        Dict that contains the game boxscore data.
    """
    def __init__(self, season, game_json):
        #TODO
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

        self._create_game(season, game_json)

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

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['AwayPlayers'] = self._away_players.to_dicts
        dic['HomePlayers'] = self._home_players.to_dicts
        return dic

class GameBoxscores:
    #todo- setup kwargs like MLB GameBoxscores ?
    """
    Game stats from multiple NBA games.

    Parameters
    ----------
    season : int
        Season (year) to get game boxscores from.

    start_date : string
        Beginning date to get game boxscores from ('MM/DD/YYYY' format)

    end_date : string
        End date to get game boxscores from ('MM/DD/YYYY' format)
    """
    def __init__(self, season, start_date, end_date):
        self._boxscores = []

        self._get_game_boxscores(season, start_date, end_date)

    def __repr__(self):
        return self._boxscores

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
                boxscore = GameBoxscore(season, game_data)
                self._boxscore.append(boxscore)
                sleep(5)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for boxscore in self.__iter__():
            dics.append(boxscore.to_dict)
        return dics
