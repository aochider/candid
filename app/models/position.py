from app.database import db

class Position():
	# TODO what values are possible?
	POSITION_STATUSES = ['active', 'inactive']

	def __init__(self):
		self.id = None
		self.creator_user_id = None
		self.position_category_id = None
		self.location_id = None
		self.statement = None
		self.created_time = None
		self.status = None

	def __repr__(self):
		return '<Position %r>' % self.id