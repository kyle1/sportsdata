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

start_date = datetime.strptime('03/28/2019', '%m/%d/%Y')
end_date = datetime.strptime('10/30/2019', '%m/%d/%Y')

loop_date = start_date

while loop_date <= end_date:
    # look into error for 7/8/2019
    date_str = datetime.strftime(loop_date, '%m/%d/%Y')
    filename_date = datetime.strftime(loop_date, '%Y-%m-%d')

    game_boxscores = GameBoxscores(date=date_str)
    game_boxscores_path = f'csv/mlb/2019/game_boxscores/{filename_date}_game_boxscores.csv'
    game_boxscores.dataframes.to_csv(game_boxscores_path)

    for game in game_boxscores._boxscores:
        player_boxscores_path = f'csv/mlb/2019/player_boxscores/{filename_date}_player_boxscores.csv'
        away_players = game._away_players.dataframes
        home_players = game._home_players.dataframes
        players_dataframes = pd.concat([away_players, home_players])
        players_dataframes.to_csv(player_boxscores_path)

    response = requests.post(url=BASE_URL + 'mlb/boxscores', json=game_boxscores.to_dicts, verify=False).json()

    loop_date = loop_date + timedelta(days=1)

# players = Players(2019)
# player_dicts = players.to_dicts
# print(player_dicts)
