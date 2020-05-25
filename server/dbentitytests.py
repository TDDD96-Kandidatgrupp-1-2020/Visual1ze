"""
This module is used to test the entity models and their attributes in the database.

- MW
"""

import unittest

from sqlalchemy.exc import IntegrityError, StatementError

from visualize import create_app
from visualize.models import *

# Values of different datatypes, used in the tests.
MAGIC_INTEGER = 42
MAGIC_STRING = "Lorem"
LOREM1 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, " \
         "magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna."
LOREM5 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, " \
         "magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna.\nNunc " \
         "viverra imperdiet enim. Fusce est. Vivamus a tellus.\nPellentesque habitant morbi tristique senectus et " \
         "netus et malesuada fames ac turpis egestas. Proin pharetra nonummy pede. Mauris et orci.\nAenean nec " \
         "lorem. In porttitor. Donec laoreet nonummy augue.\nSuspendisse dui purus, scelerisque at, vulputate vitae, " \
         "pretium mattis, nunc. Mauris eget neque at sem venenatis eleifend. Ut nonummy."

app = create_app()
from visualize.models import db  # database is created in models module

app.app_context().push()  # make all test use this context
db.drop_all()  # make sure first test starts with empty database


class EntityTests(unittest.TestCase):
	"""
	Tests that all database entities behave as expected. setUp and tearDown are ran before and after every test
	function, respectively.
	"""

	def setUp(self):
		"""Rebuild all tables before test."""
		db.create_all()

	def tearDown(self):
		"""Drop all tables before test."""
		db.session.rollback()
		db.drop_all()

	# ------------------------------------------------------------------------
	# ---------------------------------Reader---------------------------------
	# ------------------------------------------------------------------------
	def test_create_reader(self):
		"""Tests that a reader can be created as expected."""
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		db.session.commit()

	def test_datatypes_reader(self):
		"""Tests that non-string datatype constraints of attributes in Reader are enforced by the database."""

		# Tests that id must be an Integer.
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		reader.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_add(self, reader, IntegrityError)

		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		reader.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that card_id must be an Integer. NOTE: This is known to - undesirably - not be enforced.
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		reader.card_id = MAGIC_STRING  # card_id is an Integer, so this should not work.
		except_error_db_add(self, reader, IntegrityError)  # This fails, but should preferbly not.

		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		reader.card_id = MAGIC_STRING  # card_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)  # This fails, but should preferbly not.

	def test_nullable_false_reader(self):
		"""Tests that attributes in Reader with nullable=False cannot be None."""

		except_error_db_add(self, Reader(email=None, password="abc123", name="Peter", surname="Parker"), IntegrityError)
		except_error_db_add(self, Reader(email="peter@example.org", password="abc123", name=None, surname="Parker"),
		                    IntegrityError)
		except_error_db_add(self, Reader(email="peter@example.org", password="abc123", name="Peter", surname=None),
		                    IntegrityError)

		# The bcrypt password hasing function currently used raises an exception.
		# Thus, we expect to get a ValueError when creating a Reader with password set to None.
		try:
			Reader(email="peter@example.org", password=None, name="Peter", surname="Parker")
		except ValueError:
			pass
		except Exception:
			self.fail('Unexpected exception raised')
		else:
			self.fail('ValueError not raised')

	def test_nullable_reader(self):
		"""Tests that attributes in Reader with nullable=True actually can be None."""

		# Creates and adds a reader to the databse.
		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(reader)
		db.session.commit()

		# Sets card_id to an Integer value (which is expected).
		reader.card_id = MAGIC_INTEGER
		db.session.commit()

		# Sets card_id to None (which should be allowed in the database since nullable=True for card_id).
		reader.card_id = None
		db.session.commit()

	def test_uniqueness_reader(self):
		"""Tests that uniqueness constraints of attributes in Reader are enforced by the database."""

		# Same email.
		reader1 = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		reader2 = Reader(email="peter@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(reader1)
		db.session.commit()
		except_error_db_add(self, reader2, IntegrityError)

		# Same card_id.
		reader1.card_id = MAGIC_INTEGER
		reader2.email = "maryjane@example.org"
		reader2.card_id = MAGIC_INTEGER
		except_error_db_add(self, reader2, IntegrityError)

	def test_password_hashed_reader(self):
		"""Tests that the value of the password attribute in Reader is encrypted."""

		# Creates and adds a reader to the databse.
		plaintext_pw = "abc123"
		reader = Reader(email="peter@example.org", password=plaintext_pw, name="Peter", surname="Parker")
		db.session.add(reader)
		db.session.commit()

		# Tests that the password stored in the database is encrypted.
		queried_pw = Reader.query.filter_by(email="peter@example.org", name="Peter", surname="Parker").first().password
		self.assertNotEqual(plaintext_pw, queried_pw)
		self.assertNotEqual(plaintext_pw, reader.password)  # Irrelevant?
		self.assertEqual(queried_pw, reader.password)  # Irrelevant?
		self.assertIsNotNone(queried_pw)  # Irrelevant?
		self.assertIsNotNone(reader.password)  # Irrelevant?

	def test_password_functions_reader(self):
		"""Tests that password functions in Reader behaves as expected."""

		reader = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		pw_before = reader.password
		reader.set_password("def456")
		pw_after = reader.password

		# Tests that password was set (updated).
		self.assertNotEqual(pw_before, pw_after)

		# Tests that the new password is encrypted.
		self.assertTrue(reader.check_password("def456"))

	def test_id_increment_reader(self):
		"""Tests that the id attribute in Reader is consistent."""

		reader1 = Reader(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		reader2 = Reader(email="maryjane@example.org", password="def456", name="Mary Jane", surname="Watson")
		db.session.add(reader1)
		db.session.add(reader2)
		db.session.commit()

		# Tests that the value of id starts at 1 and gets incremented by 1 each time.
		self.assertEqual(Reader.query.filter_by(email="peter@example.org", name="Peter", surname="Parker").first().id,
		                 1)
		self.assertEqual(
			Reader.query.filter_by(email="maryjane@example.org", name="Mary Jane", surname="Watson").first().id, 2)

		# Tests that the value of id does not change when entires in Reader are removed.
		db.session.delete(reader1)
		db.session.commit()
		self.assertIsNone(Reader.query.filter_by(id=1).first())
		self.assertEqual(
			Reader.query.filter_by(email="maryjane@example.org", name="Mary Jane", surname="Watson").first().id, 2)

		# Tests that the value of id is incremented as expected, even though lower id values are free.
		reader3 = Reader(email="harry@example.org", password="ghi789", name="Harry", surname="Osborn")
		db.session.add(reader3)
		db.session.commit()
		self.assertIsNone(Reader.query.filter_by(id=1).first())
		self.assertEqual(Reader.query.filter_by(email="harry@example.org", name="Harry", surname="Osborn").first().id,
		                 3)

	# ------------------------------------------------------------------------
	# --------------------------------Approver--------------------------------
	# ------------------------------------------------------------------------
	def test_create_approver(self):
		"""Tests that an approver can be created as expected."""
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver)
		db.session.commit()

	def test_inheritance_approver(self):
		"""
		Tests that when an approver is created, this also results in an entry in the Reader table thanks to the
		inheritance.
		"""
		approver = Approver(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(approver)
		db.session.commit()
		self.assertIsNotNone(Reader.query.filter_by(id=approver.id).first())
		self.assertIsNone(Admin.query.filter_by(id=approver.id).first())

	# ------------------------------------------------------------------------
	# ---------------------------------Admin----------------------------------
	# ------------------------------------------------------------------------
	def test_create_admin(self):
		"""Tests that an admin can be created as expected."""
		admin = Admin(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(admin)
		db.session.commit()

	def test_inheritance_admin(self):
		"""
		Tests that when an admin is created, this also results in an entry in the Approver and Reader tables thanks to
		the inheritance.
		"""
		admin = Admin(email="peter@example.org", password="abc123", name="Peter", surname="Parker")
		db.session.add(admin)
		db.session.commit()
		self.assertIsNotNone(Approver.query.filter_by(id=admin.id).first())
		self.assertIsNotNone(Reader.query.filter_by(id=admin.id).first())

	# ------------------------------------------------------------------------
	# ----------------------------------Room----------------------------------
	# ------------------------------------------------------------------------
	def test_create_room(self):
		"""Tests that a room can be created as expected."""
		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)
		db.session.commit()

	def test_datatypes_room(self):
		"""Tests that non-string datatype constraints of attributes in Room are enforced by the database."""

		# Tests that id must be an Integer.
		room = Room(name="ISYtan1", text_id="ISY1")
		room.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_add(self, room, IntegrityError)

		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)
		room.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

	def test_nullable_false_room(self):
		"""Tests that attributes in Room with nullable=False cannot be None."""
		except_error_db_add(self, Room(name=None, text_id="ISY1"), IntegrityError)

	def test_nullable_room(self):
		"""Tests that attributes in Room with nullable=True actually can be None."""

		# Creates and adds a room to the databse.
		room = Room(name="ISYtan1", text_id="ISY1")
		db.session.add(room)
		db.session.commit()

		# Sets representation_json to a String value (which is expected).
		room.representation_json = MAGIC_STRING
		db.session.commit()

		# Sets representation_json to None (which should be allowed in the database since nullable=True for
		# representation_json).
		room.representation_json = None
		db.session.commit()

	# ------------------------------------------------------------------------
	# -------------------------------CardReader-------------------------------
	# ------------------------------------------------------------------------
	def test_create_card_reader(self):
		"""Tests that a card reader can be created as expected."""

		# Tests creating a card reader with no rooms specified.
		card_reader1 = CardReader()
		db.session.add(card_reader1)
		db.session.commit()

		# Creates and adds two rooms to the database.
		room_a = Room(name="ISYtan1", text_id="ISY1")
		room_b = Room(name="ISYtan2", text_id="ISY2")
		db.session.add(room_a)
		db.session.add(room_b)
		db.session.commit()

		# Tests creating a card reader with rooms specified. NOTE: room_x is set, not room_x_id.
		card_reader2 = CardReader(room_a=room_a, room_b=room_b)
		db.session.add(card_reader2)
		db.session.commit()

	def test_datatypes_card_reader(self):
		"""Tests that non-string datatype constraints of attributes in CardReader are enforced by the database."""

		# Tests that id must be an Integer.
		card_reader = CardReader()
		card_reader.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_add(self, card_reader, IntegrityError)

		card_reader = CardReader()
		db.session.add(card_reader)
		card_reader.id = MAGIC_STRING
		except_error_db_commit(self, IntegrityError)

		# Tests that room_x_id must be an Integer. NOTE: Accessing the room_x_id attribute may be undesired.
		card_reader1 = CardReader()
		card_reader1.room_a_id = MAGIC_STRING  # room_a_id is an Integer, so this should not work.
		except_error_db_add(self, card_reader1, IntegrityError)

		card_reader1 = CardReader()
		db.session.add(card_reader1)
		card_reader1.room_a_id = MAGIC_STRING  # room_a_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		card_reader2 = CardReader()
		card_reader2.room_b_id = MAGIC_STRING  # room_b_id is an Integer, so this should not work.
		except_error_db_add(self, card_reader2, IntegrityError)

		card_reader2 = CardReader()
		db.session.add(card_reader2)
		card_reader2.room_b_id = MAGIC_STRING  # room_b_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

	# ------------------------------------------------------------------------
	# ------------------------------AccessGroup-------------------------------
	# ------------------------------------------------------------------------
	def test_create_access_group(self):
		"""Tests that an access group can be created as expected."""
		ag = AccessGroup(name="Basic")
		db.session.add(ag)
		db.session.commit()

	def test_uniqueness_access_group(self):
		"""Tests that uniqueness constraints of attributes in AccessGroup are enforced by the database."""
		ag1 = AccessGroup(name="Basic")
		ag2 = AccessGroup(name="Basic")
		db.session.add(ag1)
		db.session.commit()
		except_error_db_add(self, ag2, IntegrityError)

	# -------------------------------------------------------------------------
	# ----------------------------AccessGroupRequest---------------------------
	# -------------------------------------------------------------------------
	def test_create_access_group_request(self):
		"""Tests that an access group request can be created as expected."""
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		db.session.add(agr)
		db.session.commit()

	def test_datatypes_access_group_request(self):
		"""
		Tests that non-string datatype constraints of attributes in AccessGroupRequest are enforced by the database.
		"""

		# Tests that id must be an Integer.
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		agr.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_add(self, agr, IntegrityError)

		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		db.session.add(agr)
		agr.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that reader_id must be an Integer.
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		agr.reader_id = MAGIC_STRING  # reader_id is an Integer, so this should not work.
		except_error_db_add(self, agr, IntegrityError)

		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		db.session.add(agr)
		agr.reader_id = MAGIC_STRING  # reader_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that ag_id must be an Integer.
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		agr.ag_id = MAGIC_STRING  # ag_id is an Integer, so this should not work.
		except_error_db_add(self, agr, IntegrityError)

		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		db.session.add(agr)
		agr.ag_id = MAGIC_STRING  # ag_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that datetime_requested must be a DateTime.
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		agr.datetime_requested = MAGIC_STRING  # datetime_requested is a DateTime, so this should not work.
		except_error_db_add(self, agr, StatementError)

		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		db.session.add(agr)
		agr.datetime_requested = MAGIC_STRING  # datetime_requested is a DateTime, so this should not work.
		except_error_db_commit(self, IntegrityError)

	def test_nullable_false_access_group_request(self):
		"""Tests that attributes in AccessGroupRequest with nullable=False cannot be None."""
		# The datetime_requested attribute has "default=datetime.utcnow",
		# and thus the None value should be replaced upon add and commit.
		agr = AccessGroupRequest(reader=None, ag=None, justification=MAGIC_STRING)
		agr.datetime_requested = None
		db.session.add(agr)
		db.session.commit()
		self.assertIsNotNone(AccessGroupRequest.query.filter_by(id=agr.id).first().datetime_requested)

	def test_varying_length_access_group_request(self):
		"""Tests that the value of String attributes in AccessGroupRequest can have different lengths."""
		agr_lorem1 = AccessGroupRequest(reader=None, ag=None, justification=LOREM1)
		agr_lorem5 = AccessGroupRequest(reader=None, ag=None, justification=LOREM5)
		db.session.add(agr_lorem1)
		db.session.add(agr_lorem5)
		db.session.commit()

	# ------------------------------------------------------------------------
	# ------------------------------RoomRequest-------------------------------
	# ------------------------------------------------------------------------
	def test_create_room_request(self):
		"""Tests that a room request can be created as expected."""
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		db.session.add(rr)
		db.session.commit()

	def test_datatypes_room_request(self):
		"""Tests that non-string datatype constraints of attributes in RoomRequest are enforced by the database."""

		# Tests that id must be an Integer.
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		rr.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_add(self, rr, IntegrityError)

		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		db.session.add(rr)
		rr.id = MAGIC_STRING  # id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that reader_id must be an Integer.
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		rr.reader_id = MAGIC_STRING  # reader_id is an Integer, so this should not work.
		except_error_db_add(self, rr, IntegrityError)

		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		db.session.add(rr)
		rr.reader_id = MAGIC_STRING  # reader_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that room_id must be an Integer.
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		rr.room_id = MAGIC_STRING  # room_id is an Integer, so this should not work.
		except_error_db_add(self, rr, IntegrityError)

		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		db.session.add(rr)
		rr.room_id = MAGIC_STRING  # room_id is an Integer, so this should not work.
		except_error_db_commit(self, IntegrityError)

		# Tests that datetime_requested must be a DateTime.
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		rr.datetime_requested = MAGIC_STRING  # datetime_requested is a DateTime, so this should not work.
		except_error_db_add(self, rr, StatementError)

		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		db.session.add(rr)
		rr.datetime_requested = MAGIC_STRING  # datetime_requested is a DateTime, so this should not work.
		except_error_db_commit(self, IntegrityError)

	def test_nullable_false_room_request(self):
		"""Tests that attributes in RoomRequest with nullable=False cannot be None."""
		# The datetime_requested attribute has "default=datetime.utcnow",
		# and thus the None value should be replaced upon add and commit.
		rr = RoomRequest(reader=None, room=None, justification=MAGIC_STRING)
		rr.datetime_requested = None
		db.session.add(rr)
		db.session.commit()
		self.assertIsNotNone(RoomRequest.query.filter_by(id=rr.id).first().datetime_requested)

	def test_varying_length_room_request(self):
		"""Tests that the value of String attributes in AccessGroupRequest can have different lengths."""
		rr_lorem1 = RoomRequest(reader=None, room=None, justification=LOREM1)
		rr_lorem5 = RoomRequest(reader=None, room=None, justification=LOREM5)
		db.session.add(rr_lorem1)
		db.session.add(rr_lorem5)
		db.session.commit()


def except_error_db_add(testcase, object, Error):
	"""
	Fails the provided testcase if an error of type Error is NOT excepted when attempting to add the provided object to
	the databse and then committing.
	"""
	try:
		db.session.add(object)
		db.session.commit()
	except Error:
		db.session.rollback()
	except Exception:
		testcase.fail('An unexpected exception was raised, rather than the expected {}.'.format(Error.__name__))
	else:
		testcase.fail('Expected an {} to be raised, however it was not.'.format(Error.__name__))


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
	"""Runs all test functions in the EntityTests class."""
	unittest.main()
