"""Database handler module

Implements interface to an sqlite3 database

Todo:
    * Implement KeyError exception for Amend method when a key in `kwargs` is not
        a column of table `tbl`

"""

import sqlite3

class Db(dict):
    """Database handler

    Extends dict. Stores table name and column/type data as a dict.

    Args:
        name (str): name of .db file without suffix. Defaults to 'default'

    Attributes:
        _name (str): full name of .db file
        _conn: sqlite3 connection
        _c: sqlite3 cursor from _conn connection

        """

    def __init__(self, name = 'default'):
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

    def cmd_check(self, cmd):
        """Do database specific error checking on supplied command

        Args:
            cmd (:obj:`musicspell.Command`): command checked against this
                database

        """
        if cmd.tbl not in self:
            raise KeyError('{} not in database'.format(cmd.tbl))
        for k in cmd.kwargs:
            if k not in self[cmd.tbl]:
                raise KeyError('{} is not a valid column of {}'.format(k, cmd.tbl))

    def execute (self, cmd):
        """Execute supplied sql command in this database

        cmd acts in a Visitor-like way.

        Args:
            cmd: sql command to be executed. (Works with
                :class:`musicspell.Command` and :class:`musicspell.ManyCommand`
                objects)

        Returns (:obj:`sqlite3.Row`, optional): the return value passed from the command execution

        """
        for c in cmd.cmds:
            self.cmd_check(c)
        return cmd.execute(self._c)

    def insert(self, tbl, **kwargs):
        """Insert row into database

        Args:
            tbl: table to be inserted into
            **kwargs: column, value pairs

        Returns:
            bool: True if successful

        Raises:
            ValueError: if `kwargs` is empty
            KeyError: if a key in `kwargs` is not a column in table `tbl`

        """
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
        """Select row from database

        Args:
            tbl: table to be inserted into
            *conditions: retrieval conditions (sql)

        Returns:
            [:obj:`sqlite3.Row`], optional: returns matching rows or None if
                there are none

        Raises:
            KeyError: If table `tbl` is not in the database

        """

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
        """Update contents of rows that satisfy conditions in database

        Args:
            tbl: table to update
            *conditions: update where these conditions are met (sql)
            **kwargs: column, value pairs to insert where conditions are met

        Raises:
            KeyError: if a key in `kwargs` is not a column in table `tbl`
            KeyError: if table `tbl` is not in database
            ValueError: if `kwargs` is empty

        """
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
        """Delete rows  that satisfy conditions from database

        Args:
          tbl: table to delete rows from
          *conditions: delete rows for which these conditions are met (sql)

        Raises:
            KeyError: if table `tbl` is not in database

        """
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
