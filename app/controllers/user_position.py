import time
from flask import request

from app.decorators import auth, validate
from app.errors import *
from app.models.position import Position
from app.models.user import User
from app.models.user_position import UserPosition

def register_routes(app):
	@app.route('/user_position/position/<int:position_id>', methods=['POST'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	@validate({
		"type": "object",
		"properties": {
			"result": {
				"type": "string",
				"enum": UserPosition.RESULTS,
			}
		},
		"required": ["result"],
	})
	def create_user_position(position_id):
		data = request.get_json()
		result = data.get('result')

		user_id = request.user.id

		if not Position.exists_by_id(position_id):
			raise INVALID_USER_POSITION_POSITION

		id = UserPosition.create(user_id, position_id, result)

		return {'id': id}