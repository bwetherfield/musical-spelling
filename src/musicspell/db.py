import sqlite3

class Db(dict):

    """database handler"""

    def __init__(self, name = 'default'):
        """TODO: to be defined1. """
        self._name = name + '.db'
        self._conn = sqlite3.connect(self._name)
        self._c = self._conn.cursor()

        # for existing database, repopulate tables
        self._c.row_factory = sqlite3.Row
        self._c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = self._c.fetchall()
        if rows is not None:
            for row in rows:
                self[row[0]] = dict(id='int')

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
        if not (isinstance(w, dict)):
            raise TypeError('Table must be of type dict')
        super().__setitem__(k, w)

    def __del__(self):
        """TODO: to be defined1. """
        self._conn.commit()
        self._conn.close()

