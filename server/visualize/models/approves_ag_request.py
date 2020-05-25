"""
Class for table approves_ag_request
"""
from datetime import datetime

from . import db


class ApprovesAgRequest(db.Model):
	"""This class connects which approver is currently responsible for which accessgroup request."""

	ag_request_id = db.Column(db.Integer, db.ForeignKey('access_group_request.id'), primary_key=True)
	approver_id = db.Column(db.Integer, db.ForeignKey('approver.reader_id'), primary_key=True)
	start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

	# ag_request backref to AccessGroupRequest
	# approver backref

	def __init__(self, ag_request, approver):
		self.ag_request = ag_request
		self.approver = approver
