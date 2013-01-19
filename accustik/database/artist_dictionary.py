from utils import get_row, run_query

class ArtistDictionary:
    """
    A cached int-unicode lookup dictionary for fast lookups of artists or artist ids
    """
    def __init__(self, db_file):
        self.dic = {}
        self.db_file = db_file

    def __getitem__(self, key):
        """
        Used by artst[id] or artist['name']
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



    def set(self, key, value):
        if key == -1:
            return -1
        elif key in self.dic:
            #update
            run_query(self.db_file, 'UPDATE artists SET artists.name=%s WHERE artists.id=%s' % (value, key))
            self.dic[key] = value
            return key
        else:
            run_query(self.db_file, 'INSERT INTO artists VALUES(null,"%s")' % value)
            return self.__getitem__(value)

    def add(self, value):
        if value in self.dic.values():
            for (k,v) in self.dic.items():
                if v == value:
                    return k
        else:
            run_query(self.db_file, 'INSERT INTO artists VALUES(null, "%s")' % value)
            return self.__getitem__(value)
        return -1
