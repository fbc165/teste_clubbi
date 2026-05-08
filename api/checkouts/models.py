from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.storage.postgresql import Base
from api.storage.postgresql.mixins import TimestampMixin


class CheckoutStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"


class PaymentMethod(str, Enum):
    PIX = "PIX"


class Checkout(TimestampMixin, Base):
    __tablename__ = "checkouts"
    __table_args__ = (
        Index("ix_checkouts_customer_id", "customer_id"),
        Index("ix_checkouts_cart_id", "cart_id"),
        Index("ix_checkouts_status", "status"),
        UniqueConstraint("cart_id", name="ux_checkouts_cart"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    cart_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("carts.id"), nullable=False
    )
    customer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("customers.id"), nullable=False
    )
    status: Mapped[CheckoutStatus] = mapped_column(
        SAEnum(CheckoutStatus, name="checkout_status"),
        nullable=False,
        default=CheckoutStatus.PENDING_PAYMENT,
    )
    payment_method: Mapped[PaymentMethod] = mapped_column(
        SAEnum(PaymentMethod, name="payment_method"),
        nullable=False,
        default=PaymentMethod.PIX,
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cart = relationship("Cart", back_populates="checkout")
    customer = relationship("Customer")
