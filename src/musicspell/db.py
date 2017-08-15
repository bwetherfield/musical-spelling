import sqlite3

class Db(dict):

    """database handler"""

    def __init__(self):
        """TODO: to be defined1. """
        # self_conn = sqlite3.connect('default.db')
        # self._c = _conn.cursor()

    def insert(self, tbl, **kwargs):
        """create / insert row into database
        :returns: TODO """
        if tbl in self:
            for k in kwargs:
                if k not in self[tbl]:
                    raise KeyError('{} not in table {}'.format(k, tbl))
                else: return True
        else: raise KeyError('{} not in database'.format(tbl))

    def retrieve(self, tbl, *conditions):
        """retrieve row from database
        :returns: TODO """
        if tbl not in self:
            raise KeyError('{} not in database'.format(tbl))
        return {}

    def amend(self, tbl, *conditions, **kwargs):
        """amend / update row in database
        :returns: TODO """
        if tbl not in self:
            raise KeyError('{} not in database'.format(tbl))

    def delete(self, tbl, *conditions):
        """delete row from database
        :returns: TODO """
        if tbl not in self:
            raise KeyError('{} not in database'.format(tbl))

    def __setitem__(self, k, w):
        """TODO: Docstring for __setitem__.
        :returns: TODO

        """
        super().__setitem__(k, w)
