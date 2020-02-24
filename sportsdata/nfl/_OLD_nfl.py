import argparse
import json
import requests
from datetime import datetime, timedelta
#from dateutil import tz
from random import randint
from time import sleep


def validate_dates(date_strings):
    try:
        begin = datetime.strptime(date_strings[0], '%m/%d/%Y')
        end = datetime.strptime(date_strings[1], '%m/%d/%Y')
        if begin <= end:
            return True
        else:
            print('Begin date argument must be before end date argument')
            return False
    except ValueError:
        print('Argument has invalid date format. Use MM/DD/YYYY.')
        return False


def validate_args(args):
    if args.seasons:
        seasons = validate_seasons(args.seasons)
    else:
        # No seasons argument passed in - this arg is required.
        return False, None, None

    if args.weeks:
        if args.weeks[0] == 'prev':
            prev_week = get_previous_nfl_week()
            if prev_week is not None:
                return True, seasons, [prev_week]
            return False, None, None
        else:
            nfl_weeks = validate_weeks(args.weeks)
            return True, seasons, nfl_weeks
        print('Invalid weeks')
        return False, None, None
    else:
        # No weeks argument passed in - get whole season(s)
        return True, args.seasons, None

    print('Invalid arguments. For more details use "python t.py -h":')
    return False, None, None


def validate_seasons(seasons):
    valid_seasons = []
    for season in seasons:
        if str(season).isdigit():
            valid_seasons.append(int(season))
        else:
            return None
    return valid_seasons


def get_previous_nfl_week():
    today = datetime.today().date()
    for i in range(len(current_season_weeks) - 1, 0, -1):
        if today >= datetime.strptime(current_season_weeks[i]['end_date'], '%m/%d/%Y').date():
            print('Previous week is ' + str(current_season_weeks[i]['week']))
            return current_season_weeks[i]['week']
    print('Could not determine previous NFL week')
    return None


def validate_weeks(weeks):
    valid_weeks = []
    for week in weeks:
        if week.isdigit():
            valid_weeks.append(week)
        else:
            return None
    return valid_weeks


def get_season_by_date_range(date_strings):
    begin = datetime.strptime(date_strings[0], '%m/%d/%Y')
    end = datetime.strptime(date_strings[1], '%m/%d/%Y')
    for season in seasons:
        if begin >= datetime.strptime(season['start_date'], '%m/%d/%Y') and end <= datetime.strptime(season['end_date'], '%m/%d/%Y'):
            return season['season']
    print('Unable to find season for the specified date range')
    return None


def get_season_by_date(date_string):
    date = datetime.strptime(date_string, '%m/%d/%Y')
    for season in seasons:
        if date >= datetime.strptime(season['start_date'], '%m/%d/%Y') and date <= datetime.strptime(season['end_date'], '%m/%d/%Y'):
            return season['season']
    print('Unable to find season for the specified date range')
    return None


def get_nfl_week(date):
    for week in nfl_weeks:
        begin = datetime.strptime(week['start_date'], '%m/%d/%Y')
        end = datetime.strptime(week['end_date'], '%m/%d/%Y')
        if date >= begin and date <= end:
            return week['week']
    print('Could not determine NFL week from date')
    raise


