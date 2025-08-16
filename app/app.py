import json
import os

from flask import Flask
from flask_cors import CORS
import psycopg2
from app.config import DevelopmentConfig, ProductionConfig
from app.database import connect_to_db
from app.errors import *
from app.models.user import User

def create_app():
	app = Flask(__name__)

	# TODO is this safe to always have on?
	CORS(app)
	
	flask_env = os.environ.get('FLASK_ENV')
	if flask_env == 'dev':
		app.config.from_object(DevelopmentConfig)
	else:
		app.config.from_object(ProductionConfig)

	connect_to_db(app.config)

	User.TOKEN_SECRET = app.config['TOKEN_SECRET']
	User.TOKEN_LIFESPAN_MIN = app.config['TOKEN_LIFESPAN_MIN']
	
	from app.controllers.user import register_routes as user_register_routes
	user_register_routes(app)

	from app.controllers.chat_log import register_routes as chat_log_register_routes
	chat_log_register_routes(app)

	from app.controllers.chat_log_message import register_routes as chat_log_message_register_routes
	chat_log_message_register_routes(app)

	from app.controllers.position import register_routes as position_register_routes
	position_register_routes(app)

	from app.controllers.user_position import register_routes as user_position_register_routes
	user_position_register_routes(app)

	@app.after_request
	def set_json_header(response):
		response.headers["Content-Type"] = "application/json"
		return response

	@app.errorhandler(InternalException)
	def handle_internal_exception(ee):
		return '{"error": "service error"}', 500

	@app.errorhandler(ValidationException)
	def handle_validation_exception(ee):
		return json.dumps({'code': ee.code, 'error': ee.message}), 400

	@app.errorhandler(Exception)
	def handle_base_exception(ee):
		import traceback
		traceback.print_exc()
		return '{"error": "service error"}', 500

	return app

