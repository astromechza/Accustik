__author__ = 'Ben'

from database import library

db = library.Library('dbfile.db')

import time
t1 = time.clock()
a = db.artists[0]
t2 = time.clock()
b = db.artists[0]
t3 = time.clock()

c = db.artists[unicode('bob')]
t4 = time.clock()
d = db.artists[unicode('charles')]
t5 = time.clock()

print 'got %s in %s'% (a, str(t2-t1))
print 'got %s in %s'% (b, str(t3-t2))
print 'got %s in %s'% (c, str(t4-t3))
print 'got %s in %s'% (d, str(t5-t4))

#db.build()

#db.add_folder('C:\\Users\\Ben\\Music')