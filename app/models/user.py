import bcrypt
from datetime import datetime, timedelta, timezone
import jwt

from app.database import execute_query, map_query_to_class

class User():
	# filled in at startup
	TOKEN_SECRET = None
	# filled in at startup
	TOKEN_LIFESPAN_MIN = None
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

	def create_token(self):
		# TODO add other stuff to the payload, such as issue time
		payload = {
			"user_id": self.id,
			"email": self.email,
			"exp": datetime.now(timezone.utc) + timedelta(minutes=self.__class__.TOKEN_LIFESPAN_MIN) # Expiration time
		}
		secret_key = self.__class__.TOKEN_SECRET
		algorithm = "HS256"

		return jwt.encode(payload, secret_key, algorithm=algorithm)

	def set_password(self, password):
		self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt(PASSWORD_HASH_ROUNDS))

	def does_password_match(self, password):
		return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password_hash, 'utf-8'))

	@staticmethod
	def authenticate():
		token = request.cookies.get('token')
		user = User.get_by_token(token)
		return user

	@staticmethod
	def create_user():
		password = b"password"  # Password must be in bytes
		salt = bcrypt.gensalt(rounds=self.__class__.PASSWORD_HASH_ROUNDS)          # Generate a random salt
		hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
		id = 1

		return id

	@staticmethod
	def decode_token(token):
		secret_key = User.TOKEN_SECRET
		algorithm = "HS256"

		try:
			decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithm])
			return decoded_payload
		except jwt.ExpiredSignatureError:
			print("Token has expired.")
		except jwt.InvalidTokenError:
			print("Invalid token.")

		# TODO throw exceptions that flask catches and returns correct http codes and messages wo leaking
		return None

	@staticmethod
	def get_all_users():
		users = map_query_to_class(execute_query("select * from \"user\""), User)
		return users

	@staticmethod
	def get_by_email(email):
		users = map_query_to_class(execute_query("select * from \"user\" where email=%s", (email,)), User)
		return users[0]

	@staticmethod
	def get_by_token(token):
		decoded_token = User.decode_token(token)
		email = decoded_token['email']
		users = map_query_to_class(execute_query("select * from \"user\" where email=%s", (email,)), User)
		return users[0]