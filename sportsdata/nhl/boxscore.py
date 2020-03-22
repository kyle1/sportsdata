import pandas as pd
import requests
from ..constants import VERIFY_REQUESTS
from ..util import utc_to_pst
from .playbyplay import PlayByPlay
from datetime import datetime
from time import sleep


class PlayerBoxscore:
    """
    Player's boxscore data from an individual NHL game.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

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
            skater_stats = box['stats']['skaterStats']
            setattr(self, '_skater_time_on_ice', skater_stats['timeOnIce'])
            setattr(self, '_skater_assists', skater_stats['assists'])
            setattr(self, '_skater_goals', skater_stats['goals'])
            setattr(self, '_skater_shots', skater_stats['shots'])
            setattr(self, '_skater_hits', skater_stats['hits'])
            setattr(self, '_skater_power_play_goals', skater_stats['powerPlayGoals'])
            setattr(self, '_skater_power_play_assists', skater_stats['powerPlayAssists'])
            if 'penaltyMinutes' in skater_stats:
                setattr(self, '_skater_penalty_mins', skater_stats['penaltyMinutes'])
            setattr(self, '_skater_takeaways', skater_stats['takeaways'])
            setattr(self, '_skater_giveaways', skater_stats['giveaways'])
            setattr(self, '_skater_short_handed_goals', skater_stats['shortHandedGoals'])
            setattr(self, '_skater_short_handed_assists', skater_stats['shortHandedAssists'])
            setattr(self, '_skater_blocked', skater_stats['blocked'])
            setattr(self, '_skater_plus_minus', skater_stats['plusMinus'])
            setattr(self, '_skater_even_time_on_ice', skater_stats['evenTimeOnIce'])
            setattr(self, '_skater_power_play_time_on_ice', skater_stats['powerPlayTimeOnIce'])
            setattr(self, '_skater_short_handed_time_on_ice', skater_stats['shortHandedTimeOnIce'])
            setattr(self, '_skater_shootout_goals', self._get_player_shootout_goals(game, box, shootout_goals))

        if has_goalie_stats:
            goalie_stats = box['stats']['goalieStats']
            setattr(self, '_goalie_time_on_ice', goalie_stats['timeOnIce'])
            setattr(self, '_goalie_assists', goalie_stats['assists'])
            setattr(self, '_goalie_goals', goalie_stats['goals'])
            setattr(self, '_goalie_pim', goalie_stats['pim'])
            setattr(self, '_goalie_shots_against', goalie_stats['shots'])
            setattr(self, '_goalie_saves', goalie_stats['saves'])
            setattr(self, '_goalie_goals_against', goalie_stats['shots'] - goalie_stats['saves'])
            setattr(self, '_goalie_power_play_saves', goalie_stats['powerPlaySaves'])
            setattr(self, '_goalie_short_handed_saves', goalie_stats['shortHandedSaves'])
            setattr(self, '_goalie_even_saves', goalie_stats['evenSaves'])
            setattr(self, '_goalie_short_handed_shots_against', goalie_stats['shortHandedShotsAgainst'])
            setattr(self, '_goalie_even_shots_against', goalie_stats['evenShotsAgainst'])
            setattr(self, '_goalie_power_play_shots_against', goalie_stats['powerPlayShotsAgainst'])
            if 'decision' in goalie_stats:
                setattr(self, '_goalie_decision', goalie_stats['decision'])
            if 'savePercentage' in goalie_stats:
                setattr(self, '_goalie_save_pct', goalie_stats['savePercentage'])
            if 'powerPlaySavePercentage' in goalie_stats:
                setattr(self, '_goalie_power_play_save_pct', goalie_stats['powerPlaySavePercentage'])
            if 'evenStrengthSavePercentage' in goalie_stats:
                setattr(self, '_goalie_even_strength_save_pct', goalie_stats['evenStrengthSavePercentage'])
            setattr(self, '_only_goalie', goalies_recorded == 1)

    def _get_team_result(self, game, team):
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

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class PlayerBoxscores:
    """
    All players' boxscore data from an individual NHL game.

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

    # todo- move this to util file?
    def _get_shootout_goals_by_game(self, game_id):
        shootout_goals = []
        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/playByPlay'
        print('Getting play-by-play data for shootout stats from ' + url)
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

    def _get_player_boxscores(self, game, team, players):
        shootout_goals = {}  # todo
        goalies_recorded = 0
        for player, stats in players.items():
            # Need to get the number of goalies recorded for fantasy point bonus eligibility
            if 'goalieStats' in stats['stats']:
                goalies_recorded += 1
        for player, stats in players.items():
            boxscore = PlayerBoxscore(game, team, stats, shootout_goals, goalies_recorded)
            if boxscore._nhl_player_id:  # some players don't have any stats
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


