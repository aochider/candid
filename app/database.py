import psycopg
from psycopg_pool import ConnectionPool

from app.errors import *

db_pool = None

def connect_to_db(config):
	global db_pool

	# let this fail if there is an error. we want the server to not start up if this doesnt work.
	#db = psycopg.connect(config['SQLALCHEMY_DATABASE_URI'])
	print("Database pool established.")
	db_pool = ConnectionPool(conninfo=config['SQLALCHEMY_DATABASE_URI'], min_size=100, open=True)


def execute_query(query, params=None):
	if db_pool is None:
		print("Database pool not established. Call connect_to_db() first.")
		return None

	is_select = query.strip().upper().startswith("SELECT")
	is_insert = query.strip().upper().startswith("INSERT")
	with db_pool.connection() as conn:
		with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
			try:
				cur.execute(query, params)
				retval = None
				if is_select:
					retval = cur.fetchall()
				if is_insert:
					retval = cur.fetchone()['id']

				conn.commit()
				return retval
			except psycopg.Error as ee:
				conn.rollback()
				raise ee

def map_query_to_class(rows, target_class):
	results = []

	if rows:
		for row in rows:
			instance = target_class()

			for col, val in row.items():
				# TODO use reflection to make this safer. we only want to map to attributes that are actually
				# on the class. better yet, we should find a way to flag attributes as being mapped from the db.
				setattr(instance, col, val)

			results.append(instance)

	return results