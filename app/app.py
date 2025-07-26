import os

from flask import Flask
from flask_cors import CORS
import psycopg2
from app.config import DevelopmentConfig, ProductionConfig
from app.database import connect_to_db

def create_app():
	app = Flask(__name__)

	CORS(app)
	
	flask_env = os.environ.get('FLASK_ENV')
	if flask_env == 'dev':
		app.config.from_object(DevelopmentConfig)
	else:
		app.config.from_object(ProductionConfig)

	connect_to_db(app.config)
	
	from app.controllers.user import register_routes as user_register_routes
	user_register_routes(app)

	from app.controllers.chat_log import register_routes as chat_log_register_routes
	chat_log_register_routes(app)

	from app.controllers.chat_log_message import register_routes as chat_log_message_register_routes
	chat_log_message_register_routes(app)

	from app.controllers.position import register_routes as position_register_routes
	position_register_routes(app)

	return app