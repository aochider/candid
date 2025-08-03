from flask import request

from app.models.user import User

def register_routes(app):
	@app.route('/user')
	def get_users():
		users = User.get_all_users()
		user_list = [{"username": user.username, "email": user.email} for user in users]
		return {"users": user_list}

	@app.route('/user', methods=['POST'])
	def create_user():
		# TODO
		data = request.get_json()

		password = data['password']

		id = User.create_user()

		return {"id": id}

	@app.route('/user/login', methods=['POST'])
	def login():
		data = request.get_json()

		# TODO add validation and make sure validation takes the same time even if the user isnt found to not leak anything
		email = data['email']
		password = data['password']

		stored_user = User.get_by_email(email)

		if not stored_user:
			raise Exception("invalid credentials")

		if stored_user.does_password_match(password):
			jwt = stored_user.create_token()
		else:
			raise Exception("invalid credentials")

		return {"id": stored_user.id, "jwt": jwt}