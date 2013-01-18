import sqlite3

def get_row(database, sql):

    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(sql)
        r = cur.fetchone()
        return r

    except sqlite3.Error, e:
        print e
        return None
    finally:
        if con:
            con.close()

def run_query(database, sql):
    """
    INSERT UPDATE DELETE
    """
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return True

    except sqlite3.Error, e:
        return False
    finally:
        if con:
            con.close()