import time
from flask import request

from app.decorators import auth, validate
from app.models.user import User
from app.models.user_position import UserPosition

def register_routes(app):
	@app.route('/user_position/position/<int:position_id>/respond', methods=['POST'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	@validate({
		"type": "object",
		"properties": {
			"result": {"type": "string"}
		},
		"required": ["result"],
	})
	def respond(position_id):
		data = request.get_json()

		# TODO validate user_id and position_id
		user_id = request.user.id

		id = UserPosition.respond(user_id, position_id, data['result'])
		return {'id': id}