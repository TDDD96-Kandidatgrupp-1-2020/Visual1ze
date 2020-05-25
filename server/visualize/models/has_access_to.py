"""
Class for table has_access_to
"""
from . import db


class HasAccessTo(db.Model):
	"""
	This class represents what user has access to which individual card reader
	and when that access expires.
	"""

	reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), primary_key=True)
	card_reader_id = db.Column(db.Integer, db.ForeignKey('card_reader.id'), primary_key=True)
	expiration_datetime = db.Column(db.DateTime, nullable=False)

	# reader backref
	# card_reader backref

	def __init__(self, reader, card_reader, expiration_datetime):
		self.reader = reader
		self.card_reader = card_reader
		self.expiration_datetime = expiration_datetime
