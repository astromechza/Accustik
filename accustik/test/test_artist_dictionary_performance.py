import accustik.database.artist_dictionary
import accustik.database.library
import accustik.database.utils as utils
import sample_data
import os
import time
import sqlite3
from accustik.logger import log
try:
    with open('t.db') as f: pass
    os.remove('t.db')
except IOError:
    pass
db = accustik.database.library.Library('t.db')
db.build()

times = 1000

i = 0
t1 = time.clock()

con = None
try:
    con = sqlite3.connect('t.db')
    cur = con.cursor()

    while i<times:
        cur.execute('INSERT INTO artists VALUES (null,"art%d")'% i)
        i+=1

    con.commit()

except sqlite3.Error, e:
    log.exception("SQLite3 ERROR %s" % e)
finally:
    if con:
        con.close()

t2 = time.clock()

print t2-t1