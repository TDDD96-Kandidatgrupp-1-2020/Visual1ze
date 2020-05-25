"""
Enum for approval states used in ag_request and room_request
"""
from enum import Enum


class RequestStatus(Enum):
	PENDING = 0
	DENIED = 1
	APPROVED = 2
