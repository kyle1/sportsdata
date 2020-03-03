from sportsdata.xfl.boxscore import Boxscores

boxscores = Boxscores(id=1)
boxscores_df = boxscores.dataframes
boxscores_df.to_csv('boxscores.csv')