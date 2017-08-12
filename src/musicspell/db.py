import sqlite3

class Db():

    """database handler"""

    def __init__(self):
        """TODO: to be defined1. """
        _conn = sqlite3.connect('default.db')
        _c = _conn.cursor()

