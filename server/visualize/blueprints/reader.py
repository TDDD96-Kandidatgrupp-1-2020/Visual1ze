"""
This module contains the logic for the calls that are related to the reader role.
The url for the calls in this module is http://127.0.0.1:5000/reader/<route>
"""

import pickle
# Standard flask libraries
from flask import Blueprint, request
# For handling JSON web tokens for authorization
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token

# Help functions for validation and simplifications
from visualize.help_functions import ok, bad_request
from visualize import validator

from visualize.models import db, Reader, BelongsTo, RoomRequest, AccessGroupRequest, ResponsibleForAg, \
	ResponsibleForRoom, AccessGroup, HasAccessTo, ApprovesRoomRequest, ApprovesAgRequest, CardReader, \
	gives_access_to, Room, RequestStatus

from datetime import date
from dateutil.relativedelta import relativedelta

reader_bp = Blueprint('reader', __name__)


@reader_bp.before_request  # before_request is run before every request in blueprint route
@jwt_required
def is_reader():
	""" Checks if the request comes from a user that is admin."""
	try:
		email = decode_token(request.headers.get('Authorization')[7:])["identity"]

		current_admin = Reader.query.filter_by(email=email).first()
	except IndexError:
		return bad_request("User is not an admin")

	if current_admin is None:
		return bad_request("User is not an admin")


@reader_bp.route("/self", methods=["GET"])  # Empty route does not work with my tests
def get_current_reader():
	"""Returns the current users data"""

	# Get the email from the reader
	email = get_jwt_identity()
	current_reader = Reader.query.filter_by(email=email).first()

	# Checks if the reader is in the database
	if current_reader is None:
		return bad_request("{} is not in the database.".format(email))

	return ok(current_reader.serialize)


@reader_bp.route("/map", methods=["GET"])
def load_map():
	"""Loads the representation of the map from local file"""
	map_repr = pickle.load(open("map_repr.pickle", "rb"))
	return ok(map_repr)


@reader_bp.route("/room", methods=["POST"])
def order_room():
	"""Order access to a room for the logged in user"""
	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	schema = {
		"room_text_id": {"type": "string"},
		"justification": {"type": "string", "maxlength": 800}
	}

	# Get the email, room and the justification for the access to said room.
	email = get_jwt_identity()
	room_text_id = request.json.get("room_text_id")
	justification = request.json.get("justification")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	# Checks if the reader exists in the database
	reader = Reader.query.filter_by(email=email).first()
	if not reader:
		return bad_request("Reader does not exist."
						   "")

	# Checks if the room exists in the database
	room = Room.query.filter_by(text_id=room_text_id).first()
	if not room:
		return bad_request("Room: {} does not exist."
						   "".format(room_text_id))

	# Checks if the reader has already sent a request for this room
	rr = RoomRequest.query.filter_by(reader_id=reader.id, room_id=room.id, status=RequestStatus.PENDING).first()
	if rr:
		return bad_request("A request for this room already exists."
						   "")

	# Gets the approver with the highest priority for this room
	rfr = ResponsibleForRoom.query \
		.filter_by(room_id=room.id) \
		.order_by(ResponsibleForRoom.priority) \
		.first()
	if rfr is None:
		return bad_request("There is no approver in charge of this room")

	# Creates a new request for the room
	room_request = RoomRequest(reader=reader, room=room, justification=justification)
	approves_room_request = ApprovesRoomRequest(room_request=room_request, approver=rfr.approver)
	db.session.add(room_request)
	db.session.add(approves_room_request)
	db.session.commit()
	return ok("Request for room {} has been sent."
			  "".format(room_text_id))


@reader_bp.route("/ag", methods=["GET"])
def get_all_access_groups():
	"""Returns all existing access groups in the database."""
	return {"access_groups": [ag.serialize for ag in AccessGroup.query.all()]}, 200


@reader_bp.route("/ag", methods=["POST"])
def order_ag():
	"""Order access to a access group for the logged in user"""

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	schema = {
		"ag_id": {"type": "integer"},
		"justification": {"type": "string", "maxlength": 220}
	}

	# Get the email, access group and the justification for the access to said access group.
	email = get_jwt_identity()
	ag_id = request.json.get("ag_id")
	justification = request.json.get("justification")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	# Checks if the reader exists in the database
	reader = Reader.query.filter_by(email=email).first()
	if not reader:
		return bad_request("Reader does not exists.")

	# Checks if the access group exists in the database
	ag = AccessGroup.query.filter_by(id=ag_id).first()
	if not ag:
		return bad_request("Access group does not exist.".format(ag_id))

	# Checks if the reader has already sent a request for this access group
	agr = AccessGroupRequest.query.filter_by(ag_id=ag_id, reader_id=reader.id, status=RequestStatus.PENDING).first()
	if agr:
		return bad_request("A request for this access group already exists.")

	# Gets the approver with the highest priority for this access group
	rfag = ResponsibleForAg.query \
		.filter_by(ag_id=ag_id) \
		.order_by(ResponsibleForAg.priority) \
		.first()
	if rfag is None:
		return bad_request("There is no approver in charge of this access group.")

	# Creates a new request for the access group
	ag_request = AccessGroupRequest(reader=reader, ag=ag, justification=justification)
	approves_ag_request = ApprovesAgRequest(ag_request=ag_request, approver=rfag.approver)
	db.session.add(ag_request)
	db.session.add(approves_ag_request)
	db.session.commit()
	return ok("Request for access group {} has been sent.".format(ag_id))


