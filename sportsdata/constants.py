VERIFY_REQUESTS = False

SPORTS = ['nfl', 'mlb', 'nba', 'nhl']

DFS_WEBSITES = ['dk', 'fd', 'yh']

DAYS_IN_MONTH = {
    1: 31,
    2: 28,  # todo- Leap years
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

############ MLB #############
MLB_SEASONS = [
    {'season': 2005, 'start_date': '04/03/2005', 'end_date': '10/26/2005'},
    {'season': 2006, 'start_date': '04/02/2006', 'end_date': '10/27/2006'},
    {'season': 2007, 'start_date': '04/01/2007', 'end_date': '10/28/2007'},
    {'season': 2008, 'start_date': '03/25/2008', 'end_date': '10/29/2008'},
    {'season': 2009, 'start_date': '04/05/2009', 'end_date': '11/04/2009'},
    {'season': 2010, 'start_date': '04/04/2010', 'end_date': '11/01/2010'},
    {'season': 2011, 'start_date': '03/31/2011', 'end_date': '10/28/2011'},
    {'season': 2012, 'start_date': '03/28/2012', 'end_date': '10/28/2012'},
    {'season': 2013, 'start_date': '03/31/2013', 'end_date': '10/30/2013'},
    {'season': 2014, 'start_date': '03/22/2014', 'end_date': '10/29/2014'},
    {'season': 2015, 'start_date': '04/05/2015', 'end_date': '11/01/2015'},
    {'season': 2016, 'start_date': '04/03/2016', 'end_date': '11/02/2016'},
    {'season': 2017, 'start_date': '04/02/2017', 'end_date': '11/01/2017'},
    {'season': 2018, 'start_date': '03/29/2018', 'end_date': '10/28/2018'},
    {'season': 2019, 'start_date': '03/28/2019', 'end_date': '11/01/2019'}]


############ NBA #############
# todo: put these in nba specific constants file
NBA_SEASONS = [
    {'season': 2018, 'start_date': '10/16/2018', 'end_date': '06/13/2019'},
    {'season': 2019, 'start_date': '10/22/2019', 'end_date': '04/15/2020'}]

PROXIES = {'https:': '41.76.218.96:8080'}

# Without the header below, python can't make the request to the endpoint
# This was taken from https://github.com/swar/nba_api/
NBA_REQUEST_HEADERS = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://stats.nba.com'  # 2019-11-12 this is now required
}

NBA_SALARY_HEADERS = ['SalaryDate', 'PlayerName', 'DraftKingsSalary', 'DraftKingsFp',
                      'FanDuelSalary', 'FanDuelFp', 'YahooSalary', 'YahooFp']

NBA_SALARIES_URL = 'http://rotoguru1.com/cgi-bin/hyday.pl?game=%s&mon=%s&day=%s&year=%s'

NAME_COL_INDEX = 1
FP_COL_INDEX = 2
SALARY_COL_INDEX = 3
TEAM_COL_INDEX = 4
OPP_COL_INDEX = 5

