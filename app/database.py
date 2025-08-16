import psycopg2
import psycopg2.extras

from app.errors import *

db = None

def connect_to_db(config):
	global db

	# let this fail if there is an error. we want the server to not start up if this doesnt work.
	db = psycopg2.connect(config['SQLALCHEMY_DATABASE_URI'])
	print("Database connection established.")

def execute_query(query, params=None):
	if db is None:
		print("Database connection not established. Call connect_to_db() first.")
		return None

	try:
		is_select = query.strip().upper().startswith("SELECT")
		is_insert = query.strip().upper().startswith("INSERT")
		with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
			cur.execute(query, params)
			retval = None
			if is_select:
				retval = cur.fetchall()
			if is_insert:
				retval = cur.fetchone()['id']

			db.commit()
			return retval
	except psycopg2.Error as ee:
		db.rollback()
		raise ee

def close_db_connection():
	global db
	if db:
		db.close()
		print("Database connection closed.")
		db = None

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