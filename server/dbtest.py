import unittest
from datetime import datetime

from visualize import create_app
from visualize.models import *

app = create_app()
from visualize.models import db  # database is created in models module

app.app_context().push()  # make all test use this context
db.drop_all()  # make sure first test starts with empty database


class TestDbModels(unittest.TestCase):
	"""Tests that all database models behave as expected."""

	def setUp(self):
		"""Rebuild all tables before test"""
		db.create_all()

	def tearDown(self):
		"""Drop all tables before test"""
		db.session.rollback()
		db.drop_all()

	def test_no_readers(self):
		"""Test the database is empty at start of test."""
		self.assertEqual(len(Reader.query.all()), 0, "Expected database to be empty after droping tables.")

	def test_create_reader(self):
		user = Reader("fakeuser@fakesite.com", "password", "name", "surname")
		db.session.add(user)
		db.session.commit()
		self.assertEqual(len(Reader.query.all()), 1, "Expected database to have reader after commit.")

	def test_still_no_readers(self):
		"""Another test to make sure database is always empty, and the first test is not only succeding because it ran first."""
		self.assertEqual(len(Reader.query.all()), 0, "Expected database to be empty in third test.")

	def test_reader_inheritance(self):
		"""Add one user with each role and make sure they appear in a query"""
		reader = Reader("fakeuser@fakesite.com", "password", "name", "surname")
		approver = Approver("fakeuser2@fakesite.com", "password2", "name", "surname")
		admin = Admin("fakeuser3@fakesite.com", "password3", "name", "surname")
		db.session.add(reader)
		db.session.add(approver)
		db.session.add(admin)

		db.session.commit()

		self.assertEqual(len(Reader.query.all()), 3, "Expected database to have 3 readers after commit.")
		self.assertEqual(len(Approver.query.all()), 2, "Expected database to have 2 approvers after commit.")
		self.assertEqual(len(Admin.query.all()), 1, "Expected database to have 1 admin after commit.")

	def test_add_card_reader(self):
		"""Test adding two rooms and adding a connection"""
		room_a = Room(name="A", text_id="A")
		room_b = Room(name="B", text_id="B")
		db.session.add(room_a)
		db.session.add(room_b)

		db.session.commit()

		self.assertEqual(len(Room.query.all()), 2, "Expected database to have 2 rooms after commit.")
		card_reader = CardReader(room_a=room_a, room_b=room_b)
		db.session.add(card_reader)

		db.session.commit()
		
		self.assertEqual(len(CardReader.query.all()), 1, "Expected database to have 1 card reader after commit.")

	def test_responsible_for_room(self):
		"""Test the relation between """
		approver = Approver("fakeuser2@fakesite.com", "password2", "name", "surname")
		room1 = Room(name="A", text_id="A")
		room2 = Room(name="B", text_id="B")
		room3 = Room(name="C", text_id="C")
		db.session.add(approver)
		db.session.add(room1)
		db.session.add(room2)
		db.session.add(room3)
		db.session.commit()
		responsible_for_room1 = ResponsibleForRoom(approver, room1, 1)
		responsible_for_room2 = ResponsibleForRoom(approver, room2, 2)
		responsible_for_room3 = ResponsibleForRoom(approver, room3, 3)
		db.session.add(approver)
		db.session.add(room1)
		db.session.add(room2)
		db.session.add(room3)
		db.session.add(responsible_for_room1)
		db.session.add(responsible_for_room2)
		db.session.add(responsible_for_room3)
		db.session.commit()
		found_relation = ResponsibleForRoom.query.filter_by(room=room2).first()
		self.assertIsNotNone(found_relation)
		self.assertEqual(found_relation.room, room2)
		self.assertEqual(found_relation.approver, approver)
		found_relations = ResponsibleForRoom.query.filter_by(approver=approver).all()
		self.assertEqual(len(found_relations), 3)
		self.assertTrue(room1 in [found_relation.room for found_relation in found_relations])
		self.assertTrue(room2 in [found_relation.room for found_relation in found_relations])
		self.assertTrue(room3 in [found_relation.room for found_relation in found_relations])

	def test_has_access_to(self):
		"""Test allowing one way passage between rooms for a reader"""
		reader = Reader("fakeuser@fakesite.com", "password", "name", "surname")
		room1 = Room(name="A", text_id="A")
		room2 = Room(name="B", text_id="B")
		db.session.add(reader)
		db.session.add(room1)
		db.session.add(room2)
		db.session.commit()
		card_reader_ab = CardReader(room_a=room1, room_b=room2)
		card_reader_ba = CardReader(room_a=room2, room_b=room1)
		db.session.add(card_reader_ab)
		db.session.add(card_reader_ba)
		db.session.commit()
		allow_ab = HasAccessTo(reader=reader, card_reader=card_reader_ab, expiration_datetime=datetime.today())
		db.session.add(allow_ab)
		db.session.commit()
		res = CardReader.query.join(HasAccessTo, HasAccessTo.card_reader_id == CardReader.id).filter_by(
			reader_id=reader.id).all()
		self.assertEqual(len(res), 1)
		self.assertEqual(res[0], card_reader_ab)


if __name__ == '__main__':
	unittest.main()
