from functools import wraps
from jsonschema import validate as jsvalidate, ValidationError
from flask import request

from app.models.user import User

def auth(min_role=User.USER_ROLE_GUEST):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			try:
				token = request.headers.get('Authorization', '').split(' ')[1]
				user = User.get_by_token(token)
				minimum_role = kwargs.get('min_role', User.USER_ROLE_GUEST)
				minimum_role_rank = User.USER_ROLE_RANKING.get(minimum_role, 0)
				current_role_rank = User.USER_ROLE_RANKING.get(user.role, -1)

				if current_role_rank < minimum_role_rank:
					raise Exception('insufficient authorization')

				request.user = user
			except Exception as e:
				print(e, flush=True)
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
				return {"error": e.message}, 400
			except Exception as e: # Handle cases where JSON is invalid or not present
				print(e, flush=True)
				return {"error": "Invalid JSON or missing payload"}, 400

			return f(*args, **kwargs)

		return decorated_function

	return decorator