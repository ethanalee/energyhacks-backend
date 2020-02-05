from unittest.mock import Mock
from app.functions.earlyEmailSignup import earlyEmailSignup
from app.common import getDb

def test_addsEmailToSignupDatabase():
	req = Mock(get_json=Mock(return_value={"email": "test@gmail.com"}), method="POST")
	earlyEmailSignup(req)
	assert(getDb().queries[0] == "INSERT into early_signups VALUES ('test@gmail.com')")
