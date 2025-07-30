import time

from app.models.chat_log import ChatLog

def register_routes(app):
	@app.route('/chat_log/position/<int:position_id>', methods=['POST'])
	def create(position_id):
		# TODO get user id from flask auth or something
		responder_user_id = 4
		id = ChatLog.create(position_id, responder_user_id)
		return {"id": id}