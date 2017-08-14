from musicspell.db import Db
import unittest

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        self.myDb = Db()
        self.myDb.tables['test'] = dict(id='int')

    def tearDown(self):
        del self.myDb

    def test_insertTable(self):
        self.assertEqual(len(self.myDb.tables), 1)

    def test_insertElt(self):
        b = self.myDb.insert('test',id=1)
        self.assertTrue(b)

if __name__ == "__main__":
    unittest.main()
