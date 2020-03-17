import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from time import sleep


class Play:
    """
    Represents a single play

    Parameters
    ----------
    game_id : int
        The game ID according to MLB's API.

    play_json : dict
        Dict that contains play information.
    """
    def __init__(self, game_id, play_json):
        self._mlb_game_id = None
        self._result_type = None
        self._event = None
        self._event_type = None
        self._description = None
        self._rbi = None
        self._away_score = None
        self._home_score = None
        self._at_bat_index = None
        self._half_inning = None
        self._is_top_inning = None
        self._inning = None
        self._is_scoring_play = None
        self._has_out = None
        self._count_balls = None
        self._count_strikes = None
        self._count_outs = None
        self._batter_id = None
        self._bat_side = None
        self._pitcher_id = None
        self._pitch_hand = None
        self._men_on_base = None

        setattr(self, '_mlb_game_id', game_id)
        self._get_play_from_json(play_json)

    def _get_play_from_json(self, play):
        setattr(self, '_result_type', play['result']['type'])
        setattr(self, '_event', play['result']['event'])
        setattr(self, '_event_type', play['result']['eventType'])
        setattr(self, '_description', play['result']['description'])
        setattr(self, '_rbi', play['result']['rbi'])
        setattr(self, '_away_score', play['result']['awayScore'])
        setattr(self, '_home_score', play['result']['homeScore'])
        setattr(self, '_at_bat_index', play['about']['atBatIndex'])
        setattr(self, '_half_inning', play['about']['halfInning'])
        setattr(self, '_is_top_inning', play['about']['isTopInning'])
        setattr(self, '_inning', play['about']['inning'])
        setattr(self, '_is_scoring_play', play['about']['isScoringPlay'])
        setattr(self, '_has_out', play['about']['hasOut'])
        setattr(self, '_count_balls', play['count']['balls'])
        setattr(self, '_count_strikes', play['count']['strikes'])
        setattr(self, '_count_outs', play['count']['outs'])
        setattr(self, '_batter_id', play['matchup']['batter']['id'])
        setattr(self, '_bat_side', play['matchup']['batSide']['code'])
        setattr(self, '_pitcher_id', play['matchup']['pitcher']['id'])
        setattr(self, '_pitch_hand', play['matchup']['pitchHand']['code'])
        setattr(self, '_men_on_base', play['matchup']['splits']['menOnBase'])

    @property
    def dataframe(self):
        fields_to_include = {
            'MlbGameId': self._mlb_game_id,
            'ResultType': self._result_type,
            'Event': self._event,
            'EventType': self._event_type,
            'Description': self._description,
            'Rbi': self._rbi,
            'AwayScore': self._away_score,
            'HomeScore': self._home_score,
            'AtBatIndex': self._at_bat_index,
            'HalfInning': self._half_inning,
            'IsTopInning': self._is_top_inning,
            'Inning': self._inning,
            'IsScoringPlay': self._is_scoring_play,
            'HasOut': self._has_out,
            'CountBalls': self._count_balls,
            'CountStrikes': self._count_strikes,
            'CountOuts': self._count_outs,
            'BatterId': self._batter_id,
            'BatSide': self._bat_side,
            'PitcherId': self._pitcher_id,
            'PitchHand': self._pitch_hand,
            'MenOnBase': self._men_on_base
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic
        

class PlayByPlay:
    """
    Represents all plays for an individual MLB game.

    Parameters
    ----------
    game_id : int
        The game ID according to MLB's API.
    """
    def __init__(self, game_id):
        self._plays = []

        self._get_play_by_play(game_id)

    def __repr__(self):
        return self._plays

    def __iter__(self):
        return iter(self.__repr__())

    def _get_play_by_play(self, game_id):
        url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/playByPlay'
        print('Getting play-by-play data from ' + url)
        pbp_json = requests.get(url, verify=VERIFY_REQUESTS).json()
        for play_json in pbp_json['allPlays']:
            play = Play(game_id, play_json)
            self._plays.append(play)

    @property
    def dataframes(self):
        frames = []
        for play in self.__iter__():
            frames.append(play.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for play in self.__iter__():
            dics.append(play.to_dict)
        return dics


# class PlayByPlays:
#     def __init__(self, games):
#         self._play_by_plays = []

#         self._get_play_by_plays(games)

#     def __repr__(self):
#         return self._play_by_plays

#     def __iter__(self):
#         return iter(self.__repr__())

#     def _get_play_by_plays(self, games):
#         for game in games:
#             pbp = PlayByPlay(game._mlb_game_id)
#             self._play_by_plays.append(pbp)
#             sleep(5)

#     @property
#     def dataframes(self):
#         frames = []
#         for pbp in self.__iter__():
#             frames.append(pbp.dataframes)
#         return pd.concat(frames)
