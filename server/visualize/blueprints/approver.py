"""
This module contains the logik for the calls that are related to the reader role.
The url for the calls in this module is http://127.0.0.1:5000/approver/<route>
"""

from datetime import date, timedelta

from flask import Blueprint, request
# For handling JSON web tokens for authorization
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
# Standard flask libraries
from sqlalchemy import and_, or_

from visualize import validator
from visualize.blueprints.reader import get_all_access_helper
# Help functions for validation and simplifications
from visualize.help_functions import ok, bad_request
# The database models
from visualize.models import db, Reader, BelongsTo, RoomRequest, AccessGroupRequest, ResponsibleForAg, \
	ResponsibleForRoom, AccessGroup, HasAccessTo, ApprovesRoomRequest, ApprovesAgRequest, CardReader, \
	gives_access_to, Room, Approver, RequestStatus, Admin

approver_bp = Blueprint('approver', __name__)
HALF_YEAR = 183  # number of days in half a year

@approver_bp.before_request  # before_request is run before every request in blueprint route
@jwt_required
def is_approver():
	""" Checks if the request comes from a user that is approver/admin."""
	try:
		email = decode_token(request.headers.get('Authorization')[7:])["identity"]

		current_approver = Approver.query.filter_by(email=email).first()
	except IndexError:
		return bad_request("User is not an admin")

	if current_approver is None:
		return bad_request("User is not an approver")


def _find_opposite_reader_helper(reader_ids):
	"""find the cardreaders on opposite sides so access is granted both ways"""
	room_reader_from = db.aliased(CardReader)

	# SELECT card_reader, room_reader_from FROM card_reader
	# JOIN card_reader AS room_reader_from
	#   ON room_reader_from.room_a_id = card_reader.room_b_id
	#     AND room_reader_from.room_b_id = card_reader.room_a_id

	opposites = db.session.query(CardReader, room_reader_from) \
		.join(room_reader_from,
			  and_(room_reader_from.room_a_id == CardReader.room_b_id,
				   room_reader_from.room_b_id == CardReader.room_a_id)) \
		.filter(CardReader.id.in_(reader_ids)).all()
	return opposites


def _find_card_readers_not_already_accessible(reader_id, cardreader_ids):
	"""Returns the ids in cardreader_ids that the reader does not already have added"""

	# SELECT card_reader, has_access_to FROM card_reader
	# LEFT OUTER JOIN has_access_to ON card_reader_id = card_reader.id AND has_access_to.reader_id = [reader_id]
	# WHERE card_reader.id IN [cardreader_ids] AND has_access_to IS NULL

	query = db.session.query(CardReader, HasAccessTo) \
		.join(HasAccessTo,
			and_(HasAccessTo.card_reader_id == CardReader.id,
				   HasAccessTo.reader_id == reader_id), isouter=True) \
		.filter(
		and_(CardReader.id.in_(cardreader_ids),
			 HasAccessTo.reader_id == None)).all()  # "is None" does not work with SQLAlchemy
	return [column[0].id for column in query]  # create a new list of cardreader ids


