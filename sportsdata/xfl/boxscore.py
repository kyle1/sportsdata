import pandas as pd
import requests
from .constants import CURRENT_SEASON
from .scoring import ScoringPlays
from .util import get_game_ids_by_season_and_week
from bs4 import BeautifulSoup
from collections import ChainMap
from itertools import groupby
from pyquery import PyQuery as pq
from selenium import webdriver
from time import sleep


class PlayerBoxscore:
    """
    Player's boxscore data from an individual XFL game.

    Parameters
    ----------
    box_json : dict
        Dict that contains the player's boxscore data.

    scoring_plays : ScoringPlays
        Object that contains scoring play information.
    """
    def __init__(self, box_json, scoring_plays):
        # self._xfl_player_id = None
        self._player_name = None
        self._xfl_game_id = None
        self._season = None
        self._away_team_id = None
        self._home_team_id = None
        self._is_away = None
        self._team_result = None
        self._result_note = None
        self._overtime = None
        self._passing_completions = None
        self._passing_attempts = None
        self._passing_completion_pct = None
        self._passing_yards = None
        self._passing_long = None
        self._passing_touchdowns = None
        self._passing_interceptions = None
        self._passing_rating = None
        self._rushing_attempts = None
        self._rushing_yards = None
        self._rushing_average = None
        self._rushing_long = None
        self._rushing_touchdowns = None
        self._receiving_targets = None
        self._receptions = None
        self._receiving_yards = None
        self._receiving_average = None
        self._receiving_long = None
        self._receiving_touchdowns = None

        self._parse_boxscore(box_json, scoring_plays)

    def _parse_boxscore(self, box, scoring_plays):
        setattr(self, '_player_name', box['PlayerName'])
        setattr(self, '_xfl_game_id', box['XflGameId'])
        setattr(self, '_away_team', box['AwayTeam'])
        setattr(self, '_home_team', box['HomeTeam'])
        setattr(self, '_is_away', box['IsAway'])
        setattr(self, '_team_result', box['TeamResult'])

        if 'PassingAttempts' in box:
            setattr(self, '_passing_completions', box['PassingCompletions'])
            setattr(self, '_passing_attempts', box['PassingAttempts'])
            setattr(self, '_passing_completion_pct', box['PassingCompletionPct'])
            setattr(self, '_passing_yards', box['PassingYards'])
            setattr(self, '_passing_long', box['PassingLong'])
            setattr(self, '_passing_touchdowns', box['PassingTouchdowns'])
            setattr(self, '_passing_interceptions', box['PassingInterceptions'])
            setattr(self, '_passing_rating', box['PassingRating'])

        if 'RushingAttempts' in box:
            setattr(self, '_rushing_attempts', box['RushingAttempts'])
            setattr(self, '_rushing_yards', box['RushingYards'])
            setattr(self, '_rushing_average', box['RushingAverage'])
            setattr(self, '_rushing_long', box['RushingLong'])
            setattr(self, '_rushing_touchdowns', box['RushingTouchdowns'])

        if 'ReceivingTargets' in box:
            setattr(self, '_receiving_targets', box['ReceivingTargets'])
            setattr(self, '_receptions', box['Receptions'])
            setattr(self, '_receiving_yards', box['ReceivingYards'])
            setattr(self, '_receiving_average', box['ReceivingAverage'])
            setattr(self, '_receiving_long', box['ReceivingLong'])
            setattr(self, '_receiving_touchdowns', box['ReceivingTouchdowns'])

        setattr(self, '_one_point_conversions', self._get_point_conversions(box['PlayerName'], scoring_plays, 1))
        setattr(self, '_two_point_conversions', self._get_point_conversions(box['PlayerName'], scoring_plays, 2))
        setattr(self, '_three_point_conversions', self._get_point_conversions(box['PlayerName'], scoring_plays, 3))

    def _get_point_conversions(self, player_name, scoring_plays, points):
        conversions = 0
        conversion_description = f'{points}pt attempt successful.'
        for scoring_play in scoring_plays:
            play_description = scoring_play._play_description
            if player_name in play_description and conversion_description in play_description:
                conversions += 1
        return conversions

    @property
    def dataframe(self):
        fields_to_include = {
            # 'XflPlayerId': self._xfl_player_id,
            'PlayerName': self._player_name,
            'XflGameId': self._xfl_game_id,
            'Season': self._season,
            # 'AwayTeamId': self._away_team_id,
            'AwayTeam': self._away_team,
            # 'HomeTeamId': self._home_team_id,
            'HomeTeam': self._home_team,
            'IsAway': self._is_away,
            'TeamResult': self._team_result,
            'ResultNote': self._result_note,
            'Overtime': self._overtime,
            'PassingCompletions': self._passing_completions,
            'PassingAttempts': self._passing_attempts,
            'PassingCompletionPct': self._passing_completion_pct,
            'PassingYards': self._passing_yards,
            'PassingLong': self._passing_long,
            'PassingTouchdowns': self._passing_touchdowns,
            'PassingInterceptions': self._passing_interceptions,
            'PassingRating': self._passing_rating,
            'RushingAttempts': self._rushing_attempts,
            'RushingYards': self._rushing_yards,
            'RushingAverage': self._rushing_average,
            'RushingLong': self._rushing_long,
            'RushingTouchdowns': self._rushing_touchdowns,
            'ReceivingTargets': self._receiving_targets,
            'Receptions': self._receptions,
            'ReceivingYards': self._receiving_yards,
            'ReceivingAverage': self._receiving_average,
            'ReceivingLong': self._receiving_long,
            'ReceivingTouchdowns': self._receiving_touchdowns,
            'OnePointConversions': self._one_point_conversions,
            'TwoPointConversions': self._two_point_conversions,
            'ThreePointConversions': self._three_point_conversions,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class PlayerBoxscores:
    """
    All players' boxscore data from an individual XFL game.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

    wd : Selenium WebDriver
        The Selenium web driver used to scrape XFL's website.
    """
    def __init__(self, game, wd):
        self._boxscores = []

        self._get_player_boxscores(game, wd)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _parse_passing_stats(self, game, rows, is_away):
        passing_stats = []
        for row in rows:
            td_list = row.text.split('\n')
            if len(td_list) > 1:
                player_passing = {
                    'JerseryNumber': td_list[0],
                    'PlayerName': td_list[1],
                    'XflGameId': game._xfl_game_id,
                    'AwayTeam': game._away_team,
                    'HomeTeam': game._home_team,
                    'IsAway': is_away,
                    'TeamResult': self._get_team_result(is_away, game._away_points, game._home_points),
                    'PassingCompletions': td_list[2],
                    'PassingAttempts': td_list[3],
                    'PassingCompletionPct': td_list[4],
                    'PassingYards': td_list[5],
                    'PassingLong': td_list[8],
                    'PassingTouchdowns': td_list[9],
                    'PassingInterceptions': td_list[10],
                    'PassingRating': td_list[11]
                }
                passing_stats.append(player_passing)
        return passing_stats

    def _parse_rushing_stats(self, game, rows, is_away):
        rushing_stats = []
        for row in rows:
            td_list = row.text.split('\n')
            if len(td_list) > 1:
                player_rushing = {
                    'JerseryNumber': td_list[0],
                    'PlayerName': td_list[1],
                    'XflGameId': game._xfl_game_id,
                    'AwayTeam': game._away_team,
                    'HomeTeam': game._home_team,
                    'IsAway': is_away,
                    'TeamResult': self._get_team_result(is_away, game._away_points, game._home_points),
                    'RushingAttempts': td_list[2],
                    'RushingYards': td_list[3],
                    'RushingAverage': td_list[4],
                    'RushingLong': td_list[5],
                    'RushingTouchdowns': td_list[6]
                }
                rushing_stats.append(player_rushing)
        return rushing_stats

    def _parse_receiving_stats(self, game, rows, is_away):
        receiving_stats = []
        for row in rows:
            td_list = row.text.split('\n')
            if len(td_list) > 1:
                player_receiving = {
                    'JerseryNumber': td_list[0],
                    'PlayerName': td_list[1],
                    'XflGameId': game._xfl_game_id,
                    'AwayTeam': game._away_team,
                    'HomeTeam': game._home_team,
                    'IsAway': is_away,
                    'TeamResult': self._get_team_result(is_away, game._away_points, game._home_points),
                    'ReceivingTargets': td_list[2],
                    'Receptions': td_list[3],
                    'ReceivingYards': td_list[4],
                    'ReceivingAverage': td_list[5],
                    'ReceivingLong': td_list[6],
                    'ReceivingTouchdowns': td_list[7]
                }
                receiving_stats.append(player_receiving)
        return receiving_stats

    def _parse_stat_tables(self, game, stat_tables, is_away):
        rushing_rows = stat_tables[0].find_elements_by_class_name('row')[1:]
        rushing_stats = self._parse_rushing_stats(game, rushing_rows, is_away)
        passing_rows = stat_tables[1].find_elements_by_class_name('row')[1:]
        passing_stats = self._parse_passing_stats(game, passing_rows, is_away)
        receiving_rows = stat_tables[2].find_elements_by_class_name('row')[1:]
        receiving_stats = self._parse_receiving_stats(game, receiving_rows, is_away)
        return rushing_stats + passing_stats + receiving_stats

    def _get_player_boxscores(self, game, wd):
        #wd = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        #wd.maximize_window()

        all_boxscores = []
        #for game_id in game_ids:
            #url = f'https://stats.xfl.com/{game_id}'
            #print('Getting boxscore data from ' + url)
            #wd.get(url)
            #sleep(12)

        away_team = wd.find_elements_by_xpath(
            '//div[contains(@class, "visitStroke")]')[0].get_attribute('class').split(' ')[1][4:]
        home_team = wd.find_elements_by_xpath(
            '//div[contains(@class, "homeStroke")]')[0].get_attribute('class').split(' ')[1][4:]
        away_score = wd.find_elements_by_xpath('//h2[@class = "score visitor"]')[0].text
        home_score = wd.find_elements_by_xpath('//h2[@class = "score home"]')[0].text

        away_div = wd.find_element_by_id('visitorIndOffenseStats')
        away_tables = away_div.find_elements_by_class_name('table')[:3]
        away_stats = self._parse_stat_tables(game, away_tables, True)
        home_div = wd.find_element_by_id('homeIndOffenseStats')
        home_tables = home_div.find_elements_by_class_name('table')[:3]
        home_stats = self._parse_stat_tables(game, home_tables, False)
        all_stats = away_stats + home_stats

        combined = map(lambda dict_tuple: dict(ChainMap(*dict_tuple[1])),
                        groupby(sorted(all_stats,
                                        key=lambda sub_dict: sub_dict['PlayerName']),
                                key=lambda sub_dict: sub_dict['PlayerName']))

        all_boxscores = all_boxscores + list(combined)

        scoring_table = wd.find_elements_by_xpath('//div[@class = "statDisplay playlistScoring scoreTable"]')[0]
        scoring_plays = ScoringPlays(game, scoring_table)

        for box in all_boxscores:
            boxscore = PlayerBoxscore(box, scoring_plays)
            self._boxscores.append(boxscore)

        #wd.close()

    def _get_team_result(self, is_away, away_score, home_score):
        if away_score == home_score:
            return 'T'
        elif is_away == (away_score > home_score):
            return 'W'
        else:
            return 'L'

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
    Game stats from an individual XFL game.

    Parameters
    ----------
    game_id : int
        The game ID according to XFL's website.

    wd : Selenium WebDriver
        The Selenium web driver used to scrape XFL's website.
    """
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

        self._players = None
        #self._scoring_plays = None  # todo
        
        self._away_team = None
        self._home_team = None
        setattr(self, '_away_team', 'todo_away')
        setattr(self, '_home_team', 'todo_home')

        self._get_game_boxscore(game_id, wd)

    def _get_game_boxscore(self, game_id, wd):
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
        setattr(self, '_away_times_sacked', away_stats['Sacks/Yards'].split('/')[0])  # todo-check this is correct
        setattr(self, '_away_yards_lost_from_sacks',
                away_stats['Sacks/Yards'].split('/')[1])  # todo-check this is correct
        # todo- net pass yards?
        setattr(self, '_away_fumbles_lost', away_stats['Fumbles Lost'])
        setattr(self, '_away_turnovers', away_stats['Turnovers'])
        setattr(self, '_away_penalty_yards', away_stats['Penalty Yards'])  # yards from penalties?
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
        setattr(self, '_home_times_sacked', home_stats['Sacks/Yards'].split('/')[0])  # todo-check this is correct
        setattr(self, '_home_yards_lost_from_sacks',
                home_stats['Sacks/Yards'].split('/')[1])  # todo-check this is correct
        # todo- net pass yards?
        setattr(self, '_home_fumbles_lost', home_stats['Fumbles Lost'])
        setattr(self, '_home_turnovers', home_stats['Turnovers'])
        setattr(self, '_home_penalty_yards', home_stats['Penalty Yards'])  # yards from penalties?
        setattr(self, '_home_total_yards', home_stats['Total Net Yards'])
        setattr(self, '_home_third_down_conversions', home_stats['Third Down'].split()[0].split('/')[0])
        setattr(self, '_home_third_down_attempts', home_stats['Third Down'].split()[0].split('/')[1])
        setattr(self, '_home_fourth_down_conversions', home_stats['Fourth Down'].split()[0].split('/')[0])
        setattr(self, '_home_fourth_down_attempts', home_stats['Fourth Down'].split()[0].split('/')[1])

        setattr(self, '_players', PlayerBoxscores(self, wd))
        setattr(self, '_scoring_plays', ScoringPlays(self, wd)) #todo

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

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['AwayPlayers'] = self._away_players.to_dicts
        dic['HomePlayers'] = self._home_players.to_dicts
        return dic


class GameBoxscores:
    """
    Game stats from multiple XFL games.

    Parameters (kwargs)
    ----------
    season : int
        Season (year) to get game boxscores from.

    week : int
        XFL week number to get game boxscores from.

    id : int
        XFL game ID according to XFL's website.
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
            game = GameBoxscore(game_id, wd)
            self._games.append(game)

    @property
    def dataframes(self):
        frames = []
        for game in self.__iter__():
            frames.append(game.dataframe)
        return pd.concat(frames)

    @property
    def player_dataframes(self):
        frames = []
        for game in self._boxscores:
            players = game._players.dataframes
            frames.append(players)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for boxscore in self.__iter__():
            dics.append(boxscore.to_dict)
        return dics