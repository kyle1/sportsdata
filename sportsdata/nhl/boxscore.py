import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from time import sleep


class PlayerBoxscore:
    """
    NHL player's boxscore data from a game.

    Parameters
    ----------
    game : dict
        Dict that contains the game data.

    team : string
        'away' or 'home'

    box_json : dict
        Dict that contains the player's boxscore data.

    shootout_goals : dict
        Dict that contains game shootout data.

    goalies_recorded : int
        Number of goalies on the player's team that played in the game.
    """

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

        self._get_boxscore_from_json(
            game, team, box_json, shootout_goals, goalies_recorded)

    def _get_boxscore_from_json(self, game, team, box, shootout_goals, goalies_recorded):
        has_skater_stats = 'skaterStats' in box['stats'] and len(
            box['stats']['skaterStats']) > 0
        has_goalie_stats = 'goalieStats' in box['stats'] and len(
            box['stats']['goalieStats']) > 0
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
            setattr(self, '_skater_time_on_ice',
                    box['stats']['skaterStats']['timeOnIce'])
            setattr(self, '_skater_assists',
                    box['stats']['skaterStats']['assists'])
            setattr(self, '_skater_goals',
                    box['stats']['skaterStats']['goals'])
            setattr(self, '_skater_shots',
                    box['stats']['skaterStats']['shots'])
            setattr(self, '_skater_hits', box['stats']['skaterStats']['hits'])
            setattr(self, '_skater_power_play_goals',
                    box['stats']['skaterStats']['powerPlayGoals'])
            setattr(self, '_skater_power_play_assists',
                    box['stats']['skaterStats']['powerPlayAssists'])
            if 'penaltyMinutes' in box['stats']['skaterStats']:
                setattr(self, '_skater_penalty_mins',
                        box['stats']['skaterStats']['penaltyMinutes'])
            setattr(self, '_skater_takeaways',
                    box['stats']['skaterStats']['takeaways'])
            setattr(self, '_skater_giveaways',
                    box['stats']['skaterStats']['giveaways'])
            setattr(self, '_skater_short_handed_goals',
                    box['stats']['skaterStats']['shortHandedGoals'])
            setattr(self, '_skater_short_handed_assists',
                    box['stats']['skaterStats']['shortHandedAssists'])
            setattr(self, '_skater_blocked',
                    box['stats']['skaterStats']['blocked'])
            setattr(self, '_skater_plus_minus',
                    box['stats']['skaterStats']['plusMinus'])
            setattr(self, '_skater_even_time_on_ice',
                    box['stats']['skaterStats']['evenTimeOnIce'])
            setattr(self, '_skater_power_play_time_on_ice',
                    box['stats']['skaterStats']['powerPlayTimeOnIce'])
            setattr(self, '_skater_short_handed_time_on_ice',
                    box['stats']['skaterStats']['shortHandedTimeOnIce'])
            setattr(self, '_skater_shootout_goals',
                    self._get_player_shootout_goals(game, box, shootout_goals))

        if has_goalie_stats:
            setattr(self, '_goalie_time_on_ice',
                    box['stats']['goalieStats']['timeOnIce'])
            setattr(self, '_goalie_assists',
                    box['stats']['goalieStats']['assists'])
            setattr(self, '_goalie_goals',
                    box['stats']['goalieStats']['goals'])
            setattr(self, '_goalie_pim', box['stats']['goalieStats']['pim'])
            setattr(self, '_goalie_shots_against',
                    box['stats']['goalieStats']['shots'])
            setattr(self, '_goalie_saves',
                    box['stats']['goalieStats']['saves'])
            setattr(self, '_goalie_goals_against',
                    box['stats']['goalieStats']['shots'] - box['stats']['goalieStats']['saves'])
            setattr(self, '_goalie_power_play_saves',
                    box['stats']['goalieStats']['powerPlaySaves'])
            setattr(self, '_goalie_short_handed_saves',
                    box['stats']['goalieStats']['shortHandedSaves'])
            setattr(self, '_goalie_even_saves',
                    box['stats']['goalieStats']['evenSaves'])
            setattr(self, '_goalie_short_handed_shots_against',
                    box['stats']['goalieStats']['shortHandedShotsAgainst'])
            setattr(self, '_goalie_even_shots_against',
                    box['stats']['goalieStats']['evenShotsAgainst'])
            setattr(self, '_goalie_power_play_shots_against',
                    box['stats']['goalieStats']['powerPlayShotsAgainst'])
            if 'decision' in box['stats']['goalieStats']:
                setattr(self, '_goalie_decision',
                        box['stats']['goalieStats']['decision'])
            if 'savePercentage' in box['stats']['goalieStats']:
                setattr(self, '_goalie_save_pct',
                        box['stats']['goalieStats']['savePercentage'])
            if 'powerPlaySavePercentage' in box['stats']['goalieStats']:
                setattr(self, '_goalie_power_play_save_pct',
                        box['stats']['goalieStats']['powerPlaySavePercentage'])
            if 'evenStrengthSavePercentage' in box['stats']['goalieStats']:
                setattr(self, '_goalie_even_strength_save_pct',
                        box['stats']['goalieStats']['evenStrengthSavePercentage'])
            setattr(self, '_only_goalie', goalies_recorded == 1)

    def _get_team_result(self, game, team):
        # if game._away_team_score == game._home_team_score:
        #     team_result = 'T'
        # elif (team == 'away') == (game._away_team_score > game._home_team_score):
        #     team_result = 'W'
        # else:
        #     team_result = 'L'
        if game._away_goals == game._home_goals:
            team_result = 'T'
        elif (team == 'away') == (game._away_goals > game._home_goals):
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


