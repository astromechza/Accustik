import schemas
import sqlite3
from accustik.logger import log
import os

import accustik.data.data as data
from accustik.database.artist_dictionary import ArtistDictionary

class Library:
    """
    MAIN LIBRARY CLASS
    ------------------
    Acts as middle man between the application and the database
    """

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.artists = ArtistDictionary(db=dbfile)
        self.albums = DBBackedDictionary(db=self, lookup_query='SELECT albums.name FROM albums WHERE albums.id=%s')
        self.genres = DBBackedDictionary(db=self, lookup_query='SELECT genres.name FROM genres WHERE genres.id=%s')


    def build(self):
        """
        build a database from scratch using the schemas,
        drop other tables without remorse
        """
        log.debug('Building database' + self.dbfile)
        conn = sqlite3.connect(self.dbfile)

        c = conn.cursor()
        for table in schemas.schema.keys():
            log.debug('Dropping table "%s"' % table)
            sql = "DROP TABLE IF EXISTS %s" % table
            c.execute(sql)

        conn.commit()

        for (table, cols) in schemas.schema.items():
            log.debug('Creating table "%s"' % table)
            sql = "CREATE TABLE %s (%s)" % (table, cols)
            c.execute(sql)

        conn.commit()

        conn.close()

    def add_file(self, filename):
        """
        Add a single local file to the library database.
        Read its metadata in order to add it
        """

        np = os.path.abspath(os.path.expanduser(os.path.expandvars(filename)))

        try:
            with open(np) as f: pass
        except IOError, e:
            log.error('File "%s" does not exist!' % np)
            return False


        song = data.load_song_from_file(np)

        if not song:
            return False



        log.debug("Adding file: " + np)

    def add_folder(self, path):
        np = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

        for root, dirs, files in os.walk(np):
            for file in files:
                ext = file[file.rfind('.')+1:]
                if ext in ['mp3']:
                    p = os.path.join(root, file)
                    self.add_file(p)

    def get_row(self, sql):

        try:
            con = sqlite3.connect(self.dbfile)

            cur = con.cursor()

            cur.execute(sql)

            r = cur.fetchone()
            return r

        except sqlite3.Error, e:
            return None
        finally:
            if con:
                con.close()



class DBBackedDictionary:
    def __init__(self, db, lookup_query):
        self.dic = {}
        self.db = db
        self.lookup_query = lookup_query

    def __getitem__(self, item):
        if item == -1:
            return None
        elif item in self.dic:
            return self.dic.__getitem__(item)
        else:
            r = self.db.get_row(self.lookup_query % item)
            if r is None:
                return None
            else:
                self.dic[item] = r[0]
                return r[0]

    def __setitem__(self, key, value):
        if key == -1:
            return False
        elif key in self.dic:
            #update
            pass
        else:
            #insert
            pass


class SongDictionary(DBBackedDictionary):
    def __init__(self, db):
        super(DBBackedDictionary, self).__init__(db, None)

    def __getitem__(self, item):
        if item == -1:
            return None
        elif item in self.dic:
            return self.dic.__getitem__(item)
        else:
            r = self.db.get_row('''SELECT   songs.title,
                                            songs.artist_id,
                                            songs.album_id,
                                            songs.genre_id,
                                            songs.length,
                                            songs.play_count,
                                            songs.file
                                            FROM songs WHERE songs.id=%s''' % item)

            if r is None:
                return None
            else:
                s = data.Song(r[0],r[1],r[3],r[2],r[6],r[4])
                return s