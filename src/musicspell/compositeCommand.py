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
        pass
