from uuid import UUID, uuid4

from sqlalchemy import Index, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.storage.postgresql import Base
from api.storage.postgresql.mixins import TimestampMixin


class Customer(TimestampMixin, Base):
    __tablename__ = "customers"
    __table_args__ = (Index("ix_customers_cnpj", "cnpj"),)

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)

    offers = relationship(
        "Offer", back_populates="customer", cascade="all, delete-orphan"
    )
