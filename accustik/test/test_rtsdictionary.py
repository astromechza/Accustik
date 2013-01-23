from accustik.database.FTSDictionary import FTSDictionary

from accustik.database.utils import run_query
from time_util import stopwatch

d = FTSDictionary('test.db', 'artists')
run_query('test.db',d.sql_drop_table)
run_query('test.db',d.sql_create_table)

def ngen():
    times = 100000
    i=0
    while i<times:
        i+=1
        yield 'derp' + str(i)


s = stopwatch()

d.add_from_generator(ngen())

print (s.stop())

s = stopwatch()

x = d[-1]

print s

print x
print d[10]

print s

d.update(10, 'johnson')

print s

print d[10]

print d['johnson']

print s.stop()
