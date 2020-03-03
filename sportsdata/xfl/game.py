import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from .boxscore import Boxscores
from .constants import CURRENT_SEASON
from .scoring import ScoringPlays
from .util import get_game_ids_by_season_and_week
from datetime import datetime, timedelta
from dateutil import tz
from selenium import webdriver
from time import sleep


class Game:
    def __init__(self, game_id, wd):
        self._xfl_game_id = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        self._game_time = None
        self._game_status = None
        self._away_team_id = None
        self._away_points = None
        self._away_first_downs = None
        self._away_rush_attempts = None
        self._away_rush_yards = None
        self._away_rush_touchdowns = None
        self._away_pass_completions = None
        self._away_pass_attempts = None
        self._away_pass_yards = None
        self._away_pass_touchdowns = None
        self._away_interceptions = None
        self._away_times_sacked = None
        self._away_yards_lost_from_sacks = None
        self._away_net_pass_yards = None
        self._away_total_yards = None
        self._away_fumbles = None
        self._away_fumbles_lost = None
        self._away_turnovers = None
        self._away_penalties = None
        self._away_yards_from_penalties = None
        self._away_third_down_conversions = None
        self._away_third_down_attempts = None
        self._away_fourth_down_conversions = None
        self._away_fourth_down_attempts = None
        self._away_time_of_possession = None
        self._away_record_wins = None
        self._away_record_losses = None
        self._away_record_pct = None
        self._home_team_id = None
        self._home_points = None
        self._home_first_downs = None
        self._home_rush_attempts = None
        self._home_rush_yards = None
        self._home_rush_touchdowns = None
        self._home_pass_completions = None
        self._home_pass_attempts = None
        self._home_pass_yards = None
        self._home_pass_touchdowns = None
        self._home_interceptions = None
        self._home_times_sacked = None
        self._home_yards_lost_from_sacks = None
        self._home_net_pass_yards = None
        self._home_total_yards = None
        self._home_fumbles = None
        self._home_fumbles_lost = None
        self._home_turnovers = None
        self._home_penalties = None
        self._home_yards_from_penalties = None
        self._home_third_down_conversions = None
        self._home_third_down_attempts = None
        self._home_fourth_down_conversions = None
        self._home_fourth_down_attempts = None
        self._home_time_of_possession = None
        self._home_team_record_wins = None
        self._home_team_record_losses = None
        self._home_team_record_pct = None
        self._xfl_venue_id = None

        self._boxscores = None
        self._scoring_plays = None #todo

        self._set_game(game_id, wd)

    def _set_game(self, game_id, wd):
        if wd == None:
            wd = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
            wd.maximize_window()
        url = f'https://stats.xfl.com/{game_id}'
        print('Getting XFL game data from ' + url)
        wd.get(url)
        sleep(5)
        game_stats_table = wd.find_elements_by_class_name('statDisplay.team')[0]   
        game_stats_bodies = game_stats_table.find_elements_by_class_name('body')
        away_stats, home_stats = {}, {}
        for game_stats_body in game_stats_bodies:
            game_stats_rows = game_stats_body.find_elements_by_class_name('row')
            for tr in game_stats_rows:
                divs = tr.find_elements_by_tag_name('div')
                col = divs[0].get_attribute('textContent')
                away_value = divs[1].get_attribute('textContent')
                home_value = divs[2].get_attribute('textContent')
                away_stats[col] = away_value
                home_stats[col] = home_value

        setattr(self, '_xfl_game_id', game_id) 
        setattr(self, '_away_first_downs', away_stats['Total First Downs'])
        setattr(self, '_away_rush_attempts', away_stats['Attempts'])
        setattr(self, '_away_rush_yards', away_stats['Net Rushing Yards'])
        setattr(self, '_away_rush_touchdowns', away_stats['TD Rushing-Passing-Defensive'].split('-')[0])
        setattr(self, '_away_pass_completions', away_stats['Completed/Attempts'].split('/')[0])
        setattr(self, '_away_pass_attempts', away_stats['Completed/Attempts'].split('/')[1].split()[0])
        setattr(self, '_away_pass_yards', away_stats['Net Passing Yards'])
        setattr(self, '_away_interceptions', away_stats['Interceptions'])
        setattr(self, '_away_times_sacked', away_stats['Sacks/Yards'].split('/')[0]) #todo-check this is correct
        setattr(self, '_away_yards_lost_from_sacks', away_stats['Sacks/Yards'].split('/')[1]) #todo-check this is correct
        #todo- net pass yards?
        setattr(self, '_away_fumbles_lost', away_stats['Fumbles Lost'])
        setattr(self, '_away_turnovers', away_stats['Turnovers'])
        setattr(self, '_away_penalty_yards', away_stats['Penalty Yards']) #yards from penalties?
        setattr(self, '_away_total_yards', away_stats['Total Net Yards'])
        setattr(self, '_away_third_down_conversions', away_stats['Third Down'].split()[0].split('/')[0])
        setattr(self, '_away_third_down_attempts', away_stats['Third Down'].split()[0].split('/')[1])
        setattr(self, '_away_fourth_down_conversions', away_stats['Fourth Down'].split()[0].split('/')[0])
        setattr(self, '_away_fourth_down_attempts', away_stats['Fourth Down'].split()[0].split('/')[1])

        setattr(self, '_home_first_downs', home_stats['Total First Downs'])
        setattr(self, '_home_rush_attempts', home_stats['Attempts'])
        setattr(self, '_home_rush_yards', home_stats['Net Rushing Yards'])
        setattr(self, '_home_rush_touchdowns', home_stats['TD Rushing-Passing-Defensive'].split('-')[0])
        setattr(self, '_home_pass_completions', home_stats['Completed/Attempts'].split('/')[0])
        setattr(self, '_home_pass_attempts', home_stats['Completed/Attempts'].split('/')[1].split()[0])
        setattr(self, '_home_pass_yards', home_stats['Net Passing Yards'])
        setattr(self, '_home_interceptions', home_stats['Interceptions'])
        setattr(self, '_home_times_sacked', home_stats['Sacks/Yards'].split('/')[0]) #todo-check this is correct
        setattr(self, '_home_yards_lost_from_sacks', home_stats['Sacks/Yards'].split('/')[1]) #todo-check this is correct
        #todo- net pass yards?
        setattr(self, '_home_fumbles_lost', home_stats['Fumbles Lost'])
        setattr(self, '_home_turnovers', home_stats['Turnovers'])
        setattr(self, '_home_penalty_yards', home_stats['Penalty Yards']) #yards from penalties?
        setattr(self, '_home_total_yards', home_stats['Total Net Yards'])
        setattr(self, '_home_third_down_conversions', home_stats['Third Down'].split()[0].split('/')[0])
        setattr(self, '_home_third_down_attempts', home_stats['Third Down'].split()[0].split('/')[1])
        setattr(self, '_home_fourth_down_conversions', home_stats['Fourth Down'].split()[0].split('/')[0])
        setattr(self, '_home_fourth_down_attempts', home_stats['Fourth Down'].split()[0].split('/')[1])

        #setattr(self, '_boxscores', Boxscores(id=game_id))
        #setattr(self, '_scoring_plays', ScoringPlays())

    @property
    def dataframe(self):
        fields_to_include = {
            'XflGameId': self._xfl_game_id,

            'AwayFirstDowns': self._away_first_downs,
            'AwayRushAttempts': self._away_rush_attempts,
            'AwayRushYards': self._away_rush_yards,
            'AwayRushTouchdowns': self._away_rush_touchdowns,
            'AwayPassCompletions': self._away_pass_completions,
            'AwayPassAttempts': self._away_pass_attempts,
            'AwayPassYards': self._away_pass_yards,
            'AwayInterceptions': self._away_interceptions,
            'AwayTimesSacked': self._away_times_sacked,
            'AwayYardsLostFromSacks': self._away_yards_lost_from_sacks,
            'AwayFumblesLost': self._away_fumbles_lost,
            'AwayTurnovers': self._away_turnovers,
            'AwayPenaltyYards': self._away_penalty_yards,
            'AwayTotalYards': self._away_total_yards,
            'AwayThirdDownConversions': self._away_third_down_conversions,
            'AwayThirdDownAttempts': self._away_third_down_attempts,
            'AwayFourthDownConversions': self._away_fourth_down_conversions,
            'AwayFourthDownAttempts': self._away_fourth_down_attempts,
            'HomeFirstDowns': self._home_first_downs,
            'HomeRushAttempts': self._home_rush_attempts,
            'HomeRushYards': self._home_rush_yards,
            'HomeRushTouchdowns': self._home_rush_touchdowns,
            'HomePassCompletions': self._home_pass_completions,
            'HomePassAttempts': self._home_pass_attempts,
            'HomePassYards': self._home_pass_yards,
            'HomeInterceptions': self._home_interceptions,
            'HomeTimesSacked': self._home_times_sacked,
            'HomeYardsLostFromSacks': self._home_yards_lost_from_sacks,
            'HomeFumblesLost': self._home_fumbles_lost,
            'HomeTurnovers': self._home_turnovers,
            'HomePenaltyYards': self._home_penalty_yards,
            'HomeTotalYards': self._home_total_yards,
            'HomeThirdDownConversions': self._home_third_down_conversions,
            'HomeThirdDownAttempts': self._home_third_down_attempts,
            'HomeFourthDownConversions': self._home_fourth_down_conversions,
            'HomeFourthDownAttempts': self._home_fourth_down_attempts
        }
        return pd.DataFrame([fields_to_include], index=[self._xfl_game_id])


class Games:
    """
    XFL games

    Parameters
    ----------
    season : int
        XFL season.

    week : int
        XFL week number.

    id : int
        XFL game ID.
    """
    def __init__(self, **kwargs):
        self._games = []

        game_ids = []
        if 'season' in kwargs:
            season = kwargs['season']  # todo
            for week in range(1, 11):
                week_game_ids = get_game_ids_by_season_and_week(season, week)
                game_ids.append(week_game_ids)
        elif 'week' in kwargs:
            season = CURRENT_SEASON
            week = kwargs['week']
            game_ids = get_game_ids_by_season_and_week(season, week)
        elif 'id' in kwargs:
            game_id = kwargs['id']
            game_ids = [game_id]

        self._get_games(game_ids)

    def __repr__(self):
        return self._games

    def __iter__(self):
        return iter(self.__repr__())

    def _get_games(self, game_ids):
        wd = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        wd.maximize_window()
        for game_id in game_ids:
            game = Game(game_id, wd)
            self._games.append(game)

    @property
    def dataframes(self):
        frames = []
        for game in self.__iter__():
            frames.append(game.dataframe)
        return pd.concat(frames)
