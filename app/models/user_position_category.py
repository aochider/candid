from app.database import db

class UserPositionCategory():
	def __init__(self):
		self.id = None
		self.user_id = None
		self.position_category_id = None
		self.priority = None

	def __repr__(self):
		return '<UserPositionCategory %r>' % self.id