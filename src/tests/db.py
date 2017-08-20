from musicspell.db import Db
import unittest

import sqlite3

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        self.myDb = Db()
        self.myDb['test'] = dict(id='int')
        # loaded db
        _tempCon = sqlite3.connect('load.db')
        _tempCon.execute('DROP TABLE if exists testTable')
        _tempCon.execute('CREATE TABLE testTable(id int)')
        _tempCon.execute('DROP TABLE if exists testTable2')
        _tempCon.execute('CREATE TABLE testTable2(id int)')
        _tempCon.commit()
        _tempCon.close()
        self.loadedDb = Db('load')

    def tearDown(self):
        del self.myDb
        del self.loadedDb

    def test_loadDatabaseTableCheck(self):
        self.assertIn('testTable', self.loadedDb)
        self.assertIn('testTable2', self.loadedDb)

    def test_namedDatabase(self):
        self.namedDb = Db('named')
        self.assertIs(type(self.myDb), type(self.namedDb))

    def test_insertTable(self):
        self.assertEqual(len(self.myDb), 1)

    def test_insertTableNonDict(self):
        self.assertRaises(TypeError, self.myDb.__setitem__, 'badTable', 'bad')

    def test_insertElt(self):
        b = self.myDb.insert('test',id=1)
        self.assertTrue(b)

    def test_insertEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.insert, 'nonTable', id=2)

    def test_insertEltBadColumn(self):
        self.assertRaises(KeyError, self.myDb.insert, 'test', nonColumn=2)

    def test_retrieveBadTable(self):
        self.assertRaises(KeyError, self.myDb.retrieve, 'nonTable')

    def test_amendEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.amend, 'nonTable', id=3)

    def test_amendElt(self):
        self.myDb.insert('test', id=1)
        self.myDb.amend('test', "id = 1", id=2)
        self.assertEqual(len(self.myDb.retrieve('test', "id = 1")), 0)

    def test_deleteEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.delete, 'nonTable')

if __name__ == "__main__":
    unittest.main()
