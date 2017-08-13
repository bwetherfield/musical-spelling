from musicspell.db import Db
import unittest

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setattr(self):
        myDb = Db()
        myDb.tables['test'] = dict(id='int')
        self.assertEqual(len(myDb.tables), 1)

if __name__ == "__main__":
    unittest.main()
