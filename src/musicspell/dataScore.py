"""Music score object that uses database and entry-builders

Todo:
    * Add method docstrings

"""
from musicspell.noteBuilder import Director, NoteBuilder, ChordBuilder
from musicspell.db import Db
import music21.note

class DataScore:
    """(musical) score abstraction on top of database

    Arguments:
        name (str): name of .db file without .db suffix (holds database).
            Defaults to 'defaultScore'

    Attributes:
        director (:class:`musicspell.noteBuilder.Director): directs row
            creation
        db: :mod:`sqlite3` database which stores note from musical score

        """

    def __init__(self, name='defaultScore'):
        self.director = Director()
        self.db = Db(name)

    def accept(self, tbl, scoreObj):
        """

        Args:
          tbl: param scoreObj:
          scoreObj: 

        Returns:

        """
        if isinstance(scoreObj, music21.note.Note):
            builder = NoteBuilder(tbl, scoreObj)
        else:
            builder = ChordBuilder(tbl, scoreObj)
        self.director.buildEntry(builder)
        newEntry = builder.getEntry()
        self.db.execute(newEntry)
