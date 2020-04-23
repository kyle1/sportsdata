import requests
from sportsdata.csgo.odds import MatchesOdds

BASE_URL = 'https://localhost:44374/api/'

odds = MatchesOdds()
print(odds.to_dicts)

response = requests.post(BASE_URL + "csgo/odds", json=odds.to_dicts, verify=False).json()
print(response)
