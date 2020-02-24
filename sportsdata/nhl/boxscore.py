import pandas as pd
import requests
from constants import VERIFY_REQUESTS
from time import sleep


class Boxscore:
    def __init__(self, game, team, box_json, shootout_goals, goalies_recorded):
        self._nhl_player_id = None
        self._nhl_game_id = None
        self._season = None
        self._away_team_id = None
        self._home_team_id = None
        self._is_away = None
        self._team_result = None
        self._result_note = None
        self._overtime = None
        self._shootout = None
        self._skater_time_on_ice = None
        self._skater_assists = None
        self._skater_goals = None
        self._skater_shots = None
        self._skater_hits = None
        self._skater_power_play_goals = None
        self._skater_power_play_assists = None
        self._skater_penalty_mins = None
        self._skater_takeaways = None
        self._skater_giveaways = None
        self._skater_short_handed_goals = None
        self._skater_short_handed_assists = None
        self._skater_blocked = None
        self._skater_plus_minus = None
        self._skater_even_time_on_ice = None
        self._skater_power_play_time_on_ice = None
        self._skater_short_handed_time_on_ice = None
        self._skater_shootout_goals = None
        self._goalie_time_on_ice = None
        self._goalie_assists = None
        self._goalie_goals = None
        self._goalie_pim = None
        self._goalie_shots_against = None
        self._goalie_saves = None
        self._goalie_goals_against = None
        self._goalie_power_play_saves = None
        self._goalie_short_handed_saves = None
        self._goalie_even_saves = None
        self._goalie_short_handed_shots_against = None
        self._goalie_even_shots_against = None
        self._goalie_power_play_shots_against = None
        self._goalie_decision = None
        self._goalie_save_pct = None
        self._goalie_power_play_save_pct = None
        self._goalie_even_strength_save_pct = None
        self._only_goalie = None

        self._get_boxscore_from_json(game, team, box_json, shootout_goals, goalies_recorded)

    def _get_boxscore_from_json(self, game, team, box, shootout_goals, goalies_recorded):
        has_skater_stats = 'skaterStats' in box['stats'] and len(box['stats']['skaterStats']) > 0
        has_goalie_stats = 'goalieStats' in box['stats'] and len(box['stats']['goalieStats']) > 0
        if not has_skater_stats and not has_goalie_stats:
            return

        setattr(self, '_nhl_player_id', box['person']['id'])
        setattr(self, '_nhl_game_id', game._nhl_game_id)
        setattr(self, '_season', game._season)
        setattr(self, '_away_team_id', game._away_team_id)
        setattr(self, '_home_team_id', game._home_team_id)
        setattr(self, '_is_away', team == 'away')
        setattr(self, '_team_result', self._get_team_result(game, team))
        setattr(self, '_result_note', game._result_note)
        setattr(self, '_overtime', game._overtime)
        setattr(self, '_shootout', game._shootout)

        if has_skater_stats:
            setattr(self, '_skater_time_on_ice', box['stats']['skaterStats']['timeOnIce'])
            setattr(self, '_skater_assists', box['stats']['skaterStats']['assists'])
            setattr(self, '_skater_goals', box['stats']['skaterStats']['goals'])
            setattr(self, '_skater_shots', box['stats']['skaterStats']['shots'])
            setattr(self, '_skater_hits', box['stats']['skaterStats']['hits'])
            setattr(self, '_skater_power_play_goals', box['stats']['skaterStats']['powerPlayGoals'])
            setattr(self, '_skater_power_play_assists', box['stats']['skaterStats']['powerPlayAssists'])
            if 'penaltyMinutes' in box['stats']['skaterStats']:
                setattr(self, '_skater_penalty_mins', box['stats']['skaterStats']['penaltyMinutes'])
            setattr(self, '_skater_takeaways', box['stats']['skaterStats']['takeaways'])
            setattr(self, '_skater_giveaways', box['stats']['skaterStats']['giveaways'])
            setattr(self, '_skater_short_handed_goals', box['stats']['skaterStats']['shortHandedGoals'])
            setattr(self, '_skater_short_handed_assists', box['stats']['skaterStats']['shortHandedAssists'])
            setattr(self, '_skater_blocked', box['stats']['skaterStats']['blocked'])
            setattr(self, '_skater_plus_minus', box['stats']['skaterStats']['plusMinus'])
            setattr(self, '_skater_even_time_on_ice', box['stats']['skaterStats']['evenTimeOnIce'])
            setattr(self, '_skater_power_play_time_on_ice', box['stats']['skaterStats']['powerPlayTimeOnIce'])
            setattr(self, '_skater_short_handed_time_on_ice', box['stats']['skaterStats']['shortHandedTimeOnIce'])
            setattr(self, '_skater_shootout_goals', self._get_player_shootout_goals(game, box, shootout_goals))

        if has_goalie_stats:
            setattr(self, '_goalie_time_on_ice', box['stats']['goalieStats']['timeOnIce'])
            setattr(self, '_goalie_assists', box['stats']['goalieStats']['assists'])
            setattr(self, '_goalie_goals', box['stats']['goalieStats']['goals'])
            setattr(self, '_goalie_pim', box['stats']['goalieStats']['pim'])
            setattr(self, '_goalie_shots_against', box['stats']['goalieStats']['shots'])
            setattr(self, '_goalie_saves', box['stats']['goalieStats']['saves'])
            setattr(self, '_goalie_goals_against', box['stats']['goalieStats']['shots'] - box['stats']['goalieStats']['saves'])
            setattr(self, '_goalie_power_play_saves', box['stats']['goalieStats']['powerPlaySaves'])
            setattr(self, '_goalie_short_handed_saves', box['stats']['goalieStats']['shortHandedSaves'])
            setattr(self, '_goalie_even_saves', box['stats']['goalieStats']['evenSaves'])
            setattr(self, '_goalie_short_handed_shots_against', box['stats']['goalieStats']['shortHandedShotsAgainst'])
            setattr(self, '_goalie_even_shots_against', box['stats']['goalieStats']['evenShotsAgainst'])
            setattr(self, '_goalie_power_play_shots_against', box['stats']['goalieStats']['powerPlayShotsAgainst'])
            if 'decision' in box['stats']['goalieStats']:
                setattr(self, '_goalie_decision', box['stats']['goalieStats']['decision'])
            if 'savePercentage' in box['stats']['goalieStats']:
                setattr(self, '_goalie_save_pct', box['stats']['goalieStats']['savePercentage'])
            if 'powerPlaySavePercentage' in box['stats']['goalieStats']:
                setattr(self, '_goalie_power_play_save_pct', box['stats']['goalieStats']['powerPlaySavePercentage'])
            if 'evenStrengthSavePercentage' in box['stats']['goalieStats']:
                setattr(self, '_goalie_even_strength_save_pct', box['stats']['goalieStats']['evenStrengthSavePercentage'])
            setattr(self, '_only_goalie', goalies_recorded == 1)

    def _get_team_result(self, game, team):
        if game._away_team_score == game._home_team_score:
            team_result = 'T'
        elif (team == 'away') == (game._away_team_score > game._home_team_score):
            team_result = 'W'
        else:
            team_result = 'L'
        return team_result

    def _get_player_shootout_goals(self, game, box, shootout_goals):
        skater_shootout_goals = 0
        if game._shootout:
            for player in shootout_goals:
                if player['player_id'] == int(box['person']['id']):
                    # Player had one or more shootout goals
                    skater_shootout_goals = player['shootout_goals']
                    break
        return skater_shootout_goals

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlPlayerId': self._nhl_player_id,
            'NhlGameId': self._nhl_game_id,
            'Season': self._season,
            'AwayTeamId': self._away_team_id,
            'HomeTeamId': self._home_team_id,
            'IsAway': self._is_away,
            'TeamResult': self._team_result,
            'ResultNote': self._result_note,
            'Overtime': self._overtime,
            'Shootout': self._shootout,
            'SkaterTimeOnIce': self._skater_time_on_ice,
            'SkaterAssists': self._skater_assists,
            'SkaterGoals': self._skater_goals,
            'SkaterShots': self._skater_shots,
            'SkaterHits': self._skater_hits,
            'SkaterPowerPlayGoals': self._skater_power_play_goals,
            'SkaterPowerPlayAssists': self._skater_power_play_assists,
            'SkaterPenaltyMins': self._skater_penalty_mins,
            'SkaterTakeaways': self._skater_takeaways,
            'SkaterGiveaways': self._skater_giveaways,
            'SkaterShortHandedGoals': self._skater_short_handed_goals,
            'SkaterShortHandedAssists': self._skater_short_handed_assists,
            'SkaterBlocked': self._skater_blocked,
            'SkaterPlusMinus': self._skater_plus_minus,
            'SkaterEvenTimeOnIce': self._skater_even_time_on_ice,
            'SkaterPowerPlayTimeOnIce': self._skater_power_play_time_on_ice,
            'SkaterShortHandedTimeOnIce': self._skater_short_handed_time_on_ice,
            'SkaterShootoutGoals': self._skater_shootout_goals,
            'GoalieTimeOnIce': self._goalie_time_on_ice,
            'GoalieAssists': self._goalie_assists,
            'GoalieGoals': self._goalie_goals,
            'GoaliePenaltyMins': self._goalie_pim,
            'GoalieShotsAgainst': self._goalie_shots_against,
            'GoalieSaves': self._goalie_saves,
            'GoalieGoalsAgainst': self._goalie_goals_against,
            'GoaliePowerPlaySaves': self._goalie_power_play_saves,
            'GoalieShortHandedSaves': self._goalie_short_handed_saves,
            'GoalieEvenSaves': self._goalie_even_saves,
            'GoalieShortHandedShotsAgainst': self._goalie_short_handed_shots_against,
            'GoalieEvenShotsAgainst': self._goalie_even_shots_against,
            'GoaliePowerPlayShotsAgainst': self._goalie_power_play_shots_against,
            'GoalieDecision': self._goalie_decision,
            'GoalieSavePct': self._goalie_save_pct,
            'GoaliePowerPlaySavePct': self._goalie_power_play_save_pct,
            'GoalieEvenStrengthSavePct': self._goalie_even_strength_save_pct,
            'OnlyGoalie': self._only_goalie,
        }
        return pd.DataFrame([fields_to_include], index=None)


