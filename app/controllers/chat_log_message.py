import time
from flask import request

from app.decorators import auth, validate
from app.models.chat_log_message import ChatLogMessage
from app.models.user import User

def register_routes(app):
	@app.route('/chat_log_message/chat_log/<int:chat_log_id>', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_chat_log_messages(chat_log_id):
		user_id = request.user.id
		# TODO validate that the user is part of the chat_log_id
		messages = ChatLogMessage.get(chat_log_id)
		messages = [{"id": msg.id, "chat_log_id": msg.chat_log_id, "user_id": msg.user_id, "message": msg.message} for msg in messages]
		return {"messages": messages}

	@app.route('/chat_log_message/chat_log/<int:chat_log_id>/message_offset/<int:message_id_offset>', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_chat_log_messages_since(chat_log_id, message_id_offset):
		user_id = request.user.id
		# TODO validate that user_id belongs to chat_log_id

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

		return {"messages": []}

	@app.route('/chat_log_message/chat_log/<int:chat_log_id>', methods=['POST'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	@validate({
		"type": "object",
		"properties": {
			"message": {"type": "string", "minLength": 1, "maxLength": 200},
		},
		"required": ["message"],
	})
	def create_chat_log_messages(chat_log_id):
		data = request.get_json()

		message = data['message']
		user_id = request.user.id
		# TODO validate that user_id belongs to chat_log_id

		id = ChatLogMessage.create(chat_log_id, user_id, message)
		return {"id": id}