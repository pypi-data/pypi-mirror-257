from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column


from commons_lib.models.entities.base_entity import BaseEntity


class CompanyEntity(BaseEntity):
    __tablename__ = "company"

    name = Column(VARCHAR(256), nullable=False)
    description = Column(VARCHAR(1000), nullable=True)