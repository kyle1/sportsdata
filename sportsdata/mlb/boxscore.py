import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from time import sleep


class Boxscore:
    """
    MLB player's boxscore data from a game.

    Parameters
    ----------
    game : dict
        Dict that contains the game data.

    team : string
        'away' or 'home'

    box_json : dict
        Dict that contains the player's boxscore data.
    """

    def __init__(self, game, team, box_json):
        self._mlb_player_id = None
        self._mlb_game_id = None
        self._season = None
        self._away_team_id = None
        self._home_team_id = None
        self._is_away = None
        self._team_result = None
        #self._extra_innings = None
        self._batting_order = None
        self._at_bats = None
        self._runs = None
        self._hits = None
        self._doubles = None
        self._triples = None
        self._home_runs = None
        self._runs_batted_in = None
        self._bases_on_balls = None
        self._intentional_bases_on_balls = None
        self._strikeouts = None
        self._hit_by_pitch = None
        self._sacrifice_hits = None
        self._sacrifice_flies = None
        self._grounded_into_double_play = None
        self._stolen_bases = None
        self._caught_stealing = None
        self._starting_pitcher = None
        self._pitching_win = None
        self._innings_pitched = None
        self._allowed_hits = None
        self._allowed_runs = None
        self._earned_runs = None
        self._earned_run_average = None
        self._pitched_strikeouts = None
        self._allowed_home_runs = None
        self._allowed_bases_on_balls = None
        self._batters_hit_by_pitch = None
        self._complete_game = None
        self._shutout = None
        self._quality_start = None

        self._get_boxscore_from_json(game, team, box_json)

    def _get_boxscore_from_json(self, game, team, box):
        has_batting_stats = len(box['stats']['batting']) > 0
        has_pitching_stats = len(box['stats']['pitching']) > 0
        if not has_batting_stats and not has_pitching_stats:
            return  # todo

        setattr(self, '_mlb_player_id', box['person']['id'])
        setattr(self, '_mlb_game_id', game._mlb_game_id)
        setattr(self, '_season', game._season)
        setattr(self, '_away_team_id', game._away_team_id)
        setattr(self, '_home_team_id', game._home_team_id)
        setattr(self, '_is_away', team == 'away')
        setattr(self, '_team_result', self._get_team_result(game, team))
        setattr(self, '_batting_order', self._get_batting_order(box))

        if has_batting_stats:
            setattr(self, '_at_bats', box['stats']['batting']['atBats'])
            setattr(self, '_runs', box['stats']['batting']['runs'])
            setattr(self, '_hits', box['stats']['batting']['hits'])
            setattr(self, '_doubles', box['stats']['batting']['doubles'])
            setattr(self, '_triples', box['stats']['batting']['triples'])
            setattr(self, '_home_runs', box['stats']['batting']['homeRuns'])
            setattr(self, '_runs_batted_in', box['stats']['batting']['rbi'])
            setattr(self, '_bases_on_balls',
                    box['stats']['batting']['baseOnBalls'])
            setattr(self, '_intentional_bases_on_balls',
                    box['stats']['batting']['intentionalWalks'])
            setattr(self, '_strikeouts', box['stats']['batting']['strikeOuts'])
            setattr(self, '_hit_by_pitch',
                    box['stats']['batting']['hitByPitch'])
            setattr(self, '_sacrifice_hits',
                    box['stats']['batting']['sacBunts'])
            setattr(self, '_sacrifice_flies',
                    box['stats']['batting']['sacFlies'])
            setattr(self, '_grounded_into_double_play',
                    box['stats']['batting']['groundIntoDoublePlay'])
            setattr(self, '_stolen_bases',
                    box['stats']['batting']['stolenBases'])
            setattr(self, '_caught_stealing',
                    box['stats']['batting']['caughtStealing'])

        if has_pitching_stats:
            setattr(self, '_starting_pitcher',
                    box['stats']['pitching']['gamesStarted'])
            setattr(self, '_pitching_win',
                    'wins' in box['stats']['pitching'] and box['stats']['pitching']['wins'] == 1)
            setattr(self, '_innings_pitched',
                    box['stats']['pitching']['inningsPitched'])
            setattr(self, '_allowed_hits', box['stats']['pitching']['hits'])
            setattr(self, '_allowed_runs', box['stats']['pitching']['runs'])
            setattr(self, '_earned_runs',
                    box['stats']['pitching']['earnedRuns'])
            setattr(self, '_earned_run_average', box['stats']['pitching']['runsScoredPer9']
                    if box['stats']['pitching']['runsScoredPer9'] != '-.--' else None)
            setattr(self, '_pitched_strikeouts',
                    box['stats']['pitching']['strikeOuts'])
            setattr(self, '_allowed_home_runs',
                    box['stats']['pitching']['homeRuns'])
            setattr(self, '_allowed_bases_on_balls',
                    box['stats']['pitching']['baseOnBalls'])
            setattr(self, '_batters_hit_by_pitch',
                    box['stats']['pitching']['hitBatsmen'])
            setattr(self, '_complete_game',
                    box['stats']['pitching']['completeGames'] == 1)
            setattr(self, '_shutout', box['stats']
                    ['pitching']['shutouts'] == 1)
            setattr(self, '_quality_start', float(
                box['stats']['pitching']['inningsPitched']) >= 6.0 and box['stats']['pitching']['runs'] <= 3.0)

    def _get_team_result(self, game, team):
        if game._away_team_score == game._home_team_score:
            team_result = 'T'
        elif (team == 'away') == (game._away_team_score > game._home_team_score):
            team_result = 'W'
        else:
            team_result = 'L'
        return team_result

    def _get_batting_order(self, box):
        if 'battingOrder' in box:
            batting_order = int(box['battingOrder'].replace('"', ''))
            if batting_order % 100 == 0:
                batting_order = int(batting_order / 100)
            else:
                batting_order = None
        else:
            batting_order = None
        return batting_order

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbPlayerId': self._mlb_player_id,
            'MlbGameId': self._mlb_game_id,
            'Season': self._season,
            'AwayTeamId': self._away_team_id,
            'HomeTeamId': self._home_team_id,
            'IsAway': self._is_away,
            'TeamResult': self._team_result,
            # 'ExtraInnings': self._extra_innings,
            'BattingOrder': self._batting_order,
            'AtBats': self._at_bats,
            'Runs': self._runs,
            'Hits': self._hits,
            'Doubles': self._doubles,
            'Triples': self._triples,
            'HomeRuns': self._home_runs,
            'RunsBattedIn': self._runs_batted_in,
            'BasesOnBalls': self._bases_on_balls,
            'IntentionalBasesOnBalls': self._intentional_bases_on_balls,
            'Strikeouts': self._strikeouts,
            'HitByPitch': self._hit_by_pitch,
            'SacrificeHits': self._sacrifice_hits,
            'SacrificeFlies': self._sacrifice_flies,
            'GroundedIntoDoublePlay': self._grounded_into_double_play,
            'StolenBases': self._stolen_bases,
            'CaughtStealing': self._caught_stealing,
            'StartingPitcher': self._starting_pitcher,
            'PitchingWin': self._pitching_win,
            'InningsPitched': self._innings_pitched,
            'AllowedHits': self._allowed_hits,
            'AllowedRuns': self._allowed_runs,
            'EarnedRuns': self._earned_runs,
            'EarnedRunAverage': self._earned_run_average,
            'PitchedStrikeouts': self._pitched_strikeouts,
            'AllowedHomeRuns': self._allowed_home_runs,
            'AllowedBasesOnBalls': self._allowed_bases_on_balls,
            'BattersHitByPitch': self._batters_hit_by_pitch,
            'CompleteGame': self._complete_game,
            'Shutout': self._shutout,
            'QualityStart': self._quality_start
        }
        return pd.DataFrame([fields_to_include], index=None)


class Boxscores:
    """
    Get MLB players' boxscore data from multiple games.

    Parameters
    ----------
    games : list
        List of games to retrieve boxscores for.
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
            url = f'https://statsapi.mlb.com/api/v1/game/{game._mlb_game_id}/boxscore'
            print('Getting boxscore data from ' + url)
            boxscores = requests.get(url, verify=VERIFY_REQUESTS).json()
            for team in ['away', 'home']:
                for player, stats in boxscores['teams'][team]['players'].items():
                    boxscore = Boxscore(game, team, stats)
                    if boxscore._mlb_player_id:  # some players don't have any stats
                        self._boxscores.append(boxscore)
            sleep(3)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)
