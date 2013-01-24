from accustik.database.FTSDictionary import FTSDictionary

from accustik.database.utils import run_query
from accustik.database.utils import stopwatch

d = FTSDictionary('test.db', 'artists')

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

print d.add('bob')
print d.add('charles')
print d.add('bob')

print d.count_cache()

d.clear_cache()

print d.count_cache()

print d.add('bob')
print d.add('charles')

print d.count_cache()

s = stopwatch()

x = d['charles']

print s

print x