class PlayerBoxscores:
    def __init__(self, game, team, players_json):
        self._boxscores = []

        self._get_player_boxscores(game, team, players_json)

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
                            shootout_goals.append(
                                {'player_id': shooter_id, 'shootout_goals': 1})
        return shootout_goals

    def _get_player_boxscores(self, game, team, players_json):
        shootout_goals = {} #todo
        goalies_recorded = 0
        for player, stats in players_json['players'].items():
            # Need to get the number of goalies recorded for fantasy point bonus eligibility
            if 'goalieStats' in stats['stats']:
                goalies_recorded += 1
        for player, stats in players_json['players'].items():
            boxscore = PlayerBoxscore(game, team, stats, shootout_goals, goalies_recorded)
            if boxscore._nhl_player_id:  # some players don't have any stats
                self._boxscores.append(boxscore)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)


import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil import tz


class GameBoxscore:
    """
    Game stats for an individual NHL game.

    Parameters
    ----------
    game_id : int
        A game ID according to NHL's API.
    """
    def __init__(self, game_id):
        self._nhl_game_id = None
        self._season = None
        self._game_date_time = None
        self._game_date = None
        #self._game_status = None
        self._away_team_id = None
        self._away_pim = None #what is this?
        self._away_shots = None
        self._away_pp_pct = None
        self._away_pp_goals = None
        self._away_pp_opportunities = None
        self._away_face_off_win_pct = None
        self._away_blocked = None
        self._away_takeaways = None
        self._away_giveaways = None
        self._away_hits = None
        self._home_team_id = None
        self._home_pim = None #what is this?
        self._home_shots = None
        self._home_pp_pct = None
        self._home_pp_goals = None
        self._home_pp_opportunities = None
        self._home_face_off_win_pct = None
        self._home_blocked = None
        self._home_takeaways = None
        self._home_giveaways = None
        self._home_hits = None
        self._nhl_venue_id = None
        self._nhl_venue_name = None
        self._result_note = None
        self._overtime = None
        self._shootout = None

        self._get_game_boxscore(game_id)

    def _get_game_boxscore(self, game_id):
        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/boxscore'
        print(f'getting game boxscore data from {url}')
        game = requests.get(url, verify=VERIFY_REQUESTS).json()

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/Los_Angeles')
        # utc = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
        # utc = utc.replace(tzinfo=from_zone)
        # pst = utc.astimezone(to_zone)
        # game_dt = pst.replace(tzinfo=None)
        # has_overtime = False
        # result_note = ''
        # for period in game['linescore']['periods']:
        #     if period['num'] >= 4:
        #         has_overtime = True
        #         result_note = period['ordinalNum']  # OT, 2OT, etc.
        # has_shootout = game['linescore']['hasShootout']
        # if has_shootout:
        #     result_note = "SO"  # Override "OT" note
        setattr(self, '_nhl_game_id', game_id)
        #setattr(self, '_season', int(game['season'][:4])),
        #setattr(self, '_game_date_time', game_dt.isoformat())
        #setattr(self, '_game_date', game_dt.date().isoformat())
        #setattr(self, '_game_time', game_dt.time().isoformat())
        #setattr(self, '_game_status', game['status']['detailedState'])
        setattr(self, '_away_team_id', game['teams']['away']['team']['id'])
        setattr(self, '_away_goals', game['teams']['away']['teamStats']['teamSkaterStats']['goals'])
        setattr(self, '_away_pim', game['teams']['away']['teamStats']['teamSkaterStats']['pim'])
        setattr(self, '_away_shots', game['teams']['away']['teamStats']['teamSkaterStats']['shots'])
        setattr(self, '_away_pp_pct', game['teams']['away']['teamStats']['teamSkaterStats']['powerPlayPercentage'])
        setattr(self, '_away_pp_goals', game['teams']['away']['teamStats']['teamSkaterStats']['powerPlayGoals'])
        setattr(self, '_away_pp_opportunities', game['teams']['away']['teamStats']['teamSkaterStats']['powerPlayOpportunities'])
        setattr(self, '_away_face_off_win_pct', game['teams']['away']['teamStats']['teamSkaterStats']['faceOffWinPercentage'])
        setattr(self, '_away_blocked', game['teams']['away']['teamStats']['teamSkaterStats']['blocked'])
        setattr(self, '_away_takeaways', game['teams']['away']['teamStats']['teamSkaterStats']['takeaways'])
        setattr(self, '_away_giveaways', game['teams']['away']['teamStats']['teamSkaterStats']['giveaways'])
        setattr(self, '_away_hits', game['teams']['away']['teamStats']['teamSkaterStats']['hits'])
        setattr(self, '_home_team_id', game['teams']['home']['team']['id'])
        setattr(self, '_home_goals', game['teams']['home']['teamStats']['teamSkaterStats']['goals'])
        setattr(self, '_home_pim', game['teams']['home']['teamStats']['teamSkaterStats']['pim'])
        setattr(self, '_home_shots', game['teams']['home']['teamStats']['teamSkaterStats']['shots'])
        setattr(self, '_home_pp_pct', game['teams']['home']['teamStats']['teamSkaterStats']['powerPlayPercentage'])
        setattr(self, '_home_pp_goals', game['teams']['home']['teamStats']['teamSkaterStats']['powerPlayGoals'])
        setattr(self, '_home_pp_opportunities', game['teams']['home']['teamStats']['teamSkaterStats']['powerPlayOpportunities'])
        setattr(self, '_home_face_off_win_pct', game['teams']['home']['teamStats']['teamSkaterStats']['faceOffWinPercentage'])
        setattr(self, '_home_blocked', game['teams']['home']['teamStats']['teamSkaterStats']['blocked'])
        setattr(self, '_home_takeaways', game['teams']['home']['teamStats']['teamSkaterStats']['takeaways'])
        setattr(self, '_home_giveaways', game['teams']['home']['teamStats']['teamSkaterStats']['giveaways'])
        setattr(self, '_home_hits', game['teams']['home']['teamStats']['teamSkaterStats']['hits'])
        #setattr(self, '_nhl_venue_id', None if 'id' not in game['venue'] else game['venue']['id'])
        #setattr(self, '_nhl_venue_name', game['venue']['name'])
        #setattr(self, '_result_note', result_note)
        #setattr(self, '_overtime', has_overtime)
        #setattr(self, '_shootout', has_shootout)

        setattr(self, '_away_players', PlayerBoxscores(self, 'away', game['teams']['away']))
        setattr(self, '_home_players', PlayerBoxscores(self, 'home', game['teams']['home']))
        #setattr(self, '_play_by_play', PlayByPlay(game_id))

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlGameId': self._nhl_game_id,
            #'Season': self._season,
            #'GameDateTime': self._game_date_time,
            #'GameDate': self._game_date,
            #'GameTime': self._game_time,
            #'GameStatus': self._game_status,
            'AwayTeamId': self._away_team_id,
            'AwayGoals': self._away_goals,
            'AwayPim': self._away_pim,
            'AwayShots': self._away_shots,
            'AwayPpPct': self._away_pp_pct,
            'AwayPpGoals': self._away_pp_goals,
            'AwayPpOpportunities': self._away_pp_opportunities,
            'AwayFaceOffWinPct': self._away_face_off_win_pct,
            'AwayBlocked': self._away_blocked,
            'AwayTakeaways': self._away_takeaways,
            'AwayGiveaways': self._away_giveaways,
            'AwayHits': self._away_hits,
            'HomeTeamId': self._home_team_id,
            'HomeGoals': self._home_goals,
            'HomePim': self._home_pim,
            'HomeShots': self._home_shots,
            'HomePpPct': self._home_pp_pct,
            'HomePpGoals': self._home_pp_goals,
            'HomePpOpportunities': self._home_pp_opportunities,
            'HomeFaceOffWinPct': self._home_face_off_win_pct,
            'HomeBlocked': self._home_blocked,
            'HomeTakeaways': self._home_takeaways,
            'HomeGiveaways': self._home_giveaways,
            'HomeHits': self._home_hits#,
            # 'NhlVenueId': self._nhl_venue_id,
            # 'NhlVenueName': self._nhl_venue_name,
            # 'ResultNote': self._result_note,
            # 'Overtime': self._overtime,
            # 'Shootout': self._shootout
        }
        return pd.DataFrame([fields_to_include], index=[self._nhl_game_id])


class GameBoxscores:
    def __init__(self, start_date, end_date):
        self._boxscores = []

        self._get_game_boxscores(start_date, end_date)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _get_game_boxscores(self, start_date, end_date):
        url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&expand=schedule.linescore'
        #print('Getting games from ' + url)
        games = requests.get(url, verify=VERIFY_REQUESTS).json()
        for date in games['dates']:
            for game_data in date['games']:
                boxscore = GameBoxscore(game_data['gamePk'])
                self._boxscores.append(boxscore)
                sleep(5)

    @property
    def dataframes(self):
        frames = []
        for boxscore in self.__iter__():
            frames.append(boxscore.dataframe)
        return pd.concat(frames)
