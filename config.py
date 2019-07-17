import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    #environ.get will look at the enviroment variables and see if the secret key is included. It will use that value if so.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    #uri for sql lite database

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
