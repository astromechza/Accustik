import os
from time_util import stopwatch
import logging
from accustik.logger import log
log.setLevel(logging.CRITICAL)

from accustik.database.AccustikLibrary import Library
os.remove('test.db')
l = Library('test.db')

mp3folder = 'C:\\Users\\Ben\\Music\\test music'

s = stopwatch()
l.add_folder(mp3folder)
print s.stop()

#for f in os.listdir(mp3folder):
#    path = os.path.join(mp3folder, f)
#    l.add_single_file(path)

