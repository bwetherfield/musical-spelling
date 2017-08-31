from musicspell.noteBuilder import Director, NoteBuilder, ChordBuilder
from musicspell.db import Db
import music21.note

class DataScore:
    """(musical) score abstraction on top of database"""

    def __init__(self, name='defaultScore'):
        self.director = Director()
        self.db = Db(name)

    def accept(self, tbl, scoreObj):
        """

        :param tbl: 
        :param scoreObj: 

        """
        if isinstance(scoreObj, music21.note.Note):
            builder = NoteBuilder(tbl, scoreObj)
        else:
            builder = ChordBuilder(tbl, scoreObj)
        self.director.buildEntry(builder)
        newEntry = builder.getEntry()
        self.db.execute(newEntry)
