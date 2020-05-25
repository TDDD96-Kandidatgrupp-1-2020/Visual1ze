"""
Class for table responsible_for_room
"""
from sqlalchemy import UniqueConstraint

from . import db


class ResponsibleForRoom(db.Model):
	"""This class represents which approvers are responsible for which individual room and with what priority."""

	approver_id = db.Column(db.Integer, db.ForeignKey('approver.reader_id'), primary_key=True)
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
	priority = db.Column(db.Integer, nullable=False)
	__table_args__ = (UniqueConstraint('room_id', 'priority', name='_responsible_for_room_uc'),)

	# approver backref
	# room backref

	def __init__(self, approver, room, priority):
		"""Constructor for the class"""
		self.approver = approver
		self.room = room
		self.priority = priority

	@property
	def serialize(self):
		"""Returns the user object as a JSON object"""
		return {
			"approver_id": self.approver_id,
			"room_id": self.room_id,
			"priority": self.priority
		}
