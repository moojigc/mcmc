import logging
from server import app

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG)
app