class GameBoxscore:
    """
    Game stats from an individual NHL game.

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
        self._game_status = None
        self._away_team_id = None
        self._away_pim = None
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
        self._home_pim = None
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
        setattr(self, '_nhl_game_id', game_id)

        url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live'
        print(f'Getting game data from {url}')
        game = requests.get(url, verify=VERIFY_REQUESTS).json()
        utc = datetime.strptime(game['gameData']['datetime']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
        game_dt = utc_to_pst(utc)
        setattr(self, '_season', int(game['gameData']['game']['season'][:4])),
        setattr(self, '_game_date_time', game_dt.isoformat())
        setattr(self, '_game_date', game_dt.date().isoformat())
        setattr(self, '_game_time', game_dt.time().isoformat())
        setattr(self, '_game_status', game['gameData']['status']['detailedState'])

        has_overtime = False
        result_note = ''
        for period in game['liveData']['linescore']['periods']:
            if period['num'] >= 4:
                has_overtime = True
                result_note = period['ordinalNum']  # OT, 2OT, etc.
        has_shootout = game['liveData']['linescore']['hasShootout']
        if has_shootout:
            result_note = "SO"  # Override "OT" note

        # url = f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/boxscore'
        # print(f'Getting game boxscore data from {url}')
        # box = requests.get(url, verify=VERIFY_REQUESTS).json()
        box = game['liveData']['boxscore']
        away_team = box['teams']['away']  # todo
        away_team_stats = box['teams']['away']['teamStats']['teamSkaterStats']
        home_team = box['teams']['away']  # todo
        home_team_stats = box['teams']['home']['teamStats']['teamSkaterStats']
        setattr(self, '_away_team_id', game['gameData']['teams']['away']['id'])
        setattr(self, '_away_goals', away_team_stats['goals'])
        setattr(self, '_away_pim', away_team_stats['pim'])
        setattr(self, '_away_shots', away_team_stats['shots'])
        setattr(self, '_away_pp_pct', away_team_stats['powerPlayPercentage'])
        setattr(self, '_away_pp_goals', away_team_stats['powerPlayGoals'])
        setattr(self, '_away_pp_opportunities', away_team_stats['powerPlayOpportunities'])
        setattr(self, '_away_face_off_win_pct', away_team_stats['faceOffWinPercentage'])
        setattr(self, '_away_blocked', away_team_stats['blocked'])
        setattr(self, '_away_takeaways', away_team_stats['takeaways'])
        setattr(self, '_away_giveaways', away_team_stats['giveaways'])
        setattr(self, '_away_hits', away_team_stats['hits'])
        setattr(self, '_home_team_id', game['gameData']['teams']['home']['id'])
        setattr(self, '_home_goals', home_team_stats['goals'])
        setattr(self, '_home_pim', home_team_stats['pim'])
        setattr(self, '_home_shots', home_team_stats['shots'])
        setattr(self, '_home_pp_pct', home_team_stats['powerPlayPercentage'])
        setattr(self, '_home_pp_goals', home_team_stats['powerPlayGoals'])
        setattr(self, '_home_pp_opportunities', home_team_stats['powerPlayOpportunities'])
        setattr(self, '_home_face_off_win_pct', home_team_stats['faceOffWinPercentage'])
        setattr(self, '_home_blocked', home_team_stats['blocked'])
        setattr(self, '_home_takeaways', home_team_stats['takeaways'])
        setattr(self, '_home_giveaways', home_team_stats['giveaways'])
        setattr(self, '_home_hits', home_team_stats['hits'])
        setattr(self, '_nhl_venue_id', None if 'id' not in game['gameData']
                ['venue'] else game['gameData']['venue']['id'])
        setattr(self, '_nhl_venue_name', game['gameData']['venue']['name'])
        setattr(self, '_result_note', result_note)
        setattr(self, '_overtime', has_overtime)
        setattr(self, '_shootout', has_shootout)

        plays = game['liveData']['plays']['allPlays']
        print(plays)

        setattr(self, '_away_players', PlayerBoxscores(self, 'away', box['teams']['away']['players']))
        setattr(self, '_home_players', PlayerBoxscores(self, 'home', box['teams']['home']['players']))
        setattr(self, '_play_by_play', PlayByPlay(game_id, plays))

    @property
    def dataframe(self):
        fields_to_include = {
            'NhlGameId': self._nhl_game_id,
            'Season': self._season,
            'GameDateTime': self._game_date_time,
            'GameDate': self._game_date,
            'GameTime': self._game_time,
            'GameStatus': self._game_status,
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
            'HomeHits': self._home_hits,
            'NhlVenueId': self._nhl_venue_id,
            'NhlVenueName': self._nhl_venue_name,
            'ResultNote': self._result_note,
            'Overtime': self._overtime,
            'Shootout': self._shootout
        }
        return pd.DataFrame([fields_to_include], index=[self._nhl_game_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['AwayPlayers'] = self._away_players.to_dicts
        dic['HomePlayers'] = self._home_players.to_dicts
        return dic


class GameBoxscores:
    # todo- setup kwargs like MLB GameBoxscores ?
    """
    Game stats from multiple NHL games.

    Parameters
    ----------
    start_date : string
        Beginning date to get game boxscores from ('MM/DD/YYYY' format)

    end_date : string
        End date to get game boxscores from ('MM/DD/YYYY' format)
    """

    def __init__(self, start_date, end_date):
        self._boxscores = []

        self._get_game_boxscores(start_date, end_date)

    def __repr__(self):
        return self._boxscores

    def __iter__(self):
        return iter(self.__repr__())

    def _get_game_boxscores(self, start_date, end_date):
        url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&expand=schedule.linescore'
        print('Getting NHL schedule from ' + url)
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

    @property
    def to_dicts(self):
        dics = []
        for boxscore in self.__iter__():
            dics.append(boxscore.to_dict)
        return dics
