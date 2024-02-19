from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, relationship, mapped_column

from commons_lib.models.entities.base_entity import BaseEntity


class OrgValueEntity(BaseEntity):
    __tablename__ = "organizationValues"

    title: Mapped[str] = Column(VARCHAR(255), nullable=False)
    description: Mapped[str] = Column(VARCHAR(1000))

    behaviors = relationship("OrgBehaviorEntity", secondary="orgvaluebehavior", back_populates="values")
    organization_id: Mapped[int] = mapped_column(BIGINT, nullable=False)



