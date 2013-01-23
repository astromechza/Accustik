import schemas
import sqlite3
from accustik.logger import log
import os
from accustik.database.FTSDictionary import FTSDictionary
import accustik.data.data as data

class Library:
    """
    MAIN LIBRARY CLASS
    ------------------
    Acts as middle man between the application and the database
    """

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.artists = FTSDictionary(self.dbfile, 'artists')
        self.albums = FTSDictionary(self.dbfile, 'albums')
        self.genres = FTSDictionary(self.dbfile, 'genres')

