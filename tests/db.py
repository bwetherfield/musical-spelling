from src.musicspell.db import Db
import unittest
import sqlite3

class TestDb(unittest.TestCase):
    """Db test class"""

    def setUp(self):
        #test db
        self.my_db = Db()
        self.my_db['test'] = dict(id='int')
        # named db
        self.named_db = Db('named')
        # loaded db
        _temp_con = sqlite3.connect('src/sql/load.db')
        _temp_con.execute('DROP TABLE if exists testTable')
        _temp_con.execute('CREATE TABLE testTable(id int, other text)')
        _temp_con.execute('DROP TABLE if exists testTable2')
        _temp_con.execute('CREATE TABLE testTable2(id int)')
        _temp_con.execute('DROP TABLE if exists retrieveTester')
        _temp_con.execute('CREATE TABLE retrieveTester(id int)')
        _temp_con.execute('INSERT INTO retrieveTester VALUES (1)')
        _temp_con.commit()
        _temp_con.close()
        self.loaded_db = Db('load')

    def TearDown(self):
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
        b = self.my_db.insert('test',id=200)
        self.assertTrue(b)
        rows = self.my_db.retrieve('test', 'id == 200')
        self.assertIsNotNone(rows)

    def test_insert_elt_bad_table(self):
        self.assertRaises(KeyError, self.my_db.insert, 'nonTable', id=2)

    def test_insert_elt_bad_column(self):
        self.assertRaises(KeyError, self.my_db.insert, 'test', nonColumn=2)

    def test_insert_elt_no_kw(self):
        self.assertRaises(ValueError, self.my_db.insert, 'test')

    def test_retrieve_bad_table(self):
        self.assertRaises(KeyError, self.my_db.retrieve, 'nonTable')

    def test_retrieve_no_conditions(self):
        rows = self.loaded_db.retrieve('retrieveTester')
        self.assertIsNotNone(rows)
        for row in rows:
            self.assertEqual(row[0], 1)

    def test_retrieve_bad_conditions(self):
        rows = self.loaded_db.retrieve('retrieveTester', 'id == 4500')
        self.assertIsNone(rows)

    def test_retrieve_good_conditions(self):
        self.loaded_db.insert('testTable', id = 4500, other = "HELLO")
        rows = self.loaded_db.retrieve('testTable', "other == 'HELLO'")
        self.assertIsNotNone(rows)

    def test_amend_elt_bad_table(self):
        self.assertRaises(KeyError, self.my_db.amend, 'nonTable', id=3)

    def test_amend_elt(self):
        self.my_db.insert('test', id=1)
        self.my_db.amend('test', "id == 1", id=2)
        rows = self.my_db.retrieve('test', "id == 1")
        self.assertIsNone(rows)

    def test_amend_no_kw(self):
        self.assertRaises(ValueError, self.my_db.amend, 'test', "id == 1")

    def test_delete_elt_bad_table(self):
        self.assertRaises(KeyError, self.my_db.delete, 'nonTable')

    def test_delete_all(self):
        self.my_db.insert('test', id=300)
        # no conditions means delete all
        self.my_db.delete('test')
        rows = self.my_db.retrieve('test')
        self.assertIsNone(rows)

    def test_delete_conditional(self):
        self.my_db.insert('test', id = 200)
        self.my_db.insert('test', id = 100)
        self.my_db.delete('test', "id > 150")
        rows = self.my_db.retrieve('test', "id > 150")
        self.assertIsNone(rows)
        rows = self.my_db.retrieve('test', "id <= 150")
        self.assertIsNotNone(rows)

if __name__ == "__main__":
    unittest.main()
