from musicspell.db import Db
from musicspell.command import Select, Insert, Command
from musicspell.compositeCommand import Union
import unittest
import sqlite3

class TestCompositeCommand(unittest.TestCase):

    """CompositeCommand test class"""

    def setUp(self):
        self.unionDb = Db('unionDb')
        self.unionDb['unionTable'] = dict(id = 'INTEGER')
        self.unionDb['unionTable2'] = dict(id = 'INTEGER')
        rowInsert = Insert('unionTable', id=1)
        rowInsert2 = Insert('unionTable2', id=2)
        self.unionDb.execute(rowInsert)
        self.unionDb.execute(rowInsert2)

    def tearDown(self):
        del self.unionDb

    def test_unionNotACommand(self):
        self.assertNotIsInstance(Union(), Command)

    def test_unionOneSelect(self):
        oneSelect = Select('unionTable', "id == 1")
        unionOneSelect = Union(oneSelect)
        rows = self.unionDb.execute(unionOneSelect)
        self.assertIsNotNone(rows)

    def test_unionTwoSelect(self):
        selectOne = Select('unionTable')
        selectTwo = Select('unionTable2')
        unionTwoSelect = Union(selectOne, selectTwo)
        rows = self.unionDb.execute(unionTwoSelect)
        self.assertEqual(len(rows), 2, msg=unionTwoSelect.getString() )

if __name__ == "__main__":
    unittest.main()
