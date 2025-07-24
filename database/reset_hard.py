import os
import psycopg2
import glob

# Global variable to store the database connection
db = None

def connect_to_db():
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')

	"""Establishes a global database connection."""
	global db
	try:
		db = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
		print("Database connection established.")
	except psycopg2.Error as e:
		print(f"Error connecting to database: {e}")

def execute_query(query, params=None):
	"""Executes a SQL query using the global connection."""
	if db is None:
		print("Database connection not established. Call connect_to_db() first.")
		return None

	try:
		with db.cursor() as cur:
			cur.execute(query, params)
			db.commit()  # Commit changes for DML operations
			if query.strip().upper().startswith("SELECT"):
				return cur.fetchall()
			else:
				return None  # No rows to fetch for DML
	except psycopg2.Error as e:
		print(f"Error executing query: {e}")
		db.rollback()  # Rollback changes on error
		return None

def close_db_connection():
	"""Closes the global database connection."""
	global db
	if db:
		db.close()
		print("Database connection closed.")
		db = None

# Example Usage:
if __name__ == "__main__":
	connect_to_db()

	tables = execute_query("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
	print(tables)

	for table in tables:
		execute_query(f"DROP TABLE IF EXISTS \"{table[0]}\" CASCADE")

	directory_path = os.path.dirname(os.path.abspath(__file__)) + "/sql" # Replace with your directory

	for filename in glob.glob(os.path.join(directory_path, "*.sql")):
		with open(filename, 'r') as file:
			content = file.read()

			# Select data
			users = execute_query(content)
			print(users)

	close_db_connection()