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
        _tempCon.execute('DROP TABLE if exists selectTester')
        _tempCon.execute('CREATE TABLE selectTester(id int)')
        _tempCon.execute('INSERT INTO selectTester VALUES (1)')
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
        insertElt = Insert('test', id=200)
        self.myDb.execute(insertElt)
        rows = self.myDb.retrieve('test', 'id == 200')
        self.assertIsNotNone(rows)

    def test_insertEltBadTable(self):
        insertEltBadTable = Insert('nonTable', id=2)
        self.assertRaises(KeyError, self.myDb.execute, insertEltBadTable)

    def test_insertEltBadColumn(self):
        insertEltBadColumn = Insert('test', nonColumn=2)
        self.assertRaises(KeyError, self.myDb.execute, insertEltBadColumn)

    def test_insertEltNoKw(self):
        insertEltNoKw = Insert('test')
        self.assertRaises(ValueError, self.myDb.execute, insertEltNoKw)

    def test_selectBadTable(self):
        selectBadTable = Select('nonTable')
        self.assertRaises(KeyError, self.myDb.execute, selectBadTable)

    def test_selectNoConditions(self):
        selectNoConditions = Select('selectTester')
        check = selectNoConditions.getString()
        self.assertEqual(check, "* from selectTester", check)
        rows = self.loadedDb.execute(selectNoConditions)
        self.assertIsNotNone(rows)
        for row in rows:
            self.assertEqual(row[0], 1)

    def test_selectBadConditions(self):
        selectBadConditions = Select('selectTester', 'id == 4500')
        rows = self.loadedDb.execute(selectBadConditions)
        self.assertIsNone(rows)

    def test_selectGoodConditions(self):
        self.loadedDb.insert('testTable', id = 4500, other = "HELLO")
        selectGoodConditions = Select('testTable', "other == 'HELLO'")
        rows = self.loadedDb.execute(selectGoodConditions)
        self.assertIsNotNone(rows)

    def test_updateEltBadTable(self):
        updateEltBadTable = Update('nonTable', id=3)
        self.assertRaises(KeyError, self.myDb.execute, updateEltBadTable)

    def test_updateElt(self):
        self.myDb.insert('test', id=1)
        updateElt = Update('test', "id == 1", id=2)
        self.myDb.execute(updateElt)
        rows = self.myDb.retrieve('test', "id == 1")
        self.assertIsNone(rows)

    def test_updateNoKw(self):
        updateNoKw = Update('test', "id == 1")
        self.assertRaises(ValueError, self.myDb.execute, updateNoKw)

    def test_deleteEltBadTable(self):
        deleteEltBadTable = Delete('nonTable')
        self.assertRaises(KeyError, self.myDb.execute, deleteEltBadTable)

    def test_deleteAll(self):
        self.myDb.insert('test', id=300)
        # no conditions means delete all
        deleteAll = Delete('test')
        self.myDb.execute(deleteAll)
        rows = self.myDb.retrieve('test')
        self.assertIsNone(rows)

    def test_deleteConditional(self):
        self.myDb.insert('test', id = 200)
        self.myDb.insert('test', id = 100)
        deleteConditional = Delete('test', "id > 150")
        self.myDb.execute(deleteConditional)
        rows = self.myDb.retrieve('test', "id > 150")
        self.assertIsNone(rows)
        rows = self.myDb.retrieve('test', "id <= 150")
        self.assertIsNotNone(rows)

if __name__ == "__main__":
    unittest.main()
