from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from mydiary.config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)

	from mydiary.main.routes import main
	from mydiary.users.routes import users
	from mydiary.pages.routes import pages

	app.register_blueprint(main)
	app.register_blueprint(users)
	app.register_blueprint(pages)
	return app