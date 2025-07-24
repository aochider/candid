from app.models.user import User

def register_routes(app):
	@app.route('/users')
	def get_users():
		users = User.get_all_users()
		user_list = [{"username": user.username, "email": user.email} for user in users]
		return {"users": user_list}