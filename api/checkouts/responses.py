from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.checkouts.models import CheckoutStatus, PaymentMethod


class CheckoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cart_id: UUID
    customer_id: UUID
    status: CheckoutStatus
    payment_method: PaymentMethod
    total_amount: Decimal
    paid_at: datetime | None
    created_at: datetime
    updated_at: datetime
