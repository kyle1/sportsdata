import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from time import sleep

# TODO- change this from nhl to mlb


class Play:
    """
    Represents a single play

    Parameters
    ----------
    game_id : int
        The game ID according to NHL's API.

    play_json : dict
        Dict that contains play information.
    """

    def __init__(self, game_id, play_json):
        self._nhl_game_id = None
        self._nhl_player_1_id = None
        self._nhl_player_1_type = None
        self._nhl_player_2_id = None
        self._nhl_player_2_type = None
        self._event = None
        self._description = None
        self._period = None
        self._period_type = None
        self._period_time = None
        self._period_time_remaining = None
        self._play_date_time = None
        self._away_goals = None
        self._home_goals = None

        setattr(self, '_nhl_game_id', game_id)
        self._get_play_from_json(play_json)

    def _get_play_from_json(self, play):
        if 'players' in play:
            players = play['players']
            setattr(self, '_nhl_player_1_id', players[0]['player']['id'])
            setattr(self, '_nhl_player_1_type', players[0]['playerType'])
            if len(players) > 1:
                setattr(self, '_nhl_player_2_id', players[1]['player']['id'])
                setattr(self, '_nhl_player_2_type', players[1]['playerType'])
        setattr(self, '_event', play['result']['event'])
        setattr(self, '_description', play['result']['description'])
        setattr(self, '_period', play['about']['period'])
        setattr(self, '_period_type', play['about']['periodType'])
        setattr(self, '_period_time', play['about']['periodTime'])
        setattr(self, '_period_time_remaining', play['about']['periodTimeRemaining'])
        setattr(self, '_play_date_time', play['about']['dateTime'])
        setattr(self, '_away_goals', play['about']['goals']['away'])
        setattr(self, '_home_goals', play['about']['goals']['away'])

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlGameId': self._nhl_game_id,
            'NhlPlayer1Id': self._nhl_player_1_id,
            'NhlPlayer1Type': self._nhl_player_1_type,
            'NhlPlayer2Id': self._nhl_player_2_id,
            'NhlPlayer2Type': self._nhl_player_2_type,
            'Event': self._event,
            'Description': self._description,
            'Period': self._period,
            'PeriodType': self._period_type,
            'PeriodTime': self._period_time,
            'PeriodTimeRemaining': self._period_time_remaining,
            'PlayDateTime': self._play_date_time,
            'AwayGoals': self._away_goals,
            'HomeGoals': self._home_goals
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class PlayByPlay:
    """
    Represents all plays for an individual NHL game.

    Parameters
    ----------
    game_id : int
        The game ID according to NHL's API.

    plays : dict
        Dict that contains the play-by-play data.
    """

    def __init__(self, game_id, plays):
        self._plays = []

        self._parse_play_by_play(game_id, plays)

    def __repr__(self):
        return self._plays

    def __iter__(self):
        return iter(self.__repr__())

    def _parse_play_by_play(self, game_id, plays):
        for play_json in plays:
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
