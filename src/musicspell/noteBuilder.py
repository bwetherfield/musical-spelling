from musicspell.command import Insert
from musicspell.compositeCommand import ManyCommand

class NoteBuilder:
    def __init__(self, tbl,  m21n):
        self._tbl = tbl
        self._m21n = m21n
        self._kw = {}

    def getEntry(self):
        return Insert(self._tbl, self._kw)

    def build_id(self):
        self._kw['id'] = self._m21n.id

class ChordBuilder:
    def __init__(self, tbl,  m21c):
        self._tbl = tbl
        self._m21c = m21c
        self._kw = {}

    def getEntry(self):
        idInsert = Insert(self._tbl, self._kw)
        return ManyCommand(idInsert)

    def build_id(self):
        self._kw['id'] = self._m21c.id

class DataScore:
    def buildEntry(self, builder):
        builder.build_id()
