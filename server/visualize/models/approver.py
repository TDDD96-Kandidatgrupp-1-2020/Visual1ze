"""
Class for table approver
"""
from . import db
from .reader import Reader


class Approver(Reader):
	"""This class represents a user with the role approver."""

	reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), primary_key=True)

	access_groups = db.relationship("ResponsibleForAg", backref="approver", lazy=True,
									cascade="all, delete, delete-orphan")
	rooms = db.relationship("ResponsibleForRoom", backref="approver", lazy=True,
							cascade="all, delete, delete-orphan")

	room_requests = db.relationship("ApprovesRoomRequest", backref="approver", lazy=True,
									cascade="all, delete, delete-orphan")
	ag_requests = db.relationship("ApprovesAgRequest", backref="approver", lazy=True,
								cascade="all, delete, delete-orphan")

	def __repr__(self):
		"""Returns the string that will be shown when trying to print this class"""
		return f"Approver('{self.id},{self.email},{self.password},{self.name},{self.surname}')"