def _find_accesible_doors_to_room_helper(reader_id, room_id):
	"""
	find all cardreaders leading to the given room
	where the reader has access to a cardreader
	that leads to the room where the first cardreader is
	"""
	room_from = db.aliased(Room)
	room_reader_from = db.aliased(CardReader)

	# SELECT card_reader FROM card_reader
	# JOIN room ON room.id = card_reader.room_a_id
	# JOIN room AS room_1 ON room_1.id = card_reader.room_b_id
	# JOIN card_reader AS card_reader_1 ON card_reader_1.room_b_id = room_1.id
	# LEFT OUTER JOIN has_access_to ON has_access_to.card_reader_id = card_reader_1.id
	# LEFT OUTER JOIN gives_access_to ON gives_access_to.cr_id = card_reader_1.id
	# LEFT OUTER JOIN access_group ON access_group.id = gives_access_to.ag_id
	# LEFT OUTER JOIN belongs_to ON belongs_to.ag_id = access_group.id
	# WHERE room.id = [room_id] AND (has_access_to.reader_id = [reader_id] OR belongs_to.reader_id = [reader_id])

	readers_in = CardReader.query \
		.join(Room, Room.id == CardReader.room_a_id) \
		.join(room_from, room_from.id == CardReader.room_b_id) \
		.join(room_reader_from, room_reader_from.room_b_id == room_from.id) \
		.join(HasAccessTo, HasAccessTo.card_reader_id == room_reader_from.id, isouter=True) \
		.join(gives_access_to, gives_access_to.c.cr_id == room_reader_from.id, isouter=True) \
		.join(AccessGroup, AccessGroup.id == gives_access_to.c.ag_id, isouter=True) \
		.join(BelongsTo, BelongsTo.ag_id == AccessGroup.id, isouter=True) \
		.filter(Room.id == room_id, or_(HasAccessTo.reader_id == reader_id, BelongsTo.reader_id == reader_id)) \
		.all()

	reader_ids = [reader.id for reader in readers_in]

	return _find_card_readers_not_already_accessible(reader_id, reader_ids)


def approve_room_request(current_approver, room_request_id):
	"""Approves a request to a room"""

	# get the approves_room_request, room_request and reader objects related to the given room_request
	res = db.session.query(ApprovesRoomRequest, RoomRequest, Reader) \
		.join(RoomRequest, RoomRequest.id == ApprovesRoomRequest.room_request_id) \
		.join(Reader, Reader.id == RoomRequest.reader_id) \
		.filter(ApprovesRoomRequest.approver_id == current_approver.id,
				RoomRequest.id == room_request_id, RoomRequest.status == RequestStatus.PENDING).first()

	if res is None:
		return bad_request("{} not a valid room request for approver.".format(room_request_id))

	approves_request = res[0]
	room_req = res[1]
	reader = res[2]

	# request is valid, add access to card readers for the user that lead to the room

	reader_ids = _find_accesible_doors_to_room_helper(reader.id, room_req.room_id)
	opposites = _find_opposite_reader_helper(reader_ids)

	expire_date = date.today() + timedelta(days=HALF_YEAR)

	for card_reader_pair in opposites:
		reader_to = card_reader_pair[0]
		reader_from = card_reader_pair[1]
		new_access_to = HasAccessTo(reader, reader_to, expire_date)
		new_access_from = HasAccessTo(reader, reader_from, expire_date)
		db.session.add(new_access_to)
		db.session.add(new_access_from)

	for card_reader in CardReader.query.filter_by(room_b_id=room_req.room_id, room_a_id=None).all():
		new_access_to = HasAccessTo(reader, card_reader, expire_date)
		db.session.add(new_access_to)

	db.session.delete(approves_request)
	room_req.status = RequestStatus.APPROVED

	db.session.commit()

	return ok('Request for room was approved')


def approve_ag_request(current_approver, ag_request_id):
	"""Approves a request to an access group"""

	# get the approves_ag_request, access_group_request and reader objects related to the given access_group_request
	res = db.session.query(ApprovesAgRequest, AccessGroupRequest, AccessGroup, Reader) \
		.join(AccessGroupRequest, AccessGroupRequest.id == ApprovesAgRequest.ag_request_id) \
		.join(AccessGroup, AccessGroup.id == AccessGroupRequest.ag_id) \
		.join(Reader, Reader.id == AccessGroupRequest.reader_id) \
		.filter(ApprovesAgRequest.approver_id == current_approver.id,
				AccessGroupRequest.id == ag_request_id, AccessGroupRequest.status == RequestStatus.PENDING).first()

	if res is None:
		return bad_request("{} not a valid ag request for approver.".format(ag_request_id))

	approves_request = res[0]
	ag_req = res[1]
	ag = res[2]
	reader = res[3]

	expire_date = date.today() + timedelta(days=HALF_YEAR)

	new_belongs_to = BelongsTo(reader, ag, expire_date)

	db.session.add(new_belongs_to)
	db.session.delete(approves_request)
	ag_req.status = RequestStatus.APPROVED
	db.session.commit()

	return ok('Request for ag was approved')


