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

    def execute(self, cursor):
        cmdList = []
        for c in self.cmds:
            cmdList.append(c.getString())
        s = ' UNION '.join(cmdList)
        s = self._cmdType + s
        cursor.execute(s)
        return cursor.fetchall()
