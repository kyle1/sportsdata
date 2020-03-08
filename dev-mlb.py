import pandas as pd
#from sportsdata.mlb.boxscore import Boxscore, Boxscores
from sportsdata.mlb.boxscore import GameBoxscore, GameBoxscores
from sportsdata.mlb.game import Game, Games
#from sportsdata.mlb.gameboxscore import GameBoxscore, GameBoxscores
#from sportsdata.mlb.injury import Injury
from sportsdata.mlb.odds import GameOdds, GamesOdds
from sportsdata.mlb.playbyplay import PlayByPlays, PlayByPlay, Play
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

box = GameBoxscore(565895)
box_df = box.dataframe
print(box_df)
box_df.to_csv('box.csv')
