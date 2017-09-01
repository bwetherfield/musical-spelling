"""Composite-Like object-oriented imlementation of bundled groups of sql
commands that are called by databases in a Visitor-like way

"""
class CompositeCommand:
    """base sql composite command

    Arguments:
        *cmds: list of commands handled by object

    Attributes:
        cmds: list of commands handled by object
        _cmd_str: overridden attribute.

    """

    _cmd_type = None

    def __init__(self, *cmds):
        self.cmds = cmds
        self._cmd_str = None

    def execute(self):
        """virtual method"""
        raise NotImplementedError

class Union(CompositeCommand):
    """concrete sql command UNION. Extends `CompositeCommand`.

    Attributes:
        _cmd_type: "SELECT". Overrides :attribute:`CompositeCommand._cmd_type`

    """

    _cmd_type = "SELECT"

    def get_string(self):
        """Getter for explicit sql command."""
        if self._cmd_str is None:
            cmd_list = []
            for c in self.cmds:
                sc = c.get_string()
                cmd_list.append(sc)
            s = ' UNION '.join(cmd_list)
            self._cmd_str = s
        return self._cmd_str

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
        s = self.get_string()
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
            s = c.get_string()
            cursor.execute(s)
