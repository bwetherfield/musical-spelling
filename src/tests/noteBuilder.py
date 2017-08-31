from musicspell.noteBuilder import *
from musicspell.command import Insert
import unittest
import music21.note as mn
import music21.chord as mc
import sqlite3

class TestBuilder(unittest.TestCase):
    """database-entry builder test class"""

    def setUp(self):
        self.director = Director()

    def tearDown(self):
        pass

    def test_noteBuilder(self):
        noteBuilder = NoteBuilder('table', mn.Note())
        self.director.buildEntry(noteBuilder)
        noteInsert = noteBuilder.getEntry()
        self.assertIsInstance(noteInsert, Insert)

    def test_chordBuilder(self):
        chordBuilder = ChordBuilder('table', mc.Chord())
        self.director.buildEntry(chordBuilder)
        chordInsert = chordBuilder.getEntry()
        self.assertIsInstance(chordInsert, ManyCommand)

if __name__ == "__main__":
    unittest.main()
