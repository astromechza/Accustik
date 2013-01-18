import logging
import sys

log = logging.getLogger('accustik')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)

log.addHandler(sh)