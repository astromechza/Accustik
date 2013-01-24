from SongData import SongData

class AudioTagReader(SongData):

    def __init__(self, filename):
        SongData.__init__(self)
        self.file = filename

    def read(self):
        return None


class ID3_reader(AudioTagReader):

    def read(self):
        from mutagen.id3 import ID3
        tags = ID3(self.file)

        self.title = tags['TIT2'].text[0] if 'TIT2' in tags else file[self.file.rfind('\\')+1:-4]

        self.artist = tags['TPE1'].text[0] if 'TPE1' in tags else None

        self.album = tags['TALB'].text[0] if 'TALB' in tags else None

        self.genre = tags['TCON'].text[0] if 'TCON' in tags else None

        return self



def get_reader(filename):
    last_dot = filename.rfind('.')
    ext = filename[last_dot+1:]

    if ext == 'mp3':
        return ID3_reader(filename)
    if ext == 'wma':
        pass
    if ext == 'wav':
        pass
    if ext == 'mp4':
        pass
    return AudioTagReader(filename)
