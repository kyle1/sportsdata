from sportsdata.nba.schedule import Schedule
from sportsdata.nba.team import Team, Teams

# teams = Teams()
# team_dicts = teams.to_dicts
# print(team_dicts)

sched = Schedule(season=2019)
sched_dicts = sched.to_dicts
print(sched_dicts)