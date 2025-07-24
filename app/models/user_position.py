from app.database import db

class UserPosition():
	RESULTS = ['agree', 'disagree', 'pass', 'chat']

	def __init__(self):
		self.id = None
		self.user_id = None
		self.position_id = None
		self.result = None

	def __repr__(self):
		return '<UserPosition %r>' % self.id