"""
This module contains the logic for the calls that are related to the reader role.
The url for the calls in this module is http://127.0.0.1:5000/admin/<route>
"""
import pickle

# Standard flask libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token

# Logical database operators
from sqlalchemy import and_, or_

# Help functions for validation and simplifications
from visualize.help_functions import ok, bad_request, created, validate_password
from visualize import validator

# The database structure
from visualize.models import db, AccessGroup, Reader, Approver, Admin, Room, RoomRequest, AccessGroupRequest, \
	ResponsibleForAg, ResponsibleForRoom, CardReader, ApprovesAgRequest, \
	gives_access_to, ApprovesRoomRequest

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request  # before_request is run before every request in blueprint route
@jwt_required
def is_admin():
	""" Checks if the request comes from a user that is admin."""
	try:
		email = decode_token(request.headers.get('Authorization')[7:])["identity"]

		current_admin = Admin.query.filter_by(email=email).first()
	except IndexError:
		return bad_request("User is not an admin")

	if current_admin is None:
		return bad_request("User is not an admin")


@admin_bp.route("/upgrade_to_approver", methods=["POST"])
def upgrade_to_approver():
	schema = {
		"email": {"type": "string"},
	}

	email = request.json.get("email")

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	reader_to_upgrade = Reader.query.filter_by(email=email).first()

	if not reader_to_upgrade:
		return bad_request("No user with email {0} exists.".format(email))

	if Approver.query.filter_by(reader_id=reader_to_upgrade.id).first() is not None:
		return bad_request("User with email {0} already have the role of approver (at least).".format(email))

	# Insert a new row in the Approver table, where reader_id is set to that of the specified reader.
	# To circumvent Flask object problems (inheritance etc.), this is done in "pure" SQL syntax.
	db.session.execute("INSERT INTO approver (reader_id) VALUES ({0});".format(reader_to_upgrade.id))
	db.session.commit()

	return ok("Reader is now an approver!")


@admin_bp.route("/upgrade_to_admin", methods=["POST"])
def upgrade_to_admin():

	schema = {
		"email": {"type": "string"},
	}

	email = request.json.get("email")

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	# Check if user is already an admin.
	if Admin.query.filter_by(email=email).first() is not None:
		return bad_request("User with email {0} already have the role of admin.".format(email))

	approver_to_upgrade = Approver.query.filter_by(email=email).first()

	# If not already, upgrade user to an approver.
	if not approver_to_upgrade:
		reader_to_upgrade = Reader.query.filter_by(email=email).first()
		if not reader_to_upgrade:
			return bad_request("No user with email {0} exists.".format(email))
		# Insert a new row in the Approver table, where reader_id is set to that of the specified reader.
		# To circumvent Flask object problems (inheritance etc.), this is done in "pure" SQL syntax.
		db.session.execute("INSERT INTO approver (reader_id) VALUES ({0});".format(reader_to_upgrade.id))
		# The user should now exist as an approver in the database.
		approver_to_upgrade = Approver.query.filter_by(email=email).first()

	# Insert a new row in the Admin table, where reader_id is set to that of the specified approver.
	# To circumvent Flask object problems (inheritance etc.), this is done in "pure" SQL syntax.
	db.session.execute("INSERT INTO admin (approver_id) VALUES ({0});".format(approver_to_upgrade.id))
	db.session.commit()

	return ok("User is now an admin!")


@admin_bp.route("/map", methods=["POST"])
def save_map():
	"""Saves the representation of the map in locale file"""
	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	pickle.dump(request.json, open("map_repr.pickle", "wb"))
	return ok("File has been saved!")


