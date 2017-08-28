from musicspell.db import Db

class Command:

    """base sql command"""

    self._cmdType = None

    def __init__(self, tbl, *conditions, **kwargs):
        self.tbl = tbl
        self.conditions = conditions
        self.kwargs = kwargs
        self._data = None
        self._cmdStr = None

    def execute(self):
        raise NotImplementedError

class Insert(Command):

    """concrete sql command INSERT"""

    self._cmdType = "INSERT"

    def getString(self):
        if self._cmdStr is None:
            tabStr = 'INTO {}'.format(self.tbl)
            klist, wlist, qlist = [], [], []
            for k in self.kwargs.keys():
                klist.append(k)
                wlist.append(self.kwargs[k])
                qlist.append('?')
            ks = ', '.join(klist)
            ws = tuple(wlist)
            qs = ', '.join(qlist)
            self._cmdStr = tabStr + '({})'.format(ks) + 'VALUES' + \
                    '({})'.format(qs)
            self._data = ws
        return self._cmdStr, self._data

    def errorCheck(self):
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, cursor):
        self.errorCheck()
        cmd, data = self.getString()
        cmd = self._cmdType + " " + cmd
        cursor.execute(cmd, data)

class Select(Command):

    """concrete sql command SELECT"""

    self._cmdType = "SELECT"

    def getString(self):
        if self._cmdStr is None:
            cmd = '* from {}'.format(self.tbl)
            if self.conditions != ():
                cond = ' AND '.join(self.conditions)
                self._cmdStr = cmd + ' WHERE ' + cond
        return self._cmdStr

    def execute(self, cursor):
        cmd = self.getString()
        cmd = self._cmdType + " " + cmd
        cursor.execute(cmd)
        rows = cursor.fetchall()
        if rows == []: return None
        else: return rows

class Update(Command):

    """concrete sql command UPDATE"""

    self._cmdType = "UPDATE"

    def getString(self):
        cmd = '{}'.format(self.tbl)
        ksubs, wlist = [], []
        for k in self.kwargs.keys():
            ksubs.append('{} = ?'.format(k))
            wlist.append(self.kwargs[k])
        ks = ' SET ' + ', '.join(ksubs)
        ws = tuple(wlist)
        if self.conditions != ():
            conds = ' WHERE ' + ' AND '.join(self.conditions)
        else: conds = ''
        self._cmdStr = cmd + ks + conds
        self._data = ws
        return self._cmdStr, self._data

    def errorCheck(self):
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, cursor):
        self.errorCheck()
        cmd, data = self.getString()
        cmd = self._cmdType + " " + cmd
        cursor.execute(cmd, data)

class Delete(Command):

    """concrete sql command DELETE"""

    self._cmdType = "DELETE"

    def getString(self):
        cmd = 'from {}'.format(self.tbl)
        if self.conditions != ():
            cond = ' AND '.join(self.conditions)
            self._cmdStr = cmd + ' WHERE ' + cond

    def execute(self, cursor):
        cmd = self.getString()
        cmd = self._cmdType + " " + cmd
        cursor.execute(cmd)