def deny_room_request(current_approver, room_request_id):
	"""Denies a request to a room"""

	# get the approves_room_request, room_request and reader objects related to the given room_request
	res = db.session.query(ApprovesRoomRequest, RoomRequest) \
		.join(RoomRequest, RoomRequest.id == ApprovesRoomRequest.room_request_id) \
		.filter(ApprovesRoomRequest.approver_id == current_approver.id,
				RoomRequest.id == room_request_id, RoomRequest.status == RequestStatus.PENDING).first()

	if res is None:
		return bad_request("{} not a valid room request for approver.".format(room_request_id))

	approves_request = res[0]
	room_req = res[1]

	db.session.delete(approves_request)
	room_req.status = RequestStatus.DENIED
	db.session.commit()

	return ok('Request for room was denied')


def deny_ag_request(current_approver, ag_request_id):
	"""Denies a request to an access group"""

	# get the approves_ag_request, access_group_request and reader objects related to the given access_group_request
	res = db.session.query(ApprovesAgRequest, AccessGroupRequest) \
		.join(AccessGroupRequest, AccessGroupRequest.id == ApprovesAgRequest.ag_request_id) \
		.filter(ApprovesAgRequest.approver_id == current_approver.id,
				AccessGroupRequest.id == ag_request_id, AccessGroupRequest.status == RequestStatus.PENDING).first()

	if res is None:
		return bad_request("{} not a valid ag request for approver.".format(ag_request_id))

	approves_request = res[0]
	ag_req = res[1]

	db.session.delete(approves_request)
	ag_req.status = RequestStatus.DENIED
	db.session.commit()

	return ok('Request for access group was denied')


@approver_bp.route("/access", methods=["POST"])
def approve_request():
	"""Approves or denies a request to a room or an access group"""

	schema = {
		"request_id": {"type": "integer"},
		"type": {"type": "string"},
		"is_access_granted": {"type": "boolean"}
	}

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	request_id = request.json.get("request_id")
	type = request.json.get("type")
	is_access_granted = request.json.get("is_access_granted")

	# Checks if the approver exists in the database
	email = get_jwt_identity()
	current_approver = Approver.query.filter_by(email=email).first()

	if current_approver is None:
		return bad_request("{} is not in the database.".format(email))

	if type == "Room":
		if is_access_granted:
			return approve_room_request(current_approver, request_id)
		else:
			return deny_room_request(current_approver, request_id)
	elif type == "AG":
		if is_access_granted:
			return approve_ag_request(current_approver, request_id)
		else:
			return deny_ag_request(current_approver, request_id)
	else:
		return bad_request("{} is not a valid type.".format(type))


@approver_bp.route("/readers_for_room", methods=["POST"])
def get_readers_for_room():
	"""Get all the readers with access to a room."""

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	schema = {
		"room_text_id": {"type": "string"}
	}

	# Get the email for the access to said room.
	email = get_jwt_identity()
	room_text_id = request.json.get("room_text_id")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	# Checks if the approver exists in the database
	approver = Approver.query.filter_by(email=email).first()
	if not approver:
		return bad_request("Approver does not exist!")

	# Checks if the room exists in the database
	room = Room.query.filter_by(text_id=room_text_id).first()
	if not room:
		return bad_request("Room: {} does not exist!".format(room_text_id))

	# Query
	reader_access = db.session.query(Room, CardReader, HasAccessTo, Reader).filter(
		HasAccessTo.card_reader_id == CardReader.id,
		HasAccessTo.reader_id == Reader.id,
		CardReader.room_b_id == Room.id,
		Room.text_id == room_text_id,
	).all()

	# Format return message
	reader_order = [
		{"name": x.Reader.name,
		 "surname": x.Reader.surname,
		 "email": x.Reader.email,
		 "id": x.Reader.id} for x in reader_access]

	return ok({"reader_access": reader_order})


