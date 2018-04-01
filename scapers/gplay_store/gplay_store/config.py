from datetime import datetime
import logging
import os

GP_FOLDER = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(format='%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
fh = logging.FileHandler(GP_FOLDER + '/logs/log.txt')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

DATEID = datetime.now().strftime("%Y-%m-%d")
