import sqlite3

class Db(dict):

    """database handler"""

    def __init__(self):
        """TODO: to be defined1. """
        # self_conn = sqlite3.connect('default.db')
        # self._c = _conn.cursor()

    def insert(self, tbl, **kwargs):
        """TODO: Docstring for insert.
        :returns: TODO

        """
        if tbl in self:
            for k in kwargs:
                if k not in self[tbl]:
                    return False
                else: return True

    def __setitem__(self, k, w):
        """TODO: Docstring for __setitem__.
        :returns: TODO

        """
        super().__setitem__(k, w)