@admin_bp.route("/ag", methods=["POST"])
def create_ag():
	"""Creates a new (or changes an already existing) access group"""
	# name: The (String) name of the access group, as will be displayed.
	# approvers: a list of email addresses belonging to approvers.
	# rooms: a list of room text_ids.
	schema = {
		"ag_name": {"type": "string", "minlength": 2},
		"approvers": {"type": "list", "schema": {"type": "string", "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"}},
		"room_text_ids": {"type": "list", "schema": {"type": "string", "minlength": 2}},
	}

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	ag_name = request.json.get("ag_name")
	approvers = request.json.get("approvers")
	room_text_ids = request.json.get("room_text_ids")

	if not approvers:
		return bad_request("The list of approvers can not be empty!")

	if not room_text_ids:
		return bad_request("The list of rooms can not be empty!")

	# If the access group DOES NOT exist create it
	ag = AccessGroup.query.filter_by(name=ag_name).first()
	if not ag:
		ag = AccessGroup(name=ag_name)
		db.session.add(ag)

	# If the access group DOES exist remove the existing card readers and approvers,
	# Move all currently tasked requests to the first new approver
	else:
		ag.card_readers.clear()
		ag.approvers.clear()
		approver = Approver.query.filter_by(email=approvers[0]).first()
		if not approver:
			return bad_request("Approver does not exist!")
		for agr in AccessGroupRequest.query.filter_by(ag_id=ag.id).all():
			aagr = ApprovesAgRequest.query.filter_by(ag_request_id=agr.id).first()
			aagr.approver_id = approver.id

	# update approves_ag_request by taking all request_ids from ag request with this ag_id
	# change the approver id in approves request to the new approver with the highest priority
	priority = 1 # First approver in list get highest priority, and so on.
	for approver_email in request.json.get("approvers"):
		approver = Approver.query.filter_by(email=approver_email).first()
		if not approver:
			return bad_request("Approver does not exist!")
		rfag = ResponsibleForAg(approver=approver, ag=ag, priority=priority) # Add and commit?
		db.session.add(rfag)
		priority += 1

	# Check if all rooms does exist
	list_of_rooms = []
	for room_text_id in room_text_ids:
		room = Room.query.filter_by(text_id=room_text_id).first()
		if not room:
			return bad_request("Room {} does not exist!".format(room_text_id))
		list_of_rooms.append(room)

	# Get a list of all card readers that link the rooms together
	list_of_room_ids = [room.id for room in list_of_rooms]
	list_of_card_readers = CardReader.query.filter(
		and_(
			CardReader.room_b_id.in_(list_of_room_ids),
			CardReader.room_a_id.in_(list_of_room_ids)
		)
	).all()

	# Check if the rooms are connected to eachother by card readers
	temp_rooms = Room.query.filter(Room.id.in_([cr.room_b_id for cr in list_of_card_readers])).all()
	requested_rooms = [room.text_id for room in list_of_rooms]
	resulting_rooms = [room.text_id for room in temp_rooms]
	diff = [room for room in requested_rooms if room not in resulting_rooms]
	if diff:
		return bad_request("The room(s) {} has no card readers connecting to the rest of the rooms!".format(diff))

	ag.card_readers = list_of_card_readers
	db.session.commit()
	return ok("Access Group was successfully created!")


@admin_bp.route("/reader/<string:reader_id>", methods=["GET"])
def get_reader(reader_id):
	"""Returns a reader with given id."""

	# Checks if the reader exist in the database
	reader = Reader.query.filter_by(id=reader_id).first()
	if not reader:
		return bad_request("Reader does not exist!")

	return reader.serialize


@admin_bp.route("approvers/", methods=["GET"])
def get_all_approvers():
	"""Returns all existing approvers in the database."""
	return {"approvers": [ap.serialize for ap in Approver.query.all()]}, 200


@admin_bp.route("admins/", methods=["GET"])
def get_all_admins():
	"""Returns all existing admins in the database."""
	return {"admin": [ad.serialize for ad in Admin.query.all()]}, 200


@admin_bp.route("/rooms", methods=["GET"])
def get_all_rooms():
	"""Returns all existing rooms in the database."""
	return {"rooms": [room.text_id for room in Room.query.all()]}, 200


