from app.database import execute_query, map_query_to_class

class ChatLog():
	def __init__(self):
		self.id = None
		self.position_id = None
		self.creator_user_id = None
		self.responder_user_id = None
		self.chat_log_time = None
		self.status = None

	def __repr__(self):
		return '<ChatLog %r>' % self.id

	@staticmethod
	def create(position_id, responder_user_id):
		id = execute_query(
			"insert into \"chat_log\" (position_id, responder_user_id, status) values (%s, %s, 'pending') returning id", (position_id, responder_user_id)
		)
		return id