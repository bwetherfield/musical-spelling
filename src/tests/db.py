from musicspell.db import Db
import unittest

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        self.myDb = Db()
        self.myDb['test'] = dict(id='int')

    def tearDown(self):
        del self.myDb

    def test_insertTable(self):
        self.assertEqual(len(self.myDb), 1)

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

    def test_deleteEltBadTable(self):
        self.assertRaises(KeyError, self.myDb.delete, 'nonTable')

if __name__ == "__main__":
    unittest.main()
