class CompositeCommand:

    """base sql composite command"""

    _cmdType = None

    def __init__(self, *cmds):
        self.cmds = cmds
        self._cmdStr = None

    def execute(self):
        raise NotImplementedError

class Union(CompositeCommand):

    """concrete sql command UNION"""

    _cmdType = "SELECT"

    def getString(self):
        if self._cmdStr is None:
            cmdList = []
            for c in self.cmds:
                sc = c._cmdType + " " + c.getString()
                cmdList.append(sc)
            s = ' UNION '.join(cmdList)
            self._cmdStr = s
        return self._cmdStr

    def execute(self, cursor):
        s = self.getString()
        cursor.execute(s)
        return cursor.fetchall()
