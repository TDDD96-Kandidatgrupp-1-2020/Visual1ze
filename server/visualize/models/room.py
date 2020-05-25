"""
Class for table room
"""
from visualize.models.card_reader import CardReader
from . import db


class Room(db.Model):
	"""This class represents a single room."""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), nullable=False)
	text_id = db.Column(db.String(), unique=True, nullable=False)

	card_readers_out = db.relationship("CardReader", primaryjoin=(CardReader.room_a_id == id), backref="room_a")
	card_readers_in = db.relationship("CardReader", primaryjoin=(CardReader.room_b_id == id), backref="room_b")
	approvers = db.relationship("ResponsibleForRoom", backref="room", lazy=True)

	def __init__(self, name, text_id):
		self.name = name
		self.text_id = text_id