@admin_bp.route("user/<reader_email>", methods=["DELETE"])
def delete_user(reader_email):
	"""Permanently deletes a reader, approver or admin and all attached information from the database."""
	reader = Reader.query.filter_by(email=reader_email).first()
	email = get_jwt_identity()

	if not reader:
		return bad_request("Reader {} does not exist.".format(reader_email))

	if reader_email == email:
		return bad_request("Deleting own account not allowed.")  # a safety to prevent the system from having no admins

	approver = Approver.query.filter_by(reader_id=reader.id).first()
	admin = Admin.query.filter_by(approver_id=reader.id).first()

	if admin:
		db.session.delete(admin)
	elif approver:
		db.session.delete(approver)  # TODO move approvals to next approver
	else:
		db.session.delete(reader)

	db.session.commit()

	return ok("Reader was successfully deleted")


@admin_bp.route("/card/<email>", methods=["DELETE"])
def remove_card(email):

	reader = Reader.query.filter_by(email=email).first()

	if not reader:
		return bad_request("No reader with email {}.".format(email))

	if not reader.card_id:
		return bad_request("Card has already been cleared.")

	reader.block_card()
	db.session.commit()

	return ok("Card for reader was cleared.")


@admin_bp.route("/reader", methods=["POST"])
def create_reader():
	"""Creates a new reader and adds to the database if correct input is given."""
	return create_user(Reader)


@admin_bp.route("/approver", methods=["POST"])
def create_approver():
	"""Creates a new reader and adds to the database if correct input is given."""
	return create_user(Approver)


@admin_bp.route("/admin", methods=["POST"])
def create_admin():
	"""Creates a new admin and adds to the database if correct input is given."""
	return create_user(Admin)


def create_user(Role):
	"""Creates a new user and adds to the database if correct input is given."""

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	schema = {
		"email": {"type": "string", "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"},
		"name": {"type": "string", "regex": "[a-zA-Z]+$", "minlength": 2, "maxlength": 12},
		"surname": {"type": "string", "regex": "[a-zA-Z]+$", "minlength": 2, "maxlength": 12},
		"password": {"type": "string"}
	}

	# Checks if input is illegal
	if not validator(request.json, schema):
		s = validator
		return bad_request(validator.errors)

	# Get the email, password, name and surname from the client
	email = request.json.get("email")
	password = request.json.get("password")
	name = request.json.get("name")
	surname = request.json.get("surname")

	# Checks if the email already is in use
	if Reader.query.filter_by(email=email).first() is not None:
		return bad_request("This email is already in use!")

	# Checks if the password is illegal
	not_fulfilled = validate_password(password)
	if not_fulfilled:
		return bad_request({"password": not_fulfilled})

	# Returns a new user
	new_user = Role(email=email, password=password, name=name, surname=surname)
	db.session.add(new_user)
	db.session.commit()
	return created("{} successfully created!".format(Role.__tablename__.capitalize()))


@admin_bp.route("/readers", methods=["GET"])
def get_all_readers_roles():
	"""Returns a list of all the readers names and email"""
	admins = [{"name": x.name, "surname": x.surname, "email": x.email, "card_id": x.card_id} for x in Admin.query.all()]
	approvers = [{"name": x.name, "surname": x.surname, "email": x.email, "card_id": x.card_id} for x in Approver.query.all()]
	readers = [{"name": x.name, "surname": x.surname, "email": x.email, "card_id": x.card_id} for x in Reader.query.all()]

	# Removes the users which are not only readers
	new_readers = []
	for reader in readers:
		if reader not in approvers:
			reader["role"] = "reader"
			new_readers.append(reader)

	new_approvers = []
	# Removes the users which are not only approvers
	for approver in approvers:
		if approver not in admins:
			approver["role"] = "approver"
			new_approvers.append(approver)

	for admin in admins:
		admin["role"] = "admin"

	return ok({"users": new_readers + new_approvers + admins})


