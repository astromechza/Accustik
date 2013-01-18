"""

This file contains the database schemas for tables used in the project, this should allow easy maintenance of
a database in testing and deployment. Schemas should follow SQL and sqlite3 specification.

"""

schema = {
    'artists' : '"id" INTEGER PRIMARY KEY AUTOINCREMENT, \
                 "name" TEXT NOT NULL',

    'genres' : '"id" INTEGER PRIMARY KEY AUTOINCREMENT, \
                 "name" TEXT NOT NULL',

    'albums' : '"id" INTEGER PRIMARY KEY AUTOINCREMENT, \
                 "name" TEXT NOT NULL',

    'songs' : '"id" INTEGER PRIMARY KEY AUTOINCREMENT, \
               "title" TEXT NOT NULL, \
               "artist_id" INTEGER, \
               "album_id" INTEGER, \
               "genre_id" INTEGER, \
               "length" FLOAT NOT NULL, \
               "play_count" INTEGER NOT NULL, \
               "file" TEXT NOT NULL'
}