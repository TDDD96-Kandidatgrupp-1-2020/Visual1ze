"""
This module is used to test the relations in the database.

- MW
"""

import unittest
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from visualize import create_app
from visualize.models import *

# Values of different datatypes, used in the tests.
MAGIC_STRING = "Lorem"

app = create_app()
from visualize.models import db  # database is created in models module

app.app_context().push()  # make all test use this context
db.drop_all()  # make sure first test starts with empty database


class RelationTests(unittest.TestCase):
	"""
	Tests that relations between entities in the database behave as expected. setUp and tearDown are ran before and
	after every test function, respectively.
	"""

	def setUp(self):
		"""Rebuild all tables before test."""
		db.create_all()

	def tearDown(self):
		"""Drop all tables before test."""
		db.session.rollback()
		db.drop_all()

	# ------------------------------------------------------------------------
	# ---------------------------ApprovesAGRequest----------------------------
	# ------------------------------------------------------------------------
	def test_create_approves_ag_request(self):
		"""Tests that an instance of ApprovesAgRequest can be created as expected."""

		# Creates an access group request and an approver (required to create an instance of ApprovesAgRequest).
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(agr)
		db.session.add(approver)

		# Create an instance of ApprovesAgRequest.
		aagr = ApprovesAgRequest(ag_request=agr, approver=approver)
		db.session.add(aagr)
		db.session.commit()

	def test_foreign_keys_approves_ag_request(self):
		"""Tests that the foreign key attributes of ApprovesAgRequest actually are keys in the other tables."""

		# Creates an access group request and an approver (required to create an instance of ApprovesAgRequest).
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(agr)
		db.session.add(approver)

		# Create an instance of ApprovesAgRequest.
		aagr = ApprovesAgRequest(ag_request=agr, approver=approver)
		db.session.add(aagr)
		db.session.commit()

		# Queries the datbase for the ApprovesAgRequest instance created just before.
		aagr_queried = ApprovesAgRequest.query.first()

		# Tests that the ag_request_id foreign key actually works as a key in the AccessGroupRequest table.
		found_agr = AccessGroupRequest.query.filter_by(id=aagr_queried.ag_request_id).first()
		self.assertIsNotNone(found_agr)

		# Tests that the approver_id foreign key actually works as a key in the Approver table.
		found_approver = Approver.query.filter_by(reader_id=aagr_queried.approver_id).first()
		self.assertIsNotNone(found_approver)

	def test_cardinality_approves_ag_request(self):
		"""Tests that the intended cardinality concerning instances of ApprovesAgRequest works as expected."""

		# Creates an access group request and an approver (required to create an instance of ApprovesAgRequest).
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		approver1 = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(agr)
		db.session.add(approver1)

		# Creates an instance of ApprovesAgRequest.
		aagr1 = ApprovesAgRequest(ag_request=agr, approver=approver1)
		db.session.add(aagr1)
		db.session.commit()

		# Creates a second approver.
		approver2 = Approver(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(approver2)

		# Tests that there can only be one approver per access group request in the ApprovesAgRequest table.
		# See the relationship request_approver in AccessGroupRequest (with uselist=False).
		aagr2 = ApprovesAgRequest(ag_request=agr, approver=approver2)
		db.session.add(aagr2)
		except_error_db_commit(self, AssertionError)

	def test_nullable_false_approves_ag_request(self):
		"""Tests that attributes in ApprovesAgRequest with nullable=False cannot be None."""
		# The start_datetime attribute has "default=datetime.utcnow",
		# and thus the None value should be replaced upon add and commit.
		aagr = get_approves_ag_request()
		aagr.start_datetime = None
		db.session.add(aagr)
		db.session.commit()
		self.assertIsNotNone(ApprovesAgRequest.query.filter_by(ag_request_id=aagr.ag_request_id,
		                                                       approver_id=aagr.approver_id).first().start_datetime)

	def test_datatypes_approves_ag_request(self):
		"""
		Tests that non-string datatype constraints of attributes in ApprovesAgRequest are enforced by the database.
		"""

		aagr = get_approves_ag_request()
		db.session.add(aagr)
		db.session.commit()

		# Tests that ag_request_id must be an Integer.
		# ag_request_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		aagr.ag_request_id = MAGIC_STRING
		except_any_error_db_commmit(self, "[ApprovesAgRequest] ag_request_id is an Integer (and a part of the Primary "
		                                  "Key), so giving it a String value should not work.")

		# Tests that approver_id must be an Integer.
		# approver_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		aagr.approver_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ApprovesAgRequest] approver_id is an Integer (and a part of the Primary Key), "
		                            "so giving it a String value should not work.")

	# ------------------------------------------------------------------------
	# --------------------------ApprovesRoomRequest---------------------------
	# ------------------------------------------------------------------------
	def test_create_approves_room_request(self):
		"""Tests that an instance of ApprovesRoomRequest can be created as expected."""

		# Creates an access group request and an approver (required to create an instance of ApprovesRoomRequest).
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(rr)
		db.session.add(approver)

		# Create an instance of ApprovesRoomRequest.
		arr = ApprovesRoomRequest(room_request=rr, approver=approver)
		db.session.add(arr)
		db.session.commit()

	def test_foreign_keys_approves_room_request(self):
		"""Tests that the foreign key attributes of ApprovesRoomRequest actually are keys in the other tables."""

		# Creates a room request and an approver (required to create an instance of ApprovesRoomRequest).
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(rr)
		db.session.add(approver)

		# Create an instance of ApprovesRoomRequest.
		arr = ApprovesRoomRequest(room_request=rr, approver=approver)
		db.session.add(arr)
		db.session.commit()

		# Queries the datbase for the ApprovesAgRequest instance created just before.
		arr_queried = ApprovesRoomRequest.query.first()

		# Tests that the room_request_id foreign key actually works as a key in the RoomRequest table.
		found_rr = RoomRequest.query.filter_by(id=arr_queried.room_request_id).first()
		self.assertIsNotNone(found_rr)

		# Tests that the approver_id foreign key actually works as a key in the Approver table.
		found_approver = Approver.query.filter_by(reader_id=arr_queried.approver_id).first()
		self.assertIsNotNone(found_approver)

	def test_cardinality_approves_room_request(self):
		"""Tests that the intended cardinality concerning instances of ApprovesRoomRequest works as expected."""

		# Creates a room request and an approver (required to create an instance of ApprovesRoomRequest).
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		approver1 = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(rr)
		db.session.add(approver1)

		# Creates an instance of ApprovesRoomRequest.
		arr1 = ApprovesRoomRequest(room_request=rr, approver=approver1)
		db.session.add(arr1)
		db.session.commit()

		# Creates a second approver.
		approver2 = Approver(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(approver2)

		# Tests that there can only be one approver per room request in the ApprovesRoomRequest table.
		# See the relationship request_approver in RoomRequest (with uselist=False).
		arr2 = ApprovesRoomRequest(room_request=rr, approver=approver2)
		db.session.add(arr2)
		except_error_db_commit(self, AssertionError)

	def test_nullable_false_approves_room_request(self):
		"""Tests that attributes in ApprovesRoomRequest with nullable=False cannot be None."""
		# The start_datetime attribute has "default=datetime.utcnow",
		# and thus the None value should be replaced upon add and commit.
		arr = get_approves_room_request()
		arr.start_datetime = None
		db.session.add(arr)
		db.session.commit()
		self.assertIsNotNone(ApprovesRoomRequest.query.filter_by(room_request_id=arr.room_request_id,
		                                                         approver_id=arr.approver_id).first().start_datetime)

	def test_datatypes_approves_room_request(self):
		"""
		Tests that non-string datatype constraints of attributes in ApprovesRoomRequest are enforced by the database.
		"""

		arr = get_approves_room_request()
		db.session.add(arr)
		db.session.commit()

		# Tests that room_request_id must be an Integer.
		# room_request_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		arr.room_request_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ApprovesRoomRequest] room_request_id is an Integer (and a part of the Primary "
		                            "Key), so giving it a String value should not work.")

		# Tests that approver_id must be an Integer.
		# approver_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		arr.approver_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ApprovesRoomRequest] approver_id is an Integer (and a part of the Primary Key), "
		                            "so giving it a String value should not work.")

	# ------------------------------------------------------------------------
	# -------------------------------BelongsTo--------------------------------
	# ------------------------------------------------------------------------
	def test_create_belongs_to(self):
		"""Tests that an instance of BelongsTo can be created as expected."""

		# Creates a reader and an access group (required to create an instance of BelongsTo).
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		# Create an instance of BelongsTo.
		bt = BelongsTo(reader=reader, ag=ag, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(bt)
		db.session.commit()

	def test_foreign_keys_belongs_to(self):
		"""Tests that the foreign key attributes of BelongsTo actually are keys in the other tables."""

		# Creates a reader and an access group (required to create an instance of BelongsTo).
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		# Creates an instance of BelongsTo.
		bt = BelongsTo(reader=reader, ag=ag, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(bt)
		db.session.commit()

		# Queries the datbase for the BelongsTo instance created just before.
		bt_queried = BelongsTo.query.first()

		# Tests that the reader_id foreign key actually works as a key in the Reader table.
		found_reader = Reader.query.filter_by(id=bt_queried.reader_id).first()
		self.assertIsNotNone(found_reader)

		# Tests that the ag_id foreign key actually works as a key in the AccessGroup table.
		found_ag = AccessGroup.query.filter_by(id=bt_queried.ag_id).first()
		self.assertIsNotNone(found_ag)

	def test_cardinality_belongs_to(self):
		"""Tests that the intended cardinality concerning instances of BelongsTo works as expected."""

		# Creates a reader and an access group (required to create an instance of BelongsTo).
		reader1 = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader1)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		# Creates an instance of BelongsTo.
		bt1 = BelongsTo(reader=reader1, ag=ag, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(bt1)
		db.session.commit()

		# Creates a second reader.
		reader2 = Reader(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(reader2)
		db.session.commit()

		# Tests that there can be several readers per access group in the BelongsTo table.
		bt2 = BelongsTo(reader=reader2, ag=ag, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(bt2)
		db.session.commit()

	def test_nullable_false_belongs_to(self):
		"""Tests that attributes in BelongsTo with nullable=False cannot be None."""
		bt = get_belongs_to()
		bt.expiration_datetime = None
		db.session.add(bt)
		except_error_db_commit(self, IntegrityError)

	def test_datatypes_belongs_to(self):
		"""Tests that non-string datatype constraints of attributes in BelongsTo are enforced by the database."""

		bt = get_belongs_to()
		db.session.add(bt)
		db.session.commit()

		# Tests that reader_id must be an Integer.
		# reader_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		bt.reader_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[BelongsTo] reader_id is an Integer (and a part of the Primary Key), so giving it "
		                            "a String value should not work.")

		# Tests that ag_id must be an Integer.
		# ag_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		bt.ag_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[BelongsTo] ag_id is an Integer (and a part of the Primary Key), so giving it a "
		                            "String value should not work.")

	# ------------------------------------------------------------------------
	# ------------------------------HasAccessTo-------------------------------
	# ------------------------------------------------------------------------
	def test_create_has_access_to(self):
		"""Tests that an instance of HasAccessTo can be created as expected."""

		# Creates a reader and a card reader (required to create an instance of HasAccessTo).
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		card_reader = CardReader()
		db.session.add(card_reader)

		# Creates an instance of HasAccessTo.
		hat = HasAccessTo(reader=reader, card_reader=card_reader, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(hat)
		db.session.commit()

	def test_foreign_keys_has_access_to(self):
		"""Tests that the foreign key attributes of HasAccessTo actually are keys in the other tables."""

		# Creates a reader and a card reader (required to create an instance of HasAccessTo).
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		card_reader = CardReader()
		db.session.add(card_reader)

		# Creates an instance of HasAccessTo.
		hat = HasAccessTo(reader=reader, card_reader=card_reader, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(hat)
		db.session.commit()

		# Queries the datbase for the HasAccessTo instance created just before.
		hat_queried = HasAccessTo.query.first()

		# Tests that the reader_id foreign key actually works as a key in the Reader table.
		found_reader = Reader.query.filter_by(id=hat_queried.reader_id).first()
		self.assertIsNotNone(found_reader)

		# Tests that the card_reader_id foreign key actually works as a key in the CardReader table.
		found_card_reader = CardReader.query.filter_by(id=hat_queried.card_reader_id).first()
		self.assertIsNotNone(found_card_reader)

	def test_cardinality_has_access_to(self):
		"""Tests that the intended cardinality concerning instances of HasAccessTo works as expected."""

		# Creates a reader and a card reader (required to create an instance of HasAccessTo).
		reader1 = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader1)
		card_reader = CardReader()
		db.session.add(card_reader)

		# Creates an instance of HasAccessTo.
		hat1 = HasAccessTo(reader=reader1, card_reader=card_reader, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(hat1)
		db.session.commit()

		# Creates a second reader.
		reader2 = Reader(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(reader2)
		db.session.commit()

		# Tests that there can be several readers per access group in the HasAccessTo table.
		hat2 = HasAccessTo(reader=reader2, card_reader=card_reader, expiration_datetime=get_datetime(years_in_future=1))
		db.session.add(hat2)
		db.session.commit()

	def test_nullable_false_has_access_to(self):
		"""Tests that attributes in HasAccessTo with nullable=False cannot be None."""
		hat = get_has_access_to()
		hat.expiration_datetime = None
		db.session.add(hat)
		except_error_db_commit(self, IntegrityError)

	def test_datatypes_has_access_to(self):
		"""Tests that non-string datatype constraints of attributes in HasAccessTo are enforced by the database."""

		hat = get_has_access_to()
		db.session.add(hat)
		db.session.commit()

		# Tests that reader_id must be an Integer.
		# reader_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		hat.reader_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[HasAccessTo] reader_id is an Integer (and a part of the Primary Key), so giving "
		                            "it a String value should not work.")

		# Tests that card_reader_id must be an Integer.
		# card_reader_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		hat.ag_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[HasAccessTo] card_reader_id is an Integer (and a part of the Primary Key), so "
		                            "giving it a String value should not work.")

	# ------------------------------------------------------------------------
	# ----------------------------ResponsibleForAG----------------------------
	# ------------------------------------------------------------------------
	def test_create_responsible_for_ag(self):
		"""Tests that an instance of ResponsibleForAg can be created as expected."""

		# Creates an approver and an access group (required to create an instance of ResponsibleForAg).
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		# Creates an instance of ResponsibleForAg.
		rfag = ResponsibleForAg(approver=approver, ag=ag, priority=1)
		db.session.add(rfag)
		db.session.commit()

	def test_foreign_keys_responsible_for_ag(self):
		"""Tests that the foreign key attributes of ResponsibleForAg actually are keys in the other tables."""

		# Creates an approver and an access group (required to create an instance of ResponsibleForAg).
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		# Creates an instance of ResponsibleForAg.
		rfag = ResponsibleForAg(approver=approver, ag=ag, priority=1)
		db.session.add(rfag)
		db.session.commit()

		# Queries the datbase for the ResponsibleForAg instance created just before.
		rfag_queried = ResponsibleForAg.query.first()

		# Tests that the approver_id foreign key actually works as a key in the Approver table.
		found_approver = Approver.query.filter_by(id=rfag_queried.approver_id).first()
		self.assertIsNotNone(found_approver)

		# Tests that the ag_id foreign key actually works as a key in the AccessGroup table.
		found_ag = AccessGroup.query.filter_by(id=rfag_queried.ag_id).first()
		self.assertIsNotNone(found_ag)

	def test_cardinality_responsible_for_ag(self):
		"""Tests that the intended cardinality concerning instances of ResponsibleForAg works as expected."""

		# Creates a reader and an access group (required to create an instance of BelongsTo).
		approver1 = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver1)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		# Creates an instance of ResponsibleForAg.
		rfag1 = ResponsibleForAg(approver=approver1, ag=ag, priority=1)
		db.session.add(rfag1)
		db.session.commit()

		# Creates a second approver.
		approver2 = Approver(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(approver2)
		db.session.commit()

		# Tests that there can be several approvers per access group in the ResponsibleForAg table.
		rfag2 = ResponsibleForAg(approver=approver2, ag=ag, priority=2)
		db.session.add(rfag2)
		db.session.commit()

	def test_nullable_false_responsible_for_ag(self):
		"""Tests that attributes in ResponsibleForAG with nullable=False cannot be None."""
		rfag = get_responsible_for_ag()
		rfag.priority = None
		db.session.add(rfag)
		except_error_db_commit(self, IntegrityError)

	def test_datatypes_responsible_for_ag(self):
		"""Tests that non-string datatype constraints of attributes in ResponsibleForAG are enforced by the database."""

		rfag = get_responsible_for_ag()
		db.session.add(rfag)
		db.session.commit()

		# Tests that approver_id must be an Integer.
		# approver_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		rfag.approver_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ResponsibleForAG] approver_id is an Integer (and a part of the Primary Key), so "
		                            "giving it a String value should not work.")

		# Tests that ag_id must be an Integer.
		# ag_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		rfag.ag_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ResponsibleForAG] ag_id is an Integer (and a part of the Primary Key), so giving "
		                            "it a String value should not work.")

	def test_uniqueness_responsible_for_ag(self):
		"""Tests that uniqueness constraints of attributes in ResponsibleForAG are enforced by the database."""

		approver1 = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver1)
		approver2 = Approver(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(approver2)
		ag = AccessGroup(name="Basic")
		db.session.add(ag)

		rfag1 = ResponsibleForAg(approver=approver1, ag=ag, priority=1)
		rfag2 = ResponsibleForAg(approver=approver2, ag=ag, priority=1)
		db.session.add(rfag1)
		except_error_db_commit(self, IntegrityError)

	# ------------------------------------------------------------------------
	# ---------------------------ResponsibleForRoom---------------------------
	# ------------------------------------------------------------------------
	def test_create_responsible_for_room(self):
		"""Tests that an instance of ResponsibleForRoom can be created as expected."""

		# Creates an approver and a room (required to create an instance of ResponsibleForRoom).
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver)
		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)

		# Creates an instance of ResponsibleForRoom.
		rfr = ResponsibleForRoom(approver=approver, room=room, priority=1)
		db.session.add(rfr)
		db.session.commit()

	def test_foreign_keys_responsible_for_room(self):
		"""Tests that the foreign key attributes of ResponsibleForRoom actually are keys in the other tables."""

		# Creates an approver and a room (required to create an instance of ResponsibleForRoom).
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver)
		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)

		# Creates an instance of ResponsibleForRoom.
		rfr = ResponsibleForRoom(approver=approver, room=room, priority=1)
		db.session.add(rfr)
		db.session.commit()

		# Queries the datbase for the ResponsibleForRoom instance created just before.
		rfr_queried = ResponsibleForRoom.query.first()

		# Tests that the approver_id foreign key actually works as a key in the Approver table.
		found_approver = Approver.query.filter_by(id=rfr_queried.approver_id).first()
		self.assertIsNotNone(found_approver)

		# Tests that the room_id foreign key actually works as a key in the Room table.
		found_room = Room.query.filter_by(id=rfr_queried.room_id).first()
		self.assertIsNotNone(found_room)

	def test_cardinality_responsible_for_room(self):
		"""Tests that the intended cardinality concerning instances of ResponsibleForRoom works as expected."""

		# Creates an approver and a room (required to create an instance of ResponsibleForRoom).
		approver1 = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver1)
		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)

		# Creates an instance of ResponsibleForRoom.
		rfr1 = ResponsibleForRoom(approver=approver1, room=room, priority=1)
		db.session.add(rfr1)
		db.session.commit()

		# Creates a second approver.
		approver2 = Approver(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(approver2)
		db.session.commit()

		# Tests that there can be several approvers per room in the ResponsibleForRoom table.
		rfr2 = ResponsibleForRoom(approver=approver2, room=room, priority=2)
		db.session.add(rfr2)
		db.session.commit()

	def test_nullable_false_responsible_for_room(self):
		"""Tests that attributes in ResponsibleForRoom with nullable=False cannot be None."""
		rfr = get_responsible_for_room()
		rfr.priority = None
		db.session.add(rfr)
		except_error_db_commit(self, IntegrityError)

	def test_datatypes_responsible_for_room(self):
		"""
		Tests that non-string datatype constraints of attributes in ResponsibleForRoom are enforced by the database.
		"""

		rfr = get_responsible_for_room()
		db.session.add(rfr)
		db.session.commit()

		# Tests that approver_id must be an Integer.
		# approver_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		rfr.approver_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ResponsibleForRoom] approver_id is an Integer (and a part of the Primary Key), "
		                            "so giving it a String value should not work.")

		# Tests that room_id must be an Integer.
		# room_id is an Integer (and a part of the Primary Key), so giving it a String value should not work.
		rfr.room_id = MAGIC_STRING
		except_any_error_db_commmit(self,
		                            "[ResponsibleForRoom] room_id is an Integer (and a part of the Primary Key), "
		                            "so giving it a String value should not work.")

	def test_uniqueness_responsible_for_room(self):
		"""Tests that uniqueness constraints of attributes in ResponsibleForRoom are enforced by the database."""

		approver1 = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver1)
		approver2 = Approver(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(approver2)
		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)

		rfr1 = ResponsibleForRoom(approver=approver1, room=room, priority=1)
		ResponsibleForRoom(approver=approver2, room=room, priority=1)  # rfr2
		db.session.add(rfr1)
		except_error_db_commit(self, IntegrityError)


