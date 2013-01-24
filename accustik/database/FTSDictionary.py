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
            if self.fromdata.has_key(item):
                log.debug('DICTIONARY_HIT: %s[%s]' % (self.table_name, item))
                return self.fromdata.__getitem__(item)
            else:
                log.debug('DICTIONARY_MISS: %s[%s]' % (self.table_name, item))
                con = None
                try:
                    con = sqlite3.connect(self.file)
                    cur = con.cursor()

                    cur.execute( self.sql_select_id_by_content,[item])
                    r = cur.fetchone()
                    if r == None:
                        log.debug('DATABASE_MISS: %s[%s]' % (self.table_name, item))
                        return None
                    id = r[0]

                    con.commit()
                    con.close()
                    con = None
                    self.todata[id] = item
                    self.fromdata[item] = id
                    return id
                except sqlite3.Error:
                    log.exception('')
                    return None
                finally:
                    if con:
                        con.close()
        else:
            if self.todata.has_key(item):
                log.debug('DICTIONARY_HIT: %s[%s]' % (self.table_name, item))
                return self.todata.__getitem__(item)
            else:
                log.debug('DICTIONARY_MISS: %s[%s]' % (self.table_name, item))
                con = None
                try:
                    con = sqlite3.connect(self.file)
                    cur = con.cursor()

                    cur.execute( self.sql_select_content_by_id,[item])
                    r = cur.fetchone()
                    if r is None:
                        log.debug('DATABASE_MISS: %s[%s]' % (self.table_name, item))
                        return None
                    content = r[0]

                    con.commit()
                    con.close()
                    con = None
                    self.todata[item] = content
                    self.fromdata[content] = item
                    return content
                except sqlite3.Error:
                    log.exception('')
                    return None
                finally:
                    if con:
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

