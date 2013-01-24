import sqlite3
from accustik.logger import log
from accustik.database.FTSDictionary import FTSDictionary

class FTSSongLibrary:

    def __init__(self, f, overwrite = False):

        self.file = f

        self.artists = FTSDictionary(self.file, 'artists', True)
        self.albums = FTSDictionary(self.file, 'albums', True)
        self.genres = FTSDictionary(self.file, 'genres', True)

        # sql statements
        self.sql_create_table = 'CREATE VIRTUAL TABLE IF NOT EXISTS songs USING fts4(' \
                                'filename TEXT UNIQUE ON CONFLICT ABORT, ' \
                                'name TEXT,' \
                                'artist_id INTEGER, ' \
                                'album_id INTEGER,' \
                                'genre_id INTEGER)'

        self.sql_drop_table = 'DROP TABLE IF EXISTS songs'

        # ensure table exists
        # if overwrite is True then drop table before creating

        con = None
        try:

            if overwrite:
                con = sqlite3.connect(self.file)
                cur = con.cursor()

                cur.execute(self.sql_drop_table)

                con.commit()
                con.close()

            con = sqlite3.connect(self.file)
            cur = con.cursor()

            cur.execute(self.sql_create_table)
            con.commit()

        except sqlite3.Error:
            log.exception('')
        finally:
            if con:
                con.close()