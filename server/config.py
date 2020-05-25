"""This module constains the public configuration for the application."""

import datetime
import os


class Config(object):
	"""Abstract config file to be inherited by the different environments."""

	DEBUG = False
	TESTING = False
	# Create app.db sqlite database in the server folder
	dir_path = os.path.dirname(os.path.realpath(__file__))
	db_uri = 'sqlite:///' + dir_path + "/app.db"
	SQLALCHEMY_DATABASE_URI = db_uri
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	# Secret key for the current instance. Will be hidden when the system goes into production.
	SECRET_KEY = b"\xc3\xf6N)]\xdb\x80\xd9a\xa2#\x93\xdb\x90\x08\xf7\x85\x0b\xf8\xd2\xa3soZ"
	SQLALCHEMY_TRACK_MODIFICATIONS = "False"
	# Blacklist stuff.
	JWT_SECRET_KEY = SECRET_KEY
	JWT_BLACKLIST_ENABLED = True
	JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
	JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)  # TODO: Change to 1 hour instead.


# This is the config that should be used when the server is finished and ready for production
class ProductionConfig(Config):
	"""Configuration for when the app is in production."""

	DATABASE_URI = 'postgresql://reader@localhost/foo'


# This config is for development purposes
class DevelopmentConfig(Config):
	"""Configuration for when the app is being developed."""

	DEBUG = True


# This config is used for testing purposes
class TestingConfig(Config):
	"""Configuration for when the app is getting tested."""

	TESTING = True
