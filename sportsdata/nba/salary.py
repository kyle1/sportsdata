import pandas as pd
import requests


class Salary:
    def __init__(self):
        self._salary_date = None
        self._player_name = None
        self._draftkings_salary = None
        self._draftkings_fantasy_points = None
        self._fanduel_salary = None
        self._fanduel_fantasy_points = None
        self._yahoo_salary = None
        self._yahoo_fantasy_points = None

        self._get_salary_data()

    def _get_salary_data(self):
        print('todo')

    @property
    def dataframe(self):
        fields_to_include = {
            'SalaryDate': self._salary_date,
            'PlayerName': self._player_name,
            'DraftKingsSalary': self._draftkings_salary,
            'DraftKingsFp': self._draftkings_fantasy_points,
            'FanDuelSalary': self._fanduel_salary,
            'FanDuelFp': self._fanduel_fantasy_points,
            'YahooSalary': self._yahoo_salary,
            'YahooFp': self._yahoo_fantasy_points
        }
        return pd.DataFrame([fields_to_include], index=None)


class Salaries:
    def __init__(self, start_date, end_date):
        self._salaries = []

        self._get_salaries(start_date, end_date)

    def __repr__(self):
        return self._salaries

    def __iter__(self):
        return iter(self.__repr__())

    def _get_salaries(self, start_date, end_date):
        while loop_date <= start_date and loop_date < end_date:
            day_dataframes = []
            for website in ['dk', 'fd', 'yh']:
                day_dataframe = get_dataframe_by_website_and_date(website, loop_date)
                day_dataframes.append(day_dataframe)
                sleep(randint(2, 4))
            joined_df = util.join_dataframes(day_dataframes, HEADERS, loop_date)
            col_mappings = {'Salary_x': 'DraftKingsSalary', 'FantasyPoints_x': 'DraftKingsFp', 'Salary_y': 'FanDuelSalary',
                            'FantasyPoints_y': 'FanDuelFp', 'Salary': 'YahooSalary', 'FantasyPoints': 'YahooFp'}
            joined_df.rename(columns=col_mappings, inplace=True)
            joined_df = joined_df.where((pd.notnull(joined_df)), None)  # nan -> None
            loop_date = loop_date + timedelta(days=1)

    def _get_dataframe_by_website_and_date(website, date):
        dataframe = pd.DataFrame()
        url = NBA_SALARIES_URL % (website, date.month, date.day, date.year)
        print('Getting salary data from: ' + url)
        salary_html = pq(url)
        if salary_html:
            dates, players, salaries, fps = [], [], [], []
            for table in salary_html('table').items():
                if table.attr['cellspacing'] == '5':
                    # The salary table is the only one with cellspacing=5
                    for row in table('tr').items():
                        if '$' in row.text():
                            dates.append(date.strftime('%Y-%m-%d'))
                            col = 0
                            for td in row('td').items():
                                if col == NAME_COL_INDEX:
                                    name = td.text().split('^')[0]
                                    if ',' in name:
                                        # Convert 'Last, First' to 'First Last'
                                        name = name.split(',')[1].strip(
                                        ) + ' ' + name.split(',')[0]
                                    players.append(name)
                                if col == SALARY_COL_INDEX:
                                    salary = td.text().replace('$', '').replace(',', '')
                                    salaries.append(salary)
                                if col == FP_COL_INDEX:
                                    fp = td.text()
                                    fps.append(fp)
                                col += 1
            dataframe['SalaryDate'] = dates
            dataframe['PlayerName'] = players
            dataframe['Salary'] = salaries
            dataframe['FantasyPoints'] = fps
        return dataframe

    @property
    def dataframes(self):
        frames = []
        for salary in self.__iter__():
            frames.append(salary.dataframe)
        return pd.concat(frames)
