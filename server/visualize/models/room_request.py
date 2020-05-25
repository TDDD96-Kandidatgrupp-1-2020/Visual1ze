"""
Class for table room_request
"""
from datetime import datetime
from . import db
from .request_status import RequestStatus


class RoomRequest(db.Model):
	"""This class represents the current requests for rooms readers have asked for."""

	id = db.Column(db.Integer, primary_key=True)
	reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	datetime_requested = db.Column(db.DateTime, nullable=False, default=datetime.now())
	justification = db.Column(db.String, nullable=False)
	status = db.Column(db.Enum(RequestStatus), nullable=False, default=RequestStatus.PENDING)

	request_approver = db.relationship("ApprovesRoomRequest", backref="room_request", uselist=False, lazy=True)
	room = db.relationship("Room", uselist=False, lazy=True)

	# reader backref
	# room backref

	def __init__(self, reader, room, justification):
		self.reader = reader
		self.room = room
		self.justification = justification


