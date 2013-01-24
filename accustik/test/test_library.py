import os
from accustik.database.utils import stopwatch
import logging
from accustik.logger import log
log.setLevel(logging.DEBUG)

from accustik.database.AccustikLibrary import Library
os.remove('test.db')
l = Library('test.db')

mp3folder = 'C:\\Users\\Ben\\Music\\test music'
#
s = stopwatch()
l.add_folder(mp3folder)
print s.stop()

l.clear_cache()

l.select()

