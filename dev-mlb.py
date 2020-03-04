import pandas as pd
#from sportsdata.mlb.boxscore import Boxscore, Boxscores
from sportsdata.mlb.game import Game, Games
from sportsdata.mlb.gameboxscore import GameBoxscore, GameBoxscores
#from sportsdata.mlb.injury import Injury
from sportsdata.mlb.odds import GameOdds, GamesOdds
from sportsdata.mlb.playbyplay import PlayByPlays, PlayByPlay, Play
from sportsdata.mlb.player import Player, Players
from sportsdata.mlb.playerboxscore import PlayerBoxscore, PlayerBoxscores
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


game_boxscore = GameBoxscore(565895)
away_players = game_boxscore._away_players
home_players = game_boxscore._home_players
pbp = game_boxscore._play_by_play

print(away_players.dataframes)
print(home_players.dataframes)
print(pbp.dataframes)


#game_boxscores = GameBoxscores(date='05/04/2019')


# player_box_dfs = []
# pbp_dfs = []
# for boxscore in game_boxscores._boxscores:
#     player_box_dfs.append(boxscore._away_players.dataframes)
#     player_box_dfs.append(boxscore._home_players.dataframes)
#     pbp_dfs.append(boxscore._play_by_play.dataframes)

# games_df = game_boxscores.dataframes
# player_boxs_df = pd.concat(player_box_dfs)
# pbps_df = pd.concat(pbp_dfs)

# print(games_df)
# print(player_boxs_df)
# print(pbps_df)

# games_df.to_csv('mlb_games.csv')
# player_boxs_df.to_csv('mlb_player_boxscores.csv')
# pbps_df.to_csv('mlb_playbyplay.csv')
