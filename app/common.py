import sqlalchemy
import pymysql
import os
from mailchimp3 import MailChimp

is_prod = os.environ.get("IS_PROD") == "1"
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
mailchimp_api_key = os.environ.get("MAILCHIMP_API_KEY")

cloud_sql_connection_name = "uwenca:us-central1:energyhacks-2020"

# Database common
db = None
class MockDb:
	def __init__(self):
		print("Using Mock DB")
		self.queries = []

	def connect(self):
		return self

	def __enter__(self):
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
				host=db_host if os.name == 'nt' else None,
				username=db_user,
				password=db_pass,
				database=db_name,
				query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)} if os.name != "nt" else {},
			),
		)
	else:
		db = MockDb()

	return db

# Web request common
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

# Mailchimp common
class MockMailchimpClient:
	def __init__(self):
		print("Using Mock Mailchimp Client")
		self.lists = self
		self.members = self
		self.lastDataAdded = None

	def create(self, list_id, data):
		self.lastDataAdded = data

mailchimpClient = None

def getMailchimpClient():
	global mailchimpClient
	if mailchimpClient:
		return mailchimpClient
	
	if is_prod:
		mailchimpClient = MailChimp(mc_api=mailchimp_api_key)
	else:
		mailchimpClient = MockMailchimpClient()

	return mailchimpClient