def get_approves_ag_request():
	"""Creates the prerequisites for - and then creates and returns an instance of - ApprovesAgRequest."""

	# Creates an access group request and an approver (required to create an instance of ApprovesAgRequest).
	agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
	approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
	db.session.add(agr)
	db.session.add(approver)

	# Returns a ApprovesAgRequest object.
	return ApprovesAgRequest(ag_request=agr, approver=approver)


def get_approves_room_request():
	"""Creates the prerequisites for - and then creates and returns an instance of - ApprovesRoomRequest."""

	# Creates a room request and an approver (required to create an instance of ApprovesRoomRequest).
	rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
	approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
	db.session.add(rr)
	db.session.add(approver)

	# Returns a ApprovesRoomRequest object.
	return ApprovesRoomRequest(room_request=rr, approver=approver)


def get_belongs_to():
	"""Creates the prerequisites for - and then creates and returns an instance of - BelongsTo."""

	# Creates a reader and an access group (required to create an instance of BelongsTo).
	reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
	db.session.add(reader)
	ag = AccessGroup(name="Basic")
	db.session.add(ag)

	# Returns an instance of BelongsTo.
	return BelongsTo(reader=reader, ag=ag, expiration_datetime=get_datetime(years_in_future=1))


def get_has_access_to():
	"""Creates the prerequisites for - and then creates and returns an instance of - HasAccessTo."""

	# Creates a reader and a card reader (required to create an instance of HasAccessTo).
	reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
	db.session.add(reader)
	card_reader = CardReader()
	db.session.add(card_reader)

	# Returns an instance of HasAccessTo.
	return HasAccessTo(reader=reader, card_reader=card_reader, expiration_datetime=get_datetime(years_in_future=1))


