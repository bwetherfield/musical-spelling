from musicspell.noteBuilder import *
from musicspell.command import Insert
import unittest
import music21.note as mn
import music21.chord as mc
import sqlite3

class TestVisitor(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_noteVisitor(self):
        self.score = DataScore()
        noteVisitor = NoteBuilder('table', mn.Note())
        self.assertRaises(KeyError, self.score.accept, noteVisitor)

if __name__ == "__main__":
    unittest.main()
