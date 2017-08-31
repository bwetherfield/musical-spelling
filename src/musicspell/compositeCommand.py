"""Composite-Like object-oriented imlementation of bundled groups of sql
commands that are called by databases in a Visitor-like way

"""
class CompositeCommand:
    """base sql composite command

    Arguments:
        *cmds: list of commands handled by object

    Attributes:
        cmds: list of commands handled by object
        _cmdStr: overridden attribute.

    """

    _cmdType = None

    def __init__(self, *cmds):
        self.cmds = cmds
        self._cmdStr = None

    def execute(self):
        """virtual method"""
        raise NotImplementedError

class Union(CompositeCommand):
    """concrete sql command UNION. Extends `CompositeCommand`.

    Attributes:
        _cmdType: "SELECT". Overrides :attribute:`CompositeCommand._cmdType`

    """

    _cmdType = "SELECT"

    def getString(self):
        """Getter for explicit sql command."""
        if self._cmdStr is None:
            cmdList = []
            for c in self.cmds:
                sc = c.getString()
                cmdList.append(sc)
            s = ' UNION '.join(cmdList)
            self._cmdStr = s
        return self._cmdStr

    def execute(self, cursor):
        """Execute sql all the contained commands

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        Returns:
            [:obj:`sqlite3.Row`], optional: rows of the database associated
                with `cursor` that meet the conditions or None if there are
                nonesuch

        """
        s = self.getString()
        cursor.execute(s)
        return cursor.fetchall()

class ManyCommand(CompositeCommand):
    """concrete sql command UNION. Extends `CompositeCommand`."""

    def execute(self, cursor):
        """Execute sql command

        Implements Visitor-like behavior

        Args:
            cursor: :obj:`sqlite3.Cursor` from database where the command is executed

        Returns:
            [:obj:`sqlite3.Row`], optional: returns the output of one of the
            commands. We are at the whims of the :mod:`sqlite3` implemtation.

        """
        for c in self.cmds:
            s = c.getString()
            cursor.execute(s)
