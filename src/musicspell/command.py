"""Object-Oriented implementation of sql commands that are called by databases
in a Visitor-like way

"""
from src.musicspell.db import Db

class Command:
    """base sql command

    Arguments:
        tbl: associated database table
        *conditions, optional: apply command to rows for which conditions are
            true
        **kwargs, optional: change rows with these column, value pairs

    Attributes:
        _cmd_type: overridden attribute
        cmds: list containing self. This accommodates
            :method:`musicspell.db.Db.checkCmd` which checks commands contained
            in its parameter objects
        tbl: associated database table
        *conditions, optional: apply command to rows for which conditions are
            true
        **kwargs, optional: change rows with these column, value pairs
        _data: overridden attribute.
        _cmd_str: overridden attribute

    """

    _cmd_type = None

    def __init__(self, tbl, *conditions, **kwargs):
        #hack for Command/CompositeCommand polymorphism
        self.cmds = [self]
        self.tbl = tbl
        self.conditions = conditions
        self.kwargs = kwargs
        self._data = None
        self._cmd_str = None

    def execute(self):
        """virtual method"""
        raise NotImplementedError

class Insert(Command):
    """concrete sql command INSERT. Extends `Command`.

    Attributes:
        _cmd_type: "INSERT". Overrides :attribute:`Command._cmd_type`

    """

    _cmd_type = "INSERT"

    def get_string(self):
        """Getter for explicit sql command and parameters

        Overrides `_data` to hold sql paramaters and `_cmd_str` to hold sql command.

        Returns:
            (str, str): tuple containing sql string and parameters

        """
        if self._cmd_str is None:
            tabStr = ' INTO {}'.format(self.tbl)
            klist, wlist, qlist = [], [], []
            for k in self.kwargs.keys():
                klist.append(k)
                wlist.append(self.kwargs[k])
                qlist.append('?')
            ks = ', '.join(klist)
            ws = tuple(wlist)
            qs = ', '.join(qlist)
            self._cmd_str = tabStr + '({})'.format(ks) + 'VALUES' + \
                    '({})'.format(qs)
            self._cmd_str = self._cmd_type + self._cmd_str
            self._data = ws
        return self._cmd_str, self._data

    def error_check(self):
        """command-specific error checking"""
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        """
        self.error_check()
        cmd, data = self.get_string()
        cursor.execute(cmd, data)

class Select(Command):
    """concrete sql command SELECT. Extends `Command`.

    Attributes:
        _cmd_type: "SELECT". Overrides :attribute:`Command._cmd_type`

    """

    _cmd_type = "SELECT"

    def get_string(self):
        """Getter for explicit sql command"""
        if self._cmd_str is None:
            cmd = ' * from {}'.format(self.tbl)
            self._cmd_str = cmd
            if self.conditions != ():
                cond = ' AND '.join(self.conditions)
                self._cmd_str = cmd + ' WHERE ' + cond
            self._cmd_str = self._cmd_type + self._cmd_str
        return self._cmd_str

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
        cmd = self.get_string()
        cursor.execute(cmd)
        rows = cursor.fetchall()
        if rows == []: return None
        else: return rows

class Update(Command):
    """concrete sql command UPDATE. Extends `Command`.

    Attributes:
        _cmd_type: "UPDATE". Overrides :attribute:`Command._cmd_type`

    """

    _cmd_type = "UPDATE"

    def get_string(self):
        """Getter for explicit sql command and parameters

        Overrides `_data` to hold sql paramaters and `_cmd_str` to hold sql command.

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
        self._cmd_str = cmd + ks + conds
        self._cmd_str = self._cmd_type + self._cmd_str
        self._data = ws
        return self._cmd_str, self._data

    def error_check(self):
        """command-specific error checking"""
        if self.kwargs == {}:
            raise ValueError('column, entry pairs needed to amend database')

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        """
        self.error_check()
        cmd, data = self.get_string()
        cursor.execute(cmd, data)

class Delete(Command):
    """concrete sql command DELETE. Extends `Command`.

    Attributes:
        _cmd_type: "DELETE". Overrides :attribute:`Command._cmd_type`

    """

    _cmd_type = "DELETE"

    def get_string(self):
        """Getter for explicit sql command"""
        cmd = ' from {}'.format(self.tbl)
        self._cmd_str = cmd
        if self.conditions != ():
            cond = ' AND '.join(self.conditions)
            self._cmd_str = cmd + ' WHERE ' + cond
        self._cmd_str = self._cmd_type + self._cmd_str
        return self._cmd_str

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        """
        cmd = self.get_string()
        cursor.execute(cmd)
