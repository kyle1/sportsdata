from sportsdata.xfl.boxscore import Boxscore, Boxscores
from sportsdata.xfl.game import Game, Games
from sportsdata.xfl.player import Player, Players
from sportsdata.xfl.scoring import ScoringPlays

# player_boxscores = Boxscores(id=1)
# player_boxscores_df = player_boxscores.dataframes
# player_boxscores_df.to_csv('xfl_player_boxscores.csv')


games = Games(week=1)
games_df = games.dataframes
games_df.to_csv('xfl_games.csv')
