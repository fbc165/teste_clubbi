from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.storage.postgresql import Base
from api.storage.postgresql.mixins import TimestampMixin


class CartStatus(str, Enum):
    OPEN = "OPEN"
    CHECKED_OUT = "CHECKED_OUT"


class Cart(TimestampMixin, Base):
    __tablename__ = "carts"
    __table_args__ = (
        Index("ix_carts_customer_id", "customer_id"),
        Index("ix_carts_status", "status"),
        Index(
            "ux_carts_open_per_customer",
            "customer_id",
            unique=True,
            postgresql_where=text("status = 'OPEN'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    customer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("customers.id"), nullable=False
    )
    status: Mapped[CartStatus] = mapped_column(
        SAEnum(CartStatus, name="cart_status"),
        nullable=False,
        default=CartStatus.OPEN,
    )
    checked_out_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    customer = relationship("Customer")
    checkout = relationship("Checkout", back_populates="cart", uselist=False)
    items = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItem(TimestampMixin, Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        Index("ix_cart_items_cart_id", "cart_id"),
        Index("ix_cart_items_offer_id", "offer_id"),
        UniqueConstraint("cart_id", "offer_id", name="ux_cart_items_cart_offer"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    cart_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("carts.id"), nullable=False
    )
    offer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("offers.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    offer = relationship("Offer")
