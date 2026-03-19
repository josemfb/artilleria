import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'IsmaelValdésVergara'
    basedir = os.path.abspath(os.path.dirname(__file__))
