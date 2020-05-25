import os

from cerberus import Validator
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from visualize.models import db, bcrypt, blacklist

jwt = JWTManager()
validator = Validator()
validator.require_all = True


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	jti = decrypted_token['jti']
	return blacklist.is_jti_in_blacklist(jti)


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)

	# load the the standard configuartion depending on environment
	if app.config["ENV"] == "production":
		app.config.from_object("config.ProductionConfig")
	elif app.config["ENV"] == "development":
		app.config.from_object("config.DevelopmentConfig")
	elif app.config["ENV"] == "testing":
		app.config.from_object("config.TestingConfig")

	if test_config is not None:
		app.config.from_object("config.TestingConfig")

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# load secret and specific config for just this application
	app.config.from_pyfile("config.py")

	CORS(app)
	jwt.init_app(app)
	db.init_app(app)
	bcrypt.init_app(app)

	with app.app_context():
		from visualize.blueprints.main import main_bp
		from visualize.blueprints.admin import admin_bp
		from visualize.blueprints.reader import reader_bp
		from visualize.blueprints.approver import approver_bp
		app.register_blueprint(main_bp, url_prefix="/")
		app.register_blueprint(admin_bp, url_prefix="/admin")
		app.register_blueprint(reader_bp, url_prefix="/reader")
		app.register_blueprint(approver_bp, url_prefix="/approver")

		db.create_all()
		return app
