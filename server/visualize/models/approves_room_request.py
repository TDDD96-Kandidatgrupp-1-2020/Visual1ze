"""
Class for table approves_room_request
"""
from datetime import datetime
from . import db


class ApprovesRoomRequest(db.Model):
	"""This class connects which approver is currently responsible for which room request."""

	room_request_id = db.Column(db.Integer, db.ForeignKey('room_request.id'), primary_key=True)
	approver_id = db.Column(db.Integer, db.ForeignKey('approver.reader_id'), primary_key=True)
	start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

	# room_request backref to RoomRequest
	# approver backref

	def __init__(self, room_request, approver):
		self.room_request = room_request
		self.approver = approver
