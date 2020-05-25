"""
Class for table responsible_for_ag
"""
from sqlalchemy import UniqueConstraint

from . import db


class ResponsibleForAg(db.Model):
	"""This class represents which approvers are responsible for which accessgroups and with what priority."""

	approver_id = db.Column(db.Integer, db.ForeignKey('approver.reader_id'), primary_key=True)
	ag_id = db.Column(db.Integer, db.ForeignKey('access_group.id'), primary_key=True)
	priority = db.Column(db.Integer, nullable=False)
	__table_args__ = (UniqueConstraint('ag_id', 'priority', name='_responsible_for_ag_uc'),)

	# approver backref
	# ag backref

	def __init__(self, approver, ag, priority):
		"""Constructor for the class"""
		self.approver = approver
		self.ag = ag
		self.priority = priority

	@property
	def serialize(self):
		"""Returns the user object as a JSON object"""
		return {
			"approver_id": self.approver_id,
			"ag_id": self.ag_id,
			"priority": self.priority
		}
