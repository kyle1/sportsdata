import pandas as pd
import requests
from time import sleep


class GameWeather:
    def __init__(self, weather):
        self._xfl_game_id = None
        self._weather_date_time = None
        self._is_game_start_time = None
        self._apparent_temperature = None
        self._humidity = None
        self._icon = None
        self._precipitation_probability = None
        self._temperature = None
        self._summary = None
        self._wind_bearing = None
        self._wind_speed = None

        self._get_game_weather(game)

    def _get_game_weather(self, game):
        darksky_url = 'todo'
        print('Getting weather data from ' + darksky_url)
        weather = requests.get(darksky_url, verify=VERIFY_REQUESTS).json()
        setattr(self, '_xfl_game_id', game['xflGameId'])
        setattr(self, '_weather_date_time', datetime.fromtimestamp(weather['currently']['time']).isoformat())
        setattr(self, '_apparent_temperature': weather['currently']['apparentTemperature'])
        setattr(self, '_humidity': weather['currently']['humidity'])
        setattr(self, '_icon': weather['currently']['icon'])
        setattr(self, '_precipitation_probability': weather['currently']['precipProbability'])
        setattr(self, '_temperature': weather['currently']['temperature'])
        setattr(self, '_summary': weather['currently']['summary'])
        setattr(self, '_wind_bearing': weather['currently']['windBearing'])
        setattr(self, '_wind_speed': weather['currently']['windSpeed'])

    @property
    def dataframe(self):
        fields_to_include = {
            'XflGameId': self._xfl_game_id,
            'WeatherDateTime': self._weather_date_time,
            'ApparentTemperature': self._apparent_temperature,
            'Humidity': self._humidity,
            'Icon': self._icon,
            'PrecipitationProbability': self._precipitation_probability,
            'Temperature': self._temperature,
            'Summary': self._summary,
            'WindBearing': self._wind_bearing,
            'WindSpeed': self._wind_speed
        }
        return pd.DataFrame([fields_to_include], index=[self._xfl_game_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class GameWeathers:
      def __init__(self, week):
        self._weathers = []

        self._get_weathers(week)

    def __repr__(self):
        return self._weathers

    def __iter__(self):
        return iter(self.__repr__())

    def _get_game_weathers(self, week):
        url = 'todo'
        print('Getting game data from ' + url)
        response = requests.get(url, verify=VERIFY_REQUESTS).json()
        games = response['data']
        for game in games:
            if now > datetime.strptime(game['gameDateTime'], '%Y-%m-%dT%H:%M:%S'):
                print(f'Skipping game {game["xflGameId"]} since it is past start time.')
                continue
            weather = GameWeather(game)
            self._weathers.append(weather)

    @property
    def dataframes(self):
        frames = []
        for weather in self.__iter__():
            frames.append(weather.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for weather in self.__iter__():
            dics.append(weather.to_dict)
        return dics