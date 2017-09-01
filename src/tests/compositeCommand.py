from musicspell.db import Db
from musicspell.command import Select, Insert, Command
from musicspell.compositeCommand import Union
import unittest
import sqlite3

class TestCompositeCommand(unittest.TestCase):
    """CompositeCommand test class"""

    def setUp(self):
        self.union_db = Db('unionDb')
        self.union_db['unionTable'] = dict(id = 'INTEGER')
        self.union_db['unionTable2'] = dict(id = 'INTEGER')
        row_insert = Insert('unionTable', id=1)
        row_insert2 = Insert('unionTable2', id=2)
        self.union_db.execute(row_insert)
        self.union_db.execute(row_insert2)

    def tearDown(self):
        del self.union_db

    def test_union_not_a_command(self):
        self.assertNotIsInstance(Union(), Command)

    def test_union_one_select(self):
        one_select = Select('unionTable', "id == 1")
        union_one_select = Union(one_select)
        rows = self.union_db.execute(union_one_select)
        self.assertIsNotNone(rows)

    def test_union_two_select(self):
        select_one = Select('unionTable')
        select_two = Select('unionTable2')
        union_two_select = Union(select_one, select_two)
        rows = self.union_db.execute(union_two_select)
        self.assertEqual(len(rows), 2, msg=union_two_select.get_string() )

if __name__ == "__main__":
    unittest.main()
