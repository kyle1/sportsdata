import pandas as pd
import requests
from datetime import datetime, timedelta
#from sportsdata.mlb.boxscore import Boxscore, Boxscores
from sportsdata.mlb.boxscore import GameBoxscore, GameBoxscores
# from sportsdata.mlb.game import Game, Games
#from sportsdata.mlb.gameboxscore import GameBoxscore, GameBoxscores
#from sportsdata.mlb.injury import Injury
from sportsdata.mlb.odds import GameOdds, GamesOdds
from sportsdata.mlb.playbyplay import PlayByPlay, Play
from sportsdata.mlb.player import Player, Players
#from sportsdata.mlb.playerboxscore import PlayerBoxscore, PlayerBoxscores
#from sportsdata.mlb.salary import Salary
from sportsdata.mlb.schedule import Schedule
from sportsdata.mlb.team import Team, Teams


# players = Players(2019)
# players_df = players.dataframes
# players_df.to_csv('mlb_players.csv')

# schedule = Schedule(season=2019)
# schedule_df = schedule.dataframes
# schedule_df.to_csv('mlb_schedule.csv')

# teams = Teams()
# teams_df = teams.dataframes
# teams_df.to_csv('mlb_teams.csv')


# schedule = Schedule(season=2019)
# print(schedule.dataframes)

BASE_URL = 'https://localhost:44374/api/'

season = '2019'

#start_date = datetime.strptime('03/28/2019', '%m/%d/%Y')
start_date = datetime.strptime('10/16/2019', '%m/%d/%Y')
end_date = datetime.strptime('10/30/2019', '%m/%d/%Y')
#end_date = datetime.strptime('3/30/2019', '%m/%d/%Y')

loop_date = start_date

while loop_date <= end_date:

    date_str = datetime.strftime(loop_date, '%m/%d/%Y')
    game_boxscores = GameBoxscores(date=date_str)

    if len(game_boxscores._boxscores) == 0:
        print('No games on ' + date_str)
        loop_date = loop_date + timedelta(days=1)
        continue

    filename_date = datetime.strftime(loop_date, '%Y-%m-%d')

    game_boxscores_path = f'csv/mlb/2019/game_boxscores/{filename_date}_game_boxscores.csv'
    game_boxscores.dataframes.to_csv(game_boxscores_path)

    player_boxscores_path = f'csv/mlb/2019/player_boxscores/{filename_date}_player_boxscores.csv'
    player_dataframes = game_boxscores.player_dataframes
    player_dataframes.to_csv(player_boxscores_path, index=False)
    # print(player_dataframes)

    pbps_path = f'csv/mlb/2019/play_by_plays/{filename_date}_pbp.csv'
    pbp_dataframes = game_boxscores.pbp_dataframes
    pbp_dataframes.to_csv(pbps_path, index=False)
    # print(pbp_dataframes)

    response = requests.post(url=BASE_URL + 'mlb/boxscores', json=game_boxscores.to_dicts, verify=False).json()

    loop_date = loop_date + timedelta(days=1)

# players = Players(2019)
# player_dicts = players.to_dicts
# print(player_dicts)
