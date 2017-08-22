import sqlite3

class Db(dict):

    """database handler"""

    def __init__(self, name = 'default'):
        """TODO: to be defined1. """
        self._name = name + '.db'
        self._conn = sqlite3.connect(self._name)
        self._c = self._conn.cursor()

        # for existing database, repopulate tables
        self._c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        rows = self._c.fetchall()
        # None indicates database is new... we are done
        if rows is not None:
            for row in rows:
                self[row[0]] = {}
                data = self._c.execute('PRAGMA table_info({})'.format(row[0]))
                for d in data:
                    self[row[0]].update({ d[1] : d[2] })

    def insert(self, tbl, **kwargs):
        """create / insert row into database
        :returns: TODO """
        if tbl in self:
            for k in kwargs:
                if k not in self[tbl]:
                    raise KeyError('{} not in table {}'.format(k, tbl))
                else:
                    ins = 'INSERT INTO {}'.format(tbl)
                    klist, wlist, qlist = [], [], []
                    for k in kwargs.keys():
                        klist.append(k)
                        wlist.append(kwargs[k])
                        qlist.append('?')
                    ks = ', '.join(klist)
                    ws = tuple(wlist)
                    qs = ', '.join(qlist)
                    ins = ins + '({})'.format(ks) + 'VALUES' + \
                            '({})'.format(qs)
                    self._c.execute(ins, ws)
                    return True
        else: raise KeyError('{} not in database'.format(tbl))

    def retrieve(self, tbl, *conditions):
        """retrieve row from database
        :returns: TODO """
        if tbl not in self:
            raise KeyError('{} not in database'.format(tbl))
        sel = 'SELECT * from {}'.format(tbl)
        if conditions != ():
            cond = ' AND '.join(conditions)
            sel = sel + ' WHERE ' + cond
        self._c.execute(sel)
        rows = self._c.fetchall()
        if rows == []: return None
        else: return rows

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
        if w != {}:
            self._c.execute('DROP TABLE IF EXISTS {}'.format(k))
            tmpList = []
            for wk in w.keys():
                tmpList.append(' '.join([wk, w[wk]]))
            s = ','.join(tmpList)
            self._c.execute('CREATE TABLE {}({})'.format(k, s))

    def __del__(self):
        """TODO: to be defined1. """
        self._conn.commit()
        self._conn.close()

