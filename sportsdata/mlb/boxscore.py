import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from ..util import utc_to_pst
from .playbyplay import PlayByPlay
from .schedule import Schedule
from .util import get_dates_by_season
from datetime import datetime
from time import sleep

# todo- check base/bases on balls


class PlayerBoxscore:
    """
    Player's boxscore data from an individual MLB game.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

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
            setattr(self, '_bases_on_balls', box['stats']['batting']['baseOnBalls'])
            setattr(self, '_intentional_bases_on_balls', box['stats']['batting']['intentionalWalks'])
            setattr(self, '_strikeouts', box['stats']['batting']['strikeOuts'])
            setattr(self, '_hit_by_pitch', box['stats']['batting']['hitByPitch'])
            setattr(self, '_sacrifice_hits', box['stats']['batting']['sacBunts'])
            setattr(self, '_sacrifice_flies', box['stats']['batting']['sacFlies'])
            setattr(self, '_grounded_into_double_play', box['stats']['batting']['groundIntoDoublePlay'])
            setattr(self, '_stolen_bases', box['stats']['batting']['stolenBases'])
            setattr(self, '_caught_stealing', box['stats']['batting']['caughtStealing'])

        if has_pitching_stats:
            setattr(self, '_starting_pitcher', box['stats']['pitching']['gamesStarted'])
            setattr(self, '_pitching_win', 'wins' in box['stats']['pitching'] and box['stats']['pitching']['wins'] == 1)
            setattr(self, '_innings_pitched', box['stats']['pitching']['inningsPitched'])
            setattr(self, '_allowed_hits', box['stats']['pitching']['hits'])
            setattr(self, '_allowed_runs', box['stats']['pitching']['runs'])
            setattr(self, '_earned_runs', box['stats']['pitching']['earnedRuns'])
            if box['stats']['pitching']['runsScoredPer9'] != '-.--':
                setattr(self, '_earned_run_average', box['stats']['pitching']['runsScoredPer9'])
            setattr(self, '_pitched_strikeouts', box['stats']['pitching']['strikeOuts'])
            setattr(self, '_allowed_home_runs', box['stats']['pitching']['homeRuns'])
            setattr(self, '_allowed_bases_on_balls', box['stats']['pitching']['baseOnBalls'])
            setattr(self, '_batters_hit_by_pitch', box['stats']['pitching']['hitBatsmen'])
            setattr(self, '_complete_game', box['stats']['pitching']['completeGames'] == 1)
            setattr(self, '_shutout', box['stats']['pitching']['shutouts'] == 1)
            quality_start = float(box['stats']['pitching']['inningsPitched']
                                  ) >= 6.0 and box['stats']['pitching']['runs'] <= 3.0
            setattr(self, '_quality_start', quality_start)

    def _get_team_result(self, game, team):
        if game._away_runs == game._home_runs:
            team_result = 'T'
        elif (team == 'away') == (game._away_runs > game._home_runs):
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

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class PlayerBoxscores:
    """
    All players' boxscore data from an individual MLB game.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

    team : string
        'away' or 'home'

    players_json : list (dict)
        List of dicts that contains the players' boxscore data.
    """

    def __init__(self, game, team, players_json):
        self._boxscores = []

        self._get_player_boxscores(game, team, players_json)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _get_player_boxscores(self, game, team, players_json):
        for player, stats in players_json['players'].items():
            boxscore = PlayerBoxscore(game, team, stats)
            if boxscore._mlb_player_id:  # some players don't have any stats
                self._boxscores.append(boxscore)

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

    def to_csv(self, filename):
        dataframe = self.dataframe
        dataframe.to_csv(filename)


class GameBoxscore:
    """
    Game stats from an individual MLB game.

    Parameters
    ----------
    game_id : int
        The game ID according to MLB's API.
    """

    def __init__(self, game_id):
        self._mlb_game_id = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        self._game_time = None
        self._day_night = None
        self._game_status = None
        self._away_team_id = None
        self._away_record_wins = None
        self._away_record_losses = None
        self._away_record_pct = None
        self._away_runs = None
        self._away_fly_outs = None
        self._away_ground_outs = None
        self._away_doubles = None
        self._away_triples = None
        self._away_home_runs = None
        self._away_strikeouts = None
        self._away_base_on_balls = None
        self._away_intentional_base_on_balls = None
        self._away_hits = None
        self._away_hit_by_pitch = None
        self._away_at_bats = None
        self._away_caught_stealing = None
        self._away_stolen_bases = None
        self._away_left_on_base = None
        self._home_team_id = None
        self._home_record_wins = None
        self._home_record_losses = None
        self._home_record_pct = None
        self._home_runs = None
        self._home_fly_outs = None
        self._home_ground_outs = None
        self._home_doubles = None
        self._home_triples = None
        self._home_home_runs = None
        self._home_strikeouts = None
        self._home_base_on_balls = None
        self._home_intentional_base_on_balls = None
        self._home_hits = None
        self._home_hit_by_pitch = None
        self._home_at_bats = None
        self._home_caught_stealing = None
        self._home_stolen_bases = None
        self._home_left_on_base = None
        self._home_plate_official_id = None
        self._first_base_official_id = None
        self._second_base_official_id = None
        self._third_base_official_id = None
        self._away_players = None
        self._home_players = None
        self._play_by_play = None
        # self._mlb_venue_id = None
        # self._series_description = None
        # self._series_game_number = None
        # self._games_in_series = None
        # self._extra_innings = None

        self._get_game_boxscore(game_id)

    def _get_game_boxscore(self, game_id):
        setattr(self, '_mlb_game_id', game_id)

        url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/feed/live'
        print(f'Getting game data from {url}')
        game = requests.get(url, verify=VERIFY_REQUESTS).json()
        utc = datetime.strptime(game['gameData']['datetime']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
        game_dt = utc_to_pst(utc)
        setattr(self, '_season', game['gameData']['game']['season'])
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_time', game_dt.time().isoformat())
        setattr(self, '_day_night', game['gameData']['datetime']['dayNight'])
        setattr(self, '_game_status', game['gameData']['status']['detailedState'])

        url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'
        print(f'Getting game boxscore data from {url}')
        box = requests.get(url, verify=VERIFY_REQUESTS).json()
        #box = game['liveData']['boxscore']
        away_team = box['teams']['away']['team']  # todo
        away_team_stats = box['teams']['away']['teamStats']
        home_team = box['teams']['away']['team']  # todo
        home_team_stats = box['teams']['home']['teamStats']
        setattr(self, '_away_team_id', away_team['id'])
        setattr(self, '_away_record_wins', away_team['record']['leagueRecord']['wins'])
        setattr(self, '_away_record_losses', away_team['record']['leagueRecord']['losses'])
        setattr(self, '_away_record_pct', away_team['record']['leagueRecord']['pct'])
        setattr(self, '_away_runs', away_team_stats['batting']['runs'])
        setattr(self, '_away_fly_outs', away_team_stats['batting']['flyOuts'])
        setattr(self, '_away_ground_outs', away_team_stats['batting']['groundOuts'])
        setattr(self, '_away_doubles', away_team_stats['batting']['doubles'])
        setattr(self, '_away_triples', away_team_stats['batting']['triples'])
        setattr(self, '_away_home_runs', away_team_stats['batting']['homeRuns'])
        setattr(self, '_away_strikeouts', away_team_stats['batting']['strikeOuts'])
        setattr(self, '_away_base_on_balls', away_team_stats['batting']['baseOnBalls'])
        setattr(self, '_away_intentional_base_on_balls', away_team_stats['batting']['intentionalWalks'])
        setattr(self, '_away_hits', away_team_stats['batting']['hits'])
        setattr(self, '_away_hit_by_pitch', away_team_stats['batting']['hitByPitch'])
        setattr(self, '_away_at_bats', away_team_stats['batting']['atBats'])
        setattr(self, '_away_caught_stealing', away_team_stats['batting']['caughtStealing'])
        setattr(self, '_away_stolen_bases', away_team_stats['batting']['stolenBases'])
        setattr(self, '_away_left_on_base', away_team_stats['batting']['leftOnBase'])
        setattr(self, '_home_team_id', box['teams']['home']['team']['id'])
        setattr(self, '_home_record_wins', home_team['record']['leagueRecord']['wins'])
        setattr(self, '_home_record_losses', home_team['record']['leagueRecord']['losses'])
        setattr(self, '_home_record_pct', home_team['record']['leagueRecord']['pct'])
        setattr(self, '_home_runs', home_team_stats['batting']['runs'])
        setattr(self, '_home_fly_outs', home_team_stats['batting']['flyOuts'])
        setattr(self, '_home_ground_outs', home_team_stats['batting']['groundOuts'])
        setattr(self, '_home_doubles', home_team_stats['batting']['doubles'])
        setattr(self, '_home_triples', home_team_stats['batting']['triples'])
        setattr(self, '_home_home_runs', home_team_stats['batting']['homeRuns'])
        setattr(self, '_home_strikeouts', home_team_stats['batting']['strikeOuts'])
        setattr(self, '_home_base_on_balls', home_team_stats['batting']['baseOnBalls'])
        setattr(self, '_home_intentional_base_on_balls', home_team_stats['batting']['intentionalWalks'])
        setattr(self, '_home_hits', home_team_stats['batting']['hits'])
        setattr(self, '_home_hit_by_pitch', home_team_stats['batting']['hitByPitch'])
        setattr(self, '_home_at_bats', home_team_stats['batting']['atBats'])
        setattr(self, '_home_caught_stealing', home_team_stats['batting']['caughtStealing'])
        setattr(self, '_home_stolen_bases', home_team_stats['batting']['stolenBases'])
        setattr(self, '_home_left_on_base', home_team_stats['batting']['leftOnBase'])

        setattr(self, '_home_plate_official_id', self._get_official_id_by_type(box['officials'], 'Home Plate'))
        setattr(self, '_first_base_official_id', self._get_official_id_by_type(box['officials'], 'First Base'))
        setattr(self, '_second_base_official_id', self._get_official_id_by_type(box['officials'], 'Second Base'))
        setattr(self, '_third_base_official_id', self._get_official_id_by_type(box['officials'], 'Third Base'))

        setattr(self, '_mlb_venue_id', None if 'id' not in game['gameData']
                ['venue'] else game['gameData']['venue']['id'])
        # setattr(self, '_series_description', game['seriesDescription'])
        # setattr(self, '_series_game_number', game['seriesGameNumber'])
        # setattr(self, '_games_in_series', game['gamesInSeries'])
        # setattr(self, '_extra_innings', 'todo')

        setattr(self, '_away_players', PlayerBoxscores(self, 'away', box['teams']['away']))
        setattr(self, '_home_players', PlayerBoxscores(self, 'home', box['teams']['home']))
        setattr(self, '_play_by_play', PlayByPlay(game_id))

    def _get_official_id_by_type(self, officials, official_type):
        for official in officials:
            if official['officialType'] == official_type:
                return official['official']['id']

    @property
    def players(self):
        return self._away_players._boxscores + self._home_players._boxscores

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbGameId': self._mlb_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'DayNight': self._day_night,
            'GameStatus': self._game_status,
            'AwayTeamId': self._away_team_id,
            'AwayRecordWins': self._away_record_wins,
            'AwayRecordLosses': self._away_record_losses,
            'AwayRecordPct': self._away_record_pct,
            'AwayRuns': self._away_runs,
            'AwayFlyOuts': self._away_fly_outs,
            'AwayGroundOuts': self._away_ground_outs,
            'AwayDoubles': self._away_doubles,
            'AwayTriples': self._away_triples,
            'AwayHomeRuns': self._away_home_runs,
            'AwayStrikeouts': self._away_strikeouts,
            'AwayBaseOnBalls': self._away_base_on_balls,
            'AwayIntentionalBaseOnBalls': self._away_intentional_base_on_balls,
            'AwayHits': self._away_hits,
            'AwayHitByPitch': self._away_hit_by_pitch,
            'AwayAtBats': self._away_at_bats,
            'AwayCaughtStealing': self._away_caught_stealing,
            'AwayStolenBases': self._away_stolen_bases,
            'AwayLeftOnBase': self._away_left_on_base,
            'HomeTeamId': self._home_team_id,
            'HomeRecordWins': self._home_record_wins,
            'HomeRecordLosses': self._home_record_losses,
            'HomeRecordPct': self._home_record_pct,
            'HomeRuns': self._home_runs,
            'HomeFlyOuts': self._home_fly_outs,
            'HomeGroundOuts': self._home_ground_outs,
            'HomeDoubles': self._home_doubles,
            'HomeTriples': self._home_triples,
            'HomeHomeRuns': self._home_home_runs,
            'HomeStrikeouts': self._home_strikeouts,
            'HomeBaseOnBalls': self._home_base_on_balls,
            'HomeIntentionalBaseOnBalls': self._home_intentional_base_on_balls,
            'HomeHits': self._home_hits,
            'HomeHitByPitch': self._home_hit_by_pitch,
            'HomeAtBats': self._home_at_bats,
            'HomeCaughtStealing': self._home_caught_stealing,
            'HomeStolenBases': self._home_stolen_bases,
            'HomeLeftOnBase': self._home_left_on_base,
            'HomePlateOfficialId': self._home_plate_official_id,
            'FirstBaseOfficialId': self._first_base_official_id,
            'SecondBaseOfficialId': self._second_base_official_id,
            'ThirdBaseOfficialId': self._third_base_official_id,
            'MlbVenueId': self._mlb_venue_id,
            # 'SeriesDescription': self._series_description,
            # 'SeriesGameNumber': self._series_game_number,
            # 'GamesInSeries': self._games_in_series,
            # 'ExtraInnings': self._extra_innings
        }
        return pd.DataFrame([fields_to_include], index=[self._mlb_game_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['AwayPlayers'] = self._away_players.to_dicts
        dic['HomePlayers'] = self._home_players.to_dicts
        return dic


class GameBoxscores:
    """
    Game stats from multiple MLB games.

    Parameters (kwargs)
    ----------
    season : int
        Season (year) to get game boxscores from.

    range : list
        Date range (inclusive) to get game boxscores from.
        range[0] = start, range[1] end ('MM/DD/YYYY' format).

    date : string
        Date to get game boxscores from ('MM/DD/YYYY' format).
    """

    def __init__(self, **kwargs):
        self._boxscores = []

        if 'season' in kwargs:
            start_date, end_date = get_dates_by_season(kwargs['season'])
            return
        elif 'range' in kwargs:
            start_date, end_date = kwargs['range'][0], kwargs['range'][1]
        elif 'date' in kwargs:
            start_date, end_date = kwargs['date'], kwargs['date']
        else:
            print('Invalid Game param(s)')
            return

        self._get_game_boxscores(start_date, end_date)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _get_game_boxscores(self, start_date, end_date):
        url = f'https://statsapi.mlb.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1'
        print('Getting MLB schedule from ' + url)
        schedule = requests.get(url, verify=VERIFY_REQUESTS).json()
        for date in schedule['dates']:
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

                boxscore = GameBoxscore(game_data['gamePk'])
                self._boxscores.append(boxscore)
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

    @property
    def player_dataframes(self):
        players = []
        for game in self._boxscores:
            away_players = game._away_players.dataframes
            home_players = game._home_players.dataframes
            players.append(pd.concat([away_players, home_players]))
        return pd.concat(players)

    def to_csv(self, filename):
        dataframes = self.dataframes
        dataframes.to_csv(filename)