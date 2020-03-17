import pandas as pd
import requests
from constants import NBA_REQUEST_PROXIES, NBA_REQUEST_HEADERS


class Boxscore:
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


class Boxscores:
    def __init__(self, games):
        self._boxscores = []

        self._get_boxscores_by_games(games)
        # print(games)

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
                url, NBA_REQUEST_PROXIES, headers=NBA_REQUEST_HEADERS, timeout=10).json()
            for results in boxscore_data['resultSets']:
                if results['name'] != 'PlayerStats':
                    # Skip team-based stats
                    continue
                stat_headers = results['headers']
                row_set = results['rowSet']
                for row in row_set:
                    boxscore = Boxscore(game, stat_headers, row)
                    self._boxscores.append(boxscore)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)
