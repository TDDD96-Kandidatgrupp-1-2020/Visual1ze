"""
Class for table reader
"""
from . import db, bcrypt
import uuid


class Reader(db.Model):
	"""This class represents a user with the role reader."""
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	name = db.Column(db.String(), nullable=False)
	surname = db.Column(db.String(), nullable=False)
	card_id = db.Column(db.String(), nullable=True)
	card_readers = db.relationship("HasAccessTo", backref="reader", lazy=True, cascade="all, delete, delete-orphan")
	access_groups = db.relationship("BelongsTo", backref="reader", lazy=True, cascade="all, delete, delete-orphan")
	room_requests = db.relationship("RoomRequest", backref="reader", lazy=True, cascade="all, delete, delete-orphan")
	access_group_requests = db.relationship("AccessGroupRequest", backref="reader", lazy=True,
											cascade="all, delete, delete-orphan")

	def __init__(self, email, password, name, surname):
		"""Constructor for the class"""
		self.email = email
		self.name = name
		self.surname = surname
		self.card_id = uuid.uuid4().hex
		self.password = bcrypt.generate_password_hash(password).decode("utf-8")

	@property
	def serialize(self):
		"""Returns the user object as a JSON object"""
		return {
			'email': self.email,
			'name': self.name,
			'surname': self.surname
		}

	def __repr__(self):
		"""Returns the string that will be shown when trying to print this class"""
		return f"Reader('{self.id},{self.email},{self.password},{self.name},{self.surname}')"

	def block_card(self):
		"""Blocks the readers card from working"""
		self.card_id = None

	def set_password(self, password):
		"""Hashes and sets the hashed password to the user in the database"""
		self.password = bcrypt.generate_password_hash(password).decode("utf-8")

	def check_password(self, password):
		"""Checks if the hash of the given password matches with the saved one"""
		return bcrypt.check_password_hash(self.password, password)
