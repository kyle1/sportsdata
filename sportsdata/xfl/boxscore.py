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


class Boxscore:
    def __init__(self, game, team, box_json, scoring_plays):
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

        self._get_boxscore_from_json(game, team, box_json, scoring_plays)

    def _get_boxscore_from_json(self, game, team, box, scoring_plays):
        setattr(self, '_player_name', box['Player'])
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

        setattr(self, '_one_point_conversions', self._get_point_conversions(box, scoring_plays, 1))
        setattr(self, '_two_point_conversions', self._get_point_conversions(box, scoring_plays, 2))
        setattr(self, '_three_point_conversions', self._get_point_conversions(box, scoring_plays, 3))

    def _get_point_conversions(self, box, scoring_plays, points):
        conversions = 0
        conversion_description = f'{points}pt attempt successful.'
        for scoring_play in scoring_plays:
            play_description = scoring_play._play_description
            if box['Player'] in play_description and conversion_description in play_description:
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


class Boxscores:
    def __init__(self, **kwargs):
        self._boxscores = []

        if 'week' in kwargs:
            season = CURRENT_SEASON
            week = kwargs['week']
            game_ids = xfl.util.get_game_ids_by_season_and_week(season, week)
        elif 'id' in kwargs:
            game_ids = [kwargs['id']]

        self._get_boxscores_by_game_ids(game_ids)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _parse_passing_stats(self, game_info, rows, is_away):
        passing_stats = []

        if game_info['visitor_score'] == game_info['home_score']:
            team_result = 'T'
        elif (is_away == (game_info['visitor_score'] > game_info['home_score'])):
            team_result = 'W'
        else:
            team_result = 'L'

        for row in rows:
            td_list = row.text.split('\n')
            if len(td_list) > 1:
                player_passing = {
                    'JerseryNumber': td_list[0],
                    'Player': td_list[1],
                    'XflGameId': game_info['game_id'],
                    'AwayTeam': game_info['visitor_team'],
                    'HomeTeam': game_info['home_team'],
                    'IsAway': is_away,
                    'TeamResult': team_result,
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

    def _parse_rushing_stats(self, game_info, rows, is_away):
        rushing_stats = []

        if game_info['visitor_score'] == game_info['home_score']:
            team_result = 'T'
        elif (is_away == (game_info['visitor_score'] > game_info['home_score'])):
            team_result = 'W'
        else:
            team_result = 'L'

        for row in rows:
            td_list = row.text.split('\n')
            if len(td_list) > 1:
                player_rushing = {
                    'JerseryNumber': td_list[0],
                    'Player': td_list[1],
                    'XflGameId': game_info['game_id'],
                    'AwayTeam': game_info['visitor_team'],
                    'HomeTeam': game_info['home_team'],
                    'IsAway': is_away,
                    'TeamResult': team_result,
                    'RushingAttempts': td_list[2],
                    'RushingYards': td_list[3],
                    'RushingAverage': td_list[4],
                    'RushingLong': td_list[5],
                    'RushingTouchdowns': td_list[6]
                }
                rushing_stats.append(player_rushing)
        return rushing_stats

    def _parse_receiving_stats(self, game_info, rows, is_away):
        receiving_stats = []

        if game_info['visitor_score'] == game_info['home_score']:
            team_result = 'T'
        elif (is_away == (game_info['visitor_score'] > game_info['home_score'])):
            team_result = 'W'
        else:
            team_result = 'L'

        for row in rows:
            td_list = row.text.split('\n')
            if len(td_list) > 1:
                player_receiving = {
                    'JerseryNumber': td_list[0],
                    'Player': td_list[1],
                    'XflGameId': game_info['game_id'],
                    'AwayTeam': game_info['visitor_team'],
                    'HomeTeam': game_info['home_team'],
                    'IsAway': is_away,
                    'TeamResult': team_result,
                    'ReceivingTargets': td_list[2],
                    'Receptions': td_list[3],
                    'ReceivingYards': td_list[4],
                    'ReceivingAverage': td_list[5],
                    'ReceivingLong': td_list[6],
                    'ReceivingTouchdowns': td_list[7]
                }
                receiving_stats.append(player_receiving)
        return receiving_stats

    def _parse_stat_tables(self, game_info, tables, is_away):
        # Rushing
        rushing_table = tables[0]
        rushing_body = rushing_table.find_element_by_class_name('body')
        rushing_rows = rushing_body.find_elements_by_class_name('row')
        rushing_stats = self._parse_rushing_stats(game_info, rushing_rows, is_away)

        # Passing
        passing_table = tables[1]
        passing_body = passing_table.find_element_by_class_name('body')
        passing_rows = passing_body.find_elements_by_class_name('row')
        passing_stats = self._parse_passing_stats(game_info, passing_rows, is_away)

        # Receiving
        receiving_table = tables[2]
        receiving_body = receiving_table.find_element_by_class_name('body')
        receiving_rows = receiving_body.find_elements_by_class_name('row')
        receiving_stats = self._parse_receiving_stats(game_info, receiving_rows, is_away)

        return rushing_stats + passing_stats + receiving_stats

    def _get_boxscores_by_game_ids(self, game_ids):
        wd = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        wd.maximize_window()

        all_boxscores = []
        for game_id in game_ids:
            url = f'https://stats.xfl.com/{game_id}'
            print('Getting boxscore data from ' + url)
            wd.get(url)
            sleep(5)

            visitor_team = wd.find_elements_by_xpath('//div[contains(@class, "visitStroke")]')[0].get_attribute('class').split(' ')[1][4:]
            home_team = wd.find_elements_by_xpath('//div[contains(@class, "homeStroke")]')[0].get_attribute('class').split(' ')[1][4:]
            visitor_score = wd.find_elements_by_xpath('//h2[@class = "score visitor"]')[0].text
            home_score = wd.find_elements_by_xpath('//h2[@class = "score home"]')[0].text

            game_info = {
                'game_id': game_id,
                'visitor_team': visitor_team,
                'home_team': home_team,
                'visitor_score': visitor_score,
                'home_score': home_score
            }

            visitor_div = wd.find_element_by_id('visitorIndOffenseStats')
            visitor_tables = visitor_div.find_elements_by_class_name('table')[:3]
            visitor_stats = self._parse_stat_tables(game_info, visitor_tables, True)
            home_div = wd.find_element_by_id('homeIndOffenseStats')
            home_tables = home_div.find_elements_by_class_name('table')[:3]
            home_stats = self._parse_stat_tables(game_info, home_tables, False)
            all_stats = visitor_stats + home_stats

            combined = map(lambda dict_tuple: dict(ChainMap(*dict_tuple[1])),
                           groupby(sorted(all_stats,
                                          key=lambda sub_dict: sub_dict['Player']),
                                   key=lambda sub_dict: sub_dict['Player']))

            all_boxscores = all_boxscores + list(combined)

            scoring_table = wd.find_elements_by_xpath('//div[@class = "statDisplay playlistScoring scoreTable"]')[0]
            scoring_plays = ScoringPlays(game_id, scoring_table)
            #print(scoring_plays.dataframes)

        for box in all_boxscores:
            boxscore = Boxscore(None, None, box, scoring_plays)
            self._boxscores.append(boxscore)

        wd.close()

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)
