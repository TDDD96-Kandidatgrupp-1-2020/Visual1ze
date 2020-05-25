"""
Class for table belongs_to
"""
from . import db


class BelongsTo(db.Model):
	"""
	This class represents what user has access to which accessgroup
	and when that access expires.
	"""

	reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), primary_key=True)
	ag_id = db.Column(db.Integer, db.ForeignKey('access_group.id'), primary_key=True)
	expiration_datetime = db.Column(db.DateTime, nullable=False)

	# reader backref
	# ag backref to AccessGroup

	def __init__(self, reader, ag, expiration_datetime):
		self.reader = reader
		self.ag = ag
		# Maybe always set to one-three years from now?
		self.expiration_datetime = expiration_datetime
