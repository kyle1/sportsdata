import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil import parser
from pyquery import PyQuery as pq
from time import sleep


class Match:
    def __init__(self, url):
        self._csgo_match_id = None
        self._match_url = None
        self._match_date_time = None
        self._team1_id = None
        self._team2_id = None
        self._best_of = None
        self._csgo_event_id = None

        self._match_maps = []

        self._get_match(url)

    def _get_match(self, url):
        match_id = url.split('/')[2]
        setattr(self, '_csgo_match_id', match_id)

        full_url = 'https://www.hltv.org' + url
        setattr(self, '_match_url', full_url)

        print('Getting match data from ' + full_url)
        match_html = pq(full_url, verify=False)
        map_divs = []
        for div in match_html('div').items():
            if div.attr['class'] == 'timeAndEvent':
                for sub_div in div('div').items():
                    if sub_div.attr['class'] == 'time':
                        match_time = sub_div.text()
                    if sub_div.attr['class'] == 'event text-ellipsis':
                        for a in sub_div('a').items():
                            setattr(self, '_csgo_event_id', a.attr['href'].split('/')[2])
            if div.attr['class'] == 'date':
                date_obj = parser.parse(div.text())
                setattr(self, '_match_date', date_obj.date())
            if div.attr['class'] == 'team1-gradient':
                for a in div('a').items():
                    setattr(self, '_team1_id', a.attr['href'].split('/')[2])
            if div.attr['class'] == 'team2-gradient':
                for a in div('a').items():
                    setattr(self, '_team2_id', a.attr['href'].split('/')[2])
            if div.attr['class'] == 'standard-box veto-box':
                if 'Best' in div.text():
                    best_of_text = div.text()
                    best_of = best_of_text.split()[2]
                    setattr(self, '_best_of', best_of)  # FIX

        hours_into_day = float(match_time.split(':')[0]) + float(match_time.split(':')[1]) / 60.0
        dt = date_obj + timedelta(hours=hours_into_day)
        setattr(self, '_match_date_time', dt)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoMatchId': self._csgo_match_id,
            'MatchUrl': self._match_url,
            'MatchDateTime': self._match_date_time,
            # 'MatchDescription': self._match_description,
            'Team1Id': self._team1_id,
            'Team2Id': self._team2_id,
            'BestOf': self._best_of,
            'CsgoEventId': self._csgo_event_id
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['MatchDateTime'] = dic['MatchDateTime'].isoformat()
        return dic


class Schedule:
    """
    Generates the upcoming CSGO schedule.

    Parameters
    ----------
    None
    """

    def __init__(self, **kwargs):
        self._matches = []

        self._get_schedule()

    def __repr__(self):
        return self._matches

    def __iter__(self):
        return iter(self.__repr__())

    def _get_schedule(self):
        url = 'https://www.hltv.org/matches'
        matches_html = pq(url, verify=False)

        for day_div in matches_html('div').items():
            if day_div.attr['class'] == 'match-day':
                for match_div in day_div('div').items():
                    if match_div.attr['class'] == 'match':
                        for a in match_div('a').items():
                            match_url = a.attr['href']
                            match = Match(match_url)
                            self._matches.append(match)
                            sleep(5)
                            break

    @property
    def dataframes(self):
        frames = []
        for match in self.__iter__():
            frames.append(match.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for match in self.__iter__():
            dics.append(match.to_dict)
        return dics
