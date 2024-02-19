from sqlalchemy import BIGINT, Column
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID


from commons_lib.models.entities.base_entity import BaseEntity


class RedeemEntity(BaseEntity):
    __tablename__ = "redeems"
    employment_uuid = Column(UUID(as_uuid=True), ForeignKey("employment.pk_uuid"))
    employee = relationship('EmploymentEntity', back_populates='redeems')
