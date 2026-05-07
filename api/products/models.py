from uuid import UUID, uuid4

from sqlalchemy import Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.storage.postgresql import Base
from api.storage.postgresql.mixins import TimestampMixin


class Product(TimestampMixin, Base):
    __tablename__ = "products"
    __table_args__ = (Index("ix_products_ean", "ean"),)

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ean: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    items_per_box: Mapped[int] = mapped_column(Integer, nullable=False)

    offers = relationship(
        "Offer", back_populates="product", cascade="all, delete-orphan"
    )
