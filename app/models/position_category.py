from app.database import execute_query

class PositionCategory():
	POSITION_CATEGORY_LABELS = ['foo', 'bar', 'baz']

	def __init__(self):
		self.id = None
		self.label = None

	def __repr__(self):
		return '<PositionCategory %r>' % self.id