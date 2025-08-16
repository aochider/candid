from app.database import db, execute_query

class UserPosition():
	RESULTS = ['agree', 'disagree', 'pass', 'chat']

	def __init__(self):
		self.id = None
		self.user_id = None
		self.position_id = None
		self.result = None

	def __repr__(self):
		return '<UserPosition %r>' % self.id

	@staticmethod
	def create(user_id, position_id, result):
		return execute_query(
			"insert into \"user_position\" (user_id, position_id, result)"
			" values (%s, %s, %s)"
			" on conflict (id) do update set result = excluded.result returning id", (user_id, position_id, result)
		)