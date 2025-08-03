import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
import uuid

from app.database import execute_query, map_query_to_class

class User():
	# filled in at startup
	TOKEN_SECRET = None
	# filled in at startup
	TOKEN_LIFESPAN_MIN = None
	TOKEN_ALGO = 'HS256'
	PASSWORD_HASH_ROUNDS = 14
	USER_ROLE_GUEST = 'guest'
	USER_ROLE_NORMAL = 'normal'
	USER_ROLE_MOD = 'mod'
	USER_ROLE_ADMIN = 'admin'
	USER_ROLE_RANKING = {
		USER_ROLE_GUEST: 1,
		USER_ROLE_NORMAL: 10,
		USER_ROLE_MOD: 20,
		USER_ROLE_ADMIN: 30,
	}

	def __init__(self):
		self.id = None
		self.username = None
		self.email = None
		self.display_name = None
		self.password_hash = None
		self.role = None
		self.created_time = None
		# TODO probably want to verify the email
		self.verified_time = None

	def __repr__(self):
		return '<User %r>' % self.username

	def create_token(self):
		now = datetime.now(timezone.utc)
		payload = {
			"user_id": self.id,
			"email": self.email,
			"sub": str(self.id),
			"iat": now,
			"exp": now + timedelta(minutes=User.TOKEN_LIFESPAN_MIN),
			"jti": str(uuid.uuid4()),
		}
		return jwt.encode(payload, User.TOKEN_SECRET, algorithm=User.TOKEN_ALGO)

	def does_password_match(self, password):
		return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password_hash, 'utf-8'))

	@staticmethod
	def authenticate():
		token = request.cookies.get('token')
		user = User.get_by_token(token)
		return user

	@staticmethod
	def create_user():
		password = b"password"
		salt = bcrypt.gensalt(rounds=User.PASSWORD_HASH_ROUNDS)
		hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
		id = 1

		return id

	@staticmethod
	def decode_token(token):
		try:
			decoded_payload = jwt.decode(token, User.TOKEN_SECRET, algorithms=User.TOKEN_ALGO)
			return decoded_payload
		except jwt.ExpiredSignatureError as e:
			print("Token has expired.", flush=True)
			raise e
		except jwt.InvalidTokenError as e:
			print("Invalid token.", flush=True)
			raise e

		# TODO throw exceptions that flask catches and returns correct http codes and messages wo leaking
		return None

	# use this to burn some time if we didnt find a user
	@staticmethod
	def fake_does_password_match():
		return bcrypt.checkpw(bytes('0123456789', 'utf-8'), bytes('9876543210', 'utf-8'))

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

		now = datetime.now(timezone.utc)
		token_exp = datetime.fromtimestamp(decoded_token['exp'], tz=timezone.utc)
		if token_exp < now:
			raise Exception('invalid token')

		email = decoded_token['email']
		users = map_query_to_class(execute_query("select * from \"user\" where email=%s", (email,)), User)
		return users[0]