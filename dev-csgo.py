import requests
from sportsdata.csgo.odds import MatchesOdds
from sportsdata.csgo.schedule import Schedule

BASE_URL = 'https://localhost:44374/api/'

# odds = MatchesOdds()
# print(odds.to_dicts)
# response = requests.post(BASE_URL + "csgo/odds", json=odds.to_dicts, verify=False).json()
# print(response)

schedule = Schedule()
print(schedule.dataframes)
print(schedule.to_dicts)
