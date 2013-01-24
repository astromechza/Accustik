import sqlite3
from accustik.logger import log

def get_row(database, sql):
    con = None
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(sql)
        r = cur.fetchone()
        return r

    except sqlite3.Error, e:
        log.exception("SQLite3 ERROR %s" % e)
        return None
    finally:
        if con:
            con.close()

def run_query(database, sql):
    """
    INSERT UPDATE DELETE
    """
    con = None
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return True

    except sqlite3.Error, e:
        log.exception("SQLite3 ERROR %s" % e)
        return False
    finally:
        if con:
            con.close()

import time
class stopwatch:
    def __init__(self):
        self.start = time.clock()
        self.running = True

    def stop(self):
        self.end = time.clock()
        self.running = False
        return self.__str__()

    def __str__(self):
        if self.running:
            t = time.clock()
            return str(t-self.start)
        else:
            return (self.end-self.start)