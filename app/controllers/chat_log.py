import time
from flask import request

from app.decorators import auth, validate
from app.errors import *
from app.models.chat_log import ChatLog
from app.models.position import Position
from app.models.user import User

def register_routes(app):
	@app.route('/chat_log/position/<int:position_id>', methods=['POST'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	@validate({
		"type": "object",
		"properties": {
		},
		"required": [],
	})
	def create_chat_log(position_id):
		responder_user_id = request.user.id

		if not Position.exists_by_id(position_id):
			raise INVALID_USER_POSITION_POSITION

		id = ChatLog.create(position_id, responder_user_id)
		return {"id": id}

	@app.route('/chat_log/<int:chat_log_id>', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_chat_log_by_id(chat_log_id):
		user_id = request.user.id

		chat_logs = ChatLog.get_by_id(chat_log_id)

		if len(chat_logs) != 1:
			raise INVALID_CHAT_LOG_ID

		chat_log = chat_logs[0]

		if user_id not in [chat_log.creator_user_id, chat_log.responder_user_id]:
			raise INVALID_CHAT_LOG_ID

		ret = {
			"id": chat_log.id,
			"position_id": chat_log.position_id,
			"creator_user_id": chat_log.creator_user_id,
			"responder_user_id": chat_log.responder_user_id,
			"statement": chat_log.statement
		}
		return ret

	@app.route('/chat_log', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_chat_log_by_user_id():
		user_id = request.user.id
		chat_logs = ChatLog.get_by_user_id(user_id)
		logs = [{"id": cl.id} for cl in chat_logs]
		return {"chat_logs": logs}