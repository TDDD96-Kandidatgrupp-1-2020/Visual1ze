"""
Module for generating data in the database
"""
from datetime import date, timedelta
from random import choice, sample, seed, randint
from time import time

from visualize import create_app
from visualize.models import *

# Gustavs spännande lösning
import os
file_dir = os.path.dirname(__file__)
names_path = r"{}/names.txt".format(file_dir)
room_csv_path = r"{}/room_csv.txt".format(file_dir)
###

app = create_app()
app.app_context().push()  # make all test use this context

HALF_YEAR = 183  # number of days in half a year
expire_date = date.today() + timedelta(days=HALF_YEAR)
expire_date_short = date.today() + timedelta(days=5)

def read_room_names(reader):
	"""Parses the room names and text ids from a text stream"""
	rooms = []
	room_dict = {}
	line = reader.readline().rstrip()
	while line:
		data = line.split(";")
		room = Room(data[0], data[1])
		rooms.append(room)
		room_dict[room.text_id] = room
		line = reader.readline().rstrip()
	return rooms, room_dict


def read_room_connections(reader, room_dict):
	"""Parses room relation data from a text stream"""
	card_readers = []
	line = reader.readline().rstrip()
	while line:
		data = line.split(";")
		if data[0]:
			room_from = room_dict[data[0]]
		else:
			room_from = None
		room_to = room_dict[data[1]]
		if data[0]:
			card_readers.append(CardReader(room_a=room_to, room_b=room_from))
		card_readers.append(CardReader(room_a=room_from, room_b=room_to))
		line = reader.readline().rstrip()
	return card_readers


def read_room_txt(room_file_name=room_csv_path):
	"""Creates rooms and card readers based on a csv file"""
	room_file = open(room_file_name, "r")
	rooms, room_dict = read_room_names(room_file)
	return rooms, read_room_connections(room_file, room_dict)


def create_random_readers(names, n=30):
	"""Returns a list of randomly generated readers"""
	readers = []
	for i in range(n):
		name, surname, password = choice(names), choice(names), choice(names)
		readers.append(Reader("{}{}@hotmail.com".format(name, surname), password, name, surname))
	return readers


def create_random_approvers(names, n=10):
	"""Returns a list of randomly generated approvers"""
	approvers = []
	for i in range(n):
		name, surname, password = choice(names), choice(names), choice(names)
		approvers.append(Approver("{}{}@hotmail.com".format(name, surname), password, name, surname))
	return approvers


def create_random_admins(names ,n=5):
	"""Returns a list of randomly generated admins"""
	admins = []
	for i in range(n):
		name, surname, password = choice(names), choice(names), choice(names)
		admins.append(Admin("{}{}@hotmail.com".format(name, surname), password, name, surname))
	return admins


def create_rooms(n=50):
	"""Creates a list of randomly generated rooms"""
	rooms = []
	for i in range(n):
		rooms.append(Room(name="room name {}".format(i), text_id="room{}".format(i)))
	return rooms


def create_ags(n=20):
	"""Creates a list of randomly generated access groups"""
	ags = []
	for i in range(n):
		ags.append(AccessGroup(name="ag name {}".format(i + 1)))
	return ags


def connect_rooms(room_list, both_ways=True):
	"""Creates a list of cardreaders connecting rooms randomly"""
	card_readers = []
	for i in range(len(room_list)):
		room_from = room_list[i]
		room_to = choice(room_list)
		while room_to == room_from:  # avoid rooms leading to themselves
			room_to = choice(room_list)
		card_readers.append(CardReader(room_a=room_from, room_b=room_to))
		if both_ways:
			card_readers.append(CardReader(room_a=room_to, room_b=room_from))
	return card_readers


def find_opposite_reader(card_reader_list, find):
	"""Returns the card reader on the opposite side of the door for the card reader in find"""
	for c in card_reader_list:
		if c.room_a == find.room_b and c.room_b == find.room_a:
			return c
	raise (Exception("No reader on opposite side found"))


def connect_ag_to_rooms(ag_list, card_reader_list, n=10):
	"""Adds about n rooms to each access group"""
	for ag in ag_list:
		used_readers = []
		for card_reader in sample(card_reader_list, n):
			if card_reader.room_a_id is None:  # access to entrances are added later
				continue
			opposite = find_opposite_reader(card_reader_list, card_reader)
			if card_reader not in used_readers:
				ag.card_readers.append(card_reader)
				ag.card_readers.append(opposite)
				used_readers.append(card_reader)
				used_readers.append(opposite)


def connect_reader_to_rooms(reader_list, card_reader_list, n=10):
	"""Adds n rooms to each reader"""
	has_access_to = []
	for reader in reader_list:
		used_readers = []
		for card_reader in sample(card_reader_list, n):
			if card_reader.room_a_id is None:  # access to entrances are added later
				continue
			opposite = find_opposite_reader(card_reader_list, card_reader)
			if card_reader not in used_readers:
				has_access_to.append(HasAccessTo(reader=reader, card_reader=card_reader, expiration_datetime=expire_date))
				has_access_to.append(HasAccessTo(reader=reader, card_reader=opposite, expiration_datetime=expire_date))
				used_readers.append(card_reader)
				used_readers.append(opposite)
	return has_access_to


