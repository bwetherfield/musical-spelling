from src.musicspell import db
import unittest

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        myDb = db.Db()

    def tearDown(self):
        del myDb

    def test_getTables(self):
        myDb.addTable("testTable")
        tables = myDb.getTables()
        self.assertEqual(tables,("testTable",))

if __name__ == "__main__":
    unittest.main()
