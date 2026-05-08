from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.carts.models import CartStatus


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    offer_id: UUID
    quantity: int
    created_at: datetime
    updated_at: datetime


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    status: CartStatus
    checked_out_at: datetime | None
    created_at: datetime
    updated_at: datetime
    items: list[CartItemResponse]
