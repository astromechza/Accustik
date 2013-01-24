from accustik.logger import log
import os
from accustik.database.FTSSongData import FTSSongData
from accustik.data.DataReaders import get_reader

class Library:
    """
    MAIN LIBRARY CLASS
    ------------------
    Acts as middle man between the application and the database
    """

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.songs = FTSSongData(self.dbfile, False)

    def add_file(self, path):
        reader = get_reader(path)
        sd = reader.read()
        if sd is None:
            log.debug('Unsupported filetype: ' + reader.file)
        else:
            self.songs.add(sd)

    def add_folder(self, path):
        self.songs.add_from_iterable(self._add_folder(path))

    def _add_folder(self, path):
        for f in os.listdir(path):
            reader = get_reader(os.path.join(path, f))
            sd = reader.read()
            if sd is None:
                log.debug('Unsupported filetype: ' + reader.file)
            else:
                yield sd

    def select(self):
        from accustik.database.utils import stopwatch
        s = stopwatch()
        songs = self.songs.select_using_cache()
        print s.stop()
        for song in songs:
            print song

    def clear_cache(self):
        self.songs.clear_cache()
