from app.common import getDb, buildReponse, checkCORS

def earlyEmailSignup(request):

	cors = checkCORS(request)
	if cors:
		return cors

	request_json = request.get_json()
	print(request_json)
	if "email" in request_json and request.method == 'POST':

		with getDb().connect() as conn:
			query = "INSERT into early_signups VALUES (NULL, '%s')" % request_json["email"]
			print("Executing %s" % query)
			conn.execute(query)
	
		return buildReponse('', 200)
	else:
		return buildReponse('', 400)
