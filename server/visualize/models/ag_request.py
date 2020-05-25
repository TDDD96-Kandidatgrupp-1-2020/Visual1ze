"""
Class for table access_group_request
"""
from datetime import datetime
from . import db
from .request_status import RequestStatus


class AccessGroupRequest(db.Model):
	"""This class represents the current requests for accessgroups readers have asked for."""

	id = db.Column(db.Integer, primary_key=True)
	reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))
	ag_id = db.Column(db.Integer, db.ForeignKey('access_group.id'))
	datetime_requested = db.Column(db.DateTime, nullable=False, default=datetime.now())
	justification = db.Column(db.String, nullable=False)
	status = db.Column(db.Enum(RequestStatus), nullable=False, default=RequestStatus.PENDING)

	request_approver = db.relationship("ApprovesAgRequest", backref="ag_request", uselist=False, lazy=True)
	ag = db.relationship("AccessGroup", uselist=False, lazy=True)

	#reader backref
	#ag backref

	def __init__(self, reader, ag, justification):
		"""Constructor for the class"""
		self.reader = reader
		self.ag = ag
		self.justification = justification

	@property
	def serialize(self):
		"""Returns the reader object as a JSON object"""

		return {
			"id": self.id,
			"reader_id": self.reader_id,
			"approver_id": self.approver_id,
			"datetime_requested": self.datetime_requested,
			"justification": self.justification
		}
