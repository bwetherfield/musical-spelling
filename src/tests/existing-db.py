from musispell.db import Db

def main():
    """here's-one-I'-made-earlier database for db.py
    :returns: TODO

    """
    madeEarlier = Db('madeEarlier')
    madeEarlier['table1'] = dict(column='int')
    madeEarlier['table2'] = dict(column='int')

if __name__ == "__main__":
    main()
