from logging import basicConfig

from flask import Flask
import obelisk.views


logger = basicConfig(
    format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
    level=logging.INFO
)
app = Flask(__name__)
