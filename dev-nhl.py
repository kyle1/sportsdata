from sportsdata.nhl.boxscore import GameBoxscore, GameBoxscores


game_boxscore = GameBoxscore(2019020196)
away_players = game_boxscore._away_players
home_players = game_boxscore._home_players
pbp = game_boxscore._play_by_play

game_boxscore_df = game_boxscore.dataframe
away_players_df = away_players.dataframes
home_players_df = home_players.dataframes
pbp_df = pbp.dataframes

# print(game_boxscore_df)
# print(away_players_df)
# print(home_players_df)
print(pbp_df)

game_boxscore.dataframe.to_csv('nhl-boxscore.csv')
away_players_df.to_csv('nhl-away-players.csv')
home_players_df.to_csv('nhl-home-players.csv')
pbp_df.to_csv('nhl-pbp.csv')
