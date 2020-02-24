import mlb.util
import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from datetime import datetime, timedelta
from dateutil import tz


# this is the boxscore with both team's data.
# could have boxscore with data from one team's perspective?
class GameBoxscore:
    """
    Game stats for an individual game.

    Parameters
    ----------
    game_id : int
        A game ID according to MLB's API.
    """

    def __init__(self, game_id):
        self._mlb_game_id = None
        self._season = None
        self._game_date_time = None
        #self._game_status = None
        self._away_team_id = None
        self._away_runs = None
        self._away_fly_outs = None
        self._away_ground_outs = None
        self._away_doubles = None
        self._away_triples = None
        self._away_home_runs = None
        self._away_strikeouts = None
        self._away_base_on_balls = None
        self._away_intentional_bases_on_balls = None
        self._away_hits = None
        self._away_hit_by_pitch = None
        self._away_at_bats = None
        self._away_caught_stealing = None
        self._away_stolen_bases = None
        self._away_left_on_base = None

        self._home_team_id = None
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

        # self._away_team_record_wins = None
        # self._away_team_record_losses = None
        # self._away_team_record_pct = None
        # self._home_team_id = None
        # self._home_team_score = None
        # self._home_team_record_wins = None
        # self._home_team_record_losses = None
        # self._home_team_record_pct = None
        # self._mlb_venue_id = None
        # self._day_night = None
        # self._series_description = None
        # self._series_game_number = None
        # self._games_in_series = None
        # self._extra_innings = None

        self._get_game_boxscore(game_id)

    def _get_game_boxscore(self, game_id):
        # from_zone = tz.gettz('UTC')
        # to_zone = tz.gettz('America/Los_Angeles')
        # utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        # utc = utc.replace(tzinfo=from_zone)
        # pst = utc.astimezone(to_zone)
        # game_dt = pst.replace(tzinfo=None)
        url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'
        print(f'getting game boxscore data from {url}')
        game = requests.get(url, verify=VERIFY_REQUESTS).json()

        setattr(self, '_mlb_game_id', game_id)
        # setattr(self, '_season', game['seasonDisplay'])
        # setattr(self, '_game_date_time', game_dt.isoformat())
        # setattr(self, '_game_date', game_dt.date().isoformat())
        # setattr(self, '_game_time', game_dt.time().isoformat())
        # setattr(self, '_game_status', game['status']['detailedState'])

        setattr(self, '_away_team_id', game['teams']['away']['team']['id'])
        setattr(self, '_away_runs', game['teams']['away']['teamStats']['batting']['runs'])
        setattr(self, '_away_fly_outs', game['teams']['away']['teamStats']['batting']['flyOuts'])
        setattr(self, '_away_ground_outs', game['teams']['away']['teamStats']['batting']['groundOuts'])
        setattr(self, '_away_doubles', game['teams']['away']['teamStats']['batting']['doubles'])
        setattr(self, '_away_triples', game['teams']['away']['teamStats']['batting']['triples'])
        setattr(self, '_away_home_runs', game['teams']['away']['teamStats']['batting']['homeRuns'])
        setattr(self, '_away_strikeouts', game['teams']['away']['teamStats']['batting']['strikeOuts'])
        setattr(self, '_away_base_on_balls', game['teams']['away']['teamStats']['batting']['baseOnBalls'])
        setattr(self, '_away_intentional_base_on_balls', game['teams']['away']['teamStats']['batting']['intentionalWalks'])
        setattr(self, '_away_hits', game['teams']['away']['teamStats']['batting']['hits'])
        setattr(self, '_away_hit_by_pitch', game['teams']['away']['teamStats']['batting']['hitByPitch'])
        setattr(self, '_away_at_bats', game['teams']['away']['teamStats']['batting']['atBats'])
        setattr(self, '_away_caught_stealing', game['teams']['away']['teamStats']['batting']['caughtStealing'])
        setattr(self, '_away_stolen_bases', game['teams']['away']['teamStats']['batting']['stolenBases'])
        setattr(self, '_away_left_on_base', game['teams']['away']['teamStats']['batting']['leftOnBase'])

        setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        setattr(self, '_home_runs', game['teams']['home']['teamStats']['batting']['runs'])
        setattr(self, '_home_fly_outs', game['teams']['home']['teamStats']['batting']['flyOuts'])
        setattr(self, '_home_ground_outs', game['teams']['home']['teamStats']['batting']['groundOuts'])
        setattr(self, '_home_doubles', game['teams']['home']['teamStats']['batting']['doubles'])
        setattr(self, '_home_triples', game['teams']['home']['teamStats']['batting']['triples'])
        setattr(self, '_home_home_runs', game['teams']['home']['teamStats']['batting']['homeRuns'])
        setattr(self, '_home_strikeouts', game['teams']['home']['teamStats']['batting']['strikeOuts'])
        setattr(self, '_home_base_on_balls', game['teams']['home']['teamStats']['batting']['baseOnBalls'])
        setattr(self, '_home_intentional_base_on_balls', game['teams']['home']['teamStats']['batting']['intentionalWalks'])
        setattr(self, '_home_hits', game['teams']['home']['teamStats']['batting']['hits'])
        setattr(self, '_home_hit_by_pitch', game['teams']['home']['teamStats']['batting']['hitByPitch'])
        setattr(self, '_home_at_bats', game['teams']['home']['teamStats']['batting']['atBats'])
        setattr(self, '_home_caught_stealing', game['teams']['home']['teamStats']['batting']['caughtStealing'])
        setattr(self, '_home_stolen_bases', game['teams']['home']['teamStats']['batting']['stolenBases'])
        setattr(self, '_home_left_on_base', game['teams']['home']['teamStats']['batting']['leftOnBase'])

        setattr(self, '_home_plate_official_id', self._get_official_id_by_type(game['officials'], 'Home Plate'))
        setattr(self, '_third_base_official_id', self._get_official_id_by_type(game['officials'], 'First Base'))
        setattr(self, '_third_base_official_id', self._get_official_id_by_type(game['officials'], 'Second Base'))
        setattr(self, '_third_base_official_id', self._get_official_id_by_type(game['officials'], 'Third Base'))

        # setattr(self, '_away_team_score', game['teams']['away']['score'])
        # setattr(self, '_away_team_record_wins', game['teams']['away']['leagueRecord']['wins'])
        # setattr(self, '_away_team_record_losses', game['teams']['away']['leagueRecord']['losses'])
        # setattr(self, '_away_team_record_pct', game['teams']['away']['leagueRecord']['pct'])
        # setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        # setattr(self, '_home_team_score', game['teams']['home']['score'])
        # setattr(self, '_home_team_record_wins', game['teams']['home']['leagueRecord']['wins'])
        # setattr(self, '_home_team_record_losses', game['teams']['home']['leagueRecord']['losses'])
        # setattr(self, '_home_team_record_pct', game['teams']['home']['leagueRecord']['pct'])
        # setattr(self, '_mlb_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        # setattr(self, '_day_night', game['dayNight'])
        # setattr(self, '_series_description', game['seriesDescription'])
        # setattr(self, '_series_game_number', game['seriesGameNumber'])
        # setattr(self, '_games_in_series', game['gamesInSeries'])
        # setattr(self, '_extra_innings', 'todo')

    def _get_official_id_by_type(self, officials, official_type):
        for official in officials:
            if official['officialType'] == official_type:
                return official['official']['id']

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbGameId': self._mlb_game_id,
            # 'Season': self._season,
            # 'GameDateTime': self._game_date_time,
            # 'GameDate': self._game_date,
            # 'GameTime': self._game_time,
            # 'GameStatus': self._game_status,
            'AwayTeamId': self._away_team_id,
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
            'ThirdBaseOfficialId': self._third_base_official_id
            # 'AwayTeamScore': self._away_team_score,
            # 'AwayTeamRecordWins': self._away_team_record_wins,
            # 'AwayTeamRecordLosses': self._away_team_record_losses,
            # 'AwayTeamRecordPct': self._away_team_record_pct,
            # 'HomeTeamId': self._home_team_id,
            # 'HomeTeamScore': self._home_team_score,
            # 'HomeTeamRecordWins': self._home_team_record_wins,
            # 'HomeTeamRecordLosses': self._home_team_record_losses,
            # 'HomeTeamRecordPct': self._home_team_record_pct,
            # 'MlbVenueId': self._mlb_venue_id,
            # 'DayNight': self._day_night,
            # 'SeriesDescription': self._series_description,
            # 'SeriesGameNumber': self._series_game_number,
            # 'GamesInSeries': self._games_in_series,
            # 'ExtraInnings': self._extra_innings
        }
        return pd.DataFrame([fields_to_include], index=[self._mlb_game_id])


class GameBoxscores:
    """
    Game stats for multiple games.

    Parameters
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
