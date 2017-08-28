from musicspell.db import Db
from musicspell.command import Select, Insert, Command
from musicspell.compositeCommand import Union
import unittest
import sqlite3

class TestCompositeCommand(unittest.TestCase):

    """CompositeCommand test class"""

    def setUp(self):
        self.myDb = Db('unionDb')
        self.myDb['unionTable'] = dict(id = 'INTEGER')
        self.myDb['unionTable2'] = dict(id = 'INTEGER')
        rowInsert = Insert('unionTable', id=1)
        rowInsert = Insert('unionTable2', id=1)
        self.myDb.execute(rowInsert)

    def tearDown(self):
        pass

    def test_unionNotACommand(self):
        self.assertNotIsInstance(Union(), Command)

    def test_unionOneSelect(self):
        oneSelect = Select('unionTable', "id == 1")
        unionOneSelect = Union(oneSelect)
        rows = self.myDb.execute(unionOneSelect)
        self.assertIsNotNone(rows)

    def test_unionTwoSelect(self):
        selectOne = Select('unionTable', "id == 1")
        selectTwo = Select('unionTable', "id == 1")
        unionTwoSelect = Union(selectOne, selectTwo)
        rows = self.myDb.execute(unionTwoSelect)
        self.assertEqual(len(rows), 2)

if __name__ == "__main__":
    unittest.main()
