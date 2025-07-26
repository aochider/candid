import time

from app.models.position import Position

def register_routes(app):
	@app.route('/position/queue')
	def get_queue_positions():
		# TODO stored a logged in user in flask somehow
		user_id = 4
		positions = Position.get_queue(user_id)
		positions = [{"id": pos.id, "statement": pos.statement} for pos in positions]
		return {"positions": positions}