from musicspell.noteBuilder import *
from musicspell.command import Insert
import unittest
import music21.note as mn
import sqlite3

class TestBuilder(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_noteBuilder(self):
        noteBuilder = NoteBuilder(mn.Note())
        score = DataScore()
        score.buildEntry(noteBuilder)
        noteInsert = noteBuilder.getEntry()
        self.assertIsInstance(noteInsert, Insert)

if __name__ == "__main__":
    unittest.main()
