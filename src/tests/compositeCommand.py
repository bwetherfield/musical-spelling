from musicspell.db import Db
from musicspell.command import Select, Insert, Command
from musicspell.compositeCommand import Union
import unittest
import sqlite3

class TestCompositeCommand(unittest.TestCase):

    """CompositeCommand test class

    Uses non-oo implementation of db to test the oo-style commands
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unionNotACommand(self):
        self.assertNotIsInstance(Union(), Command)

    def test_unionOneSelect(self):
        self.myDb = Db('unionDb')
        self.myDb['unionTable'] = dict(id = 'INTEGER')
        rowInsert = Insert('unionTable', id=1)
        oneSelect = Select('unionTable', "id == 1")
        unionOneSelect = Union(oneSelect)
        self.myDb.execute(rowInsert)
        rows = self.myDb.execute(unionOneSelect)
        self.assertIsNotNone(rows)

if __name__ == "__main__":
    unittest.main()
