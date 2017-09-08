"""Create music-based database rows in a Builder-like way

Todo:
    * Add build methods for each column of the desired table structure

"""

class AbstractBuilder:
    """Abstract ScoreBuilder

    Unimplemented methods do not raise exceptions so as to allow inheriting
    classes to pick and choose which parts to build

    """

    def build_name(self):
        """Empty overridable method"""
        pass

    def build_composer(self):
        """Empty overridable method"""
        pass

class ScoreBuilder(AbstractBuilder):
    """Scores table (holds info about musical scores) database-entry builder

    Use to build a row entry from a music21 note

    Args:
    tbl (str): name of table where entries will be inserted
    m21n (:obj:`music21.note.Note): contains note information

    Attributes:
    _tbl (str): name of table where entries will be inserted
    _m21n (:obj:`music21.note.Note): contains note information
    _kw (dict): column, value pairs for entry in database

    """

    def __init__(self, tbl="Scores", name, composer):
        self._tbl = tbl
        self._kw = {
            'name': name, 'composer': composer
        }

    def get_entry(self):
        """return sql :class:`musicspell.Insert` to insert into database"""
        return Insert(self._tbl, self._kw)

class Director:
    """Directs scorebuilders

    Calls each build method for a specific builder

    """

    def build_entry(self, builder):
        """build method caller

        Args:
            builder (:obj:`AbstractBuilder`): builder from which build methods
            are called

        """
        builder.build_name()
        builder.build_composer()
