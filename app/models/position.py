from app.database import db, execute_query, map_query_to_class

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

	@staticmethod
	def get_queue(user_id):	
		limit = 10
		positions = map_query_to_class(execute_query(
			# TODO come up with something other than random order
			# TODO2 think of another way instead of the `not in`, thats gonna be slow and might hit a limit
			"select * from \"position\""
			" where \"position\".status = 'active' and \"position\".creator_user_id != %s and \"position\".id not in"
			" (select position_id from \"user_position\" where user_id=%s)"
			" order by random() limit %s", (user_id, user_id, limit)
		), Position)
		return positions