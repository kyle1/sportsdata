import argparse

#import datetime
import requests
from config import DARKSKY_API_KEY
from constants import BASE_URL, DARKSKY_BASE_URL
from datetime import datetime
from time import sleep
from util import get_nfl_week

# unix = '1571696693'
# dt = datetime.datetime.fromtimestamp(int(unix))
# print(dt)


def validate_args(args):
    sports = ['nfl', 'mlb']
    for sport in args.sports:
        if sport not in sports:
            return False
    return True


parser = argparse.ArgumentParser(description='How to use:')
parser.add_argument('-sports', nargs='+', required=True, help='Sports to fetch forecasts for')
args = parser.parse_args()
valid_args = validate_args(args)

if valid_args:
    now = datetime.now()
    today = now.date()
    for sport in args.sports:
        game_forecasts = []
        gmt_offset = '-0800'  # todo i think this changes from -0700 to -0800 after DST on nov 3

        if sport == 'nfl':
            nfl_week = get_nfl_week_by_date(today)
            url = f'{BASE_URL}{sport}/games/gameType/{nfl_week["game_type"]}/week/{nfl_week["week"]}'
            print('Getting data from ' + url)
            response = requests.get(url, verify=VERIFY_REQUESTS).json()
            games = response['data']
        elif sport == 'mlb':
            print('todo- format date and make get request using date string')
        else:
            print('Invalid sport: ' + sport)
            continue

        for game in games:
            if now > datetime.strptime(game['gameDateTime'], '%Y-%m-%dT%H:%M:%S')
                # Don't update weather data for games that have already started.
                print(f'Skipping game {game["nflGameId"]} since it is past the game start time.')
                continue
            url = f"{DARKSKY_BASE_URL}{DARKSKY_API_KEY}/{game['latitude']},{game['longitude']},{game['gameDateTime'] + gmt_offset}"
            print('Getting weather data from ' + url)
            weather = requests.get(url, verify=VERIFY_REQUESTS).json()
            # weather['gameId'] = game['gameID']
            # dt = datetime.fromtimestamp(weather['currently']['time'])
            # weather['currently']['time'] = dt.isoformat()

            start_time = {
                'WeatherDateTime': datetime.fromtimestamp(weather['currently']['time']).isoformat(),
                'ApparentTemperature': weather['currently']['apparentTemperature'],
                'Humidity': weather['currently']['humidity'],
                'Icon': weather['currently']['icon'],
                'PrecipitationProbability': weather['currently']['precipProbability'],
                'Temperature': weather['currently']['temperature'],
                'Summary': weather['currently']['summary'],
                'WindBearing': weather['currently']['windBearing'],
                'WindSpeed': weather['currently']['windSpeed']
            }

            hourly_list = []
            for hour in weather['hourly']['data']:
                #hour['time'] = datetime.fromtimestamp(hour['time']).isoformat()
                hourly = {
                    'WeatherDateTime': datetime.fromtimestamp(hour['time']).isoformat(),
                    'ApparentTemperature': hour['apparentTemperature'],
                    'Humidity': hour['humidity'],
                    'Icon': hour['icon'],
                    'PrecipitationProbability': hour['precipProbability'],
                    'Temperature': hour['temperature'],
                    'Summary': hour['summary'],
                    'WindBearing': hour['windBearing'],
                    'WindSpeed': hour['windSpeed']
                }
                hourly_list.append(hourly)

            forecast = {
                'GameId': game['nflGameId'],
                'StartTime': start_time,
                'Hourly': hourly_list
            }
            game_forecasts.append(forecast)
            sleep(5)

        for game_forecast in game_forecasts:
            print(game_forecast)

        #response = requests.post(BASE_URL + sport + '/weather/', json=game_forecasts, verify=VERIFY_REQUESTS).json()
        print(response['data'])
else:
    print('Invalid arguments')