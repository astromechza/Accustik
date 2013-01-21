from utils import get_row, run_query
from accustik.logger import log
import sqlite3

class ArtistDictionary:
    """
    A cached int-unicode lookup dictionary for fast lookups of artists or artist ids
    """
    def __init__(self, db_file):
        self.dic = {}
        self.db_file = db_file

    def __len__(self):
        return self.dic.__len__()

    def __getitem__(self, key):
        """
        Used by artst[id] or artist['name'], this is database backed so that if items don't exist they are fetched
        from the cache
        """
        if isinstance(key, int):
            # if key is an integer
            if key in self.dic:
                # if item is in the dictionary, simply fetch it
                return self.dic.__getitem__(key)
            else:
                # otherwise fetch it from the database and store it in the dictionar for future use
                r = get_row(self.db_file, 'SELECT artists.name FROM artists WHERE artists.id=%s' % key)
                if r is None:
                    return None
                else:
                    # convert string from database into unicode
                    u = unicode(r[0])
                    self.dic[key] = u
                    return u

        elif isinstance(key, unicode):
            # if key is a unicode object
            # try to find it in the dictionary
            for (k,v) in self.dic.items():
                if v == key:
                    # if found return its key
                    return k

            # otherwise attempt to get the key from the database
            r = get_row(self.db_file, 'SELECT artists.id FROM artists WHERE artists.name LIKE "%s"' % key)

            if r is None:
                return None
            else:
                k = r[0]
                self.dic[k] = key
                return k

        elif isinstance(key, basestring):
            # if the key is a normal string, encode it as unicode and try again
            return self.__getitem__(unicode(key))



    def set(self, artist_id, artist_name):
        """
        SET an existing item in the dictionary, if the item does not exist return false
        """
        if artist_id == -1:
            return -1
        # run a get query
        existing_name = self.__getitem__(artist_id)

        if existing_name is None:
            return False
        else:
            #update

            run_query(self.db_file, 'UPDATE artists SET artists.name=%s WHERE artists.id=%s' % (artist_name, artist_id))
            self.dic[artist_id] = artist_name
            return True

    def add(self, artist_name):
        """
        Add an artist name to the dictionary and return its artist_id
        """
        artist_name = unicode(artist_name.strip())
        if artist_name == u'':
            return -1
        if artist_name in self.dic.values():
            for (k,v) in self.dic.items():
                if v == artist_name:
                    return k
        else:
            run_query(self.db_file, 'INSERT INTO artists VALUES(null, "%s")' % artist_name)
            return self.__getitem__(artist_name)
        return -1

    def add_bulk(self, artist_list):
        con = None
        try:
            con = sqlite3.connect('t.db')
            cur = con.cursor()

            for artist in artist_list:
                pass
            con.commit()

        except sqlite3.Error, e:
            log.exception("SQLite3 ERROR %s" % e)
        finally:
            if con:
                con.close()

