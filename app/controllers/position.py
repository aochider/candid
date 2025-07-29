import time
from flask import request

from app.models.position import Position
from app.models.user_position import UserPosition

def register_routes(app):
	@app.route('/position/queue')
	def get_queue_positions():
		# TODO stored a logged in user in flask somehow
		user_id = 4
		positions = Position.get_queue(user_id)
		positions = [{"id": pos.id, "statement": pos.statement} for pos in positions]
		return {"positions": positions}

	@app.route('/position/<int:position_id>/respond', methods=['POST'])
	def respond(position_id):
		# TODO stored a logged in user in flask somehow
		user_id = 4

		data = request.get_json()
		print(data, flush=True)
		position = UserPosition.respond(user_id, position_id, data['result'])
		return {'success': True}