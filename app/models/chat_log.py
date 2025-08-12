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

	@staticmethod
	def get_by_id(chat_log_id):
		chat_logs = map_query_to_class(execute_query(
			"select * from \"chat_log\" join \"position\" on \"position\".id=\"chat_log\".position_id where \"chat_log\".id=%s", (chat_log_id,)
		), ChatLog)
		return chat_logs

	@staticmethod
	def get_by_user_id(user_id):
		chat_logs = map_query_to_class(execute_query(
			"select * from \"chat_log\" join \"position\" on \"position\".id=\"chat_log\".position_id where \"position\".creator_user_id=%s or \"chat_log\".responder_user_id=%s", (user_id, user_id)
		), ChatLog)
		return chat_logs