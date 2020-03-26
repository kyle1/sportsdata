import requests
from datetime import datetime, timedelta
from sportsdata.nhl.boxscore import GameBoxscore, GameBoxscores


BASE_URL = 'https://localhost:44374/api/'

#game_boxscore = GameBoxscore(2019020196)

start_date = datetime.strptime('10/03/2018', '%m/%d/%Y')
end_date = datetime.strptime('6/12/2019', '%m/%d/%Y')

loop_date = start_date

while loop_date <= end_date:

    date_str = datetime.strftime(loop_date, '%m/%d/%Y')
    game_boxscores = GameBoxscores(date=date_str)

    if len(game_boxscores._boxscores) == 0:
        print('No games on ' + date_str)
        loop_date = loop_date + timedelta(days=1)
        continue

    filename_date = datetime.strftime(loop_date, '%Y-%m-%d')

    game_boxscores_path = f'csv/nhl/2018/game_boxscores/{filename_date}_game_boxscores.csv'
    game_boxscores_dataframe = game_boxscores.dataframes
    print(game_boxscores_dataframe)
    # game_boxscores_dataframe.to_csv(game_boxscores_path)

    player_boxscores_path = f'csv/nhl/2018/player_boxscores/{filename_date}_player_boxscores.csv'
    player_dataframes = game_boxscores.player_dataframes
    # print(player_dataframes)
    player_dataframes.to_csv(player_boxscores_path, index=False)

    pbps_path = f'csv/nhl/2018/play_by_plays/{filename_date}_pbp.csv'
    pbp_dataframes = game_boxscores.pbp_dataframes
    # print(pbp_dataframes)
    pbp_dataframes.to_csv(pbps_path, index=False)

    response = requests.post(url=BASE_URL + 'nhl/boxscores', json=game_boxscores.to_dicts, verify=False).json()

    loop_date = loop_date + timedelta(days=1)
