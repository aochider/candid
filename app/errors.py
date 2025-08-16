
class InternalException(Exception):
	def __init__(self, message=''):
		self.message = message

class ValidationException(Exception):
	def __init__(self, code, message=''):
		self.code = code
		self.message = message

INVALID_JSON_BODY = ValidationException(10001, 'request body must be json')
INVALID_JSON_SCHEMA = ValidationException(10002, 'error') # message overwritten in dynamically from the json schema result
INVALID_CREDENTIALS = ValidationException(10004, 'must have valid authentication and authorization')

INVALID_USER_POSITION_POSITION = ValidationException(20001, 'must be a valid position_id')

INVALID_USER_LOGIN = ValidationException(30001, 'must be a valid email and password')
INVALID_USER_TOKEN = ValidationException(30002, 'must be a valid token')

INVALID_CHAT_LOG_ID = ValidationException(40001, 'must be a valid chat log')



