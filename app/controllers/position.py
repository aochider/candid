import time
from flask import request

from app.decorators import auth, validate
from app.errors import *
from app.models.position import Position
from app.models.user import User
from app.models.user_position import UserPosition

def register_routes(app):
	@app.route('/position/queue', methods=['GET'])
	@auth(min_role=User.USER_ROLE_NORMAL)
	def get_position_queue():
		user_id = request.user.id
		# TODO validate user_id
		positions = Position.get_queue(user_id)
		positions = [{"id": pos.id, "statement": pos.statement} for pos in positions]
		return {"positions": positions}