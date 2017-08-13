from musicspell.db import Db
import unittest

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        myDb = Db()

    def tearDown(self):
        del myDb

    def test_insertTable(self):
        myDb.tables['test'] = dict(id='int')
        self.assertEqual(len(myDb.tables), 1)

if __name__ == "__main__":
    unittest.main()
