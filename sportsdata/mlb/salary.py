import requests
from time import sleep

#todo- find a way to get a contest id by date.
contest_id = 100000

contest_url = f'https://api.draftkings.com/contests/v1/contests/{contest_id}?format=json'
print('Getting contest data from ' + contest_url)
contest = requests.get(contest_url, verify=False).json()

sleep(5)

draft_group_id = contest['contestDetail']['draftGroupId']
draftables_url = f'https://api.draftkings.com/draftgroups/v1/draftgroups/{draft_group_id}/draftables'
print('Getting draftable player data from ' + draftables_url)
draftables = requests.get(draftables_url, verify=False).json()

for draftable in draftables['draftables']:
    print(draftable)
    print('\n')


