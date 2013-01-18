class Song:
    def __init__(self,
                 title="",
                 artist_id=-1,
                 genre_id=-1,
                 album_id=-1,
                 file="",
                 length=-1):
        self.title = title
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.album_id = album_id
        self.file = file
        self.length = length

def load_song_from_file(file):
    # find extension
    ld = file.rfind('.')
    ext = file[ld+1:]

    if ext == 'mp3':
        from mutagen.id3 import ID3
        from mutagen.mp3 import MP3
        tags = ID3(file)
        mp3 = MP3(file)
        s = Song()

        s.title = tags['TIT2'].text[0] if 'TIT2' in tags else file[file.rfind('\\')+1:ld+1]

        s.artist = tags['TPE1'].text[0] if 'TPE1' in tags else ""

        s.album = tags['TALB'].text[0] if 'TALB' in tags else ""

        s.genre = tags['TCON'].text[0] if 'TCON' in tags else ""

        s.file = file

        s.length = mp3.info.length

        return True
    else:
        return False