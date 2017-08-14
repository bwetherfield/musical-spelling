import sqlite3

class Db():

    """database handler"""

    def __init__(self):
        """TODO: to be defined1. """
        # self_conn = sqlite3.connect('default.db')
        # self._c = _conn.cursor()
        self.tables = {}

    def insert(self, tbl, **kwargs):
        """TODO: Docstring for insert.
        :returns: TODO

        """
        if tbl in self.tables:
            return True
