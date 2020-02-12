from app.common import getDb, buildReponse, checkCORS, getMailchimpClient

earlySignupList = "2f3ef0ad67"

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

		print(getMailchimpClient().lists.members.create(list_id=earlySignupList, data={
			"email_address": request_json["email"],
			"status":"subscribed"
		}))
	
		return buildReponse('', 200)
	else:
		return buildReponse('', 400)
