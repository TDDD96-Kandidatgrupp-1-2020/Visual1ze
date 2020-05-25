"""
This module contains helper functions containing
small functions that are helpful in multiple places in the project.
"""
import re


def error(message):
	"""Creates a json error with given status code"""
	return {"error": message}


def ok(message):
	"""
	It indicates that the REST API successfully carried out whatever action the client
	requested and that no more specific code in the 2xx series is appropriate.
	"""
	return message, 200


def created(message):
	"""
	A REST API responds with the 201 status code whenever a resource is created inside a collection.
	There may also be times when a new resource is created as a result of some controller action,
	in which case 201 would also be an appropriate response.
	"""
	return message, 201


def accepted(message):
	"""
	A 202 response is typically used for actions that take a long while to process.
	It indicates that the request has been accepted for processing,
	but the processing has not been completed. The request might or might not be
	eventually acted upon, or even maybe disallowed when processing occurs.
	"""
	return message, 202


def no_content(message):
	"""
	The 204 status code is usually sent out in response to a PUT,
	POST, or DELETE request when the REST API declines to send back
	any status message or representation in the response message’s body.
	"""
	return message, 204


def bad_request(message):
	"""
	400 is the generic client-side error status,
	used when no other 4xx error code is appropriate.
	Errors can be like malformed request syntax,
	invalid request message parameters, or deceptive request routing etc.
	"""
	return error(message), 400


def unauthorized(message):
	"""
	A 401 error response indicates that the client tried to operate on a
	protected resource without providing the proper authorization.
	It may have provided the wrong credentials or none at all. The response must
	include a WWW-Authenticate header field containing a challenge applicable to the requested resource.
	"""
	return error(message), 401


def validate_password(password):
	"""
	Checks if the password has the right format.
	If not returns the things that needs to be changed in a list.
	"""
	not_fulfilled = []
	try:
		password.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		not_fulfilled.append("Password contains illegal characters. ")
	if len(password) < 6:
		not_fulfilled.append("Password must be 6 characters or longer. ")
	if not re.search("[a-z]", password):
		not_fulfilled.append("Password must contain at least one lowercase letter. ")
	if not re.search("[A-Z]", password):
		not_fulfilled.append("Password must contain at least one uppercase letter. ")
	if not re.search("[0-9]", password):
		not_fulfilled.append("Password must contain at least one number. ")

	# If the password should not contain spaces
	# if re.search("\s", password):
	return not_fulfilled
