"""
Class for table Blacklist.
"""
from . import db


class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)

    def __init__(self, jti):
        self.jti = jti


def add_jti_to_blacklist(jti):
    blacklisted_jti = Blacklist(jti)
    db.session.add(blacklisted_jti)
    db.session.commit()


def is_jti_in_blacklist(jti):
    """
    Returns wether the given jti is blacklisted.
    :param jti: JWT identifier
    :return: bool
    """
    return Blacklist.query.filter_by(jti=jti).first() != None
