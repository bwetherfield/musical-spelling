from src.musicspell.notebuilder import NoteBuilder, ChordBuilder, Director
from src.musicspell.compositecommand import ManyCommand
from src.musicspell.command import Insert
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

    def test_note_builder(self):
        note_builder = NoteBuilder('table', mn.Note())
        self.director.build_entry(note_builder)
        note_insert = note_builder.get_entry()
        self.assertIsInstance(note_insert, Insert)

    def test_chord_builder(self):
        chord_builder = ChordBuilder('table', mc.Chord())
        self.director.build_entry(chord_builder)
        chord_insert = chord_builder.get_entry()
        self.assertIsInstance(chord_insert, ManyCommand)

if __name__ == "__main__":
    unittest.main()
