import pandas as pd
from datetime import datetime
from pyquery import PyQuery as pq


class Injury:
    def __init__(self, tr):
        self._report_date = None
        self._player_name = None
        self._nba_team = None
        self._injury_update_date = None
        self._injury_status = None
        self._injury_type = None
        self._details = None

        self._parse_tr(tr)

    def _parse_tr(self, tr):
        setattr(self, '_report_date', datetime.today().date().isoformat())
        for th in tr('th').items():
            if th.attr['data-stat'] == 'player':
                setattr(self, '_player_name', th.text())
        for td in tr('td').items():
            data_stat = td.attr['data-stat']
            if data_stat == 'team_name':
                setattr(self, '_nba_team', td.text())
            elif data_stat == 'date_update':
                setattr(self, '_injury_update_date', td.text())
            elif data_stat == 'note':
                # Note/description example:
                # Day To Day (Illness) - Walker is questionable for Friday's (Jan. 3) game against Atlanta
                notes = td.text().split('-')
                status_and_type = notes[0].split('(')
                setattr(self, '_injury_status', status_and_type[0].strip())
                setattr(self, '_injury_type', status_and_type[1].replace(')', '').strip())
                setattr(self, '_details', notes[1].strip())

    @property
    def dataframe(self):
        fields_to_include = {
            'ReportDate': self._report_date,
            'PlayerName': self._player_name,
            'NbaTeam': self._nba_team,
            'InjuryUpdateDate': self._injury_update_date,
            'InjuryStatus': self._injury_status,
            'InjuryType': self._injury_type,
            'Details': self._details
        }
        return pd.DataFrame([fields_to_include], index=[self._report_date])


class Injuries:
    def __init__(self):
        self._injuries = []

        self._get_injuries()

    def __repr__(self):
        return self._injuries

    def __iter__(self):
        return iter(self.__repr__())

    def _get_injuries(self):
        injuries_html = pq('https://www.basketball-reference.com/friv/injuries.cgi', verify=VERIFY_REQUESTS)
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
