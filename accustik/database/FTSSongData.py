import sqlite3
from accustik.logger import log
from accustik.data.SongData import SongData
from accustik.database.FTSDictionary import FTSDictionary

class FTSSongData:

    def __init__(self, f, overwrite = False):

        self.file = f

        self.artists = FTSDictionary(self.file, 'artists', False)
        self.albums = FTSDictionary(self.file, 'albums', False)
        self.genres = FTSDictionary(self.file, 'genres', False)

        # sql statements
        self.sql_create_table = 'CREATE VIRTUAL TABLE IF NOT EXISTS songs USING fts4(' \
                                'filename TEXT UNIQUE ON CONFLICT ABORT, ' \
                                'name TEXT,' \
                                'artist_id INTEGER, ' \
                                'album_id INTEGER,' \
                                'genre_id INTEGER)'

        self.sql_drop_table = 'DROP TABLE IF EXISTS songs'

        self.sql_insert = 'INSERT INTO songs VALUES (?, ?, ?, ?, ?)'

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

    def add(self, song_data, existing_connection = None):
        if existing_connection is not None:
            self._add(song_data, existing_connection)
        else:
            con = None
            try:
                con = sqlite3.connect(self.file)
                self._add(song_data, con)
                con.commit()
            except:
                log.exception('')
            finally:
                if con:
                    con.close()

    def add_from_iterable(self, iterable):
        con = None
        try:
            con = sqlite3.connect(self.file)
            for song_data in iterable:
                self._add(song_data, con)
            con.commit()
        except:
            log.exception('')
        finally:
            if con:
                con.close()


    def _add(self, song_data, existing_connection):
        try:
            artist_id =     -1 if song_data.artist  is None else self.artists.get_id_for_content(song_data.artist, existing_connection)
            album_id =      -1 if song_data.album   is None else self.albums.get_id_for_content(song_data.album, existing_connection)
            genre_id =      -1 if song_data.genre   is None else self.genres.get_id_for_content(song_data.genre, existing_connection)
            title = song_data.title
            cur = existing_connection.cursor()
            cur.execute(self.sql_insert, [song_data.file, title, artist_id, album_id, genre_id])
        except Exception:
            log.exception('')
            raise

    def select_using_cache(self):
        con = None
        try:
            con = sqlite3.connect(self.file)
            cur = con.cursor()

            cur.execute('SELECT * FROM songs')
            r = cur.fetchall()

            if r is None:
                return None
            else:
                songs = []
                for row in r:
                    s = SongData()
                    s.file = row[0]
                    s.title = row[1]
                    s.artist = self.artists.get_content_from_id(int(row[2]), con)
                    s.album = self.albums.get_content_from_id(int(row[3]), con)
                    s.genre = self.genres.get_content_from_id((row[4]), con)
                    songs.append(s)
                return songs
        except sqlite3.Error:
            log.exception('DIE')
            return None
        finally:
            if con:
                con.close()



    def clear_cache(self):
        self.artists.clear_cache()
        self.albums.clear_cache()
        self.genres.clear_cache()
