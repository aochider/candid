import time

from app.models.chat_log_message import ChatLogMessage

def register_routes(app):
	@app.route('/chat_log_message/chat_log/<int:chat_log_id>')
	def get_chat_log_messages(chat_log_id):
		messages = ChatLogMessage.get(chat_log_id)
		messages = [{"id": msg.id, "chat_log_id": msg.chat_log_id, "user_id": msg.user_id, "message": msg.message} for msg in messages]
		return {"messages": messages}

	@app.route('/chat_log_message/chat_log/<int:chat_log_id>/message_offset/<int:message_id_offset>')
	def get_chat_log_messages_since(chat_log_id, message_id_offset):
		timeout = app.config.get('LONG_POLL_TIMEOUT')
		start_time = time.time()

		while ((time.time() - start_time) < timeout):
			count = ChatLogMessage.get_count_since(chat_log_id, message_id_offset)

			if count > 0:
				messages = ChatLogMessage.get(chat_log_id, message_id_offset)
				messages = [{"id": msg.id, "chat_log_id": msg.chat_log_id, "user_id": msg.user_id, "message": msg.message} for msg in messages]
				return {"messages": messages}
			else:
				time.sleep(1)