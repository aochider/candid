import time
from flask import request

from app.models.user_position import UserPosition

def register_routes(app):
	@app.route('/user_position/position/<int:position_id>/respond', methods=['POST'])
	def respond(position_id):
		# TODO stored a logged in user in flask somehow
		user_id = 4

		data = request.get_json()
		id = UserPosition.respond(user_id, position_id, data['result'])
		return {'id': id}