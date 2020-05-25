"""
Class for table access_group and table gives_access_to
"""
from . import db

# many to many relationship table between access goups and card readers
gives_access_to = db.Table('gives_access_to',
						   db.Column('ag_id', db.Integer, db.ForeignKey('access_group.id'), primary_key=True),
						   db.Column('cr_id', db.Integer, db.ForeignKey('card_reader.id'), primary_key=True))


class AccessGroup(db.Model):
	"""This class represents a bundle of card readers that users can be given access to all together."""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True)

	approvers = db.relationship("ResponsibleForAg", backref="ag", lazy=True, cascade="all, delete, delete-orphan")
	members = db.relationship("BelongsTo", backref="ag", lazy=True)

	card_readers = db.relationship("CardReader", secondary=gives_access_to, lazy=True,
								   backref=db.backref("allowed_access_groups", lazy=True))

	def __init__(self, name):
		self.name = name

	@property
	def serialize(self):
		return {
			"id": self.id,
			"name": self.name
		}
