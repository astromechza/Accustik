__author__ = 'Ben'

from database import library

db = library.Library('dbfile.db')

import time
t1 = time.clock()
a = db.artists[0]
t2 = time.clock()
b = db.artists[0]
t3 = time.clock()


print 'got %s in %s'% (a, str(t2-t1))
print 'got %s in %s'% (b, str(t3-t2))

#db.build()

#db.add_folder('C:\\Users\\Ben\\Music')