@admin_bp.route("/orders", methods=["GET"])
def get_all_orders():
	"""Returns a list of ALL the orders for rooms and AGs, with reader and approver specified for each."""

	# Get a list of all the orders of access groups of all responsible approvers.
	ag_relation = ApprovesAgRequest.query \
		.join(AccessGroupRequest, AccessGroupRequest.id == ApprovesAgRequest.ag_request_id) \
		.join(Reader, Reader.id == AccessGroupRequest.reader_id) \
		.join(AccessGroup, AccessGroup.id == AccessGroupRequest.ag_id).all()
	ag_orders = []
	for ag in ag_relation:
		# Gets all the rooms in the access group
		room_relation = Room.query \
			.join(CardReader, CardReader.room_b_id == Room.id) \
			.join(gives_access_to, gives_access_to.c.cr_id == CardReader.id) \
			.filter_by(ag_id=ag.ag_request.ag.id)
		json = {
			"type": "AG",
			"rooms": [room.text_id for room in room_relation],
			"reader": {
				"email": ag.ag_request.reader.email,
				"name": ag.ag_request.reader.name,
				"surname": ag.ag_request.reader.surname
			},
			"approver": {
				"email": ag.ag_request.request_approver.approver.email,
				"name": ag.ag_request.request_approver.approver.name,
				"surname": ag.ag_request.request_approver.approver.surname
			},
			"access_name": ag.ag_request.ag.name,
			"request_id": ag.ag_request.id,
			"ag_id": ag.ag_request.ag.id,
			"justification": ag.ag_request.justification,
			"requested_datetime": ag.ag_request.datetime_requested.strftime('%Y-%m-%d')
		}
		ag_orders.append(json)

	# Get a list of all the orders of rooms this approver is responsible for.
	room_relation = ApprovesRoomRequest.query \
		.join(RoomRequest, RoomRequest.id == ApprovesRoomRequest.room_request_id) \
		.join(Reader, Reader.id == RoomRequest.reader_id) \
		.join(Room, Room.id == RoomRequest.room_id).all()
	room_orders = [
		{
			"type": "Room",
			"reader": {
				"email": x.room_request.reader.email,
				"name": x.room_request.reader.name,
				"surname": x.room_request.reader.surname,
			},
			"approver": {
				"email": x.room_request.request_approver.approver.email,
				"name": x.room_request.request_approver.approver.name,
				"surname": x.room_request.request_approver.approver.surname
			},

			"access_name": x.room_request.room.name,
			"request_id": x.room_request.id,
			"room_id": x.room_request.room.text_id,
			"justification": x.room_request.justification,
			"requested_datetime": x.room_request.datetime_requested.strftime('%Y-%m-%d')
		} for x in room_relation]

	return ok({"orders": room_orders + ag_orders})


@admin_bp.route("/remove_for_approver/ag", methods=["POST"])
def remove_ag():
	"""Remove the access group from the approvers approval area"""

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	schema = {
		"approver": {"type": "integer"}, ## varför är det integer här? är det approver_id?
		"ag": {"type": "integer"}
	}

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	approver_id = request.json.get("approver")
	ag_id = request.json.get("ag")

	responsible_for_ag = ResponsibleForAg.query.filter_by(approver_id=approver_id, ag_id=ag_id).first()

	if not responsible_for_ag:
		return bad_request("No approver {} is responsible for access group {}.".format(approver_id, ag_id))

	db.session.delete(responsible_for_ag)
	db.session.commit()

	return ok("Access group removed from approver.")


@admin_bp.route("/remove_for_approver/room", methods=["POST"])
def remove_room():
	"""Remove the room from the approvers approval area"""

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	schema = {
		"approver": {"type": "integer"}, ## varför är det integer här? är det approver_id?
		"room": {"type": "string"}
	}

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	approver_id = request.json.get("approver")
	room_text_id = request.json.get("room")

	responsible_for_room = ResponsibleForRoom.query \
		.join(Room, Room.id == ResponsibleForRoom.room_id) \
		.filter(ResponsibleForRoom.approver_id == approver_id, Room.text_id == room_text_id).first()

	if not responsible_for_room:
		return bad_request("No approver {} is responsible for room {}.".format(approver_id, room_text_id))

	db.session.delete(responsible_for_room)
	db.session.commit()

	return ok("Room removed from approver.")

