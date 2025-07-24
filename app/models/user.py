import bcrypt

from app.database import execute_query, map_query_to_class

class User():
	PASSWORD_HASH_ROUNDS = 14
	USER_TYPES = ['normal', 'mod', 'admin', 'guest']

	def __init__(self):
		self.id = None
		self.username = None
		self.email = None
		self.display_name = None
		self.password_hash = None
		self.user_type = None
		self.created_time = None
		# TODO probably want to verify the email
		self.verified_time = None

	def __repr__(self):
		return '<User %r>' % self.username

	def set_password(self, password):
		self.password_hash = hashed = bcrypt.hashpw(password, bcrypt.gensalt(PASSWORD_HASH_ROUNDS))

	def does_password_match(self, password, hashed):
		return bcrypt.checkpw(password, hashed)

	@staticmethod
	def get_all_users():
		users = map_query_to_class(execute_query("select * from \"user\""), User)
		return users