NBA_API_TEAMS = [
    {
        'team_id': 1610612737,
        'abbreviation': 'ATL',
        'team_name': 'Atlanta Hawks',
        'simple_name': 'Hawks',
        'location': 'Atlanta'
    },
    {
        'team_id': 1610612738,
        'abbreviation': 'BOS',
        'team_name': 'Boston Celtics',
        'simple_name': 'Celtics',
        'location': 'Boston'
    },
    {
        'team_id': 1610612751,
        'abbreviation': 'BKN',
        'team_name': 'Brooklyn Nets',
        'simple_name': 'Nets',
        'location': 'Brooklyn'
    },
    {
        'team_id': 1610612766,
        'abbreviation': 'CHA',
        'team_name': 'Charlotte Hornets',
        'simple_name': 'Hornets',
        'location': 'Charlotte'
    },
    {
        'team_id': 1610612741,
        'abbreviation': 'CHI',
        'team_name': 'Chicago Bulls',
        'simple_name': 'Bulls',
        'location': 'Chicago'
    },
    {
        'team_id': 1610612739,
        'abbreviation': 'CLE',
        'team_name': 'Cleveland Cavaliers',
        'simple_name': 'Cavaliers',
        'location': 'Cleveland'
    },
    {
        'team_id': 1610612742,
        'abbreviation': 'DAL',
        'team_name': 'Dallas Mavericks',
        'simple_name': 'Mavericks',
        'location': 'Dallas'
    },
    {
        'team_id': 1610612743,
        'abbreviation': 'DEN',
        'team_name': 'Denver Nuggets',
        'simple_name': 'Nuggets',
        'location': 'Denver'
    },
    {
        'team_id': 1610612765,
        'abbreviation': 'DET',
        'team_name': 'Detroit Pistons',
        'simple_name': 'Pistons',
        'location': 'Detroit'
    },
    {
        'team_id': 1610612744,
        'abbreviation': 'GSW',
        'team_name': 'Golden State Warriors',
        'simple_name': 'Warriors',
        'location': 'Golden State'
    },
    {
        'team_id': 1610612745,
        'abbreviation': 'HOU',
        'team_name': 'Houston Rockets',
        'simple_name': 'Rockets',
        'location': 'Houston'
    },
    {
        'team_id': 1610612754,
        'abbreviation': 'IND',
        'team_name': 'Indiana Pacers',
        'simple_name': 'Pacers',
        'location': 'Indiana'
    },
    {
        'team_id': 1610612746,
        'abbreviation': 'LAC',
        'team_name': 'Los Angeles Clippers',
        'simple_name': 'Clippers',
        'location': 'Los Angeles'
    },
    {
        'team_id': 1610612747,
        'abbreviation': 'LAL',
        'team_name': 'Los Angeles Lakers',
        'simple_name': 'Lakers',
        'location': 'Los Angeles'
    },
    {
        'team_id': 1610612763,
        'abbreviation': 'MEM',
        'team_name': 'Memphis Grizzlies',
        'simple_name': 'Grizzlies',
        'location': 'Memphis'
    },
    {
        'team_id': 1610612748,
        'abbreviation': 'MIA',
        'team_name': 'Miami Heat',
        'simple_name': 'Heat',
        'location': 'Miami'
    },
    {
        'team_id': 1610612749,
        'abbreviation': 'MIL',
        'team_name': 'Milwaukee Bucks',
        'simple_name': 'Bucks',
        'location': 'Milwaukee'
    },
    {
        'team_id': 1610612750,
        'abbreviation': 'MIN',
        'team_name': 'Minnesota Timberwolves',
        'simple_name': 'Timberwolves',
        'location': 'Minnesota'
    },
    {
        'team_id': 1610612740,
        'abbreviation': 'NOP',
        'team_name': 'New Orleans Pelicans',
        'simple_name': 'Pelicans',
        'location': 'New Orleans'
    },
    {
        'team_id': 1610612752,
        'abbreviation': 'NYK',
        'team_name': 'New York Knicks',
        'simple_name': 'Knicks',
        'location': 'New York'
    },
    {
        'team_id': 1610612760,
        'abbreviation': 'OKC',
        'team_name': 'Oklahoma City Thunder',
        'simple_name': 'Thunder',
        'location': 'Oklahoma City'
    },
    {
        'team_id': 1610612753,
        'abbreviation': 'ORL',
        'team_name': 'Orlando Magic',
        'simple_name': 'Magic',
        'location': 'Orlando'
    },
    {
        'team_id': 1610612755,
        'abbreviation': 'PHI',
        'team_name': 'Philadelphia 76ers',
        'simple_name': '76ers',
        'location': 'Philadelphia'
    },
    {
        'team_id': 1610612756,
        'abbreviation': 'PHX',
        'team_name': 'Phoenix Suns',
        'simple_name': 'Suns',
        'location': 'Phoenix'
    },
    {
        'team_id': 1610612757,
        'abbreviation': 'POR',
        'team_name': 'Portland Trail Blazers',
        'simple_name': 'Trail Blazers',
        'location': 'Portland'
    },
    {
        'team_id': 1610612758,
        'abbreviation': 'SAC',
        'team_name': 'Sacramento Kings',
        'simple_name': 'Kings',
        'location': 'Sacramento'
    },
    {
        'team_id': 1610612759,
        'abbreviation': 'SAS',
        'team_name': 'San Antonio Spurs',
        'simple_name': 'Spurs',
        'location': 'San Antonio'
    },
    {
        'team_id': 1610612761,
        'abbreviation': 'TOR',
        'team_name': 'Toronto Raptors',
        'simple_name': 'Raptors',
        'location': 'Toronto'
    },
    {
        'team_id': 1610612762,
        'abbreviation': 'UTA',
        'team_name': 'Utah Jazz',
        'simple_name': 'Jazz',
        'location': 'Utah'
    },
    {
        'team_id': 1610612764,
        'abbreviation': 'WAS',
        'team_name': 'Washington Wizards',
        'simple_name': 'Wizards',
        'location': 'Washington'
    }
]
