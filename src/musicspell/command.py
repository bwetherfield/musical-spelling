"""Object-Oriented implementation of sql commands that are called by databases
in a Visitor-like way

"""
from musicspell.db import Db

class Command:
    """base sql command

    Arguments:
        tbl: associated database table
        *conditions, optional: apply command to rows for which conditions are
            true
        **kwargs, optional: change rows with these column, value pairs

    Attributes:
        _cmdType: overridden attribute
        cmds: list containing self. This accommodates
            :method:`musicspell.db.Db.checkCmd` which checks commands contained
            in its parameter objects
        tbl: associated database table
        *conditions, optional: apply command to rows for which conditions are
            true
        **kwargs, optional: change rows with these column, value pairs
        _data: overridden attribute.
        _cmdStr: overridden attribute

    """

    _cmdType = None

    def __init__(self, tbl, *conditions, **kwargs):
        #hack for Command/CompositeCommand polymorphism
        self.cmds = [self]
        self.tbl = tbl
        self.conditions = conditions
        self.kwargs = kwargs
        self._data = None
        self._cmdStr = None

    def execute(self):
        """virtual method"""
        raise NotImplementedError

class Insert(Command):
    """concrete sql command INSERT. Extends `Command`.

    Attributes:
        _cmdType: "INSERT". Overrides :attribute:`Command._cmdType`

    """

    _cmdType = "INSERT"

    def getString(self):
        """Getter for explicit sql command and parameters

        Overrides `_data` to hold sql paramaters and `_cmdStr` to hold sql command.

        Returns:
            (str, str): tuple containing sql string and parameters

        """
        if self._cmdStr is None:
            tabStr = ' INTO {}'.format(self.tbl)
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
            self._cmdStr = self._cmdType + self._cmdStr
            self._data = ws
        return self._cmdStr, self._data

    def errorCheck(self):
        """command-specific error checking"""
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        """
        self.errorCheck()
        cmd, data = self.getString()
        cursor.execute(cmd, data)

class Select(Command):
    """concrete sql command SELECT. Extends `Command`.

    Attributes:
        _cmdType: "SELECT". Overrides :attribute:`Command._cmdType`

    """

    _cmdType = "SELECT"

    def getString(self):
        """Getter for explicit sql command"""
        if self._cmdStr is None:
            cmd = ' * from {}'.format(self.tbl)
            self._cmdStr = cmd
            if self.conditions != ():
                cond = ' AND '.join(self.conditions)
                self._cmdStr = cmd + ' WHERE ' + cond
            self._cmdStr = self._cmdType + self._cmdStr
        return self._cmdStr

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        Returns:
            [:obj:`sqlite3.Row`], optional: rows of the database associated
                with `cursor` that meet the conditions or None if there are
                nonesuch

        """
        cmd = self.getString()
        cursor.execute(cmd)
        rows = cursor.fetchall()
        if rows == []: return None
        else: return rows

class Update(Command):
    """concrete sql command UPDATE. Extends `Command`.

    Attributes:
        _cmdType: "UPDATE". Overrides :attribute:`Command._cmdType`

    """

    _cmdType = "UPDATE"

    def getString(self):
        """Getter for explicit sql command and parameters

        Overrides `_data` to hold sql paramaters and `_cmdStr` to hold sql command.

        Returns:
            (str, str): tuple containing sql string and parameters

        """
        cmd = ' {}'.format(self.tbl)
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
        self._cmdStr = self._cmdType + self._cmdStr
        self._data = ws
        return self._cmdStr, self._data

    def errorCheck(self):
        """command-specific error checking"""
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        """
        self.errorCheck()
        cmd, data = self.getString()
        cursor.execute(cmd, data)

class Delete(Command):
    """concrete sql command DELETE. Extends `Command`.

    Attributes:
        _cmdType: "DELETE". Overrides :attribute:`Command._cmdType`

    """

    _cmdType = "DELETE"

    def getString(self):
        """Getter for explicit sql command"""
        cmd = ' from {}'.format(self.tbl)
        self._cmdStr = cmd
        if self.conditions != ():
            cond = ' AND '.join(self.conditions)
            self._cmdStr = cmd + ' WHERE ' + cond
        self._cmdStr = self._cmdType + self._cmdStr
        return self._cmdStr

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        """
        cmd = self.getString()
        cursor.execute(cmd)