def get_responsible_for_ag():
	"""Creates the prerequisites for - and then creates and returns an instance of - ResponsibleForAg."""

	# Creates an approver and an access group (required to create an instance of ResponsibleForAg).
	approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
	db.session.add(approver)
	ag = AccessGroup(name="Basic")
	db.session.add(ag)

	# Returns an instance of ResponsibleForAg.
	return ResponsibleForAg(approver=approver, ag=ag, priority=1)


def get_responsible_for_room():
	"""Creates the prerequisites for - and then creates and returns an instance of - ResponsibleForRoom."""

	# Creates an approver and a room (required to create an instance of ResponsibleForRoom).
	approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
	db.session.add(approver)
	room = Room(name="ISYtan1", text_id="ISY1")
	db.session.add(room)

	# Returns an instance of ResponsibleForRoom.
	return ResponsibleForRoom(approver=approver, room=room, priority=1)


def get_datetime(years_in_future=0):
	"""Returns a DateTime object of today's date, years_in_the_future years in the future."""
	return datetime.now().replace(year=datetime.now().year + years_in_future)


def except_any_error_db_commmit(testcase, fail_text):
	"""
	Fails the provided testcase if NO error is excepted when attempting to make a commit to the database.
	"""
	try:
		db.session.commit()
	except Exception:
		db.session.rollback()
	else:
		testcase.fail('No exception was raised. ' + fail_text)


def except_error_db_commit(testcase, Error):
	"""
	Fails the provided testcase if an error of type Error is NOT excepted when attempting to make a commit to the
	database.
	"""
	try:
		db.session.commit()
	except Error:
		db.session.rollback()
	except Exception:
		testcase.fail('An unexpected exception was raised, rather than the expected {}.'.format(Error.__name__))
	else:
		testcase.fail('Expected an {} to be raised, however it was not.'.format(Error.__name__))


if __name__ == '__main__':
	"""Runs all test functions in the RelationTests class."""
	unittest.main()