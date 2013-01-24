
class SongData:
    def __init__(self):
        self.file = None
        self.title = None
        self.artist = None
        self.album = None
        self.genre = None

    def __str__(self):
        return "%s - %s - %s (%s)" % (self.title, self.artist, self.album, self.genre)