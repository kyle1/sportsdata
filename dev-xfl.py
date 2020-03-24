# from sportsdata.xfl.boxscore import Boxscore, Boxscores
# from sportsdata.xfl.game import Game, Games
# from sportsdata.xfl.player import Player, Players
# from sportsdata.xfl.scoring import ScoringPlays

# player_boxscores = Boxscores(id=1)
# player_boxscores_df = player_boxscores.dataframes
# player_boxscores_df.to_csv('xfl_player_boxscores.csv')


# games = Games(week=1)
# games_df = games.dataframes
# games_df.to_csv('xfl_games.csv')


from sportsdata.xfl.boxscore import GameBoxscore, GameBoxscores

week = 1

game_boxscores = GameBoxscores(week=1)

filename_date = datetime.strftime(loop_date, '%Y-%m-%d')

game_boxscores_path = f'csv/nhl/2019/game_boxscores/week-{week}_game_boxscores.csv'
game_boxscores_dataframe = game_boxscores.dataframes
print(game_boxscores_dataframe)
game_boxscores_dataframe.to_csv(game_boxscores_path)

player_boxscores_path = f'csv/nhl/2019/player_boxscores/week-{week}_player_boxscores.csv'
player_dataframes = game_boxscores.player_dataframes
print(player_dataframes)
player_dataframes.to_csv(player_boxscores_path, index=False)

# pbps_path = f'csv/nhl/2019/play_by_plays/week-{week}_pbp.csv'
# pbp_dataframes = game_boxscores.pbp_dataframes
# print(pbp_dataframes)
# pbp_dataframes.to_csv(pbps_path, index=False)


# game = GameBoxscore(1, None)
# #game_df = game.dataframe
# players_df = game._boxscores.dataframes
# print(players_df)

# players_df.to_csv('xfl_player_boxscores.csv')




