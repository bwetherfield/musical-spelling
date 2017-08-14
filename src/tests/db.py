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
        b = self.myDb.insert('nonTable',id=1)
        self.assertFalse(b)

    def test_insertEltBadColumn(self):
        b = self.myDb.insert('test',nonColumn=1)
        self.assertFalse(b)

if __name__ == "__main__":
    unittest.main()
