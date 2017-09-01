from musicspell.noteVisitor import DataScore
import unittest
import music21.note as mn
import music21.chord as mc
import sqlite3

class TestDatascore(unittest.TestCase):
    """(musical) score-database test class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_note_visitor(self):
        self.score = DataScore()
        self.assertRaises(KeyError, self.score.accept, 'table', mn.Note())

    def test_chord_visitor(self):
        self.score = DataScore()
        self.assertRaises(KeyError, self.score.accept, 'table', mc.Chord())

if __name__ == "__main__":
    unittest.main()
