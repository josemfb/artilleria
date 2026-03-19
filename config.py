import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'IsmaelValdésVergara'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'quintanet.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
