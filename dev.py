from sportsdata.xfl.boxscore import Boxscores

boxscores = Boxscores(week=1)
boxscores_df = boxscores.dataframes
print(boxscores_df)
