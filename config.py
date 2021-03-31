import os
from pathlib import Path

basedir = Path(__file__).parent


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'p140d$5qvd#z3vkdcpz))jj#dtwl1$+4^p$7o(sk*6oo17_6pa'
    BASE_DIR = basedir
