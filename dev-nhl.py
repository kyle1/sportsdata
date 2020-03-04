from sportsdata.nhl.boxscore import GameBoxscore, GameBoxscores


game_boxscore = GameBoxscore(2019020196)
away_players = game_boxscore._away_players
home_players = game_boxscore._home_players

print(game_boxscore.dataframe)
print(away_players.dataframes)
print(home_players.dataframes)