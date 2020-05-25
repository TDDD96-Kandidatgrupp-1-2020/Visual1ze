"""
Class for table card_reader
"""
from . import db


class CardReader(db.Model):
	"""This class represents a card reader forming a connection from room A to room B."""

	id = db.Column(db.Integer, primary_key=True)
	room_a_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	room_b_id = db.Column(db.Integer, db.ForeignKey('room.id'))

	allowed_readers = db.relationship("HasAccessTo", backref="card_reader", lazy=True)
