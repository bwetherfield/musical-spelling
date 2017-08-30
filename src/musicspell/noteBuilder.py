from musicspell.command import Insert

class NoteBuilder:
    def __init__(self, mn):
        self._mn = mn
        self._kw = {}

    def getEntry(self):
        return Insert('table', self._kw)

    def build_id(self):
        self._kw['id'] = self._mn.id

class DataScore:
    def buildEntry(self, builder):
        builder.build_id()
