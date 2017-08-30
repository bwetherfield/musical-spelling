from musicspell.noteVisitor import DataScore
import unittest
import music21.note as mn
import sqlite3

class TestVisitor(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_noteVisitor(self):
        self.score = DataScore()
        self.assertRaises(KeyError, self.score.accept, 'table', mn.Note())

    def test_chordVisitor(self):
        self.score = DataScore()
        self.assertRaises(KeyError, self.score.accept, 'table', mc.Chord())

if __name__ == "__main__":
    unittest.main()