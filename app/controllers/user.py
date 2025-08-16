from flask import request

from app.decorators import auth, validate
from app.errors import *
from app.models.user import User

def register_routes(app):
	@app.route('/user', methods=['POST'])
	@validate({
		"type": "object",
		"properties": {
			"name": {"type": "string"},
			"age": {"type": "integer", "minimum": 0},
		},
		"required": ["name", "age"],
	})
	def create_user():
		data = request.get_json()
		username = data['username']
		email = data['email']
		password = data['password']

		id = User.create_user()

		return {"id": id}

	@app.route('/user/login', methods=['POST'])
	@validate({
		"type": "object",
		"properties": {
			"email": {"type": "string", "pattern": "^.{2,}@[^\\.]{2,}\\.[^\\.]{2,}$"},
			"password": {"type": "string", "maxLength": 50, "minLength": 8},
		},
		"required": ["email", "password"],
	})
	def login():
		data = request.get_json()
		email = data.get('email')
		password = data.get('password')

		stored_user = User.get_by_email(email)

		if not stored_user:
			User.fake_does_password_match()
			raise INVALID_USER_LOGIN

		if stored_user.does_password_match(password):
			jwt = stored_user.create_token()
		else:
			raise INVALID_USER_LOGIN

		return {"id": stored_user.id, "token": jwt}