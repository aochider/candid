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
			"select * from \"position\""
			" left join \"user_position\" on \"user_position\".position_id = \"position\".id"
			" and \"user_position\".user_id = %s"
			" where \"position\".status = 'active' and \"position\".creator_user_id != %s and \"user_position\".position_id is null"
			" order by random() limit %s", (user_id, user_id, limit)
		), Position)
		return positions