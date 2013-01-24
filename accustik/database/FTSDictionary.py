import sqlite3
from accustik.logger import log

class FTSDictionary:

    def __init__(self, f, column_name, overwrite = False):
        self.todata = {}
        self.fromdata = {}
        self.file = f
        self.table_name = column_name
        self.sql_insert = 'INSERT INTO %s VALUES (?)' % self.table_name
        self.sql_select_id_by_content = 'SELECT rowid FROM %s WHERE content MATCH ?' % self.table_name
        self.sql_select_content_by_id = 'SELECT content FROM %s WHERE rowid = ?' % self.table_name
        self.sql_create_table = 'CREATE VIRTUAL TABLE IF NOT EXISTS %s USING fts4(content TEXT UNIQUE ON CONFLICT IGNORE)' % self.table_name
        self.sql_drop_table = 'DROP TABLE IF EXISTS ' + self.table_name
        self.sql_update_content_by_id = 'UPDATE %s SET content = ? WHERE rowid = ?' % self.table_name

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




    def add(self, data):
        if not isinstance(data, basestring):
            return -1
        if data in self.fromdata:
            return self.fromdata[data]

        con = None
        try:
            con = sqlite3.connect(self.file)
            cur = con.cursor()

            cur.execute(self.sql_insert,[data])
            cur.execute( self.sql_select_id_by_content,[data])
            r = cur.fetchone()

            id = r[0]

            con.commit()
            con.close()
            con = None
            self.todata[id] = data
            self.fromdata[data] = id
            return id
        except sqlite3.Error:
            log.exception('')
        finally:
            if con:
                con.close()
        return -1
    def add_from_generator(self, gen):
        con = None
        try:
            con = sqlite3.connect(self.file)
            cur = con.cursor()

            try:
                while 1:
                    data = gen.next()
                    cur.execute(self.sql_insert, [data])
                    if cur.rowcount == 1:
                        id = cur.lastrowid
                    else:
                        cur.execute( self.sql_select_id_by_content, [data])
                        id = cur.fetchone()[0]
                    self.todata[id] = data
                    self.fromdata[data] = id

            except StopIteration:
                pass
            con.commit()
            con.close()
            con = None
        except sqlite3.Error:
            log.exception('')
        finally:
            if con:
                con.close()


    def __getitem__(self, item):
        if isinstance(item, basestring):
            return self.get_id_for_content(item)
        elif isinstance(item, int):
            return self.get_content_from_id(item)
        raise ValueError('Unknown lookup type %s , must be of type STRING or INT' % type(item))

    def get_using_conn(self, item, connection):
        if isinstance(item, basestring):
            return self.get_id_for_content(item, connection)
        elif isinstance(item, int):
            return self.get_content_from_id(item, connection)
        raise ValueError('Unknown lookup type %s , must be of type STRING or INT' % type(item))

    def get_id_for_content(self, content, existing_connection = None):
        """
        GET the id for the given content. If a connection exists use it.
        cases:
            1. content is None or blank: return -1
            2. content is in dictionary: awesome! return the id     [CACHE HIT]
            3. content is not in dictionary: hmm check in database  [CACHE MISS]
                3.1 content was in database: great! return and update dictionary    [DATABASE HIT]
                3.2 content was NOT in database: ok ADD the content as a new id     [DATABASE MISS/SET]
        """

        if content is None or len(content) == 0:
            return -1
        elif self.fromdata.has_key(content):
            log.debug('CACHE_HIT: %s[%s]' % (self.table_name, content))
            return self.fromdata.__getitem__(content)
        else:
            log.debug('CACHE_MISS: %s[%s]' % (self.table_name, content))

            con = existing_connection
            try:
                if con is None:
                    con = sqlite3.connect(self.file)
                cur = con.cursor()
                cur.execute(self.sql_select_id_by_content, [content])
                r = cur.fetchone()
                if r is None:
                    log.debug('DATABASE INSERT: %s[%s]' % (self.table_name, content))
                    cur.execute(self.sql_insert, [content])
                    id = cur.lastrowid
                else:
                    log.debug('DATABASE HIT: %s[%s]' % (self.table_name, content))
                    id = r[0]
                self.todata[id] = content
                self.fromdata[content] = id
                return id
            except sqlite3.Error:
                log.exception('')
                return -1
            finally:
                # if an original connection existed. dont close it
                if existing_connection is None:
                    if con:
                        con.commit()
                        con.close()

    def get_content_from_id(self, id, existing_connection = None):
        """
        GET the content for a given id. If a connection exists use it.
        cases:
            1. id is invalid (id < 1) : return blank string. (Does not have an artist/genre/album)
            2. id is already in dictionary: awesome! return the data in the dictionary
            3. id is NOT in dictionary: check in database
                3.1 was in database: great! retreive and put in dictionary before returning
                3.2 was NOT in database: oh dear! return None to indicate broken link that should be repaired

        """

        if id < 1:
            return ''
        elif self.todata.has_key(id):
            log.debug('CACHE_HIT: %s[%s]' % (self.table_name, id))
            return self.todata.__getitem__(id)
        else:
            log.debug('CACHE_MISS: %s[%s]' % (self.table_name, id))

            con = existing_connection
            try:
                if con is None:
                    con = sqlite3.connect(self.file)
                cur = con.cursor()
                cur.execute(self.sql_select_content_by_id, [id])
                r = cur.fetchone()
                if r is None:
                    log.debug('DATABASE MISS: %s[%s]' % (self.table_name, id))
                    return None
                else:
                    log.debug('DATABASE HIT: %s[%s]' % (self.table_name, id))
                    content = r[0]
                    self.todata[id] = content
                    self.fromdata[content] = id
                    return content
            except sqlite3.Error:
                log.exception('')
                return None
            finally:
                # if an original connection existed. dont close it
                if existing_connection is None:
                    if con:
                        con.commit()
                        con.close()

    def update(self, lookup, new_content):
        """
        Change the content of a given rowid or existing content, and update the dictionaries to match
        """

        #first open db connection
        con = None
        try:
            con = sqlite3.connect(self.file)
            cur = con.cursor()

            #then check whether lookup exists
            if isinstance(lookup, int):
                cur.execute(self.sql_select_content_by_id, [str(lookup)])
                if cur.fetchone() is not None:
                    # update row
                    cur.execute(self.sql_update_content_by_id, [new_content, str(lookup)])

                    # update dictionary
                    t = self.todata[lookup]
                    self.todata[lookup] = new_content
                    del self.fromdata[t]
                    self.fromdata[t] = lookup

                    con.commit()

                    return True
            elif isinstance(lookup, basestring):
                cur.execute(self.sql_select_id_by_content, [str(lookup)])
                r = cur.fetchone()
                if r is not None:
                    # update row
                    id = r[0]
                    cur.execute(self.sql_update_content_by_id, [new_content, str(id)])

                    # update dictionary
                    self.todata[id] = new_content
                    del self.fromdata[lookup]
                    self.fromdata[new_content] = id

                    con.commit()

                    return True

            return False
        except sqlite3.Error:
            log.exception('')
        finally:
            if con:
                con.close()

    def clear_cache(self):
        self.fromdata.clear()
        self.todata.clear()

    def count_cache(self):
        return len(self.todata.keys())

