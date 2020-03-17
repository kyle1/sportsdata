import pandas as pd
import requests
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

# BASE_URL = 'https://localhost:44374/api/'
boxscores = GameBoxscores(date='10/30/2019')
boxscore_dicts = boxscores.to_dicts
print(boxscore_dicts)
# response = requests.post(url=BASE_URL + 'mlb/boxscores', json=boxscore_dicts, verify=False).json()

# players = Players(2019)
# player_dicts = players.to_dicts
# print(player_dicts)