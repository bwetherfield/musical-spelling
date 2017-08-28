class CompositeCommand:

    """base sql composite command"""

    _cmdType = None

    def __init__(self, *cmds):
        self.cmds = cmds

    def execute(self):
        raise NotImplementedError

class Union(CompositeCommand):

    """concrete sql command UNION"""

    _cmdType = "SELECT"

    def getString(self):
        cmdList = []
        for c in self.cmds:
            cmdList.append(c.getString())
        s = ' UNION '.join(cmdList)
        s = self._cmdType + s
        return s

    def execute(self, cursor):
        s = self.getString()
        cursor.execute(s)
        return cursor.fetchall()