# Games
def get_games(seasons, weeks):
    game_ids = []
    game_objs = []
    for season in seasons:
        for week in weeks:
            url = "https://feeds.nfl.com/feeds-rs/scores/" + \
                str(season) + "/" + \
                'REG' + "/" + str(week) + ".json"
            print("Getting game data from " + url)
            games = requests.get(url, verify=False).json()

            for game in games["gameScores"]:
                # if game['gameSchedule']['season'] > end_season:
                #     continue # skip seasons that are higher than our end range
                # if game['gameSchedule']['season'] < begin_season:
                #     #seasons are listed in descending order. if looped season is less than
                #     #season to fetch, we've already got all of the season we wanted to get.
                #     return
                game_ids.append(game['gameSchedule']['gameId'])

            sleep(randint(5, 10))

            for game_id in game_ids:

                boxscore = requests.get(
                    "https://feeds.nfl.com/feeds-rs/boxscore/" + str(game_id) + ".json", verify=False).json()

                game_obj = {
                    'NflGameId': boxscore['gameSchedule']['gameId'],
                    'Season': boxscore['gameSchedule']['season'],
                    'SeasonType': boxscore['gameSchedule']['seasonType'],
                    'Week': boxscore['gameSchedule']['week'],
                    'GameDateTime': boxscore['gameSchedule']['gameDate'] + ' ' + boxscore['gameSchedule']['gameTimeEastern'],
                    'GameDate': boxscore['gameSchedule']['gameDate'],
                    'GameTimeEastern': boxscore['gameSchedule']['gameTimeEastern'],
                    'HomeTeamId': boxscore['gameSchedule']['homeTeamId'],
                    'HomeTeamScore': boxscore['score']['homeTeamScore']['pointTotal'],
                    'HomeTeamScoreQ2': boxscore['score']['homeTeamScore']['pointQ2'],
                    'HomeTeamScoreQ3': boxscore['score']['homeTeamScore']['pointQ3'],
                    'HomeTeamScoreQ4': boxscore['score']['homeTeamScore']['pointQ4'],
                    'HomeTeamScoreOT': boxscore['score']['homeTeamScore']['pointOT'],
                    'HomeTeamTimeOfPossession': boxscore['homeTeamStats']['avgTimeOfPossession'],
                    'AwayTeamId': boxscore['gameSchedule']['visitorTeamId'],
                    'AwayTeamScore': boxscore['score']['visitorTeamScore']['pointTotal'],
                    'AwayTeamScoreQ1': boxscore['score']['visitorTeamScore']['pointQ1'],
                    'AwayTeamScoreQ2': boxscore['score']['visitorTeamScore']['pointQ2'],
                    'AwayTeamScoreQ3': boxscore['score']['visitorTeamScore']['pointQ3'],
                    'AwayTeamScoreQ4': boxscore['score']['visitorTeamScore']['pointQ4'],
                    'AwayTeamScoreOT': boxscore['score']['visitorTeamScore']['pointOT'],
                    'AwayTeamTimeOfPossession': boxscore['visitorTeamStats']['avgTimeOfPossession'],
                    'NflSiteId': boxscore['gameSchedule']['site']['siteId']
                }

                game_objs.append(game_obj)

                sleep(randint(20, 30))

    for game in game_objs:
        print(game)
        print('\n')


