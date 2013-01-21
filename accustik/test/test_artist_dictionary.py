import accustik.database.artist_dictionary
import accustik.database.library
import accustik.database.utils as utils
import sample_data
import os

os.remove('test.db')
testdb = accustik.database.library.Library('test.db')
testdb.build()

# test adding sample data
sample_data.add(testdb.dbfile)
r = testdb.get_row('SELECT COUNT(*) FROM artists')
assert r[0] == 4

# test fetching artists from database into dictionary
s = sample_data.sample
for id, artist in s['artists']:
    assert testdb.artists[id] == artist

# are they all loaded into dic
assert len(testdb.artists.dic) == len(sample_data.sample['artists'])

# test putting a record into dictionary
id = testdb.artists.add(u'Emma')
# is it there under the right id
assert testdb.artists[id] == u'Emma'
assert testdb.artists[u'Emma'] == id

# check whether it was put into the sqlite3 database properly
r = testdb.get_row('SELECT artists.name FROM artists WHERE artists.id=%d' % id)
assert r[0] == u'Emma'



