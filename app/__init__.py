from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)

#bootstrap requires app instance and always comes after app is declared

bootstrap = Bootstrap(app)



from app import routes
