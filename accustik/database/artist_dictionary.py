from utils import get_row, run_query

class ArtistDictionary:
    def __init__(self, db):
        self.dic = {}
        self.db = db

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == -1:
                return None
            elif item in self.dic:
                return self.dic.__getitem__(item)
            else:
                r = get_row(self.db, 'SELECT artists.name FROM artists WHERE artists.id=%s' % item)
                if r is None:
                    return None
                else:
                    self.dic[item] = r[0]
                    return r[0]

        elif isinstance(item, unicode) or isinstance(item, basestring):
            for (k,v) in self.dic.items():
                if v == unicode(item):
                    return k



    def __setitem__(self, key, value):
        if key == -1:
            return -1
        elif key in self.dic:
            #update
            self.dic[key] = value
            return key
        else:
            run_query(self.db, 'INSERT INTO artists VALUES(null, %s)' % value)
            r = get_row(self.db, 'SELECT artists.id FROM artists WHERE artists.name=%s' % value)

