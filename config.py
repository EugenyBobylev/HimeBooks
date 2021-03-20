import os
from pathlib import Path

basedir = Path.cwd()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'p140d$5qvd#z3vkdcpz))jj#dtwl1$+4^p$7o(sk*6oo17_6pa'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(basedir / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
