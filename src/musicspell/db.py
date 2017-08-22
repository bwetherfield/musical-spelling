import sqlite3

class Db(dict):

    """database handler"""

    def __init__(self, name = 'default'):
        """Connect to database with default name default.db
        
        Argument: pass in name without .db suffix
        Reads in table names and columns from pre-existing db automatically"""
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
        """Insert row into database"""
        if kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')
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
        """select rows that satisfy conditions from database"""
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
        """Update contents of rows that satisfy conditions in database"""
        if tbl not in self:
            raise KeyError('{} not in database'.format(tbl))
        if kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')
        upd = 'UPDATE {}'.format(tbl)
        ksubs, wlist = [], []
        for k in kwargs.keys():
            ksubs.append('{} = ?'.format(k))
            wlist.append(kwargs[k])
        ks = ' SET ' + ', '.join(ksubs)
        ws = tuple(wlist)
        if conditions != ():
            conds = ' WHERE ' + ' AND '.join(conditions)
        else: conds = ''
        upd = upd + ks + conds
        self._c.execute(upd, ws)

    def delete(self, tbl, *conditions):
        """Delete rows  that satisfy conditions from database"""
        if tbl not in self:
            raise KeyError('{} not in database'.format(tbl))
        dels = 'DELETE from {}'.format(tbl)
        if conditions != ():
            cond = ' AND '.join(conditions)
            dels = dels + ' WHERE ' + cond
        self._c.execute(dels)

    def __setitem__(self, k, w):
        """Add table to database. Extends dict.__setitem__()"""
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
        """Commit database changes and close database before deletion"""
        self._conn.commit()
        self._conn.close()

