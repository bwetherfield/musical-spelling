from musicspell.command import Insert
from musicspell.compositeCommand import ManyCommand

class AbstractBuilder:
    """abstract database-entry builder

    unimplemented methods do not raise exceptions so as to allow inheriting
    classes to pick and choose which parts to build

    """

    def build_id(self): pass

class NoteBuilder(AbstractBuilder):
        """note database-entry builder

        use to build a row entry from a music21 note

        Args:
            tbl (str): name of table where entries will be inserted
            m21n (:obj:`music21.note.Note): contains note information

        Attributes:
            _tbl (str): name of table where entries will be inserted
            _m21n (:obj:`music21.note.Note): contains note information
            _kw (dict): column, value pairs for entry in database

        """

    def __init__(self, tbl,  m21n):
        self._tbl = tbl
        self._m21n = m21n
        self._kw = {}

    def getEntry(self):
        """return sql :class:`musicspell.Insert` to insert into database"""
        return Insert(self._tbl, self._kw)

    def build_id(self):
        """ """
        self._kw['id'] = self._m21n.id

class ChordBuilder(AbstractBuilder):
    """chord database-entry builder

    use to build a row entry from a music21 chord

    Args:
        tbl (str): name of table where entries will be inserted
        m21c (:obj:`music21.chord.Chord): contains chord information

    Attributes:
        _tbl (str): name of table where entries will be inserted
        _m21c (:obj:`music21.chord.Chord): contains chord information
        _kw (dict): column, value pairs for entry in database

    """

    def __init__(self, tbl,  m21c):
        self._tbl = tbl
        self._m21c = m21c
        self._kw = {}

    def getEntry(self):
        """return sql :class:`musicspell.Insert` to insert into database"""
        idInsert = Insert(self._tbl, self._kw)
        return ManyCommand(idInsert)

    def build_id(self):
        """ """
        self._kw['id'] = self._m21c.id

class Director:
    """Directs builders

    calls each build method for a specific builder

    """

    def buildEntry(self, builder):
        """build method caller

        Args:
            builder (:obj:`AbstractBuilder`): builder from which build methods
            are called

        """
        builder.build_id()
