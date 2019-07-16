import os

class Config():
    #environ.get will look at the enviroment variables and see if the secret key is included. It will use that value if so.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
