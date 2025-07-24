import time

from app.models.chat_log import ChatLog

def register_routes(app):
	@app.route('/chat_log/position/<int:position_id>/responder_user/<int:responder_user_id>')
	def get_chat_logs(position_id, responder_user_id):
		messages = ChatLog.get(position_id, responder_user_id)
		messages = [{"position_id": msg.position_id, "responder_user_id": msg.responder_user_id, "message": msg.message} for msg in messages]
		return {"messages": messages}

	@app.route('/chat_log/position/<int:position_id>/responder_user/<int:responder_user_id>/message_offset/<int:message_id_offset>')
	def get_chat_logs_since(position_id, responder_user_id, message_id_offset):
		timeout = app.config.get('LONG_POLL_TIMEOUT')
		start_time = time.time()

		while ((time.time() - start_time) < timeout):
			count = ChatLog.get_count_since(position_id, responder_user_id, message_id_offset)

			if count > 0:
				messages = ChatLog.get(position_id, responder_user_id, message_id_offset)
				messages = [{"id": msg.id, "position_id": msg.position_id, "responder_user_id": msg.responder_user_id, "message": msg.message} for msg in messages]
				return {"messages": messages}
			else:
				time.sleep(1)