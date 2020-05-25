from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

from visualize.models.ag_request import AccessGroupRequest
from visualize.models.ag import AccessGroup, gives_access_to
from visualize.models.admin import Admin
from visualize.models.approver import Approver
from visualize.models.approves_ag_request import ApprovesAgRequest
from visualize.models.approves_room_request import ApprovesRoomRequest
from visualize.models.belongs_to import BelongsTo
from visualize.models.card_reader import CardReader
from visualize.models.has_access_to import HasAccessTo
from visualize.models.reader import Reader
from visualize.models.responsible_for_ag import ResponsibleForAg
from visualize.models.responsible_for_room import ResponsibleForRoom
from visualize.models.room_request import RoomRequest
from visualize.models.room import Room
from visualize.models.request_status import RequestStatus