class Boxscores:
    def __init__(self, games):
        self._boxscores = []

        self._get_boxscores_by_games(games)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    # todo- move this to util file?
    def _get_shootout_goals_by_game(self, game_id):
        shootout_goals = []
        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/playByPlay'
        #print('Getting play-by-play data for shootout stats from ' + url)
        pbp = requests.get(url, verify=VERIFY_REQUESTS).json()
        for play in pbp["allPlays"]:
            if (play["about"]["periodType"] == 'SHOOTOUT') and 'players' in play and play['result']['event'] == 'Goal':
                for player in play['players']:
                    if player['playerType'] == "Scorer":
                        shooter_id = player["player"]["id"]
                        index = -1
                        for i, obj in enumerate(shootout_goals):
                            if obj['player_id'] == shooter_id:
                                index = i
                                break
                        if index != -1:
                            # Player already has shootout goal. Incremement goals
                            shootout_goals[i]['shootout_goals'] += 1
                        else:
                            shootout_goals.append({'player_id': shooter_id, 'shootout_goals': 1})
        return shootout_goals

    def _get_boxscores_by_games(self, games):
        for game in games:
            url = f'https://statsapi.web.nhl.com/api/v1/game/{game._nhl_game_id}/boxscore'
            print('Getting boxscore data from ' + url)
            boxscores_json = requests.get(url, verify=VERIFY_REQUESTS).json()
            if game._shootout == True:
                shootout_goals = self._get_shootout_goals_by_game(game._nhl_game_id)
            else:
                shootout_goals = None
            for team in ['away', 'home']:
                goalies_recorded = 0
                for k, box_json in boxscores_json['teams'][team]['players'].items():
                    # Need to get the number of goalies recorded for fantasy point bonus eligibility
                    if 'goalieStats' in box_json['stats']:
                        goalies_recorded += 1
                for k, box_json in boxscores_json['teams'][team]['players'].items():
                    boxscore = Boxscore(game, team, box_json, shootout_goals, goalies_recorded)
                    if boxscore._nhl_player_id:  # some players don't have any stats
                        self._boxscores.append(boxscore)
            sleep(10)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)
