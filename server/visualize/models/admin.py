"""
Class for table admin
"""
from . import db
from .approver import Approver


class Admin(Approver):
	"""This class represents a user with the role admin."""

	approver_id = db.Column(db.Integer, db.ForeignKey('approver.reader_id'), primary_key=True)

	def __repr__(self):
		"""Returns the string that will be shown when trying to print this class"""
		return f"Admin('{self.id},{self.email},{self.password},{self.name},{self.surname}')"
