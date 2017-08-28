from db import Db

class Command:

    """base sql command"""

    self._cmdType = None

    def __init__(self, tbl, *conditions, **kwargs):
        self.tbl = tbl
        self.conditions = conditions
        self.kwargs = kwargs
        self._data = None
        self._cmdStr = None

    def errorCheck(self, db=None):
        if db is None:
            raise ValueError('Supply a database')
        elif self.tbl not in db:
            raise KeyError('{} not in database'.format(tbl))

    def execute(self):
        raise NotImplementedError

class Insert(Command):

    """concrete sql command INSERT"""

    self._cmdType = "INSERT"

    def getString(self):
        if self._cmdStr is None:
            tabStr = 'INTO {}'.format(tbl)
            klist, wlist, qlist = [], [], []
            for k in kwargs.keys():
                klist.append(k)
                wlist.append(kwargs[k])
                qlist.append('?')
            ks = ', '.join(klist)
            ws = tuple(wlist)
            qs = ', '.join(qlist)
            self._cmdStr = tabStr + '({})'.format(ks) + 'VALUES' + \
                    '({})'.format(qs)
            self._data = ws
        return self._cmdStr, self._data

    def errorCheck(self):
        super.errorCheck()
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')
        for k in kwargs:
            if k not in db[tbl]:
                raise KeyError('{} not in table {}'.format(k, tbl))

    def execute(self, db=None):
        cmd, data = self.getString()
        cmd = self._cmdType + " " + cmd
        db.execute(cmd, data)

class Select(Command):

    """concrete sql command SELECT"""

    self._cmdType = "SELECT"

    def getString(self):
        if self._cmdStr is None:
            cmd = '* from {}'.format(tbl)
            if self.conditions != ():
                cond = ' AND '.join(self.conditions)
                self._cmdStr = cmd + ' WHERE ' + cond
        return self._cmdStr

    def errorCheck(self):
        super.errorCheck()

    def execute(self, db=None):
        cmd = self.getString()
        cmd = self._cmdType + " " + cmd
        db._c.execute(cmd)
        rows = db._c.fetchall()
        if rows == []: return None
        else: return rows

class Update(Command):

    """concrete sql command UPDATE"""

    self._cmdType = "UPDATE"

    def getString(self):
        cmd = '{}'.format(tbl)
        ksubs, wlist = [], []
        for k in kwargs.keys():
            ksubs.append('{} = ?'.format(k))
            wlist.append(kwargs[k])
        ks = ' SET ' + ', '.join(ksubs)
        ws = tuple(wlist)
        if conditions != ():
            conds = ' WHERE ' + ' AND '.join(conditions)
        else: conds = ''
        self._cmdStr = cmd + ks + conds
        self._data = ws
        return self._cmdStr, self._data

    def errorCheck(self):
        super.errorCheck()
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, db=None):
        self.errorCheck()
        cmd, data = self.getString()
        cmd = self._cmdType + " " + cmd
        db.execute(cmd, data)
