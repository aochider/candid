from app.database import execute_query, map_query_to_class

class ChatLogMessage():
	def __init__(self):
		self.id = None
		self.chat_log_id = None
		self.user_id = None
		self.message = None
		self.message_time = None

	def __repr__(self):
		return '<ChatLogMessage %r>' % self.id

	@staticmethod
	def create(chat_log_id, user_id, message):
		id = execute_query(
			"insert into \"chat_log_message\" (chat_log_id, user_id, message) values (%s, %s, %s) returning id", (chat_log_id, user_id, message)
		)
		return id

	@staticmethod
	def get_by_chat_log_id(chat_log_id, message_id_offset=0):
		messages = map_query_to_class(execute_query(
			"select * from \"chat_log_message\" where chat_log_id=%s and id > %s", (chat_log_id, message_id_offset)
		), ChatLogMessage)
		return messages


	@staticmethod
	def get_count_by_chat_log_id_since(chat_log_id, message_id_offset):
		count = execute_query(
			"select count(*) from \"chat_log_message\" where chat_log_id=%s and id > %s", (chat_log_id, message_id_offset)
		)
		return count[0]['count']