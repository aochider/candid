from functools import wraps
from jsonschema import validate as jsvalidate, ValidationError
from flask import request

from app.models.user import User

def auth(min_role):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			try:
				token = request.headers.get('Authorization', '').split(' ')[1]
				user = User.get_by_token(token)
				min_role_rank = User.USER_ROLE_RANKING.get(min_role)
				print(min_role, min_role_rank, flush=True)
				if not min_role_rank:
					raise Exception('insufficient authorization')

				current_role_rank = User.USER_ROLE_RANKING.get(user.role, -1)

				if current_role_rank < min_role_rank:
					raise Exception('insufficient authorization')

				request.user = user
			except Exception as e:
				print('auth decorator exception', e, flush=True)
				import traceback
				traceback.print_exc()
				return {"error": "Invalid credentials"}, 400

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
			except ValidationError as e:
				print(e, flush=True)
				import traceback
				traceback.print_exc()
				return {"error": e.message}, 400
			except Exception as e: # Handle cases where JSON is invalid or not present
				print(e, flush=True)
				import traceback
				traceback.print_exc()
				return {"error": "Invalid JSON or missing payload"}, 400

			return f(*args, **kwargs)

		return decorated_function

	return decorator