from musicspell.noteBuilder import *
from musicspell.command import Insert
import unittest
import music21.note as mn
import music21.chord as mc
import sqlite3

class TestBuilder(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_noteBuilder(self):
        noteBuilder = NoteBuilder('table', mn.Note())
        score = DataScore()
        score.buildEntry(noteBuilder)
        noteInsert = noteBuilder.getEntry()
        self.assertIsInstance(noteInsert, Insert)

    def test_chordBuilder(self):
        chordBuilder = ChordBuilder('table', mc.Chord())
        score = DataScore()
        score.buildEntry(chordBuilder)
        chordInsert = chordBuilder.getEntry()
        self.assertIsInstance(chordInsert, Insert)

if __name__ == "__main__":
    unittest.main()
