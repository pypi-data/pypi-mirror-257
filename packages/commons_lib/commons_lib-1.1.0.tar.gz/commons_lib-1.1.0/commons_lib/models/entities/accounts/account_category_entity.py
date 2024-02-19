from sqlalchemy import VARCHAR, Column
from sqlalchemy.orm import relationship

from commons_lib.models.entities.base_entity import BaseEntity


class AccountCategoryEntity(BaseEntity):

    __tablename__ = "accounts_type"

    title: str = Column(VARCHAR(256), nullable=False)
    slug: str = Column(VARCHAR(512), nullable=True)
    accounts = relationship(argument='AccountEntity', back_populates="account_type")

