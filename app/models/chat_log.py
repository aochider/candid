from app.database import execute_query, map_query_to_class

class ChatLog():
	def __init__(self):
		self.id = None
		self.position_id = None
		self.creator_user_id = None
		self.responder_user_id = None
		self.message = None
		self.message_time = None

	def __repr__(self):
		return '<ChatLog %r>' % self.id

	@staticmethod
	def get(position_id, responder_user_id, message_id_offset=0):
		messages = map_query_to_class(execute_query(
			"select * from \"chat_log\" where position_id=%s and responder_user_id=%s and id > %s", (position_id, responder_user_id, message_id_offset)
		), ChatLog)
		return messages

	@staticmethod
	def get_count_since(position_id, responder_user_id, message_id_offset):
		count = execute_query(
			"select count(*) from \"chat_log\" where position_id=%s and responder_user_id=%s and id > %s", (position_id, responder_user_id, message_id_offset)
		)
		return count[0]['count']