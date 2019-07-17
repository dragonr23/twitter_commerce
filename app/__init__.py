from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

#initialize config variables for application

app.config.from_object(Config)

#bootstrap requires app instance and always comes after app is declared

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)




from app import routes
