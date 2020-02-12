from unittest.mock import Mock
from app.functions.earlyEmailSignup import earlyEmailSignup
from app.common import getDb, getMailchimpClient

def test_addsEmailToSignupDatabase():
	req = Mock(get_json=Mock(return_value={"email": "jamiexxyyzz@gmail.com"}), method="POST")
	earlyEmailSignup(req)

	# Must be added to our database and to mailchimps side
	assert(getDb().queries[0] == "INSERT into early_signups VALUES (NULL, 'jamiexxyyzz@gmail.com')")
	assert(getMailchimpClient().lastDataAdded["email_address"] == "jamiexxyyzz@gmail.com")
