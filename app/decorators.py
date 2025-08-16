from functools import wraps
from jsonschema import validate as jsvalidate, ValidationError as jsValidationError
from flask import request

from app.errors import *
from app.models.user import User

def auth(min_role):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			try:
				token = request.headers.get('Authorization', '').split(' ')[1]
				user = User.get_by_token(token)
				min_role_rank = User.USER_ROLE_RANKING.get(min_role)

				if not min_role_rank:
					raise INVALID_CREDENTIALS

				current_role_rank = User.USER_ROLE_RANKING.get(user.role, -1)

				if current_role_rank < min_role_rank:
					raise INVALID_CREDENTIALS

				request.user = user
			except Exception as ee:
				print('auth decorator exception', ee, flush=True)
				import traceback
				traceback.print_exc()
				raise INVALID_CREDENTIALS from ee

			return f(*args, **kwargs)

		return decorated_function

	return decorator

def validate(schema):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			try:
				data = request.json
				jsvalidate(instance=data, schema=schema)
			except jsValidationError as ee:
				ee2 = INVALID_JSON_SCHEMA
				ee2.message = ee.message
				raise ee2 from ee
			except Exception as ee: # Handle cases where JSON is invalid or not present
				raise INVALID_JSON_BODY from ee

			return f(*args, **kwargs)

		return decorated_function

	return decorator