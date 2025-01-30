import datetime as dt
import uuid
from uuid import UUID
from enum import Enum

from sqlalchemy import bindparam
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false, true
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

from app.db.base import Base


class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        letters = ['_' + i.lower() if i.isupper() else i for i in cls.__name__]
        return ''.join(letters).lstrip('_') + 's'

    created_at: M[dt.datetime] = column(server_default=func.now())
    updated_at: M[dt.datetime | None] = column(nullable=True, onupdate=func.now())
    id: M[UUID] = column(primary_key=True, index=True, default=uuid.uuid4)


class SongStatus(Enum):
    finished = 'finished'
    queued = 'queued'
    error = 'error'


class Song(BaseMixin, Base):
    user_id: M[UUID] = column(primary_key=True, index=True)
    status: M[SongStatus | None] = column(default=None)
    comment: M[str | None] = column(nullable=True)  # If comment == sending, then song is in process of sending to ai
    api_id: M[str | None] = column(nullable=True)
    audio_url: M[str | None] = column(nullable=True)
    image_url: M[str | None] = column(nullable=True)
    app_bundle: M[str]
    prompt: M[str] = column(server_default="")
    with_voice: M[bool] = column(server_default=true())