@approver_bp.route("/orders", methods=["GET"])
def get_all_orders():
	"""
	Returns a list of all the orders for rooms and AGs the logged in approver is responsible for.
	OR(!), if the approver is an admin, a list of all the orders for ALL approvers.
	"""
	email = get_jwt_identity()
	approver = Approver.query.filter_by(email=email).first()
	admin = Admin.query.filter_by(email=email).first()

	ag_relation = []
	room_relation = []
	if not admin:  # Get approves requests relations only for the logged in approver.
		# Get a list of all the orders of access groups this approver is responsible for
		ag_relation = ApprovesAgRequest.query \
			.filter_by(approver_id=approver.id) \
			.join(AccessGroupRequest, AccessGroupRequest.id == ApprovesAgRequest.ag_request_id) \
			.join(Reader, Reader.id == AccessGroupRequest.reader_id) \
			.join(AccessGroup, AccessGroup.id == AccessGroupRequest.ag_id).all()

		# Get a list of all the orders of rooms this approver is responsible for
		room_relation = ApprovesRoomRequest.query \
			.filter_by(approver_id=approver.id) \
			.join(RoomRequest, RoomRequest.id == ApprovesRoomRequest.room_request_id) \
			.join(Reader, Reader.id == RoomRequest.reader_id) \
			.join(Room, Room.id == RoomRequest.room_id).all()

	else:  # Get approves requests relations only for all approvers.
		# Get a list of all the orders of access groups of all responsible approvers.
		ag_relation = ApprovesAgRequest.query \
			.join(AccessGroupRequest, AccessGroupRequest.id == ApprovesAgRequest.ag_request_id) \
			.join(Reader, Reader.id == AccessGroupRequest.reader_id) \
			.join(AccessGroup, AccessGroup.id == AccessGroupRequest.ag_id).all()

		# Get a list of all the orders of rooms this approver is responsible for.
		room_relation = ApprovesRoomRequest.query \
			.join(RoomRequest, RoomRequest.id == ApprovesRoomRequest.room_request_id) \
			.join(Reader, Reader.id == RoomRequest.reader_id) \
			.join(Room, Room.id == RoomRequest.room_id).all()

	ag_orders = []
	for ag in ag_relation:
		# Gets all the rooms in the access group
		ag_room_relation = Room.query \
			.join(CardReader, CardReader.room_b_id == Room.id) \
			.join(gives_access_to, gives_access_to.c.cr_id == CardReader.id) \
			.filter_by(ag_id=ag.ag_request.ag.id)
		json = {
			"type": "AG",
			"rooms": [room.text_id for room in ag_room_relation],
			"reader": {
				"email": ag.ag_request.reader.email,
				"name": ag.ag_request.reader.name,
				"surname": ag.ag_request.reader.surname
			},
			"approver": {} if not admin else {
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

	room_orders = [
		{
			"type": "Room",
			"reader": {
				"email": x.room_request.reader.email,
				"name": x.room_request.reader.name,
				"surname": x.room_request.reader.surname,
			},
			"approver": {} if not admin else {
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


@approver_bp.route("/access_for_reader/<email>", methods=["GET"])
def get_all_access_for_reader(email):
	"""Get a list of all access the reader with the given email has."""

	approver_email = get_jwt_identity()
	approver = Approver.query.filter_by(email=approver_email).first()
	if not approver:
		return bad_request("This user does not have the approver role!")

	# if the user is an admin display all rooms regardless
	admin = Admin.query.filter_by(approver_id=approver.id).first()
	if admin:
		return get_all_access_helper(email)

	# display all rooms that the approver has responsibility over
	approver_rooms = get_responsibilites_helper(approver)
	return get_all_access_helper(email, approver_rooms)


@approver_bp.route("/readers", methods=["GET"])
def get_all_readers():
	"""Returns a list of all the readers names and email"""
	readers = [reader.serialize for reader in Reader.query.all()]
	return ok({"readers": readers})


def get_responsibilites_helper(approver):
	"""Returns a list of all rooms in the approvers responsibility"""

	room_relation = ResponsibleForRoom.query.filter_by(approver_id=approver.id) \
		.join(Room, Room.id == ResponsibleForRoom.room_id).all()

	room_list = [x.room.text_id for x in room_relation]

	# Get a list of all the rooms this approver is responsible for
	ag_relation = db.session.query(CardReader, ResponsibleForAg, Room, gives_access_to).filter(
		ResponsibleForAg.ag_id == gives_access_to.c.ag_id,  # Join ResponsibleForAg and gives_access_to
		gives_access_to.c.cr_id == CardReader.id,  # Join CardReader and gives_access_to
		Room.id == CardReader.room_b_id,  # Join Room and CardReader
		ResponsibleForAg.approver_id == approver.id  # Filter by appprover id
	).all()
	room_list_from_ag = [r.Room.text_id for r in ag_relation]

	# Add all rooms together, remove duplicates and sort the list
	return sorted(list(set(room_list + room_list_from_ag)))


@approver_bp.route("/responsibilities", methods=["GET"])
def get_responsibilities():
	"""Returns a list of the rooms in the approvers responsibility."""
	email = get_jwt_identity()

	# Checks if the reader is an approver
	approver = Approver.query.filter_by(email=email).first()
	if not approver:
		return bad_request("This user does not have the approver role!")

	room_list = get_responsibilites_helper(approver)

	return ok({"responsibilities": room_list})


@approver_bp.route("/revoke/room", methods=["POST"])
def revoke_room_access():
	"""Revokes a readers access to a room """
	schema = {
		"room_text_id": {"type": "string"},
		"email": {"type": "string"}
	}

	email = request.json.get("email")
	room_text_id = request.json.get("room_text_id")

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	# Checks if the reader exists in the database
	reader = Reader.query.filter_by(email=email).first()
	if not reader:
		return bad_request("Reader does not exist!")

	has_access = db.session.query(Room, CardReader, HasAccessTo).filter(
		Room.text_id == room_text_id,
		or_(CardReader.room_b_id == Room.id, CardReader.room_a_id == Room.id),
		HasAccessTo.card_reader_id == CardReader.id,
		HasAccessTo.reader_id == reader.id
	).all()

	if not has_access:
		return bad_request("The reader does not have access to this room")

	for a in has_access:
		cr_id = a.CardReader.id
		# Delete access
		HasAccessTo.query.filter_by(card_reader_id=cr_id, reader_id=reader.id).delete()

	db.session.commit()
	return ok("Access to {0} has been removed for {1}".format(room_text_id, email))


@approver_bp.route("/revoke/ag", methods=["POST"])
def revoke_ag_access():
	"""Revokes a readers access to a access group"""
	schema = {
		"ag_id": {"type": "integer"},
		"email": {"type": "string"}
	}

	email = request.json.get("email")
	ag_id = request.json.get("ag_id")

	# Checks if the request is a json
	if not request.is_json:
		return bad_request("Missing JSON in request")

	# Checks if any of the input is illegal
	if not validator(request.json, schema):
		return bad_request(validator.errors)

	# Checks if the reader exists in the database
	reader = Reader.query.filter_by(email=email).first()
	if not reader:
		return bad_request("Reader does not exist!")

	gives_access = db.session.query(gives_access_to, BelongsTo).filter(
		gives_access_to.c.ag_id == BelongsTo.ag_id,
		BelongsTo.ag_id == ag_id,
		BelongsTo.reader_id == reader.id
	).all()

	if not gives_access:
		return bad_request("The reader does not have access to this access group")

	BelongsTo.query.filter_by(reader_id=reader.id, ag_id=ag_id).delete()

	db.session.commit()
	return ok("Access to {0} has been removed for {1}".format(ag_id, email))