# Boxscores
def get_boxscores(seasons, weeks):
    for season in seasons:
        url = "https://feeds.nfl.com/feeds-rs/schedules/" + \
            str(season) + ".json"
        print("Getting list of game IDs from " + url)
        games = requests.get(url).json()
        game_ids = []
        for game in games['gameSchedules']:
            game_ids.append(game['gameId'])

        print("Getting NFL boxscore passing data for " +
              str(len(game_ids)) + " games...")

        for game_id in game_ids:
            boxscore = requests.get(
                "https://feeds.nfl.com/feeds-rs/boxscore/" + str(game_id) + ".json").json()

            home_team_id = boxscore['gameSchedule']['homeTeamId']
            away_team_id = boxscore['gameSchedule']['visitorTeamId']

            game_obj = {
                'NflGameId': game_id,
                'AwayTeamId': away_team_id,
                'HomeTeamId': home_team_id,
            }

            away_team_points = boxscore['score']['visitorTeamScore']['pointTotal']
            home_team_points = boxscore['score']['homeTeamScore']['pointTotal']
            
            if away_team_points > home_team_points:
                away_result = 'W'
                home_result = 'L'
            elif home_team_points > away_team_points:
                away_result = 'L'
                home_result = 'W'
            else:
                away_result = 'T'
                home_result = 'T'

            if boxscore['score']['visitorTeamScore']['pointOT'] > 0 or boxscore['score']['homeTeamScore']['pointOT'] > 0:
                result_note = 'OT'
            else:
                result_note = None
            #todo- if neither team scores in overtime, it won't be known that there was overtime with the current method

            distinct_player_ids = []

            teams = ['homeTeamBoxScoreStat', 'visitorTeamBoxScoreStat']
            passing_stats = []
            for team in teams:
                for player in boxscore[team]['playerBoxScorePassingStats']:
                    player_id = player['teamPlayer']['nflId']
                    if player_id not in distinct_player_ids:
                        distinct_player_ids.append(player_id)
                    player_passing = {
                        'NflPlayerId': player_id,
                        'IsAway': False if team == 'homeTeamBoxScoreStat' else True,
                        'TeamResult': home_result if team == 'homeTeamBoxScoreStat' else away_result,
                        'ResultNote': result_note,
                        'PassingAttempts': player['playerGameStat']['playerPassingStat']['passingAttempts'],
                        'PassingCompletions': player['playerGameStat']['playerPassingStat']['passingCompletions'],
                        'PassingYards': player['playerGameStat']['playerPassingStat']['passingYards'],
                        'PassingTouchdowns': player['playerGameStat']['playerPassingStat']['passingTouchdowns'],
                        'PassingInterceptions': player['playerGameStat']['playerPassingStat']['passingTouchdowns'],
                        'PassingLong': player['playerGameStat']['playerPassingStat']['passingLong'],
                        'PassingRating': player['playerGameStat']['playerPassingStat']['passingRating']
                    }
                    passing_stats.append(player_passing)

            rushing_stats = []
            for team in teams:
                for player in boxscore[team]['playerBoxScoreRushingStats']:
                    player_id = player['teamPlayer']['nflId']
                    if player_id not in distinct_player_ids:
                        distinct_player_ids.append(player_id)
                    player_rushing = {
                        'NflPlayerId': player_id,
                        'IsAway': False if team == 'homeTeamBoxScoreStat' else True,
                        'TeamResult': home_result if team == 'homeTeamBoxScoreStat' else away_result,
                        'ResultNote': result_note,
                        'RushingAttempts': player['playerGameStat']['playerRushingStat']['rushingAttempts'],
                        'RushingYards': player['playerGameStat']['playerRushingStat']['rushingYards'],
                        'RushingTouchdowns': player['playerGameStat']['playerRushingStat']['rushingTouchdowns'],
                        'RushingLong': player['playerGameStat']['playerRushingStat']['rushingLong']
                    }
                    rushing_stats.append(player_rushing)

            receiving_stats = []
            for team in teams:
                for player in boxscore[team]['playerBoxScoreReceivingStats']:
                    player_id = player['teamPlayer']['nflId']
                    if player_id not in distinct_player_ids:
                        distinct_player_ids.append(player_id)
                    player_receiving = {
                        'NflPlayerId': player_id,
                        'IsAway': False if team == 'homeTeamBoxScoreStat' else True,
                        'TeamResult': home_result if team == 'homeTeamBoxScoreStat' else away_result,
                        'ResultNote': result_note,
                        'ReceivingReceptions': player['playerGameStat']['playerReceivingStat']['receivingReceptions'],
                        'ReceivingYards': player['playerGameStat']['playerReceivingStat']['receivingYards'],
                        'ReceivingTouchdowns': player['playerGameStat']['playerReceivingStat']['receivingTouchdowns'],
                        'ReceivingLong': player['playerGameStat']['playerReceivingStat']['receivingLong']
                    }
                    receiving_stats.append(player_receiving)

            fumble_stats = []
            for team in teams:
                for player in boxscore[team]['playerBoxScoreFumbleStats']:
                    player_id = player['teamPlayer']['nflId']
                    if player_id not in distinct_player_ids:
                        distinct_player_ids.append(player_id)
                    player_fumbles = {
                        'NflPlayerId': player_id,
                        'IsAway': False if team == 'homeTeamBoxScoreStat' else True,
                        'TeamResult': home_result if team == 'homeTeamBoxScoreStat' else away_result,
                        'ResultNote': result_note,
                        'Fumbles': player['playerGameStat']['playerFumbleStat']['fumbles'],
                        'FumblesLost': player['playerGameStat']['playerFumbleStat']['fumblesLost'],
                        'FumbleReturnTouchdowns': player['playerGameStat']['playerFumbleStat']['touchdownsFumbleReturns'],
                        'OffensiveFumbleRecoveryTd': player['playerGameStat']['playerFumbleStat']['teammateFumbleTd']
                    }
                    fumble_stats.append(player_fumbles)

            # todo: look at team stats. ex- kickingFgAttMade1tTo19
            # kicking_stats = []
            # for team in teams:
            #     for player in boxscore[team]['playerBoxScoreKickingStats']:
            #         player_id = player['teamPlayer']['nflId']
            #         if player_id not in distinct_player_ids:
            #             distinct_player_ids.append(player_id)
            #         player_kicking = {
            #             'NflPlayerId': player_id,
            #             'IsAway': False,
            #         }
            #         kicking_stats.append(player_kicking)

            kick_return_stats = []
            punt_return_stats = []
            for team in teams:
                for player in boxscore[team]['playerBoxScoreReturnStats']:
                    player_id = player['teamPlayer']['nflId']
                    if player_id not in distinct_player_ids:
                        distinct_player_ids.append(player_id)
                    # todo
                    if 'playerKickReturnsStat' in player['playerGameStat']:
                        player_kick_return = {
                            'NflPlayerId': player_id,
                            'IsAway': False if team == 'homeTeamBoxScoreStat' else True,
                            'TeamResult': home_result if team == 'homeTeamBoxScoreStat' else away_result,
                            'ResultNote': result_note,
                            'KickReturnTouchdowns': player['playerGameStat']['playerKickReturnsStat']['kickReturnsTouchdowns']
                        }
                        kick_return_stats.append(player_kick_return)
                    elif 'playerPuntReturnsStat' in player['playerGameStat']:
                        player_punt_return = {
                            'NflPlayerId': player_id,
                            'IsAway': False if team == 'homeTeamBoxScoreStat' else True,
                            'TeamResult': home_result if team == 'homeTeamBoxScoreStat' else away_result,
                            'ResultNote': result_note,
                            'PuntReturnTouchdowns': player['playerGameStat']['playerPuntReturnsStat']['puntReturnsTouchdowns']
                        }
                        punt_return_stats.append(player_punt_return)



            dst_stats = []

            distinct_player_ids.append(home_team_id)
            home_dst_stats = {
                'NflPlayerId': home_team_id,
                'IsAway': False,
                'TeamResult': home_result,
                'ResultNote': result_note,
                'IsDefense': True,
                'DstPuntReturnTouchdowns': boxscore['homeTeamStats']['touchdownsPuntReturns'],
                'DstKickReturnTouchdowns': boxscore['homeTeamStats']['touchdownsKickoffReturns'],
                'DstFumbleReturnTouchdowns': boxscore['homeTeamStats']['touchdownsFumbleReturns'],
                'DefensiveSacks': boxscore['homeTeamStats']['defensiveSacks'],
                'DefensiveForcedFumbles': boxscore['homeTeamStats']['defensiveForcedFumble'],
                'DefensiveInterceptions': boxscore['homeTeamStats']['defensiveInterceptions'],
                'DefensiveInterceptionTds': boxscore['homeTeamStats']['defensiveInterceptionsTds'],
                'DefensiveSafeties': boxscore['homeTeamStats']['defensiveSafeties']
            }
            
            
            distinct_player_ids.append(away_team_id)
            away_dst_stats = {
                'NflPlayerId': away_team_id,
                'IsAway': True,
                'TeamResult': away_result,
                'ResultNote': result_note,
                'IsDefense': True,
                'DstPuntReturnTouchdowns': boxscore['visitorTeamStats']['touchdownsPuntReturns'],
                'DstKickReturnTouchdowns': boxscore['visitorTeamStats']['touchdownsKickoffReturns'],
                'DstFumbleReturnTouchdowns': boxscore['visitorTeamStats']['touchdownsFumbleReturns'],
                'DefensiveSacks': boxscore['visitorTeamStats']['defensiveSacks'],
                'DefensiveForcedFumbles': boxscore['visitorTeamStats']['defensiveForcedFumble'],
                'DefensiveInterceptions': boxscore['visitorTeamStats']['defensiveInterceptions'],
                'DefensiveInterceptionTds': boxscore['visitorTeamStats']['defensiveInterceptionsTds'],
                'DefensiveSafeties': boxscore['visitorTeamStats']['defensiveSafeties']
            }

            home_dst_points = (home_dst_stats['DstPuntReturnTouchdowns'] + home_dst_stats['DstKickReturnTouchdowns'] + home_dst_stats['DstFumbleReturnTouchdowns'] + home_dst_stats['DefensiveInterceptionTds']) * 6 + home_dst_stats['DefensiveSafeties'] * 2
            away_dst_points = (away_dst_stats['DstPuntReturnTouchdowns'] + away_dst_stats['DstKickReturnTouchdowns'] + away_dst_stats['DstFumbleReturnTouchdowns'] + away_dst_stats['DefensiveInterceptionTds']) * 6 + away_dst_stats['DefensiveSafeties'] * 2
            home_dst_stats['DstPointsAllowed'] = away_team_points - away_dst_points
            away_dst_stats['DstPointsAllowed'] = home_team_points - home_dst_points

            dst_stats.append(home_dst_stats)
            dst_stats.append(away_dst_stats)

            stats_lists = [passing_stats, rushing_stats, receiving_stats, fumble_stats,
                           kick_return_stats, punt_return_stats, dst_stats]

            boxscores = []
            for player_id in distinct_player_ids:
                boxscore = dict()
                boxscore.update(game_obj)
                for stats_list in stats_lists:
                    for stats in stats_list:
                        if stats['NflPlayerId'] == player_id:
                            boxscore.update(stats)
                            continue
                boxscores.append(boxscore)

            for boxscore in boxscores:
                print(boxscore)
                print('\n')
            response = requests.post(base_url + 'boxscores',
                                     json=boxscores, verify=False).json()
            print(response)
            sleep(randint(20, 30))


