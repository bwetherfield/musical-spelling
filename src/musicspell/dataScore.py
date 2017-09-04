"""Music score object that uses database and entry-builders

Todo:
    * Rename accept as enter
    * Change module name to lowercase

"""
from src.musicspell.notebuilder import Director, NoteBuilder, ChordBuilder
from src.musicspell.db import Db
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

    def accept(self, tbl, score_obj):
        """Add supplied (non-sql-style) object to the database

        Args:
          tbl: database table to insert into
          score_obj: basis of row creation (:obj:`music21.note.Note` or
              :obj:`music21.chord.Chord`)

        """
        if isinstance(score_obj, music21.note.Note):
            builder = NoteBuilder(tbl, score_obj)
        else:
            builder = ChordBuilder(tbl, score_obj)
        self.director.build_entry(builder)
        new_entry = builder.get_entry()
        self.db.execute(new_entry)
