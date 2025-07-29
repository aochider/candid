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
	def respond(user_id, position_id, result):
		print(user_id, position_id, result, flush=True)
		execute_query(
			"insert into \"user_position\" (user_id, position_id, result)"
			" values (%s, %s, %s)"
			" on conflict (id) do update set result = excluded.result", (user_id, position_id, result)
		)
		return True