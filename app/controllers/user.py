from flask import request

from app.models.user import User
from app.decorators import auth, validate

def register_routes(app):
	@app.route('/user')
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_users():
		users = User.get_all_users()
		user_list = [{"username": user.username, "email": user.email} for user in users]
		return {"users": user_list}

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
			raise Exception("invalid credentials")

		if stored_user.does_password_match(password):
			jwt = stored_user.create_token()
		else:
			raise Exception("invalid credentials")

		return {"id": stored_user.id, "jwt": jwt}