# todo
nfl_seasons = [
    {'season': 2005, 'start_date': '04/03/2005', 'end_date': '10/26/2005'},
    {'season': 2006, 'start_date': '04/02/2006', 'end_date': '10/27/2006'},
    {'season': 2007, 'start_date': '04/01/2007', 'end_date': '10/28/2007'},
    {'season': 2008, 'start_date': '03/25/2008', 'end_date': '10/29/2008'},
    {'season': 2009, 'start_date': '04/05/2009', 'end_date': '11/04/2009'},
    {'season': 2010, 'start_date': '04/04/2010', 'end_date': '11/01/2010'},
    {'season': 2011, 'start_date': '03/31/2011', 'end_date': '10/28/2011'},
    {'season': 2012, 'start_date': '03/28/2012', 'end_date': '10/28/2012'},
    {'season': 2013, 'start_date': '03/31/2013', 'end_date': '10/30/2013'},
    {'season': 2014, 'start_date': '03/22/2014', 'end_date': '10/29/2014'},
    {'season': 2015, 'start_date': '04/05/2015', 'end_date': '11/01/2015'},
    {'season': 2016, 'start_date': '04/03/2016', 'end_date': '11/02/2016'},
    {'season': 2017, 'start_date': '04/02/2017', 'end_date': '11/01/2017'},
    {'season': 2018, 'start_date': '03/29/2018', 'end_date': '10/28/2018'},
    # {'season': 2019, 'start_date': '03/28/2019', 'end_date': datetime.today().strftime('%m/%d/%Y')}]
    {'season': 2019, 'start_date': '03/28/2019', 'end_date': '11/01/2019'}]

