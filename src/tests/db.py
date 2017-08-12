from ..musicspell import db
import unittest

class TestDb(unittest.TestCase):

    """Db test class"""

    def setUp(self):
        myDb = db.Db()

    def tearDown(self):
        del myDb

    def test_setattr(self):
        # myDb.addTable("testTable")
        # tables = myDb.getTables()
        # self.assertEqual(tables,("testTable",))
        myDb.testTable = dict("id"="int")
        self.assertEqual(myDb.testTable,(id,))

if __name__ == "__main__":
    unittest.main()
