from musicspell.db import Db
from musicspell.command import Command, Insert, Select, Update, Delete
import unittest
import sqlite3

class TestCommand(unittest.TestCase):
    """Command test class

    Uses non-oo implementation of db to test the oo-style commands
    """

    def setUp(self):
        #test db
        self.my_db = Db()
        self.my_db['test'] = dict(id='int')
        # named db
        self.named_db = Db('named')
        # loaded db
        _temp_con = sqlite3.connect('load.db')
        _temp_con.execute('DROP TABLE if exists testTable')
        _temp_con.execute('CREATE TABLE testTable(id int, other text)')
        _temp_con.execute('DROP TABLE if exists testTable2')
        _temp_con.execute('CREATE TABLE testTable2(id int)')
        _temp_con.execute('DROP TABLE if exists selectTester')
        _temp_con.execute('CREATE TABLE selectTester(id int)')
        _temp_con.execute('INSERT INTO selectTester VALUES (1)')
        _temp_con.commit()
        _temp_con.close()
        self.loaded_db = Db('load')

    def tearDown(self):
        del self.my_db
        del self.loaded_db
        del self.named_db

    def test_load_database_table_check(self):
        self.assertIn('testTable', self.loaded_db)
        self.assertIn('testTable2', self.loaded_db)

    def test_load_database_check_columns(self):
        self.assertIn('id', self.loaded_db['testTable'].keys())
        self.assertEqual('int', self.loaded_db['testTable']['id'])
        self.assertEqual('text', self.loaded_db['testTable']['other'])

    def test_load_database_bad_column(self):
        self.assertRaises(KeyError, self.loaded_db['testTable'].__getitem__,
                          'notColumn')

    def test_load_database_column_bad_type(self):
        self.assertNotEqual('notInt', self.loaded_db['testTable']['id'])

    def test_named_database(self):
        self.assertIs(type(self.my_db), type(self.named_db))

    def test_insert_table(self):
        self.my_db['setTable'] = { 'id' : 'INTEGER', 'other' : 'TEXT' }
        _tmp_con = sqlite3.connect('default.db')
        _tmp_cur = _tmp_con.cursor()
        _tmp_cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = _tmp_cur.fetchall()
        flag = False
        for row in rows:
            if row[0] == 'setTable':
                flag = True
        self.assertTrue(flag)

    def test_insert_table_non_dict(self):
        self.assertRaises(TypeError, self.my_db.__setitem__, 'badTable', 'bad')

    def test_insert_elt(self):
        insertElt = Insert('test', id=200)
        self.my_db.execute(insertElt)
        rows = self.my_db.retrieve('test', 'id == 200')
        self.assertIsNotNone(rows)

    def test_insert_elt_bad_table(self):
        insert_elt_bad_table = Insert('nonTable', id=2)
        self.assertRaises(KeyError, self.my_db.execute, insert_elt_bad_table)

    def test_insert_elt_bad_column(self):
        insert_elt_bad_column = Insert('test', nonColumn=2)
        self.assertRaises(KeyError, self.my_db.execute, insert_elt_bad_column)

    def test_insert_elt_no_kw(self):
        insert_elt_no_kw = Insert('test')
        self.assertRaises(ValueError, self.my_db.execute, insert_elt_no_kw)

    def test_select_bad_table(self):
        select_bad_table = Select('nonTable')
        self.assertRaises(KeyError, self.my_db.execute, select_bad_table)

    def test_select_no_conditions(self):
        select_no_conditions = Select('selectTester')
        rows = self.loaded_db.execute(select_no_conditions)
        self.assertIsNotNone(rows)
        for row in rows:
            self.assertEqual(row[0], 1)

    def test_select_bad_conditions(self):
        select_bad_conditions = Select('selectTester', 'id == 4500')
        rows = self.loaded_db.execute(select_bad_conditions)
        self.assertIsNone(rows)

    def test_select_good_conditions(self):
        self.loaded_db.insert('testTable', id = 4500, other = "HELLO")
        select_good_conditions = Select('testTable', "other == 'HELLO'")
        rows = self.loaded_db.execute(select_good_conditions)
        self.assertIsNotNone(rows)

    def test_update_elt_bad_table(self):
        update_elt_bad_table = Update('nonTable', id=3)
        self.assertRaises(KeyError, self.my_db.execute, update_elt_bad_table)

    def test_update_elt(self):
        self.my_db.insert('test', id=1)
        update_elt = Update('test', "id == 1", id=2)
        self.my_db.execute(update_elt)
        rows = self.my_db.retrieve('test', "id == 1")
        self.assertIsNone(rows)

    def test_update_no_kw(self):
        update_no_kw = Update('test', "id == 1")
        self.assertRaises(ValueError, self.my_db.execute, update_no_kw)

    def test_delete_elt_bad_table(self):
        delete_elt_bad_table = Delete('nonTable')
        self.assertRaises(KeyError, self.my_db.execute, delete_elt_bad_table)

    def test_delete_all(self):
        self.my_db.insert('test', id=300)
        # no conditions means delete all
        delete_all = Delete('test')
        self.my_db.execute(delete_all)
        rows = self.my_db.retrieve('test')
        self.assertIsNone(rows)

    def test_delete_conditional(self):
        self.my_db.insert('test', id = 200)
        self.my_db.insert('test', id = 100)
        delete_conditional = Delete('test', "id > 150")
        self.my_db.execute(delete_conditional)
        rows = self.my_db.retrieve('test', "id > 150")
        self.assertIsNone(rows)
        rows = self.my_db.retrieve('test', "id <= 150")
        self.assertIsNotNone(rows)

if __name__ == "__main__":
    unittest.main()
