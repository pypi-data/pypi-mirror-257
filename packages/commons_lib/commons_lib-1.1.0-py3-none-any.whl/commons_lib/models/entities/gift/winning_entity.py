from sqlmodel import VARCHAR, Integer
from sqlalchemy import Column, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from commons_lib.models.entities.base_entity import BaseEntity


class WinningEntity(BaseEntity):
    __tablename__ = "winnings"

    title: Mapped[str] = Column(VARCHAR(255), nullable=False)
    description: Mapped[str] = Column(VARCHAR(1000))
    price: Mapped[int] = Column(Integer, nullable=False)
    organization_uuid = Column(UUID(as_uuid=True), ForeignKey("company.pk_uuid"))
