from app.database import execute_query

class Kudos():
	def __init__(self):
		self.id = None
		self.sender_user_id = None
		self.receiver_user_id = None
		self.chat_log_id = None

	def __repr__(self):
		return '<Kudos %r>' % self.id