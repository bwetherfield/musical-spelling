from musicspell.noteBuilder import Director, NoteBuilder, ChordBuilder
from musicspell.db import Db
import music21.note

class DataScore:
    def __init__(self, name='default'):
        self.director = Director()
        self.db = Db(name)

    def accept(self, tbl, scoreObj):
        if isinstance(scoreObj, music21.note.Note):
            builder = NoteBuilder(tbl, scoreObj)
        else:
            builder = ChordBuilder(tbl, scoreObj)
        self.director.buildEntry(builder)
        newEntry = builder.getEntry()
        self.db.execute(newEntry)

