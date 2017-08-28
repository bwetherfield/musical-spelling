from musicspell.db import Db
from musicspell.command import Command, Insert, Select, Update, Delete
import unittest
import sqlite3

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        #test db
        self.myDb = Db()
        self.myDb['test'] = dict(id='int')
        # named db
        self.namedDb = Db('named')
        # loaded db
        _tempCon = sqlite3.connect('load.db')
        _tempCon.execute('DROP TABLE if exists testTable')
        _tempCon.execute('CREATE TABLE testTable(id int, other text)')
        _tempCon.execute('DROP TABLE if exists testTable2')
        _tempCon.execute('CREATE TABLE testTable2(id int)')
        _tempCon.execute('DROP TABLE if exists retrieveTester')
        _tempCon.execute('CREATE TABLE retrieveTester(id int)')
        _tempCon.execute('INSERT INTO retrieveTester VALUES (1)')
        _tempCon.commit()
        _tempCon.close()
        self.loadedDb = Db('load')

    def tearDown(self):
        del self.myDb
        del self.loadedDb
        del self.namedDb

    def test_loadDatabaseTableCheck(self):
        self.assertIn('testTable', self.loadedDb)
        self.assertIn('testTable2', self.loadedDb)

    def test_loadDatabaseCheckColumns(self):
        self.assertIn('id', self.loadedDb['testTable'].keys())
        self.assertEqual('int', self.loadedDb['testTable']['id'])
        self.assertEqual('text', self.loadedDb['testTable']['other'])

    def test_loadDatabaseBadColumn(self):
        self.assertRaises(KeyError, self.loadedDb['testTable'].__getitem__,
                          'notColumn')

    def test_loadDatabaseColumnBadType(self):
        self.assertNotEqual('notInt', self.loadedDb['testTable']['id'])

    def test_namedDatabase(self):
        self.assertIs(type(self.myDb), type(self.namedDb))

    def test_insertTable(self):
        self.myDb['setTable'] = { 'id' : 'INTEGER', 'other' : 'TEXT' }
        _tmpCon = sqlite3.connect('default.db')
        _tmpCur = _tmpCon.cursor()
        _tmpCur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = _tmpCur.fetchall()
        flag = False
        for row in rows:
            if row[0] == 'setTable':
                flag = True
        self.assertTrue(flag)

    def test_insertTableNonDict(self):
        self.assertRaises(TypeError, self.myDb.__setitem__, 'badTable', 'bad')

    def test_insertElt(self):
        myInsert = Insert('test', id=200)
        myDb.execute(myInsert)
        rows = self.myDb.retrieve('test', 'id == 200')
        self.assertIsNotNone(rows)

    def test_insertEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.insert, 'nonTable', id=2)

    def test_insertEltBadColumn(self):
        self.assertRaises(KeyError, self.myDb.insert, 'test', nonColumn=2)

    def test_insertEltNoKw(self):
        self.assertRaises(ValueError, self.myDb.insert, 'test')

    def test_retrieveBadTable(self):
        self.assertRaises(KeyError, self.myDb.retrieve, 'nonTable')

    def test_retrieveNoConditions(self):
        rows = self.loadedDb.retrieve('retrieveTester')
        self.assertIsNotNone(rows)
        for row in rows:
            self.assertEqual(row[0], 1)

    def test_retrieveBadConditions(self):
        rows = self.loadedDb.retrieve('retrieveTester', 'id == 4500')
        self.assertIsNone(rows)

    def test_retrieveGoodConditions(self):
        self.loadedDb.insert('testTable', id = 4500, other = "HELLO")
        rows = self.loadedDb.retrieve('testTable', "other == 'HELLO'")
        self.assertIsNotNone(rows)

    def test_amendEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.amend, 'nonTable', id=3)

    def test_amendElt(self):
        self.myDb.insert('test', id=1)
        self.myDb.amend('test', "id == 1", id=2)
        rows = self.myDb.retrieve('test', "id == 1")
        self.assertIsNone(rows)

    def test_amendNoKw(self):
        self.assertRaises(ValueError, self.myDb.amend, 'test', "id == 1")

    def test_deleteEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.delete, 'nonTable')

    def test_deleteAll(self):
        self.myDb.insert('test', id=300)
        # no conditions means delete all
        self.myDb.delete('test')
        rows = self.myDb.retrieve('test')
        self.assertIsNone(rows)

    def test_deleteConditional(self):
        self.myDb.insert('test', id = 200)
        self.myDb.insert('test', id = 100)
        self.myDb.delete('test', "id > 150")
        rows = self.myDb.retrieve('test', "id > 150")
        self.assertIsNone(rows)
        rows = self.myDb.retrieve('test', "id <= 150")
        self.assertIsNotNone(rows)

if __name__ == "__main__":
    unittest.main()