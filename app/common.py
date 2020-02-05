import sqlalchemy
import pymysql
import os

is_prod = os.environ.get("IS_PROD") == "1"
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

db = None

class MockDb:
	def __init__(self):
		print("Using Mock DB")
		self.queries = []

	def connect(self):
		print("TEST")
		return self

	def __enter__(self):
		print("TEST")
		return self

	def __exit__(self, type, value, traceback):
		return None

	def execute(self, qeury):
		self.queries.append(qeury)

def getDb():
	global db
	if db:
		return db

	if is_prod:
		db = sqlalchemy.create_engine(
			sqlalchemy.engine.url.URL(
				drivername="mysql+pymysql",
				host="35.202.67.125" if os.name == 'nt' else None,
				username=db_user,
				password=db_pass,
				database=db_name,
				query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)} if os.name != "nt" else {},
			),
		)
	else:
		db = MockDb()

	return db

def buildReponse(message, code):
	return (message, code, {'Access-Control-Allow-Origin': '*'})

def checkCORS(request):
	if request.method == 'OPTIONS':
		# Allows GET requests from any origin with the Content-Type
		# header and caches preflight response for an 3600s
		headers = {
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET',
			'Access-Control-Allow-Headers': 'Content-Type',
			'Access-Control-Max-Age': '3600'
		}
		return ('', 204, headers)
	return None