import os

class Config:
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	LONG_POLL_TIMEOUT = 10

class DevelopmentConfig(Config):
	DEV = True
	#SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev.db'

class ProductionConfig(Config):
	DEV = False
	#SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')