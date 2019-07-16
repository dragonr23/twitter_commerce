from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)

#initialize config variables for application

app.config.from_object(Config)

#bootstrap requires app instance and always comes after app is declared

bootstrap = Bootstrap(app)





from app import routes
