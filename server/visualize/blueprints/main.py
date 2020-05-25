"""
This module contains the logik for the calls that are related to the reader role.
The url for the calls in this module is http://127.0.0.1:5000/<route>
"""

# Standard flask libraries
from flask import Blueprint, request
# Handle authorization
from flask_jwt_extended import (
	jwt_required, create_access_token, get_raw_jwt

)

# Help functions for validation and simplifications
from visualize.help_functions import *
from visualize.models import Admin, Approver, blacklist
# The database structure
from visualize.models.reader import Reader

main_bp = Blueprint('main', __name__)


@main_bp.route("/login", methods=["POST"])
def login():
	"""
	Logs in the reader and returns an access token
	if email and password matches in the database.
	"""

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Gets the email and password from the client
	email = request.json.get("email")
	password = request.json.get("password")

	if not email:
		return bad_request("The email field can not be empty")
	if not password:
		return bad_request("The password field can not be empty")

	reader = Reader.query.filter_by(email=email).first()

	# If non existing email
	if not reader:
		return bad_request("ERROR: Email not registered.")

	# If wrong password
	if not reader.check_password(password):
		return bad_request("ERROR: Wrong password.")

	approver = Approver.query.filter_by(reader_id=reader.id).first()
	admin = Admin.query.filter_by(approver_id=reader.id).first()

	# Gets the users role
	role = "reader"
	if approver:
		role = "approver"
	if admin:
		role = "admin"

	# Create the users access token
	token = create_access_token(identity=email)

	json = {"access_token": token, "email": reader.email, "name": reader.name, "surname": reader.surname, "role": role}
	return ok(json)


@main_bp.route('/logout', methods=["POST"])
@jwt_required
def logout_user():
	print("logout")
	jti = get_raw_jwt()['jti']
	blacklist.add_jti_to_blacklist(str(jti))
	return ok("logged out")

