from accustik.database.utils import run_query

sample = dict(artists=[
    (0, 'Abba'),
    (1, u'BB King'),
    (2, 'Clapton'),
    (3, u'Dally')
], genres=[
    (0, 'Rock'),
    (1, 'Jazz'),
    (2, 'Rock \'n Roll'),
    (3, 'unknown')
])


def add(database):
    for a in sample['artists']:
        run_query(database, 'INSERT INTO artists VALUES (%s, "%s")' % a)
