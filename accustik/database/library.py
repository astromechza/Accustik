import sqlite3
from accustik.logger import log
import os
from accustik.database.FTSDictionary import FTSDictionary
from accustik.database.FTSSongData import FTSSongData

class Library:
    """
    MAIN LIBRARY CLASS
    ------------------
    Acts as middle man between the application and the database
    """

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.songs = FTSSongData(self.dbfile, True)

        

