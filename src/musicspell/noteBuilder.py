from musicspell.command import Insert
from musicspell.compositeCommand import ManyCommand

class AbstractBuilder:

    """abstract database-entry builder

    unimplemented methods do not raise exceptions so as to allow inheriting
    classes to pick and choose which parts to build"""

    def build_id(self): pass

class NoteBuilder(AbstractBuilder):

    """note database-entry builder

    use to build a row entry from a music21 note"""

    def __init__(self, tbl,  m21n):
        self._tbl = tbl
        self._m21n = m21n
        self._kw = {}

    def getEntry(self):
        return Insert(self._tbl, self._kw)

    def build_id(self):
        self._kw['id'] = self._m21n.id

class ChordBuilder(AbstractBuilder):

    """chord database-entry builder

    use to build a row entry from a music21 chord"""

    def __init__(self, tbl,  m21c):
        self._tbl = tbl
        self._m21c = m21c
        self._kw = {}

    def getEntry(self):
        idInsert = Insert(self._tbl, self._kw)
        return ManyCommand(idInsert)

    def build_id(self):
        self._kw['id'] = self._m21c.id

class Director:

    """Directs builders

    calls each build method for a specific builder"""

    def buildEntry(self, builder):
        builder.build_id()