@reader_bp.route("/orders", methods=["GET"])
def get_orders():
	"""Returns a list of all requests done"""

	# Get the email from the user making the request
	email = get_jwt_identity()

	# Checks if the reader exists in the database
	reader = Reader.query.filter_by(email=email).first()
	if not reader:
		return bad_request("Reader does not exist.")

	# Gets a list of all the users requested rooms
	room_relation = RoomRequest.query \
		.filter_by(reader_id=reader.id) \
		.join(Room, Room.id == RoomRequest.room_id) \
		.join(ApprovesRoomRequest, ApprovesRoomRequest.room_request_id == RoomRequest.id) \
		.join(Reader, Reader.id == ApprovesRoomRequest.approver_id) \
		.all()
	room_orders = [
		{"room_id": x.room_id, "name": x.room.name.capitalize(), "approver": x.request_approver.approver.email,
			"date": x.datetime_requested, "type": "Room"} for x in room_relation]

	# Gets a list of all the users requested access groups
	ag_relation = AccessGroupRequest.query \
		.filter_by(reader_id=reader.id) \
		.join(AccessGroup, AccessGroup.id == AccessGroupRequest.ag_id) \
		.join(ApprovesAgRequest, ApprovesAgRequest.ag_request_id == AccessGroupRequest.id) \
		.join(Reader, Reader.id == ApprovesAgRequest.approver_id) \
		.all()
	ag_orders = [
		{"ag_id": x.ag_id, "name": x.ag.name.capitalize(), "approver": x.request_approver.approver.email,
		"date": x.datetime_requested, "type": "Access group"} for x in ag_relation
	]

	return ok({"orders": room_orders + ag_orders})


def _find_room_helper(room_obj_list, room):
	"""simple list search for finding object in first part of a tuple"""
	for r_obj in room_obj_list:
		if r_obj[0] == room:
			return r_obj[1]
	return None


@reader_bp.route("/access", methods=["GET"])
def get_all_access():
	"""Returns a list of all access the logged in user currently has"""
	# Get the email from the user making the request
	email = get_jwt_identity()
	return get_all_access_helper(email)


def get_all_access_helper(email, room_filter=None):
	""" Returns a list of all access of the reader with the given email"""

	# Checks if the reader exists in the database
	reader = Reader.query.filter_by(email=email).first()
	if not reader:
		return bad_request("Reader does not exist.")

	# get room and belongsto for all rooms current user has access to from access groups as a list of tuples
	ag_access = db.session.query(Room, BelongsTo) \
		.join(CardReader, CardReader.room_b_id == Room.id) \
		.join(gives_access_to, gives_access_to.c.cr_id == CardReader.id) \
		.join(AccessGroup, AccessGroup.id == gives_access_to.c.ag_id) \
		.join(BelongsTo, BelongsTo.ag_id == AccessGroup.id) \
		.filter_by(reader_id=reader.id) \
		.all()

	# get room and belongs to for all rooms current user has access to as a list of tuples
	room_access = db.session.query(Room, HasAccessTo) \
		.join(CardReader, CardReader.room_b_id == Room.id) \
		.join(HasAccessTo, HasAccessTo.card_reader_id == CardReader.id) \
		.filter_by(reader_id=reader.id) \
		.all()

	# build a dict to return in JSON format
	return_dict = {}

	date_next_month = date.today() + relativedelta(months=+1)

	all_rooms = Room.query.all()
	if room_filter == None:  # equals is intended, empty list should not enter.
		room_filter = [r.text_id for r in all_rooms]

	for room in all_rooms:
		ag = _find_room_helper(ag_access, room)
		r = _find_room_helper(room_access, room)

		has_access = ((ag is not None) or (r is not None)) and room.text_id in room_filter
		# python or takes object when using "ag or r"...

		room_json = {}  # dictionay object for this room's metadata
		#room_json["approvers"] = [approver.approver.serialize for approver in room.approvers]
		room_json["access"] = has_access
		room_json["name"] = room.name
		if has_access:
			if ag:
				room_json["expires"] = ag.expiration_datetime
				room_json["ag_id"] = ag.ag_id
			else:
				room_json["expires"] = r.expiration_datetime
			if room_json["expires"].date() < date_next_month:
				room_json["warn_date"] = True
		return_dict[room.text_id] = room_json

	return ok(return_dict)


@reader_bp.route("/rooms_in_ag/<accees_group_id>", methods=["GET"])
def get_ag_access(accees_group_id):
	"""Returns a list of rooms that an access group has access to"""

	rooms = Room.query \
		.join(CardReader, CardReader.room_b_id == Room.id) \
		.join(gives_access_to, gives_access_to.c.cr_id == CardReader.id) \
		.filter_by(ag_id=accees_group_id)

	data = {"rooms": [room.text_id for room in rooms]}

	return ok(data)
