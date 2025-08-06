import time
from flask import request

from app.decorators import auth, validate
from app.models.chat_log import ChatLog
from app.models.user import User

def register_routes(app):
	@app.route('/chat_log/position/<int:position_id>', methods=['POST'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	@validate({
		"type": "object",
		"properties": {
			"result": {"type": "string"}
		},
		"required": ["result"],
	})
	def create(position_id):
		responder_user_id = request.user.id
		# TODO validate user_id and position_id
		id = ChatLog.create(position_id, responder_user_id)
		return {"id": id}