import time
from flask import request

from app.decorators import auth, validate
from app.errors import *
from app.models.chat_log import ChatLog
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
		# TODO validate user_id and position_id
		id = ChatLog.create(position_id, responder_user_id)
		return {"id": id}

	@app.route('/chat_log/<int:chat_log_id>', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_chat_log_by_id(chat_log_id):
		user_id = request.user.id
		# TODO validate user_id has access to chat log
		chat_log = ChatLog.get_by_id(chat_log_id)
		# TODO check len
		ret = {
			"id": chat_log[0].id,
			"position_id": chat_log[0].position_id,
			"creator_user_id": chat_log[0].creator_user_id,
			"statement": chat_log[0].statement
		}
		return ret

	@app.route('/chat_log', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_chat_log_by_user_id():
		user_id = request.user.id
		chat_logs = ChatLog.get_by_user_id(user_id)
		logs = [{"id": cl.id} for cl in chat_logs]
		return {"chat_logs": logs}