def connect_reader_to_ags(reader_list, ag_list, n=5):
	"""Adds n access groups to each reader"""
	belongs_to = []
	for reader in reader_list:
		for ag in sample(ag_list, n):
			belongs_to.append(BelongsTo(reader=reader, ag=ag, expiration_datetime=expire_date))
	return belongs_to


def connect_approver_to_rooms(approver_list, room_list, n=2):
	"""Adds about n rooms to each approver"""
	responsible_for = []
	for room in room_list:
		i = 2
		for approver in sample(approver_list, n):
			responsible_for.append(ResponsibleForRoom(approver, room, i))
			i += 1
	return responsible_for


def connect_approver_to_ags(approver_list, ag_list, n=1):
	"""Adds about n access groups to each approver"""
	responsible_for = []
	for ag in ag_list:
		i = 2
		for approver in sample(approver_list, n):
			responsible_for.append(ResponsibleForAg(approver, ag, i))
			i += 1
	return responsible_for


def add_cardreader_to_all(card_reader):
	"""Adds the given card reader to every user"""
	accesses = []
	for reader in Reader.query.all():
		access = HasAccessTo(reader, card_reader, expire_date)
		accesses.append(access)
	for ag in AccessGroup.query.all():
		ag.card_readers.append(card_reader)
	return accesses


def reset_db():
	"""Drops and recreates all tables"""
	from visualize.models import db
	db.drop_all()
	db.create_all()


def add_all_to_db(model_lists):
	"""Takes a list of list of models and adds all models to the database"""
	from visualize.models import db
	for model_list in model_lists:
		for model in model_list:
			db.session.add(model)
	db.session.commit()


def populate_default_users(rooms, card_readers, ags):
	"""Add default users with some access and requests"""
	bobby = Reader("a@a.a", "abcABC123", "Bobby", "Big")
	jonny = Approver("b@b.b", "abcABC123", "Jonny", "Small")
	super = Admin("c@c.c", "abcABC123", "Super", "Admin")

	add_all_to_db([[bobby, jonny, super]])

	b_access = []
	# access to ing27, isy
	b_access.append(HasAccessTo(bobby, card_readers[2], expire_date))
	b_access.append(HasAccessTo(bobby, card_readers[3], expire_date))
	# access to isy, isy2
	b_access.append(HasAccessTo(bobby, card_readers[6], expire_date_short))
	b_access.append(HasAccessTo(bobby, card_readers[7], expire_date))

	responsible_for_r = []
	for room in rooms:
		responsible_for_r.append(ResponsibleForRoom(jonny, room, 1))

	responsible_for_ag = []
	for ag in ags:
		responsible_for_ag.append(ResponsibleForAg(jonny, ag, 1))

	room_requests = []
	for n in range(5):
		room_requests.append(RoomRequest(bobby, rooms[randint(0, len(rooms)-1)], "room request {}".format(n)))

	ag_requests = []
	for n in range(5):
		ag_requests.append(AccessGroupRequest(bobby, ags[randint(0, len(ags) - 1)], "ag request {}".format(n)))

	add_all_to_db([b_access, responsible_for_r, responsible_for_ag, room_requests, ag_requests])

	approves_requests = []

	for room_req in room_requests:
		approves_requests.append(ApprovesRoomRequest(room_req, jonny))

	for ag_req in ag_requests:
		approves_requests.append(ApprovesAgRequest(ag_req, jonny))

	add_all_to_db([approves_requests])


def populate_db():
	"""Generate a database with randomized users"""
	t = time()

	print("Removing existing database...")
	reset_db()
	seed(1)

	print("Reading example name file (time passed {})".format(time() - t))
	names_txt = open(names_path, "r")
	temp_names = names_txt.readlines()
	names = [name.rstrip() for name in temp_names]

	print("Generating data (time passed {})".format(time() - t))
	readers = create_random_readers(names)
	approvers = create_random_approvers(names)
	admins = create_random_admins(names)
	# rooms = create_rooms()
	rooms, card_readers = read_room_txt()
	ags = create_ags()

	print("Adding data to db (time passed {})".format(time() - t))
	add_all_to_db([readers, approvers, admins, rooms, ags])
	# TODO add access relation data to approvers (and admins?)

	print("Generating relation data (time passed {})".format(time() - t))
	# card_readers = connect_rooms(rooms)
	connect_ag_to_rooms(ags, card_readers, n=1)  # note this is different because it does not have association table
	reader_accesses = connect_reader_to_rooms(readers, card_readers, n=2)
	ag_accesses = connect_reader_to_ags(readers, ags, n=1)
	approver_rooms = connect_approver_to_rooms(approvers, rooms, n=2)
	approver_ags = connect_approver_to_ags(approvers, ags, n=1)

	print("Adding relational data (time passed {})".format(time() - t))
	add_all_to_db([card_readers, reader_accesses, ag_accesses, approver_rooms, approver_ags])

	print("Add default users to database (time passed {})".format(time() - t))
	populate_default_users(rooms, card_readers, ags)

	print("Add entrances to all users and access groups (time passed {})".format(time() - t))
	for card_reader in [card_reader for card_reader in card_readers if not card_reader.room_a_id]:
		add_all_to_db([add_cardreader_to_all(card_reader)])

	print("Done creating database (time passed {})".format(time() - t))
	return


if __name__ == "__main__":
	populate_db()