current_season_weeks = [
    {'week': 1, 'start_date': '09/05/2019', 'end_date': '09/09/2019'},
    {'week': 2, 'start_date': '09/12/2019', 'end_date': '09/16/2019'},
    {'week': 3, 'start_date': '09/19/2019', 'end_date': '09/23/2019'},
    {'week': 4, 'start_date': '09/26/2019', 'end_date': '09/30/2019'},
    {'week': 5, 'start_date': '10/03/2019', 'end_date': '10/07/2019'},
    {'week': 6, 'start_date': '10/10/2019', 'end_date': '10/14/2019'},
    {'week': 7, 'start_date': '10/17/2019', 'end_date': '10/21/2019'},
    {'week': 8, 'start_date': '10/24/2019', 'end_date': '10/28/2019'},
    {'week': 9, 'start_date': '10/31/2019', 'end_date': '11/04/2019'},
    {'week': 10, 'start_date': '11/07/2019', 'end_date': '11/11/2019'},
    {'week': 11, 'start_date': '11/14/2019', 'end_date': '11/18/2019'},
    {'week': 12, 'start_date': '11/21/2019', 'end_date': '11/25/2019'},
    {'week': 13, 'start_date': '11/28/2019', 'end_date': '12/02/2019'},
    {'week': 14, 'start_date': '12/05/2019', 'end_date': '12/09/2019'},
    {'week': 15, 'start_date': '12/12/2019', 'end_date': '12/16/2019'},
    {'week': 16, 'start_date': '12/19/2019', 'end_date': '12/23/2019'},
    {'week': 17, 'start_date': '12/29/2019', 'end_date': '12/29/2019'}
]

nfl_weeks = [
    {'game_type': 'PRE', 'weeks': [0, 1, 2, 3, 4]},
    {'game_type': 'REG', 'weeks': [1, 2, 3, 4, 5, 6,
                                   7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]},
    {'game_type': 'POST', 'weeks': [18, 19, 20, 22]},
    {'game_type': 'PRO', 'weeks': [21]}
]

parser = argparse.ArgumentParser(description='How to use:')
#group = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('-seasons', nargs='+', help='Seasons to fetch records for')
# group.add_argument('-yesterday', action='store_true',
#                    help='Grab records from yesterday')
parser.add_argument('-weeks', nargs='+',
                    help='Weeks to fetch records for (use "prev" for previous week)')
parser.add_argument('-games', action='store_true', help='Grab game records')
parser.add_argument('-boxscores', action='store_true',
                    help='Grab boxscore records')
args = parser.parse_args()
valid_args, seasons, weeks = validate_args(args)
if not valid_args:
    print('invalid args')
    exit

print(seasons)
print(weeks)

base_url = 'https://localhost:44374/api/nfl/'
# from_zone = tz.gettz('UTC')
# to_zone = tz.gettz('America/Los_Angeles')

if args.games:
    get_games(seasons, weeks)

# if args.boxscores:
#     get_boxscores(seasons, weeks)
