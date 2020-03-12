import pandas as pd
from datetime import datetime
from pyquery import PyQuery as pq


class Injury:
    """
    Player injury information.

    Parameters
    ----------
    tr : dict
        HTML table row that is parsed for injury data.
    """
    def __init__(self, tr):
        self._report_date = None
        self._player_name = None
        self._nhl_team = None
        self._date_of_injury = None
        self._injury_status = None
        self._injury_type = None
        self._details = None

        self._parse_injury_row(tr)

    def _parse_injury_row(self, tr):
        setattr(self, '_report_date', datetime.today().date().isoformat())
        for th in tr('th').items():
            if th.attr['data-stat'] == 'player':
                setattr(self, '_player_name', th.text())
        for td in tr('td').items():
            data_stat = td.attr['data-stat']
            if data_stat == 'team_name':
                setattr(self, '_nhl_team', td.text())
            elif data_stat == 'date_injury':
                setattr(self, '_date_of_injury', td.text())
            elif data_stat == 'injury_type':
                setattr(self, '_injury_type', td.text())
            elif data_stat == 'injury_note':
                # Note/description example:
                # Saad will miss at least a couple of weeks, according to a report from the Chicago Sun-Times
                setattr(self, '_details', td.text())
            # todo- status?

    @property
    def dataframe(self):
        fields_to_include = {
            'ReportDate': self._report_date,
            'PlayerName': self._player_name,
            'NhlTeam': self._nhl_team,
            'DateOfInjury': self._date_of_injury,
            'InjuryType': self._injury_type,
            'Details': self._details
        }
        return pd.DataFrame([fields_to_include], index=[self._report_date])


class Injuries:
    """
    Players injury information.

    Parameters
    ----------
    None
    """
    def __init__(self):
        self._injuries = []

        self._get_injuries()

    def __repr__(self):
        return self._injuries

    def __iter__(self):
        return iter(self.__repr__())

    def _get_injuries(self):
        url = 'https://www.hockey-reference.com/friv/injuries.cgi'
        print('Getting data from ' + url)
        injuries_html = pq(url, verify=VERIFY_REQUESTS)
        for table in injuries_html('table').items():
            if table.attr['id'] == 'injuries':
                injuries_table = table
        first_row = True
        for tr in injuries_table('tr').items():
            if first_row:
                first_row = False
                continue  # Skip header row
            injury = Injury(tr)
            self._injuries.append(injury)

    @property
    def dataframes(self):
        frames = []
        for injury in self.__iter__():
            frames.append(injury.dataframe)
        return pd.concat(frames)
