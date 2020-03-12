import pandas as pd


class ScoringPlay:
    """
    Details of a play resulting in a score.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

    tr : dict
        HTML table row that is parsed for play information.
    """
    def __init__(self, game, tr):
        self._xfl_game_id = None
        self._xfl_team_abbrev = None
        self._quarter = None
        self._play_start_time = None
        self._situation = None
        self._play_description = None
        self._drive_play_count = None
        self._drive_yards = None
        self._drive_time = None
        self._end_away_score = None
        self._end_home_score = None

        self._parse_scoring_play(game_id, tr)

    def _parse_scoring_play(self, game, tr):
        div = tr.find_elements_by_class_name('row.playRow.teamRow')[0]

        # Extract team abbreviation from the logo image src tag.
        logo_src = div.find_element_by_tag_name('img').get_attribute('src')
        team_abbrev = logo_src.split('/')[len(logo_src.split('/')) - 1].split('.')[0]

        quarter = div.find_element_by_class_name('rQtr').get_attribute('textContent')
        start = div.find_element_by_class_name('rStart').get_attribute('textContent')
        situation = div.find_element_by_class_name('rPossDown').get_attribute('textContent')
        play_description = div.find_element_by_class_name('rPlayDesc').get_attribute('textContent').strip()
        drive_play_count = div.find_element_by_class_name('rPlays').get_attribute('textContent')
        drive_yards = div.find_element_by_class_name('rYards').get_attribute('textContent')
        drive_time = div.find_element_by_class_name('rTime').get_attribute('textContent')
        end_away_score = div.find_element_by_class_name('rVisitor').get_attribute('textContent')
        end_home_score = div.find_element_by_class_name('rHome').get_attribute('textContent')

        setattr(self, '_xfl_game_id', game._xfl_game_id)
        setattr(self, '_xfl_team_abbrev', team_abbrev)
        setattr(self, '_quarter', quarter)
        setattr(self, '_play_start_time', start)
        setattr(self, '_situation', situation)
        setattr(self, '_play_description', play_description)
        setattr(self, '_drive_play_count', drive_play_count)
        setattr(self, '_drive_yards', drive_yards)
        setattr(self, '_drive_time', drive_time)
        setattr(self, '_end_away_score', end_away_score)
        setattr(self, '_end_home_score', end_home_score)

    @property
    def dataframe(self):
        fields_to_include = {
            'XflGameId': self._xfl_game_id,
            'XflTeamAbbrev': self._xfl_team_abbrev,
            'Quarter': self._quarter,
            'PlayStartTime': self._play_start_time,
            'Situation': self._situation,
            'PlayDescription': self._play_description,
            'DrivePlayCount': self._drive_play_count,
            'DriveYards': self._drive_yards,
            'DriveTime': self._drive_time,
            'EndAwayScore': self._end_away_score,
            'EndHomeScore': self._end_home_score,
        }
        return pd.DataFrame([fields_to_include], index=None)


class ScoringPlays:
    """
    Details of a plays resulting in a score.

    Parameters
    ----------
    game : GameBoxscore
        Object that contains game-level boxscore data.

    scoring_table : dict
        HTML Table that is parsed for play information.
    """
    def __init__(self, game, scoring_table):
        self._scoring_plays = []

        self._get_scoring_plays(game, scoring_table)

    def __repr__(self):
        return self._scoring_plays

    def __iter__(self):
        return iter(self.__repr__())

    def _get_scoring_plays(self, game, scoring_table):
        rows = scoring_table.find_elements_by_class_name('body')
        for tr in rows:
            scoring_play = ScoringPlay(game, tr)
            self._scoring_plays.append(scoring_play)

    @property
    def dataframes(self):
        frames = []
        for scoring_play in self.__iter__():
            frames.append(scoring_play.dataframe)
        return pd.concat(frames)
