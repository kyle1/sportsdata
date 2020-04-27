import pandas as pd
import requests
from pyquery import PyQuery as pq


class Event:
    """
    CSGO event.

    Parameters
    ----------
    a_tag : todo
        todo
    """

    def __init__(self, a_tag):
        self._csgo_event_id = None
        self._event_name = None

        self._parse_event(a_tag)

    def _parse_event(self, a_tag):
        event_id = a_tag.attr['href'].split('/')[2]
        for img in a_tag('img').items():
            event_name = img.attr['title']
            break
        setattr(self, '_csgo_event_id', event_id)
        setattr(self, '_event_name', event_name)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoEventId': self._csgo_event_id,
            'EventName': self._event_name,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Events:
    def __init__(self):
        self._events = []

        self._get_events()

    def _get_events(self):
        url = 'https://www.hltv.org/events#tab-ALL'
        events_html = pq(url, verify=False)

        for div in events_html('div').items():
            if div.attr['id'] == 'ALL':
                for a_tag in div('a').items():
                    if a_tag.attr['class'] == 'a-reset ongoing-event':
                        event = Event(a_tag)
                        self._events.append(event)

    def __repr__(self):
        return self._events

    def __iter__(self):
        return iter(self.__repr__())

    @property
    def dataframes(self):
        frames = []
        for event in self.__iter__():
            frames.append(event.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for event in self.__iter__():
            dics.append(event.to_dict)
